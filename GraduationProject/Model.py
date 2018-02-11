import numpy as np
import warnings

class Map:
    def __init__(self,h, w, s, e, ri):
        self.mapHeight = h
        self.mapWidth = w
        self.mapStart = s
        self.mapEnd = e
        
        
        tmpMapInfo = [[[] for i in range(w)] for j in range(h)]# 存放：-1表示路径，其余表示敌人的eID
        #print(tmpMapInfo)
        tmpMapInfo = np.array(tmpMapInfo).tolist()
        self.roadInfo = ri
        for grid in ri:
            [x,y] = grid
            tmpMapInfo[x][y] += [-1]
        self.mapInfo = tmpMapInfo

class EnemyInstance:
    def __init__(self, type, hp, speed, reward):
        self.eType = type
        self.eHP = hp
        self.eSpeed = speed
        self.eNextMoveTimeRest = 0 # 表示下次移动还剩多少回合，max(int(1/eSpeed)-1,0)
        self.position = -1 # 表示在道路上的第几个格子上
        self.eRestHP = hp
        self.eCurrSpeed = speed
        self.eReward = reward

    def reveive_attack(self, subHP, subSpeed):
        self.eRestHP -= subHP
        self.eCurrSpeed *= subSpeed
        if self.eRestHP <= 0:
            return -1
        return 0
    
    def go_forward(self): # TODO:确定返回值格式
        if self.eNextMoveTimeRest > 0: # 这一回合不能前进，需要等待
            self.eNextMoveTimeRest -= 1
            return -100
        if self.eCurrSpeed == 0: # 这一回合能前进，但是速度为0
            self.eCurrSpeed = self.eSpeed
            return -200
        self.eCurrSpeed = self.eSpeed
        self.eNextMoveTimeRest = max(int(1/self.eCurrSpeed)-1,0) # 这一回合能前进，看速度
        return self.position + max(1, self.eCurrSpeed)

class TowerInstance:
    def __init__(self, type, attack, price, range, freq, slowrate, pos):
        self.tType = type # 塔的攻击种类——单体、群体攻击
        self.tAttack = attack # 攻击力
        self.tPrice = price # 建造价格
        self.tRange = range # 攻击范围，也即射程
        self.tFreq = freq # 攻击频率，使用时需要 int(1/self.tFreq)来判断几回合进行一次攻击
        self.tSlowRate = slowrate # 表示塔的减速率，让敌人减速减到int(Enemy.eSpeed * Tower.tSlowRate) 格子/回合
        self.tNextAttackTimeRest = 0 # 表示下次攻击还剩多少回合
        self.position = pos # [x, y]
    
    # 返回值：对于某个固定的炮塔侦测到可以实施打击的敌人eID，并且可以打击掉敌人多少血量，减慢敌人多少速度
    def detect_and_attack(self, map): 
        if self.tNextAttackTimeRest > 0: # 这一回合炮塔不能攻击
            self.tNextAttackTimeRest -= 1
            return {"-1": {"ePos":[-1,-1], "tAttack":0, "tSlowRate":1}}

        dictEidEhpEspeed = {}
        roadInfo = map.roadInfo
        for i in range(len(roadInfo)-1,-1,-1): # 找触发条件
            if len(dictEidEhpEspeed.keys()) > 0:
                break
            [x, y] = roadInfo[i] # x,y是道路的某个格子的横纵坐标
            dis = np.linalg.norm((np.array(roadInfo[i]) - np.array(self.position)), ord=2) # 先确定是否在射程之内
            if dis > self.tRange:
                continue
            if len(map.mapInfo[x][y]) == 0: # 确定在射程之内的格子上是否有敌人
                continue

            # 触发攻击条件：射程内的某格子上存在敌人，可以实施打击（根据炮塔种类确定是否打击）
            towerType = self.tType
            [sx, sy] = self.position # sx和sy是炮塔的横纵坐标，含义为self.x
            if "single" in towerType: # 只攻击一个敌人
                for k in map.mapInfo[x][y]:
                    dictEidEhpEspeed[k] = {"ePos":[x,y], "tAttack": self.tAttack, "tSlowRate":self.tSlowRate}
                    return dictEidEhpEspeed
                # 暂时选择（1）中的FIFO —— 有几种炮塔的攻击策略：
                # （1）根据敌人在list中的顺序FIFO/LIFO； （2）根据敌人的剩余血量从大到小/从小到大
                # （3）根据敌人的速度从大到小/从小到大； （4）根据敌人种类手动排序 。。。 
            elif "pack" in towerType:
                if "round" in towerType: # 攻击一周的敌人
                    for j in range(i, -1, -1):
                        [tx, ty] = roadInfo[j] # 道路上的第j个格子，做tmpx之意
                        for k in map.mapInfo[tx][ty]:
                            if k < 0 or type(k) != 'int': # k要保证是大于等于0的整数
                                continue
                            dictEidEhpEspeed[k] = {"ePos":[tx,ty], "tAttack": self.tAttack, "tSlowRate":self.tSlowRate}
                elif "line" in towerType:
                    if sx != x and sy != y: # 只攻击在竖直方向和水平方向上的敌人
                        continue
                    elif sx == x and sy == y:
                        print("Model-error：炮塔和道路的横纵坐标重合")
                    elif sx == x: # dictEidEhpEspeed，把敌人的eID和攻击杀掉的血量、减慢的速度倍速放在这里
                        for j in range(i, -1, -1):
                            [tx, ty] = roadInfo[j]
                            if tx != x or (sy - y)*(sy - ty) <= 0: # 道路上的格子不在一条横线上，或与敌人不在炮塔的同一侧
                                continue
                            for k in map.mapInfo[tx][ty]: # mapInfo的list里存放的是移动到这里的敌人的eID，要么为空
                                if k < 0 or type(k) != 'int': # k要保证是大于等于0的整数
                                    continue
                                dictEidEhpEspeed[k] = {"ePos":[tx,ty], "tAttack": self.tAttack, "tSlowRate":self.tSlowRate}
                    else:
                        for j in range(i, -1, -1):
                            [tx, ty] = roadInfo[j]
                            if ty != y or (sx - x)*(sx - tx) <= 0: # 竖线，类似以上的横线处理
                                continue
                            for k in map.mapInfo[tx][ty]:
                                if k < 0 or type(k) != 'int': 
                                    continue
                                dictEidEhpEspeed[k] = {"ePos":[tx,ty], "tAttack": self.tAttack, "tSlowRate":self.tSlowRate}
        self.tNextAttackTimeRest = 0
        if len(dictEidEhpEspeed.keys()) > 0:
            tmpKey = list(dictEidEhpEspeed.keys())
            numEnemy = sum(1 for number in tmpKey if number > 0)
            if numEnemy > 0:
                self.tNextAttackTimeRest = max(int(1/self.tFreq)-1, 0)
        return dictEidEhpEspeed


a = [1,2,3,4,5]
a.pop(3) # list.pop(index)
if 3 in a:
    a.remove(3) # list.remove(value)
else:
    print("a数组中没有3")
# list concat : [] + [] direct add

a = ['1','2','3','4']+[3,3,4,5,6,7]  # list可以直接相加    
