import matplotlib as mpl
import matplotlib.backends.backend_tkagg as tkBEnd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tkinter as tk
counter=0
def increase_counter():
    global dataf1, dataf2,counter
    counter +=1
    if counter%2==1:
        print('A'+str(counter))
        ax.clear()
        dataf2.plot(kind="line", legend=True, ax=ax)
    else:
        print('B'+str(counter))
        ax.clear()
        dataf1.plot(kind="line", legend=True, ax=ax)
data1=pd.read_csv(r"example2.csv")
data2=pd.read_csv(r"example1.csv")
dataf1=pd.DataFrame(data1)
dataf2=pd.DataFrame(data2)
print(dataf1)
root= tk.Tk()
root.title('pinging')
root.resizable(False,False)
fig=plt.Figure(figsize=(8,5),dpi=100)
ax=fig.add_subplot()
graph=tkBEnd.FigureCanvasTkAgg(fig,root)
graph.get_tk_widget().pack()
dataf1.plot(kind="line", legend=True, ax=ax)
tk.Button(root,text="└────────────┘",command=increase_counter,width=50).pack()
root.mainloop()