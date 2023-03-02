import customtkinter as ctk

from .tabview_v2 import TabView


class MainViewer(ctk.CTkFrame):
    
    """The main viewer of the TGS application.
    """
    
    def __init__(self, parent):
        
        self.parent = parent
        super().__init__(self.parent, border_color="black", border_width=1)
        self.tabview = TabView(self)
        self.tabview.pack(fill="both", expand=True)
        self.pack(fill="both", expand=True, padx=5, pady=5)