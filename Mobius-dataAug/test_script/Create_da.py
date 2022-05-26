import requests
import time

url = "http://127.0.0.1:7579/Mobius"

def create_da():
	payload= {
		"m2m:da": {
		 	"rn": "rotate_water_img1",
		 	"augty": "rotate",
    		"srsrc": "/virtualStore/classifier/target/water_img1",
    		"augprm": {
    			"max_left_rotation": "20",
    			"max_right_rotation": "20",
    			"sample": "20",
    			"label": "water"
    		},
    		"trgrsrc": "/virtualStore/classifier/target"
		 }
	}
	headers = {
	  'Accept': 'application/json',
	  'X-M2M-RI': '12345',
	  'X-M2M-Origin': 'SvirtualStore',
	  'Content-Type': 'application/vnd.onem2m-res+json; ty=50'
	}
	response = requests.post(url+'/virtualStore', json=payload, headers=headers)
	print(response.text)
	
create_da()
