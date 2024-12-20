import requests

response = requests.get("http://127.0.0.1:5000/getMedicalInfo", params={"abha_id": "ABHA123456"})
print(response.json())
