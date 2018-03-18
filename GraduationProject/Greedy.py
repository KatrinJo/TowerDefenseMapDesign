import json
import numpy as np
from User import User
from Model import EnemyInstance, TowerInstance, Map, dataPack
import random
import operator
import copy
# from EnvironmentSet import data


x = {1: 2, 3: 4, 4: 3, 2: 1, 0: 0}
sorted_x_val = sorted(x.items(), key=operator.itemgetter(1), reverse=True)
sorted_x_key = sorted(x.items(), key=operator.itemgetter(0))

def buildTower():
    full_input = json.loads(input())
    requests = full_input["requests"]
    turnNum = len(requests)
    data = requests[0]
    arr = full_input["responses"]

    gridMap = Map(data["Map"]["mapHeight"], data["Map"]["mapWidth"], data["Map"]["mapStart"], data["Map"]["mapEnd"], data["Road"])

    roadInfo = data["Road"]
    lenRoad = len(roadInfo) # 1~lenRoad-1

    initWealth = data["UserInitialWealth"]
    user = User(initWealth)

    towerConfig = data["Tower"]
    enemyConfig = data["Enemy"]
    enemyWave = data["EnemyWave"] # ����֮�����ֵ���ÿ�غϳ���һ��

    TECount = dataPack() # enemyCount, towerCount
    towerIns, enemyIns = {}, {} # ��ŵ�������ʵ������ʾ���� {id:instance} 
    
    flag = 0
    
    dist = {
        1:[(0,-1),(0,1),(1,0),(-1,0)],
        2:[(-1,-1),(-1,1),(1,1),(1,-1)],
        4:[(0,-2),(0,2),(2,0),(-2,0)],
        5:[(-1,-2),(-2,-1),(1,-2),(-2,1),(1,2),(2,1),(-1,2),(2,-1)],
        8:[(-2,-2),(-2,2),(2,2),(2,-2)],
        9:[(0,-3),(0,3),(3,0),(-3,0)]
        } # �����ƽ��

    wealthWave, costWave, rewardWave = {}, {}, {} # enemyConfig["1"]["eReward"]
    wealthWave["0"] = initWealth
    costWave["0"] = 0 # cost_k <= wealthWave[str(k)] - costWave[str(k - 1)] , costWave[str(k)] = costWave[str(k - 1)] + cost_k 
    for i in range(1, len(enemyWave.keys()) + 1):
        wealthWave[str(i)] = wealthWave[str(i - 1)] + sum([enemyWave[str(i)][k] * enemyConfig[str(k+1)]["eReward"] for k in range(3)])
    
    def invalidXY(x, y):
        if x < 0 or x >= gridMap.mapWidth or y < 0 or y >= gridMap.mapHeight:
            return False
        return True

    round2Map, round3Map, line3Map = {}, {}, {} # 距离在2格子以内的
    tmp2Map, tmp3Map, tmpLineMap = {}, {}, {}

    for x in range(gridMap.mapWidth): # 统计在三个格子内能碰到的连续横向格子数和竖向格子数
        for y in range(gridMap.mapHeight):
            if [x,y] in roadInfo:
                continue
            tmpArr = [0,0,0,0]
            tmpFlag = 0
            for nx in range(x-1, -1, -1):
                if nx < x-3 and tmpArr[0] == 0: # 如果在三个格子之内碰不到
                    break   
                if tmpFlag == 1 and [nx, y] not in roadInfo: # 断了连续的条件
                    break
                if [nx, y] in roadInfo:
                    tmpFlag = 1
                    tmpArr[0] += 1
            tmpFlag = 0
            for nx in range(x+1, gridMap.mapWidth):
                if nx > x+3 and tmpArr[1] == 0:
                    break   
                if tmpFlag == 1 and [nx, y] not in roadInfo:
                    break
                if [nx, y] in roadInfo:
                    tmpFlag = 1
                    tmpArr[1] += 1
            tmpFlag = 0
            for ny in range(y-1, -1, -1):
                if ny < y-3 and tmpArr[2] == 0: # 如果在三个格子之内碰不到
                    break   
                if tmpFlag == 1 and [x, ny] not in roadInfo: # 断了连续的条件
                    break
                if [x, ny] in roadInfo:
                    tmpFlag = 1
                    tmpArr[2] += 1
            tmpFlag = 0
            for ny in range(y+1, gridMap.mapHeight):
                if ny > y+3 and tmpArr[3] == 0: # 如果在三个格子之内碰不到
                    break   
                if tmpFlag == 1 and [x, ny] not in roadInfo: # 断了连续的条件
                    break
                if [x, ny] in roadInfo:
                    tmpFlag = 1
                    tmpArr[3] += 1
            if sum(tmpArr) !=  0:
                line3Map[str((x,y))] = tmpArr
                # tmpLineMap[str((x,y))] = sum(tmpArr)
                
    
    for i in range(len(roadInfo)-1, -1, -1):
        (x, y) = roadInfo[i]
        for k in dist.keys():
            for t in dist[k]:
                (dx, dy) = t
                (nx, ny) = (dx + x, dy + y)
                if not invalidXY(nx, ny):
                    continue
                if [nx, ny] in roadInfo:
                    continue
                tmp = str((nx, ny))
                if tmp not in round3Map:
                    round3Map[tmp] = [i]
                    tmp3Map[tmp] = 1
                else:
                    round3Map[tmp] += [i]
                    tmp3Map[tmp] += 1
                if k > 4:
                    continue
                if tmp not in round2Map:
                    round2Map[tmp] = [i]
                    tmp2Map[tmp] = 1
                else:
                    round2Map[tmp] += [i]
                    tmp2Map[tmp] += 1


    # solvePT是字典，{"(x,y)":k}，表示在(x,y)放置一个第k类型的塔
    def simulation(i, solvePT, money):
        sMap = copy.deepcopy(gridMap)
        sUser = User(money) # sUser = copy.deepcopy(user)
        stIns = copy.deepcopy(towerIns)
        steCount = copy.deepcopy(TECount)
        seIns = copy.deepcopy(enemyIns)
        sEnemyWave = copy.deepcopy(enemyWave[str(i)])
        sFlag = 0
        def try_place(pT):
            sFlag = 0
            tmp = pT.keys()
            po = [tuple(int(i) for i in el.strip('()').split(',')) for el in tmp]
            tmp = pT.values()
            costCount = sum([towerConfig[str(k)]["tPrice"] for k in tmp])
            if sUser.uWealth < costCount:
                return -2
            for k in po:
                (x,y) = k
                if not invalidXY(x, y):
                    print("模拟中出错：建塔点不能超出地图范围")
                    sFlag = -1
                    break
                if [x,y] in roadInfo:
                    print("模拟中出错：建塔点不能在道路上")
                    sFlag = -3
                    break
                if len(sMap.mapInfo[x][y]) > 0:
                    print("模拟中出错：建塔点不能在已有塔的格子上")
                    sFlag = -4
                    break
                newTowerType = pT[str(k)]
                newTowerData = towerConfig[str(newTowerType)]
                stIns[steCount.towerCount] = TowerInstance(newTowerData["tType"],newTowerData["tAttack"],newTowerData["tPrice"],newTowerData["tRange"],newTowerData["tFreq"],newTowerData["tSlowRate"], [x,y])
                sMap.mapInfo[x][y] += [steCount.towerCount]
                steCount.towerCount += 1
            if sFlag == 0:
                sUser.uWealth -= costCount
            return sFlag
        
        def try_attack():
            dictAttack = {-1: {"ePos":[-1,-1], "tAttack":0, "tSlowRate":1}}
            sFlag = 0
            for i in stIns.keys():
                tower = stIns[i]
                tpos = tower.position
                dictAttack = tower.detect_and_attack(sMap)
                enemyKeys = dictAttack.keys()

                if len(enemyKeys) == 0:
                    continue
                for k in enemyKeys:
                    if k < 0: 
                        continue
                    if k not in seIns:
                        sFlag = -5
                        break
                    tAttack = dictAttack[k]["tAttack"]
                    tSlowRate = dictAttack[k]["tSlowRate"]
                    res = seIns[k].reveive_attack(tAttack, tSlowRate)
                    if res == -1:
                        pos = seIns[k].position
                        [x, y] = sMap.roadInfo[pos]
                        [x2, y2] = dictAttack[k]["ePos"]
                        if x != x2 or y != y2:
                            sFlag = -6
                            break
                        sUser.uWealth += seIns[k].eReward
                        seIns.pop(k)
                        if k not in sMap.mapInfo[x][y]:
                            sFlag = -7
                            break
                        sMap.mapInfo[x][y].remove(k) # remove(value)
                if sFlag != 0:
                    break
            return sFlag
        
        def try_produce(en):
            if sum(en) == 0:
                return en
            tmpID = steCount.enemyCount
            for i in range(len(en)):
                tmpNum = en[i]
                if tmpNum > 0: # 新敌人持续产生
                    en[i] -= 1
                    eType = str(i+1) # "Enemy"
                    seIns[tmpID] = EnemyInstance(eType, enemyConfig[eType]["eHP"], enemyConfig[eType]["eSpeed"], enemyConfig[eType]["eReward"]) 
                    tmpID += 1
            steCount.enemyCount = tmpID
            return en
    
        def try_goahead():
            sFlag = 0
            for k in seIns.keys():
                pos = seIns[k].position
                if pos < 0:
                    seIns[k].position = 0
                    [x, y] = sMap.roadInfo[0]
                    sMap.mapInfo[x][y] += [k]
                    continue
                [x, y] = sMap.roadInfo[pos]
                if k not in sMap.mapInfo[x][y]:
                    sFlag = -8
                    break
                res = seIns[k].go_forward()
                if res == -100 or res == -200:
                    continue
                if res != -100 and res != -200:
                    if res < 0:
                        sFlag = -9
                        break
                    elif res >= lenRoad:
                        sFlag = 1
                        break
                sMap.mapInfo[x][y].remove(k) # remove(value)
                seIns[k].position = res
                [x, y] = sMap.roadInfo[res]
                sMap.mapInfo[x][y] += [k]
            return sFlag

        # TODO: according to the i-th wave and tehe config, place the tower and do simulation   
        sFlag = try_place(solvePT) # 缺少参数pT
        if sFlag != 0:
            return sFlag, "place_tower：建塔失败，花费超出财富值"
        while True:
            restEnemy = len(seIns.keys())
            if restEnemy == 0 and sum(sEnemyWave) == 0:
                break
            sFlag = try_attack()
            if sFlag != 0:
                return sFlag, "try_attack：攻击失败"
            sEnemyWave = try_produce(sEnemyWave)
            sFlag = try_goahead()
            if sFlag == 1:
                return sFlag, "try_goahead：有敌人抵达终点"
            if sFlag != 0:
                return sFlag, "try_goahead：前进失败"
        return sFlag, "本关模拟通过"
    
    def place_tower(pT): # 表示在实际中放置塔这个操作
        tmp = pT.keys()
        po = [tuple(int(i) for i in el.strip('()').split(',')) for el in tmp]
        tmp = pT.values()
        costCount = sum([towerConfig[str(k)]["tPrice"] for k in tmp])
        user.uWealth -= costCount
        flag = 0
        for k in po:
            (x,y) = k
            newTowerType = pT[str(k)]
            newTowerData = towerConfig[str(newTowerType)]
            towerIns[TECount.towerCount] = TowerInstance(newTowerData["tType"],newTowerData["tAttack"],newTowerData["tPrice"],newTowerData["tRange"],newTowerData["tFreq"],newTowerData["tSlowRate"], [x,y])
            gridMap.mapInfo[x][y] += [TECount.towerCount]
            TECount.towerCount += 1
        return costCount

    poIceStar = [] # distance->sum([(a[i] - b[i])**2 for i in range(2)])
    # recover the history
    numOfTowerType = [0,0,0,0,0] # array-[],idx+1:type of tower, val:number of tower
    for i in range(len(arr)): # arr�����飬��ŵ��Ǹ�����֮ǰ�Ľ�����i<->��i+1����
        dictSolve = arr[i] # dictSolve-{"(x,y)":typeOfTower}
        for k in dictSolve:
            type = dictSolve[k]
            numOfTowerType[type-1] += 1
            poIceStar += [tuple(int(i) for i in k.strip('()').split(','))]
            tmp2Map.pop(k)
            tmp3Map.pop(k)
            line3Map.pop(k)
        cost_k = place_tower(dictSolve) # cost of placing the tower in specific position
        costWave[str(i+1)] = costWave[str(i)] + cost_k

    user.uWealth = wealthWave[str(turnNum - 1)] - costWave[str(turnNum - 1)]

    sort_tmp2_val = sorted(tmp2Map.items(), key=operator.itemgetter(1), reverse=True) # [('(6, 9)', 5), ('(8, 8)', 5)...]
    sort_tmp3_val = sorted(tmp3Map.items(), key=operator.itemgetter(1), reverse=True)
    sort_line_val = sorted(line3Map.items(), key=operator.itemgetter(1), reverse=True)
    
    # TODO: ensure the strategy of placing towers
    money = user.uWealth
    numOfNewTowerType = numOfTowerType
    priceOfTower = [towerConfig[str(i)]["tPrice"] for i in range(1,6)]
    res = {}
    lastResKeysNum = 0
    breakCondition = 0
    while True: # 一个cycle就决定建一座塔！先确定塔的类型，再决定建在哪里
        if money < min(priceOfTower):
            break
        lastResKeysNum = len(res.keys())
        if max(numOfNewTowerType) - min(numOfNewTowerType) > 3 and min(numOfNewTowerType) <= 2 and breakCondition == 0:
            # 如果上下差距过大，那么优先建的是数量少的塔，保证有一定的合作度
            idx = [i for i,val in enumerate(numOfNewTowerType) if val == min(numOfNewTowerType) and money >= priceOfTower[i]]
            if len(idx) == 0:
                breakCondition = 1
                continue
            for time in range(1,-1,-1):
                if breakCondition == 2:
                    # breakCondition = 0
                    break
                if 2 in idx and not breakCondition: # sun
                    for t in sort_tmp2_val:
                        (po, val) = t
                        if val < 3 and time:
                            break
                        (tx, ty) = tuple(int(i) for i in po.strip('()').split(','))
                        if po in res or len(gridMap.mapInfo[tx][ty]) > 0:
                            continue
                        res[po] = 3
                        money -= priceOfTower[2]
                        numOfNewTowerType[2] += 1
                        breakCondition = 2 # 找到一个解，可以找下一个了
                        break
                if 4 in idx and not breakCondition: # iceStar
                    for t in sort_tmp3_val:
                        (po, val) = t
                        if val < 3 and time:
                            break
                        (tx, ty) = tuple(int(i) for i in po.strip('()').split(','))
                        if po in res or len(gridMap.mapInfo[tx][ty]) > 0:
                            continue
                        res[po] = 5
                        money -= priceOfTower[4]
                        numOfNewTowerType[4] += 1
                        breakCondition = 2 # 找到一个解，可以找下一个了
                        break         
                if 0 in idx and not breakCondition: # gas bottle
                    for t in sort_tmp2_val:
                        (po, val) = t
                        if val < 3 and time:
                            break
                        (tx, ty) = tuple(int(i) for i in po.strip('()').split(','))
                        if po in res or len(gridMap.mapInfo[tx][ty]) > 0:
                            continue
                        a = (tx, ty)
                        dist2IceStar = [sum([(a[i] - b[i])**2 for i in range(2)]) for b in poIceStar]
                        if len(dist2IceStar) == 0 or min(dist2IceStar) > 9:
                            res[po] = 1
                            money -= priceOfTower[0]
                            numOfNewTowerType[0] += 1
                            breakCondition = 2 # 找到一个解，可以找下一个了
                            break
                        else:
                            tmpIdx = [i for i,val in enumerate(dist2IceStar) if val == min(dist2IceStar)]
                            res[po] = 1
                            money -= priceOfTower[0]
                            numOfNewTowerType[0] += 1
                            breakCondition = 2 # 找到一个解，可以找下一个了
                            break        
                if 3 in idx and not breakCondition: # fan
                    for t in sort_line_val:
                        (po, val) = t
                        if max(val) < 3 and time:
                            break
                        (tx, ty) = tuple(int(i) for i in po.strip('()').split(','))
                        if po in res or len(gridMap.mapInfo[tx][ty]) > 0:
                            continue
                        res[po] = 4
                        money -= priceOfTower[3]
                        numOfNewTowerType[3] += 1
                        breakCondition = 2 # 找到一个解，可以找下一个了
                        break    
                if 1 in idx and not breakCondition: # bottle, poIceStar = [(1,2),(2,3)]
                    for t in sort_tmp2_val:
                        (po, val) = t
                        if val < 3 and time:
                            break
                        (tx, ty) = tuple(int(i) for i in po.strip('()').split(','))
                        if po in res or len(gridMap.mapInfo[tx][ty]) > 0:
                            continue
                        a = (tx, ty)
                        dist2IceStar = [sum([(a[i] - b[i])**2 for i in range(2)]) for b in poIceStar]
                        if len(dist2IceStar) == 0 or min(dist2IceStar) > 9:
                            res[po] = 2
                            money -= priceOfTower[1]
                            numOfNewTowerType[1] += 1
                            breakCondition = 2 # 找到一个解，可以找下一个了
                            break
                        else:
                            tmpIdx = [i for i,val in enumerate(dist2IceStar) if val == min(dist2IceStar)]
                            res[po] = 2
                            money -= priceOfTower[1]
                            numOfNewTowerType[1] += 1
                            breakCondition = 2 # 找到一个解，可以找下一个了
                            break
                
        else:
            if breakCondition == 1:
                breakCondition = 0
            idx = [i for i,val in enumerate(numOfNewTowerType) if money >= priceOfTower[i]]
            for time in range(1,-1,-1):
                if 2 in idx and not breakCondition: # sun
                    for t in sort_tmp2_val:
                        (po, val) = t
                        if val < 3 and time:
                            break
                        (tx, ty) = tuple(int(i) for i in po.strip('()').split(','))
                        if po in res or len(gridMap.mapInfo[tx][ty]) > 0:
                            continue
                        res[po] = 3
                        money -= priceOfTower[2]
                        numOfNewTowerType[2] += 1
                        breakCondition = 2 # 找到一个解，可以找下一个了
                        break
                if 4 in idx and not breakCondition: # iceStar
                    for t in sort_tmp3_val:
                        (po, val) = t
                        if val < 3 and time:
                            break
                        (tx, ty) = tuple(int(i) for i in po.strip('()').split(','))
                        if po in res or len(gridMap.mapInfo[tx][ty]) > 0:
                            continue
                        res[po] = 5
                        money -= priceOfTower[4]
                        numOfNewTowerType[4] += 1
                        breakCondition = 2 # 找到一个解，可以找下一个了
                        break
                if 0 in idx and not breakCondition: # gas bottle
                    for t in sort_tmp2_val:
                        (po, val) = t
                        if val < 3 and time:
                            break
                        (tx, ty) = tuple(int(i) for i in po.strip('()').split(','))
                        if po in res or len(gridMap.mapInfo[tx][ty]) > 0:
                            continue
                        a = (tx, ty)
                        dist2IceStar = [sum([(a[i] - b[i])**2 for i in range(2)]) for b in poIceStar]
                        if len(dist2IceStar == 0) or min(dist2IceStar) > 9:
                            res[po] = 1
                            money -= priceOfTower[0]
                            numOfNewTowerType[0] += 1
                            breakCondition = 2 # 找到一个解，可以找下一个了
                            break
                        else:
                            tmpIdx = [i for i,val in enumerate(dist2IceStar) if val == min(dist2IceStar)]
                            res[po] = 1
                            money -= priceOfTower[0]
                            numOfNewTowerType[0] += 1
                            breakCondition = 2 # 找到一个解，可以找下一个了
                            break
                if 1 in idx and not breakCondition: # bottle, poIceStar = [(1,2),(2,3)]
                    for t in sort_tmp2_val:
                        (po, val) = t
                        if val < 3 and time:
                            break
                        (tx, ty) = tuple(int(i) for i in po.strip('()').split(','))
                        if po in res or len(gridMap.mapInfo[tx][ty]) > 0:
                            continue
                        a = (tx, ty)
                        dist2IceStar = [sum([(a[i] - b[i])**2 for i in range(2)]) for b in poIceStar]
                        if len(dist2IceStar == 0) or min(dist2IceStar) > 9:
                            res[po] = 2
                            money -= priceOfTower[1]
                            numOfNewTowerType[1] += 1
                            breakCondition = 2 # 找到一个解，可以找下一个了
                            break
                        else:
                            tmpIdx = [i for i,val in enumerate(dist2IceStar) if val == min(dist2IceStar)]
                            res[po] = 2
                            money -= priceOfTower[1]
                            numOfNewTowerType[1] += 1
                            breakCondition = 2 # 找到一个解，可以找下一个了
                            break
                if 3 in idx and not breakCondition: # fan
                    for t in sort_line_val:
                        (po, val) = t
                        if max(val) < 3 and time:
                            break
                        (tx, ty) = tuple(int(i) for i in po.strip('()').split(','))
                        if po in res or len(gridMap.mapInfo[tx][ty]) > 0:
                            continue
                        res[po] = 4
                        money -= priceOfTower[3]
                        numOfNewTowerType[3] += 1
                        breakCondition = 2 # 找到一个解，可以找下一个了
                        break
        sFlag, _ = simulation(len(arr)+1, res, user.uWealth)
        if sFlag == 0 or len(res.keys()) == lastResKeysNum: # avoid dead cycle
            break
        if sFlag != 0 and breakCondition == 2:
            breakCondition = 0
    
    
    turnID = len(full_input["requests"])
    print(json.dumps({
            "response": res
        }))

buildTower()