import kafkaModule
import imgDecoding
import subprocess
import msgParser


def main(IoTDevicePath, IoTDeviceData, AIModelName):
    print("IoT Device Path: " + IoTDevicePath + " , AIModelName: " + AIModelName)
    
    if AIModelName == "humanDetection": 
        img_path= imgDecoding.decode(AIModelName, IoTDeviceData)
        print("humanDetection connect")  

        python_path = "python /{filepath}/AIServiceHub_Mgmt/AIServiceHub/yolov5_crowdhuman/detect.py"
        msg = subprocess.check_output(python_path + " --source " + img_path  + " --save-txt", shell=True).decode("utf-8")

        count = msgParser.msgParsing(AIModelName, msg)
        
        print("********** count: " + str(count) + " ,IoTDevicePath: "+ IoTDevicePath + " ************")
        count_data = {"IoTDevicePath":IoTDevicePath, "AIModelName":AIModelName, "reportData": count}
        kafkaModule.Producer("AIServiceHub_responseData", count_data)
        print("kafka produce success")


    elif AIModelName == "visualLocalization":
        img_path= imgDecoding.decode(AIModelName, IoTDeviceData) 
        print("visualLocalization connect")

        python_path = "python /{filepath}/AIServiceHub_Mgmt/AIServiceHub/Patch_NetVLAD/all_in_one.py"
        msg = subprocess.check_output(python_path, shell=True).decode("utf-8")

        location = msgParser.msgParsing(AIModelName, msg)
        
        print("********** location: " + str(location) + " IoTDevicePath: "+ IoTDevicePath + " ************")
        location_data = {"IoTDevicePath":IoTDevicePath, "AIModelName":AIModelName, "reportData":location}
        kafkaModule.Producer("AIServiceHub_responseData", location_data)
        print("kafka produce success")

 
    else:
        pass
