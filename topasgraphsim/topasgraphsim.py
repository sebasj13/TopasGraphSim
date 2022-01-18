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

from src.classes.main_viewer import MainApplication


def topasgraphsim():

    root = tk.Tk()
    root.geometry(f"{root.winfo_screenwidth()//2}x{root.winfo_screenheight()//2}+0+0")
    root.title("Simulationsauswertung")
    root.iconbitmap(
        str(os.path.dirname(os.path.realpath(__file__)) + "\\src\\resources\\icon.ico")
    )
    style = ttk.Style(root)
    root.tk.call(
        "source",
        str(
            os.path.dirname(os.path.realpath(__file__))
            + "\\src\\Azure-ttk-theme\\azure.tcl"
        ),
    )
    root.tk.call("set_theme", "light")
    Main = MainApplication(root)
    root.mainloop()


if __name__ == "__main__":
    topasgraphsim()
