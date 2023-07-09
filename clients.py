import requests

# response = requests.get('http://127.0.0.1:5000/ads/1')
# print(response.status_code)
# print(response.text)

# response = requests.delete('http://127.0.0.1:5000/ads/1')
# print(response.status_code)
# print(response.text)

# response = requests.post('http://127.0.0.1:5000/user', json={"name": 'user_4', 'email': 'assdf@ym.com',  'password': '12gdfgdfv3'})
# print(response.status_code)
# print(response.text)

# response = requests.post('http://127.0.0.1:5000/ads', json={"title": 'World', 'description': 'i love world',  'autor': 1})
# print(response.status_code)
# print(response.text)

response = requests.get("http://127.0.0.1:5000/user/1")
print(response.status_code)
print(response.text)
