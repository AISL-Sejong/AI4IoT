import base64
import os

Pid = os.getpid()

def decode(AIModelname, IoTDeviceData):
    imgdata = base64.b64decode(IoTDeviceData)

    if AIModelname == "humanDetection":
        filename = '/{filepath}/AIServiceHub_Mgmt/AIServiceHub/yolov5_crowdhuman/PID'+str(Pid)+'Image.jpg' 

    elif AIModelname == "visualLocalization":
        filename = '/{filepath}/AIServiceHub_Mgmt/AIServiceHub/Patch_NetVLAD/patchnetvlad/mobius/union/query.jpg' 

    with open(filename, 'wb') as f:
        f.write(imgdata)

    return filename