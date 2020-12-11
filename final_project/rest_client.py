import requests

url = "http://192.168.1.132:8090/mdm/xcorexml/services/queries/SelectQueryText"

payload={}
headers = {
  'Authorization': 'Basic YWRtaW46YWRtaW4='}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

