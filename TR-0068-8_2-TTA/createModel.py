#!/usr/bin/env python
# coding: utf-8

# In[171]:


import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

from tensorflow.keras.models import load_model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout, Flatten, Dense, Conv2D, MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator , load_img
from tensorflow.keras import optimizers, initializers, regularizers, metrics
from sklearn.model_selection import train_test_split


from tensorflow.keras.applications import VGG16
print(np.__version__)


# In[172]:


import random
import os
import pandas as pd

# In[173]:


# 이미지 설정
AST_RUN = False
IMAGE_WIDTH = 150 # 이미지 크기 선언
IMAGE_HEIGHT = 150
IMAGE_SIZE = (IMAGE_WIDTH, IMAGE_HEIGHT)
IMAGE_CHANNELS = 3 # R,G,B


# In[174]:


# 물, 콜라 구분
filenames = os.listdir("./train")
categories = []
for filename in filenames:
    category = filename.split('_')[0]
    if category == 'water':
        categories.append(1)
    else:
        categories.append(0)

df = pd.DataFrame({
    'filename' : filenames,
    'category' : categories
})

# In[175]:


df.head(10)
df.tail(10)

# In[176]:


# 이미지 확인
sample = random.choice(filenames)
image = load_img("./train/"+sample)
plt.imshow(image)

# In[177]:


# 모델 설정 (전이 학습)
transfer_model = VGG16(weights='imagenet', include_top=False, input_shape= (150,150,3)) # 기존 모델을 가져옴
# transfer_model.trainable = True # => 전체 모델 학습

# 일부 모델만 학습 시켜줌
transfer_model.layers[1].trainable = False
transfer_model.layers[2].trainable = False

model = Sequential()
model.add(transfer_model)

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('sigmoid'))

# model.add(Dense(2, activation='softmax')) # 나중에 분류를 여러개로 할 것을 대비해서 softmax


model.summary()

# In[178]:


# 물, 콜라 분류
df["category"] = df["category"].replace({0:'coke', 1:'water'})

train_df, validate_df = train_test_split(df, test_size = 0.40, random_state=42) # 교차검증
train_df = train_df.reset_index(drop=True)
validate_df = validate_df.reset_index(drop=True)

train_datagen = ImageDataGenerator(rescale=1./255, #데이터 정규화
                                  horizontal_flip=True, # 수평 대칭 이미지 50퍼 확률로
                                  width_shift_range=0.1, # 전체 크기의 10% 범위에서 좌우로 이동
                                  height_shift_range=0.1, # 위, 아래로 이동
                                  # rotation_range=5, # 5도 사이의 값으로
                                  #shear_range=0.7,
                                  # zoom_range=[0.9, 2.2],
                                  #vertical_flip=True,
                                  fill_mode='nearest') # 빈 데이터는 가장 가까운 픽셀데이터를 넣어줌
train_datagen

# In[179]:


total_train = df.shape[0]
total_validate = validate_df.shape[0]
batch_size = 5
total_train

# In[180]:


# 이미지 데이터 정규화
train_generator = train_datagen.flow_from_dataframe(
    train_df,
    "./train",
    x_col='filename',
    y_col='category',
    target_size=IMAGE_SIZE,
    class_mode='binary', # categorical
    batch_size=batch_size
)
validation_datagen = ImageDataGenerator(rescale=1./255, #데이터 정규화
                                  horizontal_flip=True, # 수평 대칭 이미지 50퍼 확률로
                                  width_shift_range=0.1, # 전체 크기의 10% 범위에서 좌우로 이동
                                  height_shift_range=0.1, # 위, 아래로 이동
                                  # rotation_range=5, # 5도 사이의 값으로
                                  #shear_range=0.7,
                                  # zoom_range=[0.9, 2.2],
                                  #vertical_flip=True,
                                  fill_mode='nearest') # 빈 데이터는 가장 가까운 픽셀데이터를 넣어줌
validation_generator = validation_datagen.flow_from_dataframe(
     validate_df,
     "./train/",
     x_col='filename',
     y_col='category',
     target_size=IMAGE_SIZE,
     class_mode='categorical',
     batch_size=batch_size
 )

# In[181]:


augs = train_generator.__getitem__(0 )
plt.figure(figsize=(30,30))
for i, img in enumerate(augs[0]):
    plt.subplot(4,8,i+1)
    plt.axis('off')
    plt.imshow(img.squeeze())

# In[185]:


from keras.callbacks import ModelCheckpoint, EarlyStopping
import os # 저장

MODEL_DIR = './model/'
if not os.path.exists(MODEL_DIR):
    os.mkdir(MODEL_DIR)
    
modelpath = './model/ {epoch:02d} - {val_loss:.4f}.hdf5'
checkpointer = ModelCheckpoint(filepath=modelpath, monitor='val_loss', verbose = 1, save_best_only=True)

early_stopping_callback = EarlyStopping(monitor='val_loss', patience=10)

model.compile(loss='binary_crossentropy', optimizer= optimizers.Adam(learning_rate=0.0002),# instance 사용가능
             metrics=['accuracy'])  # categorical_crossentropy
history = model.fit(train_generator,  epochs=50, 
                    validation_data=validation_generator,validation_steps=24,
                   steps_per_epoch=32, callbacks=[early_stopping_callback, checkpointer]) # 모델 컴파일 및 학습

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
y_vloss = history.history['val_loss']
y_loss = history.history['loss']

x_len = np.arange(len(y_loss))
plt.plot(x_len, acc, marker='.', c='red', label='Trainset_acc')
plt.plot(x_len, val_acc, marker='.', c='lightcoral', label='Testset_acc')
plt.plot(x_len, y_vloss, marker=".", c="cornflowerblue", label='Testset_loss')
plt.plot(x_len, y_loss, marker=".", c="blue", label='Trainset_loss')

plt.legend(loc='upper right')
plt.grid
plt.xlabel('epoch')
plt.ylabel('loss')
plt.show()
