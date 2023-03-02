import customtkinter as ctk
from PIL import Image
import os

from ..resources.language import Text
from .tabview_v2 import TabView


class MainViewer(ctk.CTkFrame):
    
    """The main viewer of the TGS application.
    """
    
    def __init__(self, parent):
        
        self.parent = parent
        super().__init__(self.parent, border_color="black", border_width=1)
        text = Text()
        l = self.parent.lang.get()
        
        size = self.parent.winfo_screenwidth()//8
        self.logo = ctk.CTkImage(
            Image.open(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    "..",
                    "resources",
                    "icon.png",
                            )
                     ).resize((size, size), Image.LANCZOS), size=(size, size)
                                )
        
        self.tabview = TabView(self)
        title = self.parent.appname + "\n\nv. " + self.parent.version
        self.logolabel = ctk.CTkLabel(self.tabview, text=title, image = self.logo, font=("Bahnschrift", 30), compound="top")
        self.logolabel.place(relx=0.5, rely=0.5, anchor="center")
        self.tabview.pack(fill="both", expand=True)
        
        self.pack(fill="both", expand=True, padx=5, pady=5)