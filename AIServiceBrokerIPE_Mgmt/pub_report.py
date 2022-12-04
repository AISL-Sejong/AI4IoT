import os
import kafkaModule
import post

pid = os.getpid()

def consuming(IoTDevicePath, AImodelName):
    print("connecting . . .")
    while True:
        data = kafkaModule.Consumer("AIServiceHub_responseData")
        print(data)
        if (data["IoTDevicePath"] == IoTDevicePath) & (data["AIModelName"] == AImodelName):
            reportData = data["reportData"]
            data = {"IoTDevicePath":IoTDevicePath, "InferencedData":reportData}
            post.posting_report(AImodelName, data)
        else:
            pass