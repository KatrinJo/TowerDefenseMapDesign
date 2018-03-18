import random
from Simulator import simulation


class Application:
    def __init__(self):
        self.mapgrid = []
        self.logs = []
        self.logs2 = []
        self.create_widgets()

    def create_widgets(self):
        for i in range(10):
            row = []
            self.mapgrid.append(row)
            for j in range(10):
               b = {}
               row.append(b)

app = Application()

iterator = simulation(app)

try:
    while True:
        iterator.send(None)
except Exception as e:
    pass