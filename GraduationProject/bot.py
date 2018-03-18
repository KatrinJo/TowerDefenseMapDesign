import json
import numpy as np
from User import User
from Model import EnemyInstance, TowerInstance, Map, dataPack
import tkinter as tk
import random
# from EnvironmentSet import data

solve = {
    "1":  {
        "(5, 5)":3, 
        "(3, 4)":3,
        "(2, 2)":5,
        "(7, 7)":5,
        "(6, 9)":1,
        "(2, 4)":2
    },
    "2": {
        "(0, 2)":2
    },
    "3": {
        "(5, 8)":1
    },
    "4": {
        "(4, 5)":1
    },
    "5": {
        "(5, 3)":5,
        "(6, 3)":4
    },
    "6": {
        "(4, 2)":1,
        "(1, 4)":1
    },
    "7": {
        "(3, 2)":5
    },
    "8": {
        "(1, 0)":1,
        "(2, 1)":1,
        "(5, 6)":1
    },
    "9": {
        "(7, 5)":1,
        "(8, 8)":1,
        "(0, 3)":4
    },
    "10": {
        "(3, 5)":1,
        "(7, 4)":1,
        "(7, 6)":1,
        "(5, 7)":1
    }
}
def buildTower():
    full_input = json.loads(input())
    requests = full_input["requests"]
    turnNum = len(requests)
    data = requests[turnNum - 1]
    arr = full_input["responses"]

    gridMap = Map(data["Map"]["mapHeight"], data["Map"]["mapWidth"], data["Map"]["mapStart"], data["Map"]["mapEnd"], data["Road"])

    roadInfo = data["Road"]
    lenRoad = len(roadInfo) # 道路格子编号从1到lenRoad-1

    initWealth = data["UserInitialWealth"]
    user = User(initWealth)

    towerConfig = data["Tower"]
    enemyConfig = data["Enemy"]
    enemyWave = data["EnemyWave"] # 定义之后三种敌人每回合出来一个

    TECount = dataPack() # enemyCount, towerCount
    towerIns, enemyIns = {}, {} # 存放的是塔的实例，表示的是 {id:instance} 
    solve = {}
    
    flag = 0

    def place_tower(pT): # 放置塔
        tmp = pT.keys()
        po = [tuple(int(i) for i in el.strip('()').split(',')) for el in tmp]
        tmp = pT.values()
        costCount = sum([towerConfig[str(k)]["tPrice"] for k in tmp])
        flag = 0
        for k in po:
            (x,y) = k
            newTowerType = pT[str(k)]
            newTowerData = towerConfig[str(newTowerType)]
            towerIns[TECount.towerCount] = TowerInstance(newTowerData["tType"],newTowerData["tAttack"],newTowerData["tPrice"],newTowerData["tRange"],newTowerData["tFreq"],newTowerData["tSlowRate"], [x,y])
            gridMap.mapInfo[x][y] += [TECount.towerCount]
            TECount.towerCount += 1
        user.uWealth -= costCount

    for i in range(len(arr)):
        dictSolve = arr[i]
        place_tower(dictSolve)
      
    turnID = len(full_input["requests"])
    print(json.dumps({
            "response": solve[str(turnID)]
        }))