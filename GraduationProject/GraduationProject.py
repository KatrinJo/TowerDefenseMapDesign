import json
import numpy as np
from pprint import pprint
from collections import OrderedDict
from User import User
from Model import EnemyInstance, TowerInstance, Map
import tkinter as tk
import random

blankColor = "#000000" # 黑色
roadColor = "#FFFFFF" # 白色
enemyColor = "#0000FF" # 蓝色
towerColor = "#FF0000" # 红色


with open("../config/record.json","r") as f:
    data = json.load(f)

with open("../config/solve.json","r") as f:
    solve = json.load(f)
        
towerName = {1:"汽油", 2:"瓶子", 3:"太阳", 4:"风扇", 5:"冰星"}
enemyName = {1:"a", 2:"b", 3:"c"}

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

def place_tower(app, num): # 放置塔
    global solve, gridMap, towerConfig, flag, user, towerCount, towerIns
    pT = solve[str(num)]
    tmp = pT.keys()
    po = [tuple(int(i) for i in el.strip('()').split(',')) for el in tmp]
    tmp = pT.values()
    costCount = sum([towerConfig[str(k)]["tPrice"] for k in tmp])
    if costCount > user.uWealth:
        print("财富不足以建塔")
        flag = -4
        return po, flag
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
            print("格子上有：" + str(gridMap.mapInfo[x][y]) + ", 坐标为" + str((x,y)))
            print("不能在已有塔处建塔")
            flag = -3
            break

        newTowerType = pT[str(k)]
        newTowerData = towerConfig[str(newTowerType)]
        towerIns[towerCount] = TowerInstance(newTowerData["tType"],newTowerData["tAttack"],newTowerData["tPrice"],newTowerData["tRange"],newTowerData["tFreq"],newTowerData["tSlowRate"], [x,y])
        gridMap.mapInfo[x][y] += [towerCount]
        towerCount += 1
        
        app.mapgrid[x][y]["bg"] = towerColor # TODO
        app.mapgrid[x][y]["text"] = "波次" + str(num) + towerName[newTowerType]
    if flag == 0:
        user.uWealth -= costCount
        app.logs.insert(tk.END, "成功放置塔：")
        for k in pT:
            app.logs.insert(tk.END, str(k) + ":" + towerName[pT[k]])
    return po, flag

def attack_enemy(app):
    global towerIns, enemyIns, gridMap, flag, user
    app.logs.insert(tk.END, "开始攻击")
    dictEidEhpEspeed = {-1: {"ePos":[-1,-1], "tAttack":0, "tSlowRate":1}}
    for i in towerIns.keys(): # 对于每个塔都要进行攻击统计
        tower = towerIns[i]
        tpos = tower.position
        dictEidEhpEspeed = tower.detect_and_attack(gridMap)
        enemyKeys = dictEidEhpEspeed.keys()# enemyKeys = [int(e) for e in enemyKeys]
        if len(enemyKeys) == 0:
            continue
        for k in enemyKeys:
            if k < 0: 
                continue
            if k not in enemyIns:
                print("敌人实例列表中没有此敌人")
                flag = -40
                break
            tAttack = dictEidEhpEspeed[k]["tAttack"]
            tSlowRate = dictEidEhpEspeed[k]["tSlowRate"]
            app.logs2.insert(tk.END, str(k)+"号敌人遭受攻击前，原血量为"+ str(enemyIns[k].eRestHP) + "，应减少血量" + str(tAttack))
            res = enemyIns[k].reveive_attack(tAttack, tSlowRate)
            app.logs2.insert(tk.END, str(k)+"号敌人遭受攻击后，血量变为"+ str(enemyIns[k].eRestHP))
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
                if len(gridMap.mapInfo[x][y]) == 1: # 这个格子的敌人被打死了，之后这个格子里没有了敌人
                    app.mapgrid[x][y]["bg"] = roadColor
                app.mapgrid[x][y]["text"] = ''.join(enemyName[int(enemyIns[e].eType)] for e in gridMap.mapInfo[x][y] if e >= 0)
        if flag != 0:
            break
    return flag

