import requests



URL = 'https://www.facebook.com/v11.0/dialog/oauth?client_id=4234105266683469&redirect_uri=https://goodmemories.herokuapp.com&state={"{st=state123abc,ds=123456789}"}'

r = requests.get(URL)
print(r.url)