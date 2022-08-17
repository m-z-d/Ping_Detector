import subprocess,sys, matplotlib, numpy,tkinter
import matplotlib.pyplot as plt
website_to_ping="google.com"
process=subprocess.Popen(["ping",website_to_ping,"-t"],stdout=subprocess.PIPE,universal_newlines=True)
  #open a pipe from the ping command to the application
root=tkinter.Tk()
ping_counter=-3
with open(r"example2.csv",'a') as f:
  print(f"\"Ping response times from {website_to_ping}\"",file=f)
def ping_display():
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
    root.title(ping_ms+"►"+website_to_ping)
    
root.after(100,ping_display)
root.mainloop()