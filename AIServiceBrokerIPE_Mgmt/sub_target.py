import paho.mqtt.client as mqtt
from json import loads, dumps
import os
import time
import multiprocess
import DB
import post
import publish_basic


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
            req_ID = con_msg["ReqID"]
            info = con_msg["Info"]

            if req_ID == 0: #AIaaS 요청
                for i in range(len(info)):
                    IoTDevicePath = info[i]["IoTDevicePath"]
                    AImodelName = info[i]["AImodelName"]
                    # 컨테이너 자동 생성
                    AEname = IoTDevicePath.split('/')[2]
                    publish_basic.publishing(AEname, '/Mobius/AIServiceEnabler/'+AImodelName)
                    multiprocess.mprocess(IoTDevicePath,AImodelName)
                    time.sleep(3)

            elif req_ID == 1: #AIaaS 요청 해제
                for i in range(len(info)):
                    IoTDevicePath = info[i]["IoTDevicePath"]
                    AImodelName = info[i]["AImodelName"]

                    metaData = DB.discovery() #DB 내 metaData 확인
            
                    for i in range(len(metaData)):
                        j = len(metaData) - i - 1 #최근 쌓인 내용부터 순차적으로

                        if (metaData[j][0] == IoTDevicePath) & (metaData[j][1] == AImodelName):                            
                            pid = metaData[j][2] #IoTDevicePath와 AImodelName을 통해 pid 알아내기

                            print(pid)

                            DB.delete(pid) #DB 내에서 pid를 통해 관련 메타데이터 삭제
                            time.sleep(2)

                            remainData = DB.discovery()

                            if len(remainData) == 0:
                                post.posting_status("None")
                            
                            else:
                                post.posting_status(remainData)
                            
                            try:
                                os.kill(int(pid), 2) #pid kill
                            except:
                                pass
                            
                        else:
                            pass
            else:
                pass
        else:
            pass
        

def subscribing(source = 'AIServiceEnabler_target' , ip = '{ip}' , port = {port}):
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
    # sub리소스 생성할 때 적은 nu 값으로 연결 
    client.subscribe('/oneM2M/req/+/'+source+'/#')
    client.loop_forever() # 네트웍 트래픽을 처리, 콜백 디스패치, 재접속 등을 수행하는 블러킹 함수
                        # 멀티스레드 인터페이스나 수동 인터페이스를 위한 다른 loop*() 함수도 있음

if __name__ == "__main__":
    subscribing()