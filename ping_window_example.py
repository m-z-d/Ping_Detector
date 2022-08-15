from time import perf_counter
import matplotlib as mpl
import matplotlib.backends.backend_tkagg as tkBEnd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tkinter as tk
import subprocess as sp
import re as re
import logging as lg
import CustomExceptionHandler
lg.basicConfig(level=lg.INFO)
class App(tk.Tk):
    def __init__(self,output_csv:str|None=r"example5.csv",input_url:str|None="python.org") -> None:
        super().__init__()
        self.resizable(width=False, height=False)  #custom window settings
        self.configure(bg='#202020')


        self.output_csv=output_csv
        self.pinged_adress=input_url
        self.ping_stream=sp.Popen(["ping",str(self.pinged_adress),"-t"],stdout=sp.PIPE,universal_newlines=True)
        with open(self.output_csv,'w')as f:
            print('',file=f,end='')  #clearing the file contents. (yes, inefficient, but it's enough)
        with open(self.output_csv,'a') as f:
            print("\"time(s)\",\"ping(ms)\"\n\"0\",\"0\"",file=f)
        self.MakeWidgets()
        self.start_time_value=perf_counter()
        self.ReadPingStream()

    def ReadPingStream(self):
        self.last_line_read=self.ping_stream.stdout.readline()
        self.after(1000,self.ReadPingStream)
        #input sanitisation
        regex_match=re.search("time=[0-9]*",self.last_line_read)
        if regex_match:self.current_ping_time=regex_match.group()[5:]
        else:self.current_ping_time=np.NaN ;lg.info("failed to detect ping")
        self.time_since_start=round(perf_counter()-self.start_time_value,1)  #time index rounded to tenth for readability
          #log the value to relevant outputs 
        self.title(f"{self.current_ping_time}ms►{self.pinged_adress}")
        with open(self.output_csv,'a') as f:
            print(f"\"{self.time_since_start}\",\"{self.current_ping_time}\"",file=f)
        self.RedrawGraph()

    def RedrawGraph(self):
        df=pd.read_csv(self.output_csv)
        self.ax.clear()
        self.ax.plot(df["time(s)"],df["ping(ms)"],linestyle=':',color="#cfd5ff",lw=2)
        self.ax.set_ylabel("Ping response time(ms)",size=20,color="#cfd5ff")
        self.ax.set_xlabel("Time since start(ms)",size=20,color="#cfd5ff")
        self.graph.draw()
        self.fig.savefig("Figure.svg")

    def MakeWidgets(self):
        self.top_label=tk.Label(self,
            text=f'pinging {self.pinged_adress}...',
            font=("Arial","20"),
            bg="#202020",fg="#cfd5ff")
        self.explaining_label=tk.Label(self,
            text="the graph represents the values written in the specified CSV file.\nA hole in the graph represents a ping timeout",
            font=("Arial",8),
            bg="#202020",fg="#cfd5ff")
        self.GenerateGraphs()
        self.graph.get_tk_widget().pack(side=tk.BOTTOM)
        self.top_label.pack(side=tk.TOP)
        self.explaining_label.pack(side=tk.TOP)
    def GenerateGraphs(self):
        df=pd.read_csv(self.output_csv)
        self.fig:plt.Figure=plt.Figure(
            figsize=(16,9),
             dpi=50,
             facecolor="#202020",)
        self.ax:plt.Axes=self.fig.add_subplot()
        self.ax.set_facecolor("#202020")
        self.ax.tick_params(which="both",colors="#cfd5ff",length=5,labelsize=20)
        self.ax.set_ylabel("Ping response time(ms)")
        self.ax.set_xlabel("Time since start(ms)")
        # for i in self.ax.spines.values():
        #     i.set_color("#cfd5ff")
        self.ax.spines['bottom'].set_color("#cfd5ff")
        self.ax.spines['left'].set_color("#cfd5ff")
        self.ax.spines['top'].set_color("#202020")
        self.ax.spines['right'].set_color("#202020")
        self.graph=tkBEnd.FigureCanvasTkAgg(self.fig,master=self)
        self.ax.plot(df,'o--b')
        self.graph.draw()


        




app=App()
app.mainloop()