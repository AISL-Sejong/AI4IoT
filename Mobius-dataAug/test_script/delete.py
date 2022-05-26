import requests

url = "http://127.0.0.1:7579/Mobius"

def delete_ae():
	payload={}
	headers = {
	  'Accept': 'application/json',
	  'X-M2M-RI': '12345',
	  'X-M2M-Origin': 'SvirtualStore'
	}
	
	response = requests.delete(url+'/virtualStore', json=payload, headers=headers)
	print(response.text)

delete_ae()
