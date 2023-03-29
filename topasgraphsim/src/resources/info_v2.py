import os
import sys
import webbrowser
from PIL import Image
import customtkinter as ctk

from ..classes.profile import ProfileHandler

class show_info(ctk.CTkToplevel):
    
    """Shows information about the application.
    """
    
    def __init__(self, parent):
        
        self.parent = parent        
        super().__init__(self.parent)
        
        self.title("")
        self.overrideredirect(True)
        
        def resource_path(relative_path):
            """ Get absolute path to resource, works for dev and for PyInstaller """
            if hasattr(sys, '_MEIPASS'):
                return os.path.join(sys._MEIPASS, "TopasGraphSim", relative_path)

            return os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir, os.pardir, relative_path) 
        self.columnconfigure(0, weight=1)
        self.closebutton = ctk.CTkButton(self, text=" X ", command=self.close, width=2, height=1, font=("Bahnschrift", 12))
        self.closebutton.grid(row=0, column=0, sticky="ne", padx=(0, 4), pady=(4, 4))
        im = Image.open(resource_path(os.path.join("topasgraphsim", "src", "resources", "images", "icon.png")))
        ph = ctk.CTkImage(im, size=(64,64))
        self.imagelabel = ctk.CTkLabel(self, image=ph, text="TopasGraphSim", compound="top", font=("Bahnschrift", 16))
        self.authorlabel = ctk.CTkLabel(self, text=self.parent.author+"\n\n"+self.parent.affiliation, font=("Bahnschrift", 12))
        self.versionlabel = ctk.CTkLabel(self, text=f"v. {self.parent.version}", font=("Bahnschrift", 12))
        icon = {True: "✅", False: "❌"}
        self.dndlabel = ctk.CTkLabel(
            self,
            text=f"Drag and Drop: {icon[ProfileHandler().get_attribute('draganddrop')]}",
            font=("Bahnschrift", 12)
        )
        ghimage_light = Image.open(resource_path(os.path.join("topasgraphsim", "src", "resources", "images", "gh_light.png")))
        ghimage_dark = Image.open(resource_path(os.path.join("topasgraphsim", "src", "resources", "images", "gh_dark.png")))
        self.ghimage = ctk.CTkImage(ghimage_light, ghimage_dark, size=(32,32))
        self.button = ctk.CTkButton(self, image=self.ghimage, command=self.open_github, text="", width=64)
        self.imagelabel.grid(row=1, column=0, sticky="nsew", pady=(8,0))
        self.versionlabel.grid(row=2, column=0, sticky="nsew", pady=(0,8))
        self.dndlabel.grid(row=3, column=0, sticky="nsew", pady=(0,8))
        self.button.grid(row=4, column=0, sticky="ns", pady=(0,8))
        self.authorlabel.grid(row=5, column=0, sticky="nsew", pady=(0,8))
        
        self.bind("<Configure>", self.move)

        
    def open_github(self):
            webbrowser.open("https://github.com/sebasj13/topasgraphsim")    
            
    def move(self, event):
        self.lift()
        self.geometry(self.geometry(f"180x320+{self.parent.winfo_rootx()+self.parent.winfo_width()//2-90}+{self.parent.winfo_rooty()+self.parent.winfo_height()//2-160}"))
        
    def close(self):
        self.destroy()
        