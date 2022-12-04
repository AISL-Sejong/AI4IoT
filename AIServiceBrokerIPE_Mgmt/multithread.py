from threading import Thread
import sub_device
import pub_report

def mthread(IoTDevicePath,AImodelName): #multithreading
    th1 = Thread(target= sub_device.subscribing, args=(IoTDevicePath,AImodelName))
    th2 = Thread(target= pub_report.consuming, args=(IoTDevicePath, AImodelName))
    th1.start()
    th2.start()
    
