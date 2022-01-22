# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 12:47:50 2021

@author: Sebastian Schäfer
@institution: Martin-Luther-Universität Halle-Wittenberg
@email: sebastian.schaefer@student.uni-halle.de
"""

import os
import tkinter as tk

from src.classes.main_viewer import MainApplication


def topasgraphsim():

    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    width = screen_width / 2
    height = screen_height / 2
    x = screen_width / 2 - width / 2
    y = screen_height / 2 - height / 2
    root.geometry("%dx%d+%d+%d" % (width, height, x, y))
    root.iconbitmap(
        str(os.path.dirname(os.path.realpath(__file__)) + "\\src\\resources\\icon.ico")
    )
    MainApplication(root, root.winfo_geometry())
    root.mainloop()


if __name__ == "__main__":
    topasgraphsim()
