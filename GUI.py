# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 12:47:50 2021

@author: Sebastian Schäfer
@institution: Martin-Luther-Universität Halle-Wittenberg
@email: sebastian.schaefer@student.uni-halle.de
"""

import os
import tkinter as tk
import tkinter.ttk as ttk

from main.classes.main_viewer import MainApplication

root = tk.Tk()
root.geometry("960x540")
root.title("Simulationsauswertung")
style = ttk.Style(root)
root.tk.call("source", str(os.getcwd()) + "\\Azure-ttk-theme\\azure.tcl")
root.tk.call("set_theme", "light")
Main = MainApplication(root)
root.mainloop()
