import kafkaModule
import multiprocess


while True:
    data = kafkaModule.Consumer("AIServiceEnabler_requestData")
    IoTDevicePath = data["IoTDevicePath"]
    IoTDeviceData = data["IoTDeviceData"]
    AIModelName = data["AIModelName"]
    Pid = data["Pid"]

    print("uploded Data from " + IoTDevicePath)
    multiprocess.mprocess(IoTDevicePath, IoTDeviceData, AIModelName, Pid)