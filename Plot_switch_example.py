import matplotlib as mpl
import matplotlib.backends.backend_tkagg as tkBEnd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tkinter as tk

class MainApp(tk.Tk):
    def __init__(self,**kws) -> None:
        super().__init__()
        self.GridMainwindow()
    
    def GridMainwindow(self):
        self.main_window_frame=tk.Frame(self)
        self.display_graph_1=False
        self.main_window_refresh_button=tk.Button(self.main_window_frame,
            text="Refresh",command=self.RefreshGraph)
        self.GenerateGraphs()
        self.main_window_frame.pack()
        self.main_window_graph.get_tk_widget().grid(row=0,column=0)
        self.main_window_refresh_button.grid(row=0,column=1)

    def RefreshGraph(self):
        self.display_graph_1= not self.display_graph_1
        if self.display_graph_1:
            self.ax.clear()
            self.ax.plot(self.dataf1)
            self.main_window_graph.draw()
        else:
            self.ax.clear()
            self.ax.plot(self.dataf2)
            self.main_window_graph.draw()
    def GenerateGraphs(self):
        self.data1=pd.read_csv(r"Ping_detector/example2.csv")
        self.data2=pd.read_csv(r"Ping_detector/example.csv")
        self.dataf1=pd.DataFrame(self.data1)
        self.dataf2=pd.DataFrame(self.data2)
        self.fig=plt.Figure()
        self.ax=self.fig.add_subplot()
        self.ax.plot(self.dataf1)[0]
        self.ax.set_xlabel("X AXIS")
        self.ax.set_ylabel("Y AXIS")
        self.main_window_graph=tkBEnd.FigureCanvasTkAgg(self.fig,master=self.main_window_frame)
        self.main_window_graph.draw()

screen=MainApp()
screen.RefreshGraph()
screen.mainloop()