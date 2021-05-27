from requests.auth import HTTPBasicAuth
import requests
url = "https://water.hostman.site/api/get_orders1c/"
auth = HTTPBasicAuth('admin','123')
r = requests.get(url=url)


f = requests.get(url, auth=HTTPBasicAuth('yuriy', '123'))


resp = requests.post('http://127.0.0.1:8000/login/', {'username': 'akshar', 'password': 'abc'})



