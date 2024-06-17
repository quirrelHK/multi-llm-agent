import requests

# Replace with the actual path to your "test.py" file
with open("test.py", "r") as file:
    code_contents = file.read()

url = "https://api.example.com/items"
headers = {"Content-Type": "application/json"}
data = {"code": code_contents}

response = requests.post(url, headers=headers, json=data)

if response.status_code == 201:
    print("Item created successfully")
else:
    print(f"Error creating item: {response.status_code} - {response.text}")
