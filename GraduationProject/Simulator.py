import json
import numpy as np
from Model import EnemyInstance, TowerInstance, Map, dataPack, User, Score
import random
from EnvironmentSet import data

def simulation(app):
    blankColor = "#000000" # 黑色
    roadColor = "#FFFFFF" # 白色
    enemyColor = "#0000FF" # 蓝色
    towerColor = "#FF0000" # 红色
    towerName = {1:"汽油", 2:"瓶子", 3:"太阳", 4:"风扇", 5:"冰星"}
    enemyName = {1:"a", 2:"b", 3:"c"}

    gridMap = Map(data["Map"]["mapHeight"], data["Map"]["mapWidth"], data["Map"]["mapStart"], data["Map"]["mapEnd"], data["Road"])

    roadInfo = data["Road"]
    lenRoad = len(roadInfo) # 道路格子编号从0到lenRoad-1

    initWealth = data["UserInitialWealth"]
    user = User(initWealth)

    towerConfig = data["Tower"]
    enemyConfig = data["Enemy"]
    enemyWave = data["EnemyWave"] # 定义之后三种敌人每回合出来一个

    TECount = dataPack()
    TDScore = Score()
    towerIns, enemyIns = {}, {} # 存放的是塔的实例，表示的是 {id:instance} 
    solve = {}
    
    flag = 0
    
    full_input = json.loads(input())
    if len(full_input["log"]) == 0:
        print(json.dumps({
            "command": "request",
            "content": {
                "0": data
            },
            "display": data
        }))
        exit()
    else:
        for i in range(1, len(full_input["log"]), 2):
            solve[str(int((i+1)/2))] = full_input["log"][i]["0"]["response"]
    
    #elif len(full_input["log"]) == 2:
    #    solve = full_input["log"][1]["0"]["response"]
    
    def place_tower(app, num): # 放置塔
        pT = solve[str(num)]
        tmp = pT.keys()
        po = [tuple(int(i) for i in el.strip('()').split(',')) for el in tmp]
        tmp = pT.values()
        costCount = sum([towerConfig[str(k)]["tPrice"] for k in tmp])
        flag = 0
        if costCount > user.uWealth:
            app.logs.insert(len(app.logs), "财富不足以建塔")
            flag = -2
            return po, flag
        for k in po:
            (x,y) = k
            if x < 0 or x >= gridMap.mapWidth or y < 0 or y >= gridMap.mapHeight:
                app.logs.insert(len(app.logs), "建塔点不能超出地图范围：" + str((x,y)))
                flag = -1
                break
            if [x,y] in roadInfo:
                app.logs.insert(len(app.logs), "建塔点不能在道路上：" + str((x,y)))
                flag = -3
                break
            elif len(gridMap.mapInfo[x][y]) > 0:
                app.logs.insert(len(app.logs), "建塔点不能在已有塔格点处：" + str((x,y)) + "，格点处已有塔：" + str(gridMap.mapInfo[x][y])) 
                flag = -4
                break

            newTowerType = pT[str(k)]
            newTowerData = towerConfig[str(newTowerType)]
            towerIns[TECount.towerCount] = TowerInstance(newTowerData["tType"],newTowerData["tAttack"],newTowerData["tPrice"],newTowerData["tRange"],newTowerData["tFreq"],newTowerData["tSlowRate"], [x,y])
            gridMap.mapInfo[x][y] += [TECount.towerCount]
            TECount.towerCount += 1
        
            app.mapgrid[x][y]["bg"] = towerColor # TODO
            app.mapgrid[x][y]["text"] = "波次" + str(num) + towerName[newTowerType]
        if flag == 0:
            user.uWealth -= costCount
            app.logs.insert(len(app.logs), "成功放置塔：")
            for k in pT:
                app.logs.insert(len(app.logs), str(k) + ":" + towerName[pT[k]])
        return po, flag

    def attack_enemy(app):
        app.logs.insert(len(app.logs), "开始攻击")
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
                    app.logs2.insert(len(app.logs2), "攻击敌人时，敌人实例列表中没有此敌人")
                    flag = -5
                    break
                tAttack = dictEidEhpEspeed[k]["tAttack"]
                tSlowRate = dictEidEhpEspeed[k]["tSlowRate"]
                app.logs2.insert(len(app.logs2), str(k)+"号敌人遭受攻击前，原血量为"+ str(enemyIns[k].eRestHP) + "，应减少血量" + str(tAttack))
                res = enemyIns[k].reveive_attack(tAttack, tSlowRate)
                app.logs2.insert(len(app.logs2), str(k)+"号敌人遭受攻击后，血量变为"+ str(enemyIns[k].eRestHP))
                if res == -1:
                    pos = enemyIns[k].position
                    [x, y] = gridMap.roadInfo[pos]
                    [x2, y2] = dictEidEhpEspeed[k]["ePos"]
                    if x != x2 or y != y2:
                        app.logs2.insert(len(app.logs2), "攻击敌人时，敌人在地图上的坐标" + str(x,y) + "与塔检测坐标" + str((x2,y2)) + "不一致")
                        flag = -6
                        break
                    gridMap.enemyStep[-1] += pos # 计算小分：计算敌人走了几步
                    gridMap.enemyReward[-1] += enemyIns[k].eReward # 计算小分：计算消灭敌人获得了多少奖励
                    user.uWealth += enemyIns[k].eReward # 消灭敌人得的奖励
                    enemyIns.pop(k)
                    if k not in gridMap.mapInfo[x][y]:
                        app.logs2.insert(len(app.logs2), "攻击敌人时，塔检测实施打击的位于" + str((x,y)) + "的敌人不在地图上")
                        flag = -7
                        break
                    gridMap.mapInfo[x][y].remove(k) # remove(value)
                    if len(gridMap.mapInfo[x][y]) == 1: # 这个格子的敌人被打死了，之后这个格子里没有了敌人
                        app.mapgrid[x][y]["bg"] = roadColor
                    app.mapgrid[x][y]["text"] = ''.join(enemyName[int(enemyIns[e].eType)] for e in gridMap.mapInfo[x][y] if e >= 0)
            if flag != 0:
                break
        return flag

    def produce_enemy(app, en):
        sen = ""
        tmpID = TECount.enemyCount
        for i in range(len(en)):
            tmpNum = en[i]
            if tmpNum > 0: # 新敌人持续产生
                en[i] -= 1
                eType = str(i+1) # "Enemy"
                enemyIns[tmpID] = EnemyInstance(eType, enemyConfig[eType]["eHP"], enemyConfig[eType]["eSpeed"], enemyConfig[eType]["eReward"]) 
                tmpID += 1
                sen += enemyName[i+1]
        if len(sen) != 0:
            app.logs2.insert(len(app.logs2), "等待产生的敌人为：" + sen)
        TECount.enemyCount = tmpID
        return en

    def go_ahead_enemy(app, num):
        app.logs2.insert(len(app.logs2), "敌人行进")
        flag = 0
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
                app.logs2.insert(len(app.logs2), "敌人行进时，坐标" + str((x,y)) + "处没有此敌人")
                flag = -8
                break
            res = enemyIns[k].go_forward()
            if res == -100 or res == -200:
                continue
            if res != -100 and res != -200:
                if res < 0:
                    app.logs2.insert(len(app.logs2), "敌人行进时的道路格子下标成负数了")
                    flag = -9
                    break
                elif res >= lenRoad:
                    app.logs.insert(len(app.logs), "波次"+str(num)+"没有成功")
                    app.logs2.insert(len(app.logs2), "编号为"+str(k)+"的敌人抵达了终点")
                    flag = 1
                    break
            gridMap.mapInfo[x][y].remove(k) # remove(value)
            if len(gridMap.mapInfo[x][y]) == 1: # 这个格子的敌人向前进了一步，之后这个格子里没有了敌人
                app.mapgrid[x][y]["bg"] = roadColor

            # print(str(gridMap.mapInfo[x][y]))
            app.mapgrid[x][y]["text"] = ''.join(enemyName[int(enemyIns[e].eType)] for e in gridMap.mapInfo[x][y] if e >= 0)

            enemyIns[k].position = res
            [x, y] = gridMap.roadInfo[res]
            gridMap.mapInfo[x][y] += [k]
            app.mapgrid[x][y]["bg"] = enemyColor
            if "text" in app.mapgrid[x][y]:
                app.mapgrid[x][y]["text"] += enemyName[int(enemyIns[k].eType)]
            else:
                app.mapgrid[x][y]["text"] = enemyName[int(enemyIns[k].eType)]
        return flag


    for x in range(gridMap.mapWidth):
        for y in range(gridMap.mapHeight):
            app.mapgrid[x][y]["bg"] = blankColor

    for grid in gridMap.roadInfo:
        [x,y] = grid
        app.mapgrid[x][y]["bg"] = roadColor

    cycle = min(int(len(full_input["log"])/2), len(enemyWave.keys()))
    enemyStat = [0, 0, 0]
    for i in range(1, cycle + 1): # 从波次1到现在的波次，range的右边这项最大是len(enemyWave.keys()) + 1
        en = enemyWave[str(i)] # 按波次放敌人，[num1，num2，num3]表示三种类型敌人的个数
        enemyStat = [enemyStat[i] + en[i] for i in range(3)]
        flag = 0 # towerCount = len(towerIns.keys())
        if i == 1:
            app.logs.insert(len(app.logs), "第"+str(i)+"波次")
            app.logs2.insert(len(app.logs2), "第"+str(i)+"波次")
        else:
            app.logs.insert(len(app.logs), "第"+str(i)+"波次")
            app.logs2.insert(len(app.logs2), "第"+str(i)+"波次")
        gridMap.enemyStep += [0]
        gridMap.enemyReward += [0]
        # TODO：放置塔
        po, flag = place_tower(app, i)
        yield

        if flag != 0:
            break

        # 开始模拟攻击及敌人行进
        while True:
            restEnemy = len(enemyIns.keys())
            if restEnemy == 0 and sum(en) == 0: # 敌人实例被消灭完且这一波没有产生新的敌人
                break
            flag = attack_enemy(app)# 攻击
            yield flag
            if flag != 0:
                break
            en = produce_enemy(app, en)# 新敌人的产生
            yield
            flag = go_ahead_enemy(app, i)# 敌人行进
            yield flag
            if flag != 0:
                break
        if flag != 0:
            break
    
    TDScore.reward = 0.1 * sum(gridMap.enemyReward) / sum([enemyConfig[str(i+1)]["eReward"] * enemyStat[i] for i in range(3)])
    TDScore.step = 0.1 * (1 - sum(gridMap.enemyStep) / ( sum(enemyStat) * lenRoad ) )
    
    command = "request"
    if flag == 0 and len(full_input["log"]) == 2 * len(enemyWave.keys()):
        app.logs.insert(len(app.logs), "本关通过")
        app.logs2.insert(len(app.logs2), "本关通过")
        TDScore.result = 1
        command = "finish"
    elif flag != 0:
        app.logs.insert(len(app.logs), "本关未通过")
        app.logs2.insert(len(app.logs2), "本关未通过")
        TDScore.result = 0
        command = "finish"
    print(json.dumps({
            "command": command,
            "content": {
                "0": flag
            },
            "display": {
                "flag": flag,
                "logs": app.logs[-1],
                "logs2": app.logs2[-1],
                "gridMap": gridMap,
                "score": TDScore
            }
        }, default=lambda o:o.__dict__))