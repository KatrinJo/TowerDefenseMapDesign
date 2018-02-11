import tkinter as tk
import random

def say_fuck():
    print("fuck")

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
               b["bg"] = "#" + format(r.randint(0, (1 << 24) - 1), "06x")
               b["text"] = (i, j)

        btnframe = tk.Frame(self)
        btnframe.pack()

        self.test = tk.Button(btnframe)
        self.test["text"] = "Say H*"
        self.test["command"] = self.say_hi
        self.test.pack(side=tk.LEFT)

        self.test2 = tk.Button(btnframe)
        self.test2["text"] = "Say F*"
        self.test2["command"] = say_fuck
        self.test2.pack(side=tk.LEFT)

        logframe = tk.Frame(self)
        logframe.pack(fill=tk.BOTH, expand=1)

        scrollbar = tk.Scrollbar(logframe, orient=tk.VERTICAL)
        self.logs = tk.Listbox(logframe, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.logs.yview)
        self.logs.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        scrollbar.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.logs.insert(tk.END, "log1", "log22222222222222222222222222222", "log3")
        
        scrollbar2 = tk.Scrollbar(logframe, orient=tk.VERTICAL)
        self.logs2 = tk.Listbox(logframe, yscrollcommand=scrollbar2.set)
        scrollbar2.config(command=self.logs2.yview)
        self.logs2.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        scrollbar2.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.logs2.insert(tk.END, "log1", "log2", "log3")

    def say_hi(self):
        print("hi there, everyone!")

#root = tk.Tk()
#app = Application(master=root)
#app.mainloop()