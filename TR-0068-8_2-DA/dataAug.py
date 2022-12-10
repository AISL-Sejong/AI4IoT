import socket
import json
import base64
import os
import Augmentor
import shutil
from PIL import Image
import base64
from io import BytesIO

first_trigger_state = True
response_trigger_state = True

HOST = 'localhost' #socket(client) 통신, HOST IP는 사용 PC에 따라 달라질 수 있음.
PORT =  20521
#CNT_AIMLSVC = '/Mobius/augmentor/aiMLSvc/'
CNT_TRAININGDATA = 'trainingData'
CNT_DATAAUG = 'dataAug'

NAME = (HOST,PORT)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(NAME)

first_trigger_data = '{"ctname": "' + CNT_TRAININGDATA + '", "con": "hello"}' + '<EOF>' #server에 trData를 듣겠다고 인사
client_socket.send(first_trigger_data.encode('utf-8'))

configindex = 0
while True:
    print('::WAIT')
    data = client_socket.recv(1000000)

    if first_trigger_state : # trigger를 걸면 first_trigger_data 2001 response 무시
        print("-- ", CNT_TRAININGDATA)
        first_trigger_state = False
        continue

    dec_data = data.decode('utf-8')
    jsonObj = json.loads(dec_data)

    img_byte = base64.b64decode(jsonObj['con'])

    img = Image.open(BytesIO(img_byte))
    img.show()

    # to jpg
    out_jpg = img.convert("RGB")

    # save file
    out_jpg.save("augmentData\\trData.jpg")

    #path = os.path.realpath('augmentData\\')
    #os.startfile(path)
    
    dataAugParam = {}
    with open('conf.json') as cf:
        config = json.load(cf)
    augType = config['augConfig'][configindex]['augType']
    dataAugParam = config['augConfig'][configindex]['dataAugParam']
    print(augType)
    configindex += 1
    if configindex == 3 :
        configindex = 0

    #create cin(dataAug(request))
    dataAugCon = {
        "status" : "request",
        "srcRrc" : jsonObj['rUri'],
        "augType" : augType,
        "augprm" : dataAugParam
    }

    dataAug_sok = '{"ctname": "dataAug", "con": '+ json.dumps(dataAugCon) +'}' + '<EOF>'
    client_socket.send(dataAug_sok.encode('utf-8'))

    directory = 'augmentData//'
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory.' + directory)

    p = Augmentor.Pipeline(directory)

    if augType == 'rotate':
        p.rotate(probability=1, max_left_rotation=dataAugParam['left'], max_right_rotation=dataAugParam['right'])

    if augType == 'distortion':
        p.random_distortion(probability=1, grid_width=dataAugParam['width'], grid_height=dataAugParam['height'], magnitude=dataAugParam['magnitude'])

    if augType == 'zoom':
        p.zoom(probability=1, min_factor=dataAugParam['min_factor'], max_factor=dataAugParam['max_factor'])
    
    
    p.sample(dataAugParam['amount'])
    
    augDataPath = directory+ jsonObj['rn'] + '-' + augType
    os.rename(directory + 'output', augDataPath)

    
    #create cin(dataAug(done))
    dataAugCon = {
        "status" : "done",
        "augDataPath" : 'augmented//' + jsonObj['rn'] + '-' + augType,
        "srcRrc" : jsonObj['rUri'],
        "augType" : augType,
        "augprm" : dataAugParam
    }

    dataAug_sok = '{"ctname": "dataAug", "con": '+ json.dumps(dataAugCon) +'}' + '<EOF>'
    client_socket.send(dataAug_sok.encode('utf-8'))

    if response_trigger_state:  #2001, cin
        for i in range(0,3):
            data = client_socket.recv(1000000)

    #shutil.rmtree(augDataPath)

    #re-path, move and open
    shutil.move(augDataPath, 'augmented')
    augDataPath = 'augmented//' + jsonObj['rn'] + '-' + augType
    os.startfile(os.path.realpath(augDataPath))
    