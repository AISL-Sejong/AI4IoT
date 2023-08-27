import kafkaModule
import imgDecoding
import subprocess
import msgParser


def main(IoTDevicePath, IoTDeviceData, AIModelName, Pid):
    print("IoT Device Path: " + IoTDevicePath + " , AIModelName: " + AIModelName)
    
    if AIModelName == "humanDetection": 
        img_path= imgDecoding.decode(AIModelName, IoTDeviceData, Pid)
        print("humanDetection connect")  

        python_path = "python {address}/AI4IoT/AIServiceHub_Mgmt/AIServiceHub/yolov5_crowdhuman/detect.py"
        msg = subprocess.check_output(python_path + " --source " + img_path  + " --save-txt", shell=True).decode("utf-8")

        count = msgParser.msgParsing(AIModelName, msg)
        
        print("********** count: " + str(count) + " ,IoTDevicePath: "+ IoTDevicePath + " ************")
        count_data = {"IoTDevicePath":IoTDevicePath, "AIModelName":AIModelName, "reportData": count}
        kafkaModule.Producer("AIServiceEnabler_responseData", count_data)
        print("kafka produce success")


    elif AIModelName == "visualLocalization":
        img_path= imgDecoding.decode(AIModelName, IoTDeviceData, Pid) 
        print("visualLocalization connect")

        python_path = "python {address}/AI4IoT/AIServiceHub_Mgmt/AIServiceHub/Patch_NetVLAD/all_in_one.py"
        msg = subprocess.check_output(python_path + " --source " + img_path , shell=True).decode("utf-8")

        location = msgParser.msgParsing(AIModelName, msg)
        
        print("********** location: " + str(location) + " IoTDevicePath: "+ IoTDevicePath + " ************")
        location_data = {"IoTDevicePath":IoTDevicePath, "AIModelName":AIModelName, "reportData":location}
        kafkaModule.Producer("AIServiceEnabler_responseData", location_data)
        print("kafka produce success")

    #GPS 데이터 추가

    elif AIModelName == "potholeDetection": 
        img_path= imgDecoding.decode(AIModelName, IoTDeviceData, Pid) 
        print("potholeDetection connect")

        python_path = "python {address}/AI4IoT/AIServiceHub_Mgmt/AIServiceHub/yolov5_pothole/detect.py"
        msg = subprocess.check_output(python_path + " --source " + img_path  + " --img 416 --conf 0.5 --save-txt", shell=True).decode("utf-8")

        detect = msgParser.msgParsing(AIModelName, msg)
        
        print("********** detect: " + str(detect) + " IoTDevicePath: "+ IoTDevicePath + " ************")
        detect_data = {"IoTDevicePath":IoTDevicePath, "AIModelName":AIModelName, "reportData":detect}
        kafkaModule.Producer("AIServiceEnabler_responseData", detect_data)
        print("kafka produce success")
 
 
    elif AIModelName == "speedbumpDetection":
        img_path= imgDecoding.decode(AIModelName, IoTDeviceData, Pid) 
        print("speedbumpDetection connect")

        python_path = "python {address}/AI4IoT/AIServiceHub_Mgmt/AIServiceHub/yolov5_speedbump/detect.py"
        msg = subprocess.check_output(python_path + " --source " + img_path  + " --img 416 --conf 0.5 --save-txt", shell=True).decode("utf-8")

        detect = msgParser.msgParsing(AIModelName, msg)
        
        print("********** detect: " + str(detect) + " IoTDevicePath: "+ IoTDevicePath + " ************")
        detect_data = {"IoTDevicePath":IoTDevicePath, "AIModelName":AIModelName, "reportData":detect}
        kafkaModule.Producer("AIServiceEnabler_responseData", detect_data)
        print("kafka produce success")
 
 
    else:
        pass
