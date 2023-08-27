import paho.mqtt.client as mqtt
import json
import random
import time

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected OK")
    else:
        print("Bad connection Returned code=", rc)


def on_disconnect(client, userdata, flags, rc=0):
    print(str(rc))


def on_publish(client, userdata, mid):
    print("In on_pub callback mid= ", mid)


def crt_cnt(cnt_name, path):
    rand = str(int(random.random()*100000))
    crt_cnt = {
                "to": path,
                "fr": "AIServiceEnabler",
                "op":1,
                "ty":3,
                "rqi": rand,
                "pc":{
                    "m2m:cnt": {
                        "rn": cnt_name,
                        "mni":100
                        }
                    }
            }
    return crt_cnt

def crt_sub(cnt_name, path):
    rand = str(int(random.random()*100000))
    crt_sub = {
                    "to": path+'/'+cnt_name,
                    "fr": "AIServiceEnabler",
                    "op":1,
                    "ty":23,
                    "rqi": rand,
                    "pc":{
                        "m2m:sub": {
                            "rn": cnt_name+"_sub",
                            "enc":{"net":[3]},
                            "nu":["mqtt://{ip}/test_tt?ct=json"]
                            }
                        }
                }
    return crt_sub

def crt_cin(msg, path):
    rand = str(int(random.random()*100000))
    crt_cin = {
            "to": path,
            "fr": "AIServiceEnabler",
            "op":1,
            "ty":4,
            "rqi": rand,
            "pc":{
                "m2m:cin": {
                    "con": msg
                    }
                }
        }
    return crt_cin

def publishing(cnt_name, path):
    # 새로운 클라이언트 생성
    client = mqtt.Client()

    # 콜백 함수 설정 on_connect(브로커에 접속), on_disconnect(브로커에 접속중료), on_publish(메세지 발행)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_publish = on_publish

    # address : localhost, port: 1883 에 연결
    client.connect('{ip}', {port})

    init_cnt = json.dumps(crt_cnt(cnt_name, path))
    # init_sub = json.dumps(crt_sub(cnt_name, path))
    report_cnt = json.dumps(crt_cnt("report", path+"/"+cnt_name))
    # report_sub = json.dumps(crt_sub("report", path+cnt_name+"/"))
    # init_cin = json.dumps(crt_cin(cnt_name, path))

    # common topic 으로 메세지 발행
    client.publish('/oneM2M/req/{RI}/Mobius2/json', init_cnt)
    time.sleep(1)
    client.publish('/oneM2M/req/{RI}/Mobius2/json', report_cnt)
    time.sleep(1)

    # 연결 종료
    client.disconnect()

if __name__ == "__main__":
    for i in range(100):
        publishing(i, "Mobius/{AE}/test")
        time.sleep(1)
