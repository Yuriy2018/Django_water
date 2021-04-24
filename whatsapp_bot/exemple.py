from requests.auth import HTTPBasicAuth
import requests
url = "http://127.0.0.1:8000/common/get_settings/"
auth = HTTPBasicAuth('yuriy','123')
r = requests.get(url=url,auth=auth)


f = requests.get(url, auth=HTTPBasicAuth('yuriy', '123'))


resp = requests.post('http://127.0.0.1:8000/login/', {'username': 'akshar', 'password': 'abc'})



