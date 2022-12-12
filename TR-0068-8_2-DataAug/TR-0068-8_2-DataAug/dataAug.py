import mobiusAPI as mb
import time
import json
import os
import Augmentor
import shutil
from PIL import Image
import base64
from io import BytesIO

ct = ""
configindex = 0
mobiusRI = '/Mobius/augmentor/aiMLSvc/trainingData/'

def augProcess(data):
    global configindex
    global mobiusRI
    jsonObj = data
    img_byte = base64.b64decode(data['con'])

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
        "srcRrc" : mobiusRI + jsonObj['rn'],
        "augType" : augType,
        "augprm" : dataAugParam
    }

    mb.createContentInstance('augmentor', 'aiMLSvc/dataAug', dataAugCon, 'http://203.250.148.120:20519', 'SOrigin')


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
        "srcRrc" : mobiusRI + jsonObj['rn'],
        "augType" : augType,
        "augprm" : dataAugParam
    }

    mb.createContentInstance('augmentor', 'aiMLSvc/dataAug', dataAugCon, 'http://203.250.148.120:20519', 'SOrigin')

    #shutil.rmtree(augDataPath)

    #re-path, move and open
    shutil.move(augDataPath, 'augmented')
    augDataPath = 'augmented//' + jsonObj['rn'] + '-' + augType
    os.startfile(os.path.realpath(augDataPath))

if (__name__ == "__main__"):
    cin = mb.getContentInstance('augmentor', 'aiMLSvc/trainingData/la', 'http://203.250.148.120:20519')
    ct = cin['m2m:cin']['ct']
    while True:
        cin = mb.getContentInstance('augmentor', 'aiMLSvc/trainingData/la', 'http://203.250.148.120:20519')
        # print(cin)
        if ct != cin['m2m:cin']['ct']:
            ct = cin['m2m:cin']['ct']
            augProcess(cin['m2m:cin'])
        time.sleep(5)