import cv2
import time
import requests
import socket
import json
import encoding as enc

cap = cv2.VideoCapture(0)  # 0번 카메라 연결
fig_count=1

HOST = '192.168.0.48' #socket(client) 통신, HOST IP는 사용 Rasp에 따라 달라질 수 있음.
PORT =  3105
NAME = (HOST,PORT)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(NAME)

#start = '{"ctname": "target", "con": "hello"}' + '<EOF>' #server에 target을 듣겠다고 인사(추후 수정)
#client_socket.send(start.encode('utf-8'))

if cap.isOpened() :
    while True:
        if __name__ == '__main__':

            ret, frame = cap.read()                 # 카메라 한 프레임씩 읽기
            if ret:                                 # 비디오 프레임 제대로 읽으면 True, 실패하면 false
                cv2.imshow('camera',frame)          # 프레임 화면에 표시
                cv2.imwrite('./image.jpg', frame)   # 프레임을 'image.jpg'에 저장(덮어쓰기)
                encoding = enc.encode_img('./image.jpg')
                encoding_str = encoding.decode('utf-8')
                data = '{"ctname": "display1", "con": '+'\"'+encoding_str+'\"'+'}' + '<EOF>' #display1_cnt로 데이터 send
                client_socket.send(data.encode('utf-8'))
                time.sleep(1)
else:
    print('no camera!')
cap.release()
cv2.destroyAllWindows()
