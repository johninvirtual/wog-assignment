import requests

res = requests.get("https://jsonplaceholder.typicode.com/users")
json_data = res.json()

print(json_data)

with open("data.json", 'w') as f:
    f.write(str(json_data))