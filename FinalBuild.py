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
from PIL import Image as img
from PIL import ImageTk as tkimg
from tkinter import messagebox as tkmb
from tkinter import filedialog as tkfd
lg.basicConfig(level=lg.INFO)


def silence_exception(func, exception):
    try:
        func()
    except exception:
        pass


class UtilityContainer(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.configure(bg="#202020")
        self.WelcomeApp = WelcomeScreenApp(self)
        self.PingApp = PingGraphingApp(self)
        self.current_app="WelcomeApp"
        self.WelcomeApp.init()

    def switchApp(self, file: str | None = r"example5.csv", adress: str | None = "python.org"):
        if self.current_app=="WelcomeApp":
            lg.info("switching to PingApp")
            for i in self.grid_slaves():
                i.destroy()
            self.current_app="PingApp"
            self.PingApp.init(output_csv=file,input_url=adress)
        else:
            lg.info("switching to WelcomeApp")
            for i in self.pack_slaves():
                i.destroy()
            self.PingApp.ping_stream=None  #stop the stream to limit CPU/RAM usage
            self.after_cancel(self.PingApp.after_method_id)
            self.current_app="WelcomeApp"
            self.WelcomeApp.init()


class WelcomeScreenApp(tk.Frame):
    def __init__(self, master: UtilityContainer):
        super().__init__(master)
        self.master = master
        self.filename=None
        self.adress=None

    def init(self, *argv):
        self.GridWidgets()

    def GridWidgets(self):
        self.welcome_label = tk.Label(
            self.master, text="Welcome!", font=("Arial", "25"), width=20,
            bg='#202020', fg="#cfd5ff"
        )
        self.version_label = tk.Label(
            self.master, text="to Ping Detector vα1", font=("Arial", "15"),
            bg='#202020', fg="#cfd5ff"
        )
        self.about_button = tk.Button(
            self.master, text="About...", font=("Arial", "10"), width=21, bg='#202020', fg="#cfd5ff",
            command=lambda: silence_exception(lambda: sp.run(['notepad', r'README.md'],
                                                             shell=True, timeout=0.1), sp.TimeoutExpired),  # opens essential info for the user in a separate program
            relief='flat')
        self.options_image = tkimg.PhotoImage(img.open(r"settings.png"))
        self.options_button = tk.Button(
            self.master, image=self.options_image, height=21, width=24, bg='#202020', fg="#cfd5ff",
            command=lambda: silence_exception(lambda: sp.run(['notepad', r'OPTIONS.json'],
                                                             shell=True, timeout=0.1, stderr=None), sp.TimeoutExpired),
            relief='flat'
        )
        self.ping_button = tk.Button(
            self.master, text="Ping!", font=("Arial", "10"), width=21, bg='#202020', fg="#cfd5ff",
            relief='flat',command=lambda:self.master.switchApp(file=self.filename,adress=self.adress)
        )
        self.entry_label=tk.Label(
            self.master, text="Enter the adress you want to ping and choose where you want to save the data:", font=("Arial", 7), width=70,
            bg='#202020', fg="#cfd5ff"
        )
        # self.csv_entry = tk.Entry(
        #     self.master, relief='flat'
        # )
        self.csv_save_button= tk.Button(
            self.master, text="Pick CSV", font=("Arial", "10"), width=21, bg='#202020', fg="#cfd5ff",
            relief='flat',command=self.AskCSVFile
        )
        self.adress_entry=tk.Entry(relief="flat",bg="#cfd5ff",fg="#202020",textvariable=self.adress)

        self.welcome_label.grid(row=0, column=0, columnspan=5)
        self.version_label.grid(row=1, column=0, columnspan=5)
        self.about_button.grid(row=2, column=0, columnspan=2)
        self.options_button.grid(row=2, column=2, columnspan=1)
        self.ping_button.grid(row=2, column=3, columnspan=2)
        # self.csv_entry.grid(row=4,column=0,columnspan=2)
        self.entry_label.grid(row=3,column=0,columnspan=5)
        self.csv_save_button.grid(row=4,column=0,columnspan=2)
        self.adress_entry.grid(row=4,column=3,columnspan=2)
    def AskCSVFile(self):
        file=tkfd.asksaveasfile(parent=self.master,title='Pick A CSV File...',initialfile="Untitled.csv")
        if file is not None:
            lg.info(f"opened {file.name}")
            self.filename=file.name

class PingGraphingApp(tk.Frame):
    """Main ping detector app"""

    def __init__(self, master: UtilityContainer):
        super().__init__(master, bg="#202020")
        self.master = master

    def init(self, output_csv: str | None = r"example5.csv", input_url: str | None = "python.org"):
        # custom window settings
        self.master.resizable(width=True, height=True)
        self.pack()

        if output_csv is None:self.output_csv=r"example5.csv"
        else:self.output_csv = output_csv  #catch NoneTypes
        if input_url is None:self.pinged_adress="python.org"
        else:self.pinged_adress = input_url
        self.ping_stream = sp.Popen(
            ["ping", str(self.pinged_adress), "-t"], stdout=sp.PIPE, universal_newlines=True)
        with open(self.output_csv, 'w')as f:
            # clearing the file contents. (yes, inefficient, but it's enough)
            print('', file=f, end='')
        with open(self.output_csv, 'a') as f:
            print("\"time(s)\",\"ping(ms)\"\n\"0\",\"0\"", file=f)
        lg.info("Set up csv file, ping IO")
        self.MakeWidgets()
        lg.info("widgets packed to frame")
        self.start_time_value = perf_counter()
        self.ReadPingStream()
        lg.info("first ping read")

    def ReadPingStream(self):
        self.last_line_read = self.ping_stream.stdout.readline()
        self.after_method_id=self.master.after(1000, self.ReadPingStream)
        # input sanitisation
        regex_match = re.search("time=[0-9]*", self.last_line_read)
        if regex_match:
            self.current_ping_time = regex_match.group()[5:]
        else:
            self.current_ping_time = np.NaN
            lg.info("failed to detect ping")
        # time index rounded to tenth for readability
        self.time_since_start = round(perf_counter()-self.start_time_value, 1)
        # log the value to relevant outputs
        self.master.title(f"{self.current_ping_time}ms►{self.pinged_adress}")
        with open(self.output_csv, 'a') as f:
            print(
                f"\"{self.time_since_start}\",\"{self.current_ping_time}\"", file=f)
        self.RedrawGraph()

    def RedrawGraph(self):
        df = pd.read_csv(self.output_csv)
        self.ax.clear()
        self.ax.plot(df["time(s)"], df["ping(ms)"],
                     linestyle=':', color="#cfd5ff", lw=2)
        self.ax.set_ylabel("Ping response time(ms)", size=20, color="#cfd5ff")
        self.ax.set_xlabel("Time since start(ms)", size=20, color="#cfd5ff")
        self.graph.draw()
        self.fig.savefig("Figure.svg")

    def MakeWidgets(self):
        self.top_label = tk.Label(self,
                                  text=f'pinging {self.pinged_adress}...',
                                  font=("Arial", "20"),
                                  bg="#202020", fg="#cfd5ff")
        self.explaining_label = tk.Label(self,
                                         text="the graph represents the values written in the specified CSV file.\nA hole in the graph represents a ping timeout",
                                         font=("Arial", 8),
                                         bg="#202020", fg="#cfd5ff")
        self.return_button=tk.Button(
            self.master, text="Return to Welcome Screen", font=("Arial", "10"), width=21, bg='#202020', fg="#cfd5ff",
            relief='ridge',command=lambda:self.master.switchApp())
        self.GenerateGraphs()
        self.graph.get_tk_widget().pack(side=tk.BOTTOM)
        self.top_label.pack(side=tk.TOP)
        self.explaining_label.pack(side=tk.TOP)
        self.return_button.pack(side=tk.TOP)

    def GenerateGraphs(self):
        df = pd.read_csv(self.output_csv)
        self.fig: plt.Figure = plt.Figure(
            figsize=(16, 9),
            dpi=50,
            facecolor="#202020",)
        self.ax: plt.Axes = self.fig.add_subplot()
        self.ax.set_facecolor("#202020")
        self.ax.tick_params(which="both", colors="#cfd5ff",
                            length=5, labelsize=20)
        self.ax.set_ylabel("Ping response time(ms)")
        self.ax.set_xlabel("Time since start(ms)")
        # for i in self.ax.spines.values():
        #     i.set_color("#cfd5ff")
        self.ax.spines['bottom'].set_color("#cfd5ff")
        self.ax.spines['left'].set_color("#cfd5ff")
        self.ax.spines['top'].set_color("#202020")
        self.ax.spines['right'].set_color("#202020")
        self.graph = tkBEnd.FigureCanvasTkAgg(self.fig, master=self)
        self.ax.plot(df, 'o--b')
        self.graph.draw()


root = UtilityContainer()
root.mainloop()
