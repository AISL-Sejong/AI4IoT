import requests
import json

def posting_report(AImodelName, data):
    AEname = data["IoTDevicePath"].split('/')[2] # AE name만 추출
    url = "http://{ip}:{port}/Mobius/AIServiceEnabler/"+ AImodelName + "/" + AEname +"/report"
    print(url)
    payload = {}
    payload["m2m:cin"] = {}
    payload["m2m:cin"]["con"] = data
    payload = json.dumps(payload)

    headers = {
    'Accept': 'application/json',
    'X-M2M-RI': '12345',
    'X-M2M-Origin': 'IoTHubMgmt',
    'Content-Type': 'application/json; ty=4'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print("Send Report Data to Mobius")

def posting_status(data):
    url = "http://{ip}:{port}/Mobius/AIServiceEnabler/status"
    print(url)
    payload = {}
    payload["m2m:cin"] = {}
    payload["m2m:cin"]["con"] = data
    payload = json.dumps(payload)

    headers = {
    'Accept': 'application/json',
    'X-M2M-RI': '12345',
    'X-M2M-Origin': 'IoTHubMgmt',
    'Content-Type': 'application/json; ty=4'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print("Send Status Data to Mobius")