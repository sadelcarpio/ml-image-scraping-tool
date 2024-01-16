import requests
response = requests.get('http://dag-info:3000')
dags_metadata = response.json()
