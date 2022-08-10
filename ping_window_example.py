import matplotlib as mpl
import matplotlib.backends.backend_tkagg as tkBEnd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tkinter as tk

class App(tk.Tk):
    def __init__(self, screenName: str | None = ..., baseName: str | None = ..., className: str = ..., useTk: bool = ..., sync: bool = ..., use: str | None = ...) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)