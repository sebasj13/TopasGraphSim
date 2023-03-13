import customtkinter as ctk
from .profile import ProfileHandler
from ..resources.language import Text
 
       
class Settings(ctk.CTkFrame):
    
    """A tab of the TGS application.
    """
    
    def __init__(self, parent, name, index, lang):
        self.parent = parent
        self.lang = lang
        self.index = index
        self.name = name
        self.saved = False
        super().__init__(self.parent, border_color="black", border_width=1)
        
        self.grid_propagate(False)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        
        self.settingslabel = ctk.CTkLabel(self, text=Text().settings[self.lang], font=("Bahnschrift", 32))
        self.generalframe = ctk.CTkFrame(self, border_color="black", border_width=1)
        self.generalframe.grid_propagate(False)
        self.plotframe = ctk.CTkFrame(self, border_color="black", border_width=1)
        self.plotframe.grid_propagate(False)
        self.gammaframe = ctk.CTkFrame(self, border_color="black", border_width=1)
        self.gammaframe.grid_propagate(False)
        self.savebutton = ctk.CTkButton(self, text=Text().savesettings[self.lang], fg_color="green", command=self.save, font = ("Bahnschrift", 16, "bold"))
        self.closetabbutton = ctk.CTkButton(self, text=Text().closetab1[self.lang], command=self.close, font = ("Bahnschrift", 16, "bold"))
        self.revertbutton = ctk.CTkButton(self, text=Text().reset[self.lang], fg_color="red", command=self.reset, font = ("Bahnschrift", 16, "bold"))
        
        self.settingslabel.grid(row=0, columnspan=3, padx=5, pady=5, sticky="nsew")
        self.generalframe.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.plotframe.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        self.gammaframe.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")
        self.closetabbutton.grid(row=2, column=2, padx=5, pady=5, sticky="nsew")
        self.revertbutton.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
        self.savebutton.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
        
        #############################
        
        self.generallabel = ctk.CTkLabel(self.generalframe, text=Text().generalsettings[self.lang], font=("Bahnschrift", 24))
        self.generallabel.grid(pady=5, sticky="nsew", padx=5)
        
        ############################
        
        self.plotlabel = ctk.CTkLabel(self.plotframe, text=Text().plotsettings[self.lang], font=("Bahnschrift", 24))
        self.plotlabel.grid(pady=(5, 0), sticky="nsew", padx=5)
        
        ############################
        
        self.gammalabel = ctk.CTkLabel(self.gammaframe, text=Text().gammasettings[self.lang], font=("Bahnschrift", 24))
        self.gammalabel.grid(pady = (5, 0), sticky="nsew", padx=5)
        
        ############################
        
    def save(self):
        self.saved = True

    def reset(self):
        pass
    
    def close(self):
        self.parent.master.remove_tab(self.index)
        