import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.ticker import AutoLocator, AutoMinorLocator
from .options import Options
  
       
class Tab(ctk.CTkFrame):
    
    """A tab of the TGS application.
    """
    
    def __init__(self, parent, name, index, lang):
        
        self.parent = parent
        self.name = name
        self.lang = lang
        
        self.saved = False
        
        self.plots = []
        super().__init__(self.parent, border_color="black", border_width=1)
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, minsize=310)
        self.rowconfigure(0, weight=1)
        self.figure, self.ax = plt.subplots()
        
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.navbar = NavigationToolbar2Tk(self.canvas, self, pack_toolbar=False)  
        self.options = Options(self, index, self.lang)

        
        self.navbar._buttons["Save"].config(command=self.options.save)
        
        self.bind("<Configure>", lambda event: self.config(event))
        self.update()
        
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        self.options.grid(row=0, rowspan=2, column=1, sticky="nsew")
        self.navbar.grid(row=1, column=0, sticky="nsew")
        
    def config(self, event=None): 
        self.figure.subplots_adjust(left=0.09, right=0.92, top=0.92, bottom=0.1, wspace=0.2, hspace=0.2)
        
    def update(self):
        self.ax.clear()
        for plot in self.plots[::-1]:
            plot.plot(self.ax)
        self.options.set_ax_names()
        self.options.toggle_legend_options()
        self.options.toggle_grid_options()
        self.ax.xaxis.set_major_locator(AutoLocator())
        self.ax.xaxis.set_minor_locator(AutoMinorLocator())
        self.ax.yaxis.set_major_locator(AutoLocator())
        self.ax.yaxis.set_minor_locator(AutoMinorLocator())
        self.canvas.draw()
            

        
