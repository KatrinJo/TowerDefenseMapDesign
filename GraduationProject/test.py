import numpy as np
import math
import os
import io 
import string
import json



def tet():
    print(a[0])
a = [1,2,3,4]

# b = 0
def func():
    global b
    b += 3
    print(b)

{
    "display": {
        "Road": [[0, 0], [0, 1], [1, 1], [1, 2], [1, 3], [2, 3], [3, 3], [4, 3], [4, 4], [5, 4], [6, 4], [6, 5], [6, 6], [6, 7], [6, 8], [7, 8], [7, 9], [8, 9], [9, 9]], 
        "EnemyTypeNum": 3, 
        "UserInitialWealth": 1000, 
        "EnemyWave": {
            "9": [2, 3, 7], 
            "8": [0, 4, 5], 
            "10": [2, 5, 10],
            "6": [0, 3, 2], 
            "2": [1, 3, 0], 
            "1": [2, 1, 0], 
            "4": [2, 3, 1], 
            "7": [0, 4, 3], 
            "3": [2, 2, 1], 
            "5": [0, 3, 0]}, 
            "Enemy": {
                "2": {
                    "eSpeed": 2, 
                    "eReward": 56, 
                    "eHP": 20
                    }, 
                "1": {
                    "eSpeed": 1, 
                    "eReward": 28, 
                    "eHP": 30
                    }, 
                "3": {
                    "eSpeed": 0.5, 
                    "eReward": 98, 
                    "eHP": 800
                    }
            }, 
            "Map": {"mapEnd": [9, 9], "mapHeight": 10, "mapStart": [0, 0], "mapWidth": 10}, 
            "Tower": {"4": {"tFreq": 1, "tPrice": 160, "tType": "pack-line", "tSlowRate": 1, "tAttack": 12, "tRange": 3}, "5": {"tFreq": 0.25, "tPrice": 180, "tType": "pack-round", "tSlowRate": 0, "tAttack": 5, "tRange": 3}, "2": {"tFreq": 1, "tPrice": 100, "tType": "single", "tSlowRate": 1, "tAttack": 10, "tRange": 2}, "1": {"tFreq": 1, "tPrice": 160, "tType": "single", "tSlowRate": 1, "tAttack": 24, "tRange": 2}, "3": {"tFreq": 1, "tPrice": 180, "tType": "pack-round", "tSlowRate": 1, "tAttack": 17, "tRange": 2}}, "TowerTypeNum": 5}, 
            "command": "request", 
            "content": {
                "0": {
                    "Road": [[0, 0], [0, 1], [1, 1], [1, 2], [1, 3], [2, 3], [3, 3], [4, 3], [4, 4], [5, 4], [6, 4], [6, 5], [6, 6], [6, 7], [6, 8], [7, 8], [7, 9], [8, 9], [9, 9]], 
                    "EnemyTypeNum": 3, "UserInitialWealth": 1000, "EnemyWave": {"9": [2, 3, 7], "8": [0, 4, 5], "10": [2, 5, 10], "6": [0, 3, 2], "2": [1, 3, 0], "1": [2, 1, 0], "4": [2, 3, 1], "7": [0, 4, 3], "3": [2, 2, 1], "5": [0, 3, 0]}, "Enemy": {"2": {"eSpeed": 2, "eReward": 56, "eHP": 20}, "1": {"eSpeed": 1, "eReward": 28, "eHP": 30}, "3": {"eSpeed": 0.5, "eReward": 98, "eHP": 800}}, "Map": {"mapEnd": [9, 9], "mapHeight": 10, "mapStart": [0, 0], "mapWidth": 10}, "Tower": {"4": {"tFreq": 1, "tPrice": 160, "tType": "pack-line", "tSlowRate": 1, "tAttack": 12, "tRange": 3}, "5": {"tFreq": 0.25, "tPrice": 180, "tType": "pack-round", "tSlowRate": 0, "tAttack": 5, "tRange": 3}, "2": {"tFreq": 1, "tPrice": 100, "tType": "single", "tSlowRate": 1, "tAttack": 10, "tRange": 2}, "1": {"tFreq": 1, "tPrice": 160, "tType": "single", "tSlowRate": 1, "tAttack": 24, "tRange": 2}, "3": {"tFreq": 1, "tPrice": 180, "tType": "pack-round", "tSlowRate": 1, "tAttack": 17, "tRange": 2}}, "TowerTypeNum": 5}}}
