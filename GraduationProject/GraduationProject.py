import json
import numpy as np
from pprint import pprint
from collections import OrderedDict
from User import User
from Model import EnemyInstance, TowerInstance, Map

def distance(point1, point2):
    return np.linalg.norm((np.array(point1) - np.array(point2)), ord=2)

def simulation():
    global towerCount, enemyCount
    if towerCount <= 0 or enemyCount <= 0:
        return -1 # TODO：确定返回值格式
    pass


if __name__ == '__main__':
    with open("../config/record.json","r") as f:
        data = json.load(f)
        # pprint(data)
        # print(type(data))

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
    for i in range(1, len(enemyWave.keys()) + 1):
        en = enemyWave[str(i)] # 按波次放敌人，[num1，num2，num3]表示三种类型敌人的个数
        flag = 0
        while True:
            towerCount = len(towerIns.keys())
            enemyCount = len(enemyIns.keys())
            if enemyCount == 0 and sum(en) == 0: # 敌人实例被消灭完且这一波没有产生新的敌人
                break
            # TODO：读入User的place_new_tower函数，确定在地图上的哪一些位置需要放置塔的实例
            # 返回的是字典，key表示坐标，value表示放置第几类炮塔
            
            newTowers, cost = user.place_new_tower(gridMap,towerConfig)
            costCount = 0
            for k in newTowers.keys():
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
                    print("不能在已有塔处建塔")
                    flag = -3
                    break
                newTowerType = newTowers[k]
                newTowerData = towerConfig[newTowerType]
                towerIns[towerCount] += [TowerInstance(newTowerData["tType"],newTowerData["tAttack"],newTowerData["tPrice"],newTowerData["tRange"],newTowerData["tFreq"],newTowerData["tSlowRate"])]
                costCount += newTowerData["tPrice"]
                if costCount > user.uWealth:
                    print("财富不足以建塔")
                    flag = -4
                    break
                gridMap.mapInfo[x][y] += [towerCount]
                towerCount += 1
            if flag != 0:
                break
            # TODO：攻击
            for i in towerCount.keys(): # 对于每个塔都要进行攻击统计
                tower = towerIns[i]
                tid = tower.tid
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
                        enemyIns.pop(k)
            # TODO：新敌人的产生
            for i in len(en):
                tmpNum = en[i]
                if tmpNum > 0: # 新敌人持续产生
                    en[i] -= 1
                    eType = "eType"+str(i+1) # "Enemy"
                    enemyIns[enemyMaxID] = EnemyInstance(eType, enemyConfig[eType]["eHP"], enemyConfig[eType]["eSpeed"])
                    enemyMaxID += 1
            # TODO：敌人行进
            for k in enemyIns.keys():
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
            if flag != 0:
                break
        if flag != 0:
            break
    if flag == 0:
        print("本关通过")