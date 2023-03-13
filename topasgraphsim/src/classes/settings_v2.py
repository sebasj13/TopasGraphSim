import customtkinter as ctk
from .profile import ProfileHandler
 
       
class Settings(ctk.CTkFrame):
    
    """A tab of the TGS application.
    """
    
    def __init__(self, parent, name, lang):
        self.parent = parent
        self.lang = lang
        self.name = name
        self.saved = False
        super().__init__(self.parent, border_color="black", border_width=1)