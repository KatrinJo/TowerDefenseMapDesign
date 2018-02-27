import tkinter as tk
import random
from GraduationProject import simulation

blankColor = "#000000" # 黑色
roadColor = "#FFFFFF" # 白色
enemyColor = "#0000FF" # 蓝色
towerColor = "#FF0000" # 红色

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=1)
        self.mapgrid = []
        self.create_widgets()

    def create_widgets(self):
        r = random.Random()
        g = self.mapgridwidget = tk.Frame(self)
        g.pack()
        for i in range(10):
            row = []
            self.mapgrid.append(row)
            for j in range(10):
               b = tk.Button(g)
               row.append(b)
               b.grid(row=i, column=j)
               b.config(height = 2, width = 10)
               b["bg"] = blankColor # "#" + format(r.randint(0, (1 << 24) - 1), "06x") #  "#{:06x}".format(r.randint(0, (1 << 24) - 1))
               # b["text"] = (i, j)

        btnframe = tk.Frame(self)
        btnframe.pack()

        self.test = tk.Button(btnframe)
        self.test["text"] = "Next"
        self.test.pack(side=tk.LEFT)

        logframe = tk.Frame(self)
        logframe.pack(fill=tk.BOTH, expand=1)

        scrollbar = tk.Scrollbar(logframe, orient=tk.VERTICAL)
        self.logs = tk.Listbox(logframe, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.logs.yview)
        
        self.logs.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y, expand=1)
        
        scrollbar2 = tk.Scrollbar(logframe, orient=tk.VERTICAL)
        self.logs2 = tk.Listbox(logframe, yscrollcommand=scrollbar2.set)
        scrollbar2.config(command=self.logs2.yview)
        self.logs2.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        scrollbar2.pack(side=tk.LEFT, fill=tk.Y, expand=1)

    def say_hi(self):
        print("hi there, everyone!")

root = tk.Tk()
app = Application(master=root)

iterator = simulation(app)

def go_next():
    iterator.send(None)

app.test["command"] = go_next
app.mainloop()