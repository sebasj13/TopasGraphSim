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
        self.wm_attributes("-toolwindow", True)
        
        def resource_path(relative_path):
            """ Get absolute path to resource, works for dev and for PyInstaller """
            if hasattr(sys, '_MEIPASS'):
                return os.path.join(sys._MEIPASS, relative_path)

            return os.path.join(os.path.abspath("."), relative_path) 
        
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
        self.imagelabel.pack(side="top")
        self.versionlabel.pack()
        self.dndlabel.pack(pady=(0,8))
        self.button.pack()
        self.authorlabel.pack(pady=(10,0))
        
        self.bind("<Configure>", self.move)

        
    def open_github(self):
            webbrowser.open("https://github.com/sebasj13/topasgraphsim")    
            
    def move(self, event):
        self.lift()
        self.geometry(self.geometry(f"180x280+{self.parent.winfo_rootx()+self.parent.winfo_width()//2-90}+{self.parent.winfo_rooty()+self.parent.winfo_height()//2-140}"))
        