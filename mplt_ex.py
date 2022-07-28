import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tkinter as tk
data1=pd.read_csv(r"example.csv")
dataf1=pd.DataFrame(data1)
print(dataf1)
root= tk.Tk()
root.wm_title('pinging')
fig=plt.Figure(figsize=(5,5),dpi=200)
ax=fig.add_subplot()