from multiprocessing import Process
import AIModelmatching

def mprocess(IoTDevicePath, IoTDeviceData, AIModelName):
    process = Process(target= AIModelmatching.main, args=(IoTDevicePath, IoTDeviceData, AIModelName))
    process.start()
