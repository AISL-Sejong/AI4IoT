import kafkaModule
import multiprocess


while True:
    data = kafkaModule.Consumer("AIServiceHub_requestData")
    IoTDevicePath = data["IoTDevicePath"]
    IoTDeviceData = data["IoTDeviceData"]
    AIModelName = data["AIModelName"]

    print("uploded Data from " + IoTDevicePath)
    multiprocess.mprocess(IoTDevicePath, IoTDeviceData, AIModelName)
