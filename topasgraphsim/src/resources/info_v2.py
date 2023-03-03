import os
import webbrowser
from PIL import Image
import customtkinter as ctk

class show_info(ctk.CTkToplevel):
    
    """Shows information about the application.
    """
    
    def __init__(self, parent):
        
        self.parent = parent
        super().__init__(self.parent)
        
        self.title("")
        self.geometry(f"180x240+{parent.winfo_rootx()+parent.winfo_width()//2-90}+{parent.winfo_rooty()+parent.winfo_height()//2-120}")
        self.wm_attributes("-toolwindow", True)
        
        im = Image.open(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), "icon.png")
        )
        ph = ctk.CTkImage(im, size=(64,64))
        self.imagelabel = ctk.CTkLabel(self, image=ph, text="TopasGraphSim", compound="top", font=("Bahnschrift", 16))
        self.authorlabel = ctk.CTkLabel(self, text=self.parent.author+"\n\n"+self.parent.affiliation, font=("Bahnschrift", 12))
        self.versionlabel = ctk.CTkLabel(self, text=f"v. {self.parent.version}", font=("Bahnschrift", 12))
        ghimage_light = Image.open(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), f"gh_light.png")
        )
        ghimage_dark = Image.open(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), f"gh_dark.png")
        )
        self.ghimage = ctk.CTkImage(ghimage_light, ghimage_dark, size=(32,32))
        self.button = ctk.CTkButton(self, image=self.ghimage, command=self.open_github, text="", width=64)
        self.imagelabel.pack(side="top")
        self.versionlabel.pack()
        self.button.pack()
        self.authorlabel.pack(pady=(10,0))
        
        self.bind("<Configure>", self.move)

        
    def open_github(self):
            webbrowser.open("https://github.com/sebasj13/topasgraphsim")    
            
    def move(self, event):
        self.lift()
        self.geometry(self.geometry(f"180x240+{self.parent.winfo_rootx()+self.parent.winfo_width()//2-90}+{self.parent.winfo_rooty()+self.parent.winfo_height()//2-120}"))
        