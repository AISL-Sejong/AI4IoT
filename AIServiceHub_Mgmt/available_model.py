import requests
import json

def posting_available_model(data):
    url = "http://{ip}:{port}/Mobius/AIServiceEnabler/availableAIModel"
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
    

metadata = [
    {"AIModel": "beverageCf", "State": "stopped", "InputSample": "Img encoding data", "Description": "Classification of Coke, Fanta, Water, Toretta"},
    {"AIModel": "humanDetection", "State": "stopped", "InputSample": "Img encoding data", "Description": "Detection of human"},
    {"AIModel": "visualLocalization", "State": "running", "InputSample": "Img encoding data", "Description": "indoor/outdoor location positioning"},
    {"AIModel": "potholeDetection", "State": "running", "InputSample": "Img encoding data", "Description": "Detection of pothole"},
    {"AIModel": "speedbumpDetection", "State": "running", "InputSample": "Img encoding data", "Description": "Detection of speedbump"}
]

posting_available_model(metadata)