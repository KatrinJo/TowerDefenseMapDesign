import numpy as np
import io
import os
from Model import EnemyInstance, TowerInstance, Map


class User:
    def __init__(self, wealth):
        self.uWealth = wealth

    def place_new_tower(self, map, towerConfig): # 返回的是字典，key表示坐标，value表示放置第几类炮塔
        newTower = {}
        cost = 0
        for x in range(map.mapHeight):
            for y in range(map.mapWidth):
                if [x,y] in map.roadInfo: # 要建塔的位置在道路上
                    continue
                if len(map.mapInfo[x][y]) > 0: # 要建塔的位置上已经有塔了
                    continue
                for k in towerConfig.keys():
                    if cost + towerConfig[k]["tPrice"] > self.uWealth:
                        continue
                    # TODO : 放置炮塔策略
                    if False:
                        newTower[(x, y)] = k
                        cost += towerConfig[k]["tPrice"]
        return newTower, cost

    def reduce_wealth(self, cost):
        self.uWealth -= cost