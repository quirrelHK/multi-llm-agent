import os
from dotenv import load_dotenv
from llama_parse import LlamaParse
from pydantic import BaseModel
from llama_index.core.output_parsers import PydanticOutputParser
from llama_index.core.query_pipeline import QueryPipeline
from llama_index.core.agent import ReActAgent
from llama_index.core.embeddings import resolve_embed_model 
from llama_index.core.tools import ToolMetadata, QueryEngineTool
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, PromptTemplate
from llama_index.llms.groq import Groq
from llama_index.llms.huggingface import HuggingFaceInferenceAPI
from prompts import context, code_parser_template
from huggingface_hub import login
from code_reader import code_reader
import ast


load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
huggingface_api_key = os.getenv("HUGGINGFACE_API_TOKEN")

login(huggingface_api_key)

llm = Groq(model="mixtral-8x7b-32768", api_key=groq_api_key)

llm2 = HuggingFaceInferenceAPI(
    model_name="HuggingFaceH4/zephyr-7b-alpha",
    token = huggingface_api_key
)
parser = LlamaParse(result_type="markdown")

file_extractor = {".pdf": parser}
documents = SimpleDirectoryReader("./data", file_extractor=file_extractor).load_data()

embed_model = resolve_embed_model("local:BAAI/bge-small-en-v1.5")
vector_index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)
query_engine = vector_index.as_query_engine(llm = llm2)

# result = query_engine.query("what are some of the routes in the api?")
# print(result)

tools = [
    QueryEngineTool(
        query_engine=query_engine,
        metadata=ToolMetadata(
            name="apiDocumentation",
            description="this gives documentation about code for an API. Use this for reading docs for the API"
        )
    ),
    code_reader,
]

agent = ReActAgent.from_tools(tools, llm=llm, verbose=True, context=context)


class CodeOutput(BaseModel):
    code: str
    description: str
    filename: str

parser = PydanticOutputParser(CodeOutput)
json_prompt_str = parser.format(code_parser_template)
json_prompt_tmpl = PromptTemplate(json_prompt_str)
output_pipeline = QueryPipeline(chain=[json_prompt_tmpl, llm])


while (prompt := input("Enter a prompt (q to quit): ")) != "q":
    
    retries = 0
    
    while retries < 3:
        try:
            result = agent.query(prompt)
            # print(result)
            next_result = output_pipeline.run(response=result)
            cleaned_json = ast.literal_eval(str(next_result).replace("assistant:",""))
            break
        except Exception as e:
            retries += 1
            print(f"Error occured, retry #{retries}:",e)
    
    if retries >= 3:
        print("Unable to process request, try again...")
        continue
        
    print("Code generated")
    print(cleaned_json["code"])
    
    print("\n\nDescription",cleaned_json["description"])
    
    filename = cleaned_json["filename"]
    
    try:
        with open(os.path.join("output",filename),"w") as f:
            f.write(cleaned_json["code"])
        print("File saved",filename)
    except Exception as e:
        print("Error saving",filename, e)
