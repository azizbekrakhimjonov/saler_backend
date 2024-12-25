import requests

data = {
    'code': 'STS0DB',
    'user': 'Tom Smith'
}
res = requests.post('http://127.0.0.1:8000/api/code/', json=data)
print(res.text)