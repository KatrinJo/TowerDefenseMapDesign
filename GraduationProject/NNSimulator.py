import json
import numpy as np
from Model import EnemyInstance, TowerInstance, Map, dataPack, User, Score
import random
from EnvironmentSet import data
import copy

def simulation(paraGridMap, paraUser, paraTECount, paraTowerIns, paraEnemyWave, solve):
    gridMap = copy.deepcopy(paraGridMap)
    TECount = copy.deepcopy(paraTECount)
    user = copy.deepcopy(paraUser)
    towerIns = copy.deepcopy(paraTowerIns)
    roadInfo = gridMap.roadInfo
    lenRoad = len(roadInfo) # 道路格子编号从0到lenRoad-1

    towerConfig = data["Tower"]
    enemyConfig = data["Enemy"]
    enemyWave = data["EnemyWave"] # 定义之后三种敌人每回合出来一个

    TDScore = Score()
    enemyIns = {} # 存放的是塔的实例，表示的是 {id:instance} 
    
    flag = 0
    
    def place_tower(num): # 放置塔
        pT = solve
        tmp = pT.keys()
        po = [tuple(int(i) for i in el.strip('()').split(',')) for el in tmp]
        tmp = pT.values()
        costCount = sum([towerConfig[str(k)]["tPrice"] for k in tmp])
        flag = 0
        if costCount > user.uWealth:
            flag = -2
            return po, flag
        for k in po:
            (x,y) = k
            if x < 0 or x >= gridMap.mapWidth or y < 0 or y >= gridMap.mapHeight:
                flag = -1
                break
            if [x,y] in roadInfo:
                flag = -3
                break
            elif len(gridMap.mapInfo[x][y]) > 0:
                flag = -4
                break

            newTowerType = pT[str(k)]
            newTowerData = towerConfig[str(newTowerType)]
            towerIns[TECount.towerCount] = TowerInstance(newTowerData["tType"],newTowerData["tAttack"],newTowerData["tPrice"],newTowerData["tRange"],newTowerData["tFreq"],newTowerData["tSlowRate"], [x,y])
            gridMap.mapInfo[x][y] += [TECount.towerCount]
            TECount.towerCount += 1
        
        if flag == 0:
            user.uWealth -= costCount
        return po, flag

    def attack_enemy():
        dictEidEhpEspeed = {-1: {"ePos":[-1,-1], "tAttack":0, "tSlowRate":1}}
        flag = 0
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
                    flag = -5
                    break
                tAttack = dictEidEhpEspeed[k]["tAttack"]
                tSlowRate = dictEidEhpEspeed[k]["tSlowRate"]
                res = enemyIns[k].reveive_attack(tAttack, tSlowRate)
                if res == -1:
                    pos = enemyIns[k].position
                    [x, y] = gridMap.roadInfo[pos]
                    [x2, y2] = dictEidEhpEspeed[k]["ePos"]
                    if x != x2 or y != y2:
                        flag = -6
                        break
                    gridMap.enemyStep[-1] += pos # 计算小分：计算敌人走了几步
                    gridMap.enemyReward[-1] += enemyIns[k].eReward # 计算小分：计算消灭敌人获得了多少奖励
                    user.uWealth += enemyIns[k].eReward # 消灭敌人得的奖励
                    enemyIns.pop(k)
                    if k not in gridMap.mapInfo[x][y]:
                        flag = -7
                        break
                    gridMap.mapInfo[x][y].remove(k) # remove(value)
            if flag != 0:
                break
        return flag

    def produce_enemy(en):
        tmpID = TECount.enemyCount
        for i in range(len(en)):
            tmpNum = en[i]
            if tmpNum > 0: # 新敌人持续产生
                en[i] -= 1
                eType = str(i+1) # "Enemy"
                enemyIns[tmpID] = EnemyInstance(eType, enemyConfig[eType]["eHP"], enemyConfig[eType]["eSpeed"], enemyConfig[eType]["eReward"]) 
                tmpID += 1
        TECount.enemyCount = tmpID
        return en

    def go_ahead_enemy():
        flag = 0
        for k in enemyIns.keys():
            pos = enemyIns[k].position
            if pos < 0:
                enemyIns[k].position = 0
                [x, y] = gridMap.roadInfo[0]
                gridMap.mapInfo[x][y] += [k]
                continue
            [x, y] = gridMap.roadInfo[pos]
            if k not in gridMap.mapInfo[x][y]:
                flag = -8
                break
            res = enemyIns[k].go_forward()
            if res == -100 or res == -200:
                continue
            if res != -100 and res != -200:
                if res < 0:
                    flag = -9
                    break
                elif res >= lenRoad:
                    flag = 1
                    break
            gridMap.mapInfo[x][y].remove(k) # remove(value)

            enemyIns[k].position = res
            [x, y] = gridMap.roadInfo[res]
            gridMap.mapInfo[x][y] += [k]
        return flag

    enemyStat = [0, 0, 0]
    for i in range(1, 2): # 从波次1到现在的波次，range的右边这项最大是len(enemyWave.keys()) + 1
        en = copy.deepcopy(paraEnemyWave) # 按波次放敌人，[num1，num2，num3]表示三种类型敌人的个数
        enemyStat = [enemyStat[i] + en[i] for i in range(3)]
        flag = 0 # towerCount = len(towerIns.keys())
        gridMap.enemyStep += [0]
        gridMap.enemyReward += [0]
        # TODO：放置塔
        po, flag = place_tower(i)
        yield

        if flag != 0:
            break

        # 开始模拟攻击及敌人行进
        while True:
            restEnemy = len(enemyIns.keys())
            if restEnemy == 0 and sum(en) == 0: # 敌人实例被消灭完且这一波没有产生新的敌人
                break
            flag = attack_enemy()# 攻击
            yield flag
            if flag != 0:
                break
            en = produce_enemy(en)# 新敌人的产生
            yield
            flag = go_ahead_enemy()# 敌人行进
            yield flag
            if flag != 0:
                break
        if flag != 0:
            break
    
    TDScore.reward = 0.1 * sum(gridMap.enemyReward) / sum([enemyConfig[str(i+1)]["eReward"] * enemyStat[i] for i in range(3)])
    TDScore.step = 0.1 * (1 - sum(gridMap.enemyStep) / ( sum(enemyStat) * lenRoad ) )
    
    if flag == 0:
        TDScore.result = 1
    elif flag != 0:
        TDScore.result = 0

    return TDScore