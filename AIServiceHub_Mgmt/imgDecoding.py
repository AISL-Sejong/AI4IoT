import base64
import os
import write_txt

def decode(AIModelname, IoTDeviceData, Pid):
    imgdata = base64.b64decode(IoTDeviceData)

    if AIModelname == "humanDetection":
        filename = '{address}/AI4IoT/AIServiceHub_Mgmt/AIServiceHub/yolov5_crowdhuman/PID'+str(Pid)+'Image.jpg' 

    elif AIModelname == "visualLocalization":
        filename = '{address}/AI4IoT/AIServiceHub_Mgmt/AIServiceHub/Patch_NetVLAD/patchnetvlad/mobius/union/PID'+str(Pid)+'Image.jpg' 
        write_txt.create('{address}/AI4IoT/AIServiceHub_Mgmt/AIServiceHub/Patch_NetVLAD/patchnetvlad/dataset_imagenames/PID'+str(Pid)+'Image.txt', filename)
        print(Pid)
        
    elif AIModelname == "potholeDetection":
        filename = '{address}/AI4IoT/AIServiceHub_Mgmt/AIServiceHub/yolov5_pothole/PID'+str(Pid)+'Image.jpg' 
        print(Pid)

    elif AIModelname == "speedbumpDetection":
        filename = '{address}/AI4IoT/AIServiceHub_Mgmt/AIServiceHub/yolov5_speedbump/PID'+str(Pid)+'Image.jpg' 

    with open(filename, 'wb') as f:
        f.write(imgdata)

    return filename