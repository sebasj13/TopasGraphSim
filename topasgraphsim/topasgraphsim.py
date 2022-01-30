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
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    width = screen_width // 2
    height = screen_height // 2
    x = screen_width // 2 - width // 2
    y = screen_height // 2 - height // 2
    root.minsize(width + 50, height)
    root.geometry("%dx%d+%d+%d" % (width + 50, height, x - 25, y))
    style = ttk.Style(root)
    root.tk.call(
        "source",
        str(
            os.path.dirname(os.path.realpath(__file__))
            + "\\src\\Azure-ttk-theme\\azure.tcl"
        ),
    )
    app = MainApplication(root, root.winfo_geometry())
    root.after(
        50,
        root.iconbitmap(
            str(
                os.path.dirname(os.path.realpath(__file__))
                + "\\src\\resources\\icon.ico"
            )
        ),
    )
    root.mainloop()


if __name__ == "__main__":
    topasgraphsim()
