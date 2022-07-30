import tkinter as tk
import matplotlib.pyplot as mplt
import subprocess as sp
import pandas as pd



root=tk.Tk()
root.wm_title("Pinging...")
root.resizable(width=False, height=False)

WelcomeLabel=tk.Label(root,text="Welcome!",font=("Arial","25"),width=25)
AboutButton=tk.Button(
    root,text="About...",font=("Arial","10"),width=10,
    command=lambda :sp.run(['notepad',r'README.md'],shell=True)
    )
OptionsButton=tk.Button()

WelcomeLabel.grid(row=0,column=0,columnspan=5)
AboutButton.grid(row=1,column=0,columnspan=2,sticky="W")

root.mainloop()
