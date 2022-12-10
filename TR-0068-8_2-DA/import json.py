import json

dataAugParam = {}
with open('conf.json') as f:
    config = json.load(f)
augtype = config['augType']
dataAugParam = config['dataAugParam']    

print(dataAugParam)