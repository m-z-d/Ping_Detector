import tkinter as tk
from tkinter import messagebox as tkmb
import matplotlib.pyplot as mplt
import subprocess as sp
import pandas as pd
from PIL import Image as img
from PIL import ImageTk as tkimg

DEBUG=True

def silence_exception(func,exception):
    try:func()
    except exception:pass
def ping_button_function(website_to_ping="google.com"):
    global process
    process=sp.Popen(["ping",website_to_ping,"-t"],stdout=sp.PIPE,universal_newlines=True)
    root.after(200,ping_display('google.com'))
ping_counter=-3
def ping_display(website):
    root.after(100,ping_display)
    global process
    global ping_counter
    ping_stat=process.stdout.readline()
    ping_counter+=1
    if ping_counter<0: return
    ping_ms=ping_stat.split('time=')[-1].split()[0]
    ping_int=int(ping_ms[:-2])
    with open(r"example2.csv",'a') as f:
        print(f'"{ping_int}"',file=f)
    if DEBUG:print('ping: '+ping_ms+f"({ping_int})")
    root.title(ping_ms+"►"+website)
root=tk.Tk()
root.title("Pinging...")
root.resizable(width=False, height=False)
root.wm_attributes("-transparentcolor", 'grey')

WelcomeLabel=tk.Label(
    root,text="Welcome!",font=("Arial","25"),width=20,
    bg='#202020',fg="#cfd5ff",cursor="tcross"
    )
VersionLabel=tk.Label(
    root,text="to Ping Detector vα0.01",font=("Arial","15"),
    bg='#202020',fg="#cfd5ff"
    )

AboutButton=tk.Button(
    root,text="About...",font=("Arial","10"),width=21,bg='#202020',fg="#cfd5ff",
    command=lambda : silence_exception(lambda :sp.run(['notepad',r'Ping_detector/README.md'],
    shell=True,timeout=0.1),sp.TimeoutExpired) #opens essential info for the user in a separate program
    ) #stdout uncluttered by ignoring timeout exception
OptionsImage=tkimg.PhotoImage(img.open(r"settings.png"))
OptionsButton=tk.Button(
    root,image=OptionsImage,height=21,width=24,bg='#202020',fg="#cfd5ff",
    command=lambda: silence_exception(lambda :sp.run(['notepad',r'Ping_detector/OPTIONS.json'],
    shell=True,timeout=0.1,stderr=None),sp.TimeoutExpired)
)
PingButton=tk.Button(
    root,text="Ping",font=("Arial","10"),width=21,bg='#202020',fg="#cfd5ff",
    command=lambda:tkmb.showwarning("Ping?",f"you are pinging \"{AdressEntry.get()}\"",)
    )
AdressEntry=tk.Entry(root,relief='sunken',
    font=("Arial","15"),width=25
)


WelcomeLabel.grid(row=0,column=0,columnspan=5)
VersionLabel.grid(row=1,column=0,columnspan=5)
AboutButton.grid(row=2,column=0,columnspan=2)
OptionsButton.grid(row=2,column=2,columnspan=1)
PingButton.grid(row=2,column=4,columnspan=2)
AdressEntry.grid(row=3,column=0,columnspan=5)

root.mainloop()