def produce_enemy(app, en, enemyMaxID):
    global enemyIns, enemyConfig
    sen = ""
    for i in range(len(en)):
        tmpNum = en[i]
        if tmpNum > 0: # 新敌人持续产生
            en[i] -= 1
            eType = str(i+1) # "Enemy"
            enemyIns[enemyMaxID] = EnemyInstance(eType, enemyConfig[eType]["eHP"], enemyConfig[eType]["eSpeed"], enemyConfig[eType]["eReward"]) 
            enemyMaxID += 1
            sen += enemyName[i+1]
    if len(sen) != 0:
        app.logs2.insert(tk.END, "等待产生的敌人为：" + sen) # print("等待产生的敌人为：" + sen)
    return en, enemyMaxID

def go_ahead_enemy(app, num):
    global enemyIns, gridMap, flag, lenRoad
    app.logs2.insert(tk.END, "敌人行进")
    for k in enemyIns.keys():
        pos = enemyIns[k].position
        if pos < 0:
            enemyIns[k].position = 0
            [x, y] = gridMap.roadInfo[0]
            gridMap.mapInfo[x][y] += [k]
            app.mapgrid[x][y]["bg"] = enemyColor
            continue
        [x, y] = gridMap.roadInfo[pos]
        if k not in gridMap.mapInfo[x][y]:
            print("道路格子上没有这个敌人编号")
            flag = -11
            break
        res = enemyIns[k].go_forward()
        if res == -100 or res == -200:
            continue
        if res != -100 and res != -200:
            if res < 0:
                print("道路格子下标成负数了")
                flag = -2
                break
            elif res >= lenRoad:
                app.logs.insert(tk.END, "波次"+str(num)+"没有成功")
                app.logs2.insert(tk.END, "编号为"+str(k)+"的敌人抵达了终点")
                flag = 1
                break
        gridMap.mapInfo[x][y].remove(k) # remove(value)
        if len(gridMap.mapInfo[x][y]) == 1: # 这个格子的敌人向前进了一步，之后这个格子里没有了敌人
            app.mapgrid[x][y]["bg"] = roadColor

        print(str(gridMap.mapInfo[x][y]))
        app.mapgrid[x][y]["text"] = ''.join(enemyName[int(enemyIns[e].eType)] for e in gridMap.mapInfo[x][y] if e >= 0)

        enemyIns[k].position = res
        [x, y] = gridMap.roadInfo[res]
        gridMap.mapInfo[x][y] += [k]
        app.mapgrid[x][y]["bg"] = enemyColor
        app.mapgrid[x][y]["text"] += enemyName[int(enemyIns[k].eType)]
    if flag == 0:
        pass
    return flag

def simulation(app):
    global data, solve, towerName, enemyName, gridMap, roadInfo, lenRoad, initWealth, user, towerConfig, enemyConfig
    global enemyWave, towerMaxID, enemyMaxID, towerCount, enemyCount, towerIns, enemyIns, flag

    for x in range(gridMap.mapWidth):
        for y in range(gridMap.mapHeight):
            app.mapgrid[x][y]["bg"] = blankColor

    for grid in gridMap.roadInfo:
        [x,y] = grid
        app.mapgrid[x][y]["bg"] = roadColor

    for i in range(1, len(enemyWave.keys()) + 1):
        en = enemyWave[str(i)] # 按波次放敌人，[num1，num2，num3]表示三种类型敌人的个数
        flag = 0 # towerCount = len(towerIns.keys())
        if i == 1:
            app.logs.insert(tk.END, "第"+str(i)+"波次")
            app.logs2.insert(tk.END, "第"+str(i)+"波次")
        else:
            app.logs.insert(tk.END, "", "第"+str(i)+"波次")
            app.logs2.insert(tk.END, "", "第"+str(i)+"波次")
        # TODO：放置塔
        po, flag = place_tower(app, i)
        yield

        if flag != 0:
            break

        # 开始模拟攻击及敌人行进
        while True:
            enemyCount = len(enemyIns.keys())
            if enemyCount == 0 and sum(en) == 0: # 敌人实例被消灭完且这一波没有产生新的敌人
                break
            flag = attack_enemy(app)# 攻击
            yield flag
            en, enemyMaxID = produce_enemy(app, en, enemyMaxID)# 新敌人的产生
            yield
            flag = go_ahead_enemy(app, i)# 敌人行进
            yield flag
            if flag != 0:
                break
        if flag != 0:
            break
    print(flag)
    if flag == 0:
        print("本关通过")