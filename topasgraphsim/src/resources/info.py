import os
import tkinter as tk
import tkinter.ttk as ttk
import webbrowser

from PIL import Image, ImageTk

from ..classes.profile import ProfileHandler


class show_info:
    def __init__(self, parent, lang, mode):

        author = {
            "de": "TopasGraphSim\n\nAutor: Sebastian Schäfer",
            "en": "TopasGraphSim\n\nAuthor: Sebastian Schäfer",
        }
        version = {"de": "Version: 17.2.9\n ", "en": "Version: 17.2.9\n "}

        if mode == True:
            pic = "light"
        else:
            pic = "dark"

        window = tk.Toplevel()
        window.title("")
        window.resizable(False, False)
        window.geometry(f"180x240+{parent.winfo_rootx()}+{parent.winfo_rooty()}")
        window.wm_attributes("-toolwindow", True)
        im = Image.open(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), "icon.png")
        ).resize((64, 64))
        ph = ImageTk.PhotoImage(im)
        imagelabel = tk.Label(window, image=ph,)
        imagelabel.image = ph
        authorlabel = tk.Label(window, text=author[lang])
        versionlabel = tk.Label(window, text=version[lang])
        icon = {True: "✅", False: "❌"}
        DnDlabel = tk.Label(
            window,
            text=f"Drag and Drop: {icon[ProfileHandler().get_attribute('draganddrop')]}",
        )
        ghimage = Image.open(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), f"gh_{pic}.png")
        )
        self.ghimage = ImageTk.PhotoImage(ghimage)
        button = ttk.Button(window, image=self.ghimage, command=self.open_github)
        imagelabel.pack()
        authorlabel.pack()
        DnDlabel.pack()
        versionlabel.pack()
        button.pack()

    def open_github(self):
        webbrowser.open("https://github.com/sebasj13/topasgraphsim")
