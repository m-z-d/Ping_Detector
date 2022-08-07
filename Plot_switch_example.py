import matplotlib as mpl
import matplotlib.backends.backend_tkagg as tkBEnd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tkinter as tk

class MainApp(tk.Tk):
    def __init__(self,**kws) -> None:
        super().__init__()
        self.GenerateGraphs()
        self.GridMainwindow()
    
    def GridMainwindow(self):
        self.main_window_frame=tk.Frame(self)
        self.main_window_graph=tk.Canvas(self.main_window_frame)
        self.display_graph_1=False
        self.main_window_refresh_button=tk.Button(self.main_window_frame,
            text="Refresh",command=self.RefreshGraph)

    def RefreshGraph(self):
        self.display_graph_1= not self.display_graph_1
    def GenerateGraphs(self):
        data1 =pd.read_csv()

screen=MainApp()
screen.RefreshGraph()