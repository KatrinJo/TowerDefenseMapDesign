import json
import numpy as np
from pprint import pprint
from collections import OrderedDict
from User import User
from Model import EnemyInstance, TowerInstance, Map
from GUI import Application
import tkinter as tk
import random

def simulation():
    global towerCount, enemyCount
    if towerCount <= 0 or enemyCount <= 0:
        return -1 # TODO：确定返回值格式
    return 0


if __name__ == '__main__':
    with open("../config/record.json","r") as f:
        data = json.load(f)

    with open("../config/solve.json","r") as f:
        solve = json.load(f)
        
            

    gridMap = Map(data["Map"]["mapHeight"], data["Map"]["mapWidth"], data["Map"]["mapStart"], data["Map"]["mapEnd"], data["Road"])
    roadInfo = data["Road"]
    lenRoad = len(roadInfo) # 道路格子编号从1到lenRoad-1

    initWealth = data["UserInitialWealth"]
    user = User(initWealth)

    towerConfig = data["Tower"]
    enemyConfig = data["Enemy"]
    enemyWave = data["EnemyWave"] # 定义之后三种敌人每回合出来一个

    towerMaxID, enemyMaxID = 0, 0
    towerCount, enemyCount = 0, 0
    towerIns, enemyIns = {}, {} # 存放的是塔的实例，表示的是 {id:instance} 
    
    flag = 0
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

    for i in range(1, len(enemyWave.keys()) + 1):
        en = enemyWave[str(i)] # 按波次放敌人，[num1，num2，num3]表示三种类型敌人的个数
        flag = 0
        # towerCount = len(towerIns.keys())

        # TODO：放置塔
        placeNewTower = solve[str(i)]
        tmp = placeNewTower.keys()
        po = [tuple(int(i) for i in el.strip('()').split(',')) for el in tmp]
        tmp = placeNewTower.values()
        costCount = 0
        for k in tmp:
            costCount += towerConfig[str(k)]["tPrice"]
        if costCount > user.uWealth:
            print("财富不足以建塔")
            flag = -4
            break
        print(po)
        for k in po:
            (x,y) = k
            if x < 0 or x >= gridMap.mapHeight or y < 0 or y >= gridMap.mapWidth:
                print("不能超出地图范围")   
                flag = -5
                break
            if [x,y] in roadInfo:
                print("不能在道路上建塔")
                flag = -1
                break
            if len(gridMap.mapInfo[x][y]) > 0:
                print(gridMap.mapInfo[x][y])
                print((x,y))
                print("不能在已有塔处建塔")
                flag = -3
                break
            newTowerType = placeNewTower[str(k)]
            newTowerData = towerConfig[str(newTowerType)]
            towerIns[towerCount] = TowerInstance(newTowerData["tType"],newTowerData["tAttack"],newTowerData["tPrice"],newTowerData["tRange"],newTowerData["tFreq"],newTowerData["tSlowRate"], [x,y])
            gridMap.mapInfo[x][y] += [towerCount]
            towerCount += 1

        user.uWealth -= costCount

        if flag != 0:
            break

        # print("tower:"+str(towerIns))
        # print("enemy:"+str(enemyIns))
        dictEidEhpEspeed = {"-1": {"ePos":[-1,-1], "tAttack":0, "tSlowRate":1}}
        while True:
            enemyCount = len(enemyIns.keys())
            if enemyCount == 0 and sum(en) == 0: # 敌人实例被消灭完且这一波没有产生新的敌人
                break
            # TODO：攻击
            for i in towerIns.keys(): # 对于每个塔都要进行攻击统计
                tower = towerIns[i]
                tpos = tower.position
                dictEidEhpEspeed = tower.detect_and_attack(gridMap)
                enemyKeys = dictEidEhpEspeed.keys()
                if len(enemyKeys) == 0:
                    continue
                for k in enemyKeys:
                    if k < 0 or type(k) != 'int': 
                        continue
                    if k not in enemyIns:
                        print("敌人实例列表中没有此敌人")
                        break
                    tAttack = dictEidEhpEspeed[k]["tAttack"]
                    tSlowRate = dictEidEhpEspeed[k]["tSlowRate"]
                    res = enemyIns[k].reveive_attack(tAttack, tSlowRate)
                    if res == -1:
                        pos = enemyIns[k].position
                        [x, y] = gridMap.roadInfo[pos]
                        [x2, y2] = dictEidEhpEspeed[k]["ePos"]
                        if x != x2 or y != y2:
                            flag = -10
                            break
                        user.uWealth += enemyIns[k].eReward
                        enemyIns.pop(k)
                        if k not in gridMap.mapInfo[x][y]:
                            flag = -11
                            break
                        gridMap.mapInfo[x][y].remove(k) # remove(value)
            # TODO：新敌人的产生
            for i in range(len(en)):
                tmpNum = en[i]
                if tmpNum > 0: # 新敌人持续产生
                    en[i] -= 1
                    eType = str(i+1) # "Enemy"
                    enemyIns[enemyMaxID] = EnemyInstance(eType, enemyConfig[eType]["eHP"], enemyConfig[eType]["eSpeed"], enemyConfig[eType]["eReward"]) 
                    enemyMaxID += 1
            print("enemy:"+str([enemyIns[e].position for e in enemyIns.keys()]))
            # TODO：敌人行进
            print("enemyIns.keys() = " + str(enemyIns.keys()))
            for k in enemyIns.keys():
                pos = enemyIns[k].position
                if pos < 0:
                    enemyIns[k].position = 0
                    [x, y] = gridMap.roadInfo[0]
                    gridMap.mapInfo[x][y] += [k]
                    continue
                [x, y] = gridMap.roadInfo[pos]
                #print(dictEidEhpEspeed)
                #[x2, y2] = dictEidEhpEspeed[k]["ePos"]
                #if x != x2 or y != y2:
                #    flag = -10
                #    break
                #enemyIns.pop(k)
                print("k = "+str(k))
                print("[x,y] = " + str([x,y]) + ", " + str(gridMap.mapInfo[x][y]))
                if k not in gridMap.mapInfo[x][y]:
                    print("道路格子上没有这个敌人编号")
                    flag = -11
                    break
                res = enemyIns[k].go_forward()
                if res != -100 and res != -200:
                    if res < 0:
                        print("道路格子下标成负数了")
                        flag = -2
                        break
                    elif res >= lenRoad:
                        print("波次"+str(i+1)+"没有成功，编号为"+str(k)+"的敌人抵达了终点")
                        flag = 1
                        break
                gridMap.mapInfo[x][y].remove(k) # remove(value)
                enemyIns[k].position = res
                [x, y] = gridMap.roadInfo[res]
                gridMap.mapInfo[x][y] += [k]
            if flag != 0:
                break
        if flag != 0:
            break
    print(flag)
    if flag == 0:
        print("本关通过")