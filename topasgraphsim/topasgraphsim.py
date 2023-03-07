#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 12:47:50 2021

@author: Sebastian Schäfer
@institution: Martin-Luther-Universität Halle-Wittenberg
@email: sebastian.schaefer@student.uni-halle.de
"""

import os
import sys
import tkinter as tk
import tkinter.ttk as ttk

from .src.classes.main_viewer import MainApplication
from .src.classes.profile import ProfileHandler
from .src.classes.update import CheckForUpdates


def topasgraphsim():

    try: 
        import tkinterDnD as dnd
        root = dnd.Tk()
    except ImportError:
        root = tk.Tk()
        ProfileHandler().set_attribute("draganddrop", False)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    width = screen_width // 2
    height = screen_height // 2
    root.minsize(width, height - 100)

    try:
        root.geometry(ProfileHandler().get_attribute("geometry"))
    except Exception:
        x = screen_width // 2 - width // 2
        y = screen_height // 2 - height // 2
        root.geometry(f"{width}x{height}+{x-25}+{y}")
    try:
        root.state(ProfileHandler().get_attribute("state"))
    except Exception:
        root.state("normal")

    ttk.Style(root)
    root.tk.call(
        "source",
        str(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "src",
                "Azure-ttk-theme",
                "azure.tcl",
            )
        ),
    )
    root.after(
        50,
        root.iconphoto(
            True,
            tk.PhotoImage(
                file=os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    "src",
                    "resources",
                    "icon.png",
                ),
                master=root,
            ),
        ),
    )
    
    app = MainApplication(root, file=sys.argv[1] if len(sys.argv) > 1 else None)
    
    if ProfileHandler().get_attribute("draganddrop"):
        def drop(event):
            if event.data:
                app.load_dropped_file(event.data)
            return event.action
        
        def drag_command(event):
            return (dnd.COPY, "DND_Text", "")
        
        app.register_drop_target("*")
        app.bind("<<Drop>>", drop)
        app.register_drag_source("*")
        app.bind("<<DragInitCmd>>", drag_command)
    
    CheckForUpdates()

    root.mainloop()


if __name__ == "__main__":
    topasgraphsim()
