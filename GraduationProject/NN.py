import os
import io
import math
import codecs
import numpy as np
import string
import shutil
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential, Model
from keras.layers import Conv2D, MaxPooling2D, Input
from keras.layers.core import Reshape
from keras.layers import Activation, Dropout, Flatten, Dense, Embedding, LSTM
from keras import backend as K
import tensorflow as tf
from keras.optimizers import SGD,Adam,Adagrad
from keras.layers.merge import Concatenate
import json
import numpy as np
from Model import EnemyInstance, TowerInstance, Map, dataPack, User, Score
import random
import copy
from EnvironmentSet import data
from NNSimulator import simulation

roadInfo = [
    [ 0, 0 ],
    [ 0, 1 ],
    [ 1, 1 ],
    [ 1, 2 ],
    [ 1, 3 ],
    [ 2, 3 ],
    [ 3, 3 ],
    [ 4, 3 ],
    [ 4, 4 ],
    [ 5, 4 ],
    [ 6, 4 ],
    [ 6, 5 ],
    [ 6, 6 ],
    [ 6, 7 ],
    [ 6, 8 ],
    [ 7, 8 ],
    [ 7, 9 ],
    [ 8, 9 ],
    [ 9, 9 ]
]

enemyWave = [3,3,2]

w, h = 10, 10
tmpMapInfo = [[0 for i in range(w)] for j in range(h)]# 存放：-1表示路径，其余表示敌人的eID
tmpMapInfo = np.array(tmpMapInfo) # .tolist()
x_train0 = copy.deepcopy(tmpMapInfo)
x_train1 = copy.deepcopy(tmpMapInfo)
x_train2 = copy.deepcopy(tmpMapInfo)
x_train3 = copy.deepcopy(tmpMapInfo)
x_train4 = copy.deepcopy(tmpMapInfo)
x_train5 = copy.deepcopy(tmpMapInfo)
in0,in1,in2,in3,in4,in5 = 0,0,0,0,0,0
for grid in roadInfo:
    [x,y] = grid
    x_train0[x][y] = 1

main_input = Input(shape=(10,10, ), dtype='int32', name='main_input')

gridMap = Map(data["Map"]["mapHeight"], data["Map"]["mapWidth"], data["Map"]["mapStart"], data["Map"]["mapEnd"], data["Road"])
towerConfig = data["Tower"]
enemyConfig = data["Enemy"]
enemyWave = data["EnemyWave"]
def my_loss(y_true, y_pred):
    global in0,in1,in2,in3,in4,in5,gridMap,enemyWave
    inputs = [in1,in2,in3,in4,in5]
    towerIns = {}
    TECount = dataPack()
    tmpMap = copy.deepcopy(gridMap)
    user = User(1000)
    solve = {}
    flag = 0
    for i in range(10):
        if flag:
            break
        for j in range(10):
            if flag:
                break
            for k in range(5):
                if y_pred[k][i][j]:
                    if str((i,j)) in solve:
                        flag = 1
                        break
                    solve[str((i,j))] = k
                if inputs[k][i][j]: # recover
                    newTowerData = towerConfig[str(k+1)]
                    towerIns[TECount.towerCount] = TowerInstance(newTowerData["tType"],newTowerData["tAttack"],newTowerData["tPrice"],newTowerData["tRange"],newTowerData["tFreq"],newTowerData["tSlowRate"], [i,j])
                    tmpMap.mapInfo[i][j] += [TECount.towerCount]
                    TECount.towerCount += 1
    if flag == 1:
        return 100000
    res = simulation(tmpMap, user, TECount, towerIns, enemyWave, solve) # paraGridMap, paraUser, paraTECount, paraTowerIns, paraEnemyWave, solve):
    if res.result == 1:
        return 5000*(0.1-res.step)
    else:
        return 500000*(0.2-res.reward-res.step)

with tf.device('/cpu:0'):
    try:
        input_shape = (10, 10, )

        in0 = Input(shape = input_shape)
        in1 = Input(shape = input_shape)
        in2 = Input(shape = input_shape)
        in3 = Input(shape = input_shape)
        in4 = Input(shape = input_shape)
        in5 = Input(shape = input_shape)

        ou1 = Dense(100, activation='sigmoid')(Flatten()(in1))
        ou2 = Dense(100, activation='sigmoid')(Flatten()(in2))
        ou3 = Dense(100, activation='sigmoid')(Flatten()(in3))
        ou4 = Dense(100, activation='sigmoid')(Flatten()(in4))
        ou5 = Dense(100, activation='sigmoid')(Flatten()(in5))
        
        ou1 = Reshape((10,10))(ou1)
        ou2 = Reshape((10,10))(ou2)
        ou3 = Reshape((10,10))(ou3)
        ou4 = Reshape((10,10))(ou4)
        ou5 = Reshape((10,10))(ou5)
        
        model = Model(inputs = [in0,in1,in2,in3,in4,in5], outputs = [ou1,ou2,ou3,ou4,ou5])
        rmsprop = Adagrad(lr=0.01, epsilon=1e-8, decay=0.)#Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)
        # sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        model.compile(optimizer=rmsprop,loss=my_loss,metrics=['accuracy'])
        graph = tf.get_default_graph()

        # 改成
        model.fit(x = [x_train0,x_train1,x_train2,x_train3,x_train4,x_train5], y = [[], [], [], [], []])

        # model.save('model')
    finally:
        pass
  

print(np.mean(result,axis=0))
print('hello')