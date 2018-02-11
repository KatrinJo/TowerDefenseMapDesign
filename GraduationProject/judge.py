import numpy as np
import warnings
import json
import os
import io
import queue

que = queue.PriorityQueue()
que.put(3)
que.put(1)
que.put(10)
que.get()

