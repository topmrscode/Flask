
import requests
pload = {'username':'xavier','password':'xavier123','email':'test'}
r = requests.post('http://localhost:5000/register/',data = pload)
print(r.text)