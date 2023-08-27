from multiprocessing import Process
import AIModelmatching

def mprocess(IoTDevicePath, IoTDeviceData, AIModelName, Pid):
    process = Process(target= AIModelmatching.main, args=(IoTDevicePath, IoTDeviceData, AIModelName, Pid))
    process.start()
