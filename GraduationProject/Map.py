import numpy as np
import warnings
# from collections import namedtuple

# Pair = namedtuple("Pair", ["first", "second"])

class Map:
    def __init__(self,h, w, s, e, ri):
        self.mapHeight = h
        self.mapWidth = w
        self.mapStart = s
        self.mapEnd = e
        
        tmpMapInfo = [[]] * w # 存放：-1表示路径
        tmpMapInfo = [tmpMapInfo] * h
        self.mapInfo = np.array(tmpMapInfo)
        self.roadInfo = np.array(ri)
        
        for i in range(len(ri)):
            [x,y] = ri[i]
            np.append(self.mapInfo[x][y], -(i+1)) # the road is not overlapped



