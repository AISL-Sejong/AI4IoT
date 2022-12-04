import paho.mqtt.client as mqtt
from json import loads, dumps
import os
import DB
import kafkaModule
import post
import time


def on_connect(client, userdata, flags, rc): # 클라이언트가 서버에게서 CONNACK 응답을 받을 때 호출되는 콜백
    if rc == 0:
        print("connected OK")
    else:
        print("Bad connection Returned code=", rc)


def on_disconnect(client, userdata, flags, rc=0):
    print(str(rc))


def on_subscribe(client, userdata, mid, granted_qos):
    print("subscribed: " + str(mid) + " " + str(granted_qos))


def on_message(client, userdata, msg): # 서버에게서 PUBLISH 메시지를 받을 때 호출되는 콜백
    msg = msg.payload.decode("utf-8") #byte 형태 -> str 형태
    msg = loads(msg) #json(str)형태 -> dict 형태
    cin_msg = msg["pc"]["m2m:sgn"]["nev"]["rep"]

    for key in cin_msg.keys():

        if key == "m2m:cin":
            con_msg = cin_msg["m2m:cin"]["con"]
            data = {"IoTDevicePath":IoTDevicepath, "IoTDeviceData":con_msg, "AIModelName":AImodelname}
            kafkaModule.Producer("AIServiceHub_requestData", data)
            print("Upload Data from "+IoTDevicepath)

        else:
            pass
        

def subscribing(IoTDevicePath, AImodelName , ip = '{ip}' , port = '{port}'):  
    #subprocess metadata를 DB에 저장
    Pid = os.getpid()
    DB.insert(IoTDevicePath, AImodelName, Pid)
    time.sleep(2)
    metaData = DB.discovery()
    post.posting_status(metaData)
    
    # 새로운 클라이언트 생성
    client = mqtt.Client()
    # 콜백 함수 설정 on_connect(브로커에 접속), on_disconnect(브로커에 접속중료), on_subscribe(topic 구독),
    # on_message(발행된 메세지가 들어왔을 때)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    # address : Mobius Senrver IP, port: Mobius MQTT PORT에 연결
    client.connect(ip, port)

    # IoTDevicePath -> Sub 토픽 알아내기
    AEname = IoTDevicePath.split('/')[2] #[1] = Mobius, [2] = AE_name
    Cntname = IoTDevicePath.split('/')[-1] #[-1] = cnt_name
    topic = AEname + '_' + Cntname
    print(topic)

    #IoTDevicePath를 on_message에 넘겨주기 위해서, 전역변수 처리
    global IoTDevicepath
    IoTDevicepath = IoTDevicePath

    #AImodelname을 on_message에 넘겨주기 위해서, 전역변수 처리
    global AImodelname
    AImodelname = AImodelName

    client.subscribe('/oneM2M/req/+/'+topic+'/#')
    client.loop_forever() # 네트웍 트래픽을 처리, 콜백 디스패치, 재접속 등을 수행하는 블러킹 함수
                        # 멀티스레드 인터페이스나 수동 인터페이스를 위한 다른 loop*() 함수도 있음


if __name__ == "__main__":
    subscribing()