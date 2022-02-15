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

from .src.classes.install_dnd import InstallDnD
from .src.classes.main_viewer import MainApplication
from .src.classes.profile import ProfileHandler
from .src.classes.update import CheckForUpdates


def topasgraphsim():

    if ProfileHandler().get_attribute("draganddrop") == True:

        try:
            import TkinterDnD2 as dnd
        except ImportError:

            drag = InstallDnD()
            print(drag.message)

            if drag.install_success == True:
                python = sys.executable
                args = "-m topasgraphsim"
                os.execl(python, python, args)
                return

        if "TkinterDnD2" in sys.modules.keys():
            try:
                root = dnd.TkinterDnD.Tk()
            except RuntimeError:
                ProfileHandler().set_attribute("draganddrop", False)
                python = sys.executable
                args = args = "-m topasgraphsim"
                os.execl(python, python, args)
                return
        else:
            ProfileHandler().set_attribute("draganddrop", False)
            python = sys.executable
            os.execl(python, python, *sys.argv)
            return
    else:
        root = tk.Tk()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    width = screen_width // 2
    height = screen_height // 2
    x = screen_width // 2 - width // 2
    y = screen_height // 2 - height // 2
    root.minsize(width, height - 100)
    root.geometry(f"{width}x{height}+{x-25}+{y}")
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

    app = MainApplication(root)

    try:

        def drop_enter(event):
            event.widget.focus_force()
            return event.action

        def drop_position(event):
            return event.action

        def drop_leave(event):
            return event.action

        def drop(event):
            if event.data:
                app.load_dropped_file(event.data)
            return event.action

        root.drop_target_register(dnd.DND_FILES)
        root.dnd_bind("<<DropEnter>>", drop_enter)
        root.dnd_bind("<<DropPosition>>", drop_position)
        root.dnd_bind("<<DropLeave>>", drop_leave)
        root.dnd_bind("<<Drop>>", drop)
    except Exception:
        pass

    CheckForUpdates()

    root.mainloop()


if __name__ == "__main__":
    topasgraphsim()
