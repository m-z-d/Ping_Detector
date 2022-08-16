import sys
from tkinter import messagebox

def hook(exctype, value, traceback):
    messagebox.showerror(str(exctype),message=f"Python exception detected: {exctype} with value {value} \nTraceback:{traceback}")
    # sys.__excepthook__(exctype, value, traceback)


if __name__ !="__main__":
    sys.excepthook=hook