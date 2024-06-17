# Multi-LLM-agent

A multi-LLM-agent with RAG capabilities, for rapid and intelligent code generation and API documentation parsing. `mixtral-8x7b-32768` model from the GROQ API is used, which provides lighting-fast inference time. Huggingface's `zephyr-7b-alpha` model serves as the initial query engine. It gives the user power to generate and save python code, it parses PDFs for API details, and generates code based on user query. The code is saved in a python file in local storage.

## How to setup
### Clone this repo
```console
https://github.com/quirrelHK/multi-llm-agent.git

cd multi-llm-agent
```

### Add a .env file with environment variables
```
HUGGINGFACE_API_TOKEN=<your-huggingface-api-token>
GROQ_API_KEY=<your-GROQ-api-key>
LLAMA_CLOUD_API_KEY=<your-llama-cloud-api-key>
```

### Create and activate a virtual environment
```console
python -m venv base

base\Scripts\activate.bat
```

### Install the requirements
```console
pip install -r requirements.txt
```

### Run the tool
```bash
python main.py
```