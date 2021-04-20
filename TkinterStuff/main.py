from Games import *
from tkinter import ttk

root = Tk()
root.title("Tab Widget")
tabControl = ttk.Notebook(root)

tab1 = GameOfLifeFrame(root, 10, 10)
tab2 = TickTacToeFrame(root)
tab3 = ChaosTheoryFrame(root, 1000, 1000)

tabControl.add(tab1, text = 'Game of life')
tabControl.add(tab2, text = 'TickTacToe')
tabControl.add(tab3, text = 'ChaosTheoryDemo')
tabControl.pack(expand = 1, fill ="both")

root.mainloop()