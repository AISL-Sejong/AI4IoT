import tensorflow as tf
import numpy as np
import time
import socket
import json
import decoding as dec
import base64
import random
import os
import pandas as pd
import io
from PIL import ImageFile

from tensorflow.keras.models import load_model
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense, Activation, Dropout, Flatten, Dense, Conv2D, MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator , load_img
# from tensorflow.keras import optimizers, initializers, regularizers, metrics
# from sklearn.model_selection import train_test_split
from tensorflow.keras.applications import VGG16


batch_size = 5
AST_RUN = False
IMAGE_WIDTH = 150 # 이미지 크기 선언
IMAGE_HEIGHT = 150
IMAGE_SIZE = (IMAGE_WIDTH, IMAGE_HEIGHT)
IMAGE_CHANNELS = 3 # R,G,B
ImageFile.LOAD_TRUNCATED_IMAGES = True

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)
 
createFolder('./inference')

first_trigger_state = True
response_trigger_state = True

HOST = '192.168.247.1' #socket(client) 통신, HOST IP는 사용 PC에 따라 달라질 수 있음.
PORT =  3105
NAME = (HOST,PORT)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(NAME)

first_trigger_data = '{"ctname": "display1", "con": "hello"}' + '<EOF>' #server에 display1을 듣겠다고 인사
client_socket.send(first_trigger_data.encode('utf-8'))

while True:
    data = client_socket.recv(1000000)

    if first_trigger_state : # trigger를 걸면 first_trigger_data 2001 response 무시
        print("first_data")
        first_trigger_state = False
        continue

    dec_data = str(data)
    #print(dec_data)
    replace_t1 = dec_data.replace("\"","") #표준 형식들 제거하여 인코딩 data만 추출
    replace_t2 = replace_t1.replace("<EOF>","")
    replace_t3 = replace_t2.replace("b","",1)
    #print(replace_t3)

    decoding = dec.decode_img(replace_t3) #디코딩 모듈 불러와서 디코딩
    #print(type(decoding))
    decoding_str = str(decoding)
    #print(decoding_str)
    decoding.save("./inference/image.jpg",'BMP') #동일 디렉토리 내 inference 폴더 내 이미지 생성(덮어쓰기) 
    
    #딥러닝 파트 (파일 불러오기)
    test_filenames = os.listdir("./inference") 

    test_df = pd.DataFrame({
        'filename' : test_filenames
    })
    nb_samples = test_df.shape[0]

    # 테스트 데이터 정규화
    test_datagen = ImageDataGenerator(rescale=1./255)

    test_generator = test_datagen.flow_from_dataframe(
        test_df,
        "./inference/",
        x_col='filename',
        y_col=None,
        class_mode=None,
        target_size=IMAGE_SIZE,
        batch_size=batch_size,
        shuffle=False
    )

    # 모델 불러오기 및 예측
    model = tf.keras.models.load_model("./03 - 0.0356.hdf5")
    predict = model.predict_generator(test_generator, steps=np.ceil(nb_samples/batch_size))
    print(predict)
    predict1= predict.round(0).astype(int)
    predict2 = np.array(predict1).flatten().tolist()

    test_df['category'] = predict2
    # 카테고리에 이름 라벨링
    for i in range(len(predict2)):
        if (test_df['category'][i] == 1):
            test_df['category'][i] = 'water'
        else:
            test_df['category'][i] = 'coke'

    # 예측 모델 테스트(필요없음)
    """
    sample_test = test_df.head(21)
    sample_test.head()
    plt.figure(figsize=(12,24))
    for index, row in sample_test.iterrows():
        filename = row['filename']
        category = row['category']
        img = load_img("./test/"+filename, target_size=IMAGE_SIZE)
        plt.subplot(7,3,index +1)
        plt.imshow(img)
        plt.xlabel(filename+'('+"{}".format(category)+')')

    plt.tight_layout()
    plt.show()
    """
    if predict<0.5:      #coke predict change %
        predict = int((1-predict)*100)
    else:                #wawter predict change %
        predict = int(predict*100)    

    
    label = test_df['category'][0] # coke
    image = replace_t3 #img
    accuracy = str(predict) +'%' # acc

    print(label)
    print(image)
    print(accuracy)

    label_sok = '{"ctname": "label", "con": '+'\"'+str(label)+'\"'+'}' + '<EOF>' #label_cnt로 데이터 send
    client_socket.send(label_sok.encode('utf-8'))

    image_sok = '{"ctname": "image", "con": '+'\"'+str(image)+'\"'+'}' + '<EOF>' #image_cnt로 데이터 send
    client_socket.send(image_sok.encode('utf-8'))

    accuracy_sok = '{"ctname": "accuracy", "con": '+'\"'+accuracy+'\"'+'}' + '<EOF>' #accuracy_cnt로 데이터 send
    client_socket.send(accuracy_sok.encode('utf-8'))

    if response_trigger_state:  #report 2001 response가 반환되므로 무시
        for i in range(0,6):
            data = client_socket.recv(1000000)
            print(data)
