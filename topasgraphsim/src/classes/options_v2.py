import customtkinter as ctk


class Options(ctk.CTkFrame):
    
    """The options frame of the TGS application.
    """
    
    def __init__(self, parent):
        
        self.parent = parent        
        super().__init__(self.parent, border_color="black", border_width=1)
        