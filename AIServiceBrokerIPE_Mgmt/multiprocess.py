from multiprocessing import Process
import multithread

def mprocess(IoTDevicePath,AImodelName):
    process = Process(target= multithread.mthread, args=(IoTDevicePath,AImodelName))
    process.start()
