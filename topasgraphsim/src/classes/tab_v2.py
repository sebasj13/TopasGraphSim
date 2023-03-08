import customtkinter as ctk
import tkinter.ttk as ttk
import tkinterDnD as tkdnd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends._backend_tk import NavigationToolbar2Tk

from .options_v2 import Options
  
       
class Tab(ctk.CTkFrame):
    
    """A tab of the TGS application.
    """
    
    def __init__(self, parent, name, index, lang):
        
        self.parent = parent
        self.name = name
        self.lang = lang
        
        self.saved = False
        
        super().__init__(self.parent, border_color="black", border_width=1)
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, minsize=200)
        self.rowconfigure(0, weight=1)
        self.figure, self.ax = plt.subplots()
        
        class DnDPlot(ttk.Frame):
            
            def __init__(self, parent):
                
                self.parent = parent
                super().__init__(self.parent)
                
                self.rowconfigure(0, weight=1)
                self.columnconfigure(0, weight=1)
                
                self.canvas = FigureCanvasTkAgg(self.parent.figure, master=self)
                self.navbar = NavigationToolbar2Tk(self.canvas, self, pack_toolbar=False)   
                
                self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
                self.navbar.grid(row=1, column=0, sticky="nsew")
                
                self.register_drop_target("*")
                self.bind("<<Drop>>", self.drop)

            def drop(self, event):
                print(self.parent.name)
                
        self.plot = DnDPlot(self)
        self.canvas = self.plot.canvas
        self.options = Options(self, index, self.lang)
        
        self.plot.grid(row=0, column=0, sticky="nsew")
        self.options.grid(row=0, column=1, sticky="nsew")
        
        self.bind("<Configure>", lambda event: self.config(event))
        
    def config(self, event=None): 
        self.figure.subplots_adjust(left=0.08, right=0.92, top=0.92, bottom=0.08, wspace=0.2, hspace=0.2)
            

        
