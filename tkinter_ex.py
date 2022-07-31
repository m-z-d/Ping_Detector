import tkinter as tk
import matplotlib.pyplot as mplt
import subprocess as sp
import pandas as pd
from PIL import Image as img
from PIL import ImageTk as tkimg


root=tk.Tk()
root.wm_title("Pinging...")
root.resizable(width=False, height=False)

WelcomeLabel=tk.Label(
    root,text="Welcome!",font=("Arial","25"),width=20,
    background="#afafaf",fg="#ffffff",cursor="tcross"
    )
AboutButton=tk.Button(
    root,text="About...",font=("Arial","10"),width=21,
    command=lambda :sp.run(['notepad',r'Ping_detector/README.md'],shell=True,timeout=0.1)
    )
OptionsImage=tkimg.PhotoImage(img.open(r"Ping_detector/settings.png"))
OptionsButton=tk.Button(
    root,image=OptionsImage,height=20,width=22,
    command=lambda :sp.run(['notepad',r'Ping_detector/OPTIONS.json'],shell=True,timeout=0.1)
)
PingButton=tk.Button(
    root,text="Ping",font=("Arial","10"),width=21)

WelcomeLabel.grid(row=0,column=0,columnspan=5,sticky="W")
AboutButton.grid(row=1,column=0,columnspan=2,sticky="W")
OptionsButton.grid(row=1,column=2,columnspan=1,sticky="W")
PingButton.grid(row=1,column=4,columnspan=2,sticky="W")

root.mainloop()
