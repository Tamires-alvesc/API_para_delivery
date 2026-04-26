import requests

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzc3NzU3NTk3fQ.AUm8epeV2OUzQn9rstRdFxVLlkSAIVZ-JcGV538Tbe0"
}

requisicao = requests.get("http://localhost:8000/auth/refresh/", headers=headers)
print(requisicao)
print(requisicao.json())