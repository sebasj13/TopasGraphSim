import customtkinter as ctk
import numpy as np
import tkinter.filedialog as fd
from tkinter import colorchooser
from PIL import Image, ImageTk
import io
import os
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
import logging
from pymedphys import gamma
from scipy.interpolate import Akima1DInterpolator
from .xrange_slider import Slider

logging.getLogger("matplotlib").setLevel(level=logging.CRITICAL)

from ..resources.language import Text
from ..functions import dp, pdd
from .scrollframe import ScrollFrame
from .tgs_graph import TGS_Plot
from .sim_import import Simulation
from .ptw_import import PTWMultimporter
from .raystation_import import RayStationMultiImporter
from .radcalc_import import RadCalc
from .eclipse_import import Eclipse
from .meas_import import TXTImporter
from .profile import ProfileHandler
from .paramframe import Parameters

class Options(ctk.CTkTabview):
    
    """The options frame of the TGS application.
    """
    
    def __init__(self, parent, index, lang):

        self.parent = parent      
        self.index = index
        self.lang = lang
        self.parent.saved = True
        self.p = ProfileHandler()
        super().__init__(self.parent, width=200, border_color="black", border_width=1)
        
        self.newtabname = ""
        
        self.plotbuttons = []
        self.filenames = []
        
        self.add(Text().data[self.lang])
        self.add(Text().settings1[self.lang])
        self.add(Text().analysis[self.lang])
        self.add(Text().parameters[self.lang])

        self.tab(Text().data[self.lang]).rowconfigure(0, weight=1, minsize=220)
        self.tab(Text().data[self.lang]).rowconfigure(1, weight=1)  
        self.tab(Text().data[self.lang]).columnconfigure(0, weight=1)     
        self.tab(Text().data[self.lang]).grid_propagate(False)
               
        self.dataframe1 = ctk.CTkFrame(self.tab(Text().data[self.lang]))
        self.dataframe2 = ctk.CTkFrame(self.tab(Text().data[self.lang]), border_color="black", border_width=1)
        self.dataframe1.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.dataframe1.grid_propagate(False)
        self.dataframe1.columnconfigure(0, weight=1)
        self.dataframe1.columnconfigure(1, weight=1)
        self.dataframe1.columnconfigure(2, weight=1)
        self.dataframe1.rowconfigure(0, weight=1)
        self.dataframe1.rowconfigure(1, minsize=30)
        self.dataframe2.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.dataframe2.grid_propagate(False)
        self.dataframe2.pack_propagate(False)
        self.dataframe2.columnconfigure(0, weight=1, minsize=144)
        self.dataframe2.columnconfigure(1, weight=1)

        self.graphlist = ScrollFrame(self.dataframe1)
        
        def resource_path(relative_path):
            """ Get absolute path to resource, works for dev and for PyInstaller """
            if hasattr(sys, '_MEIPASS'):
                return os.path.join(sys._MEIPASS, "TopasGraphSim", relative_path)

            return os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir, os.pardir,  relative_path) 
        
        path = resource_path(os.path.join("topasgraphsim", "src", "resources", "images"))
        self.uparrowimage = ctk.CTkImage(Image.open(os.path.join(path,"uparrow.png")), size=(20,20))
        self.downarrowimage = ctk.CTkImage(Image.open(os.path.join(path,"downarrow.png")), size=(20,20))
        self.uparrow = ctk.CTkButton(self.dataframe1, text="",image=self.uparrowimage, width=20, command = lambda: self.change_order("up"))
        self.downarrow = ctk.CTkButton(self.dataframe1, text="",image=self.downarrowimage, width=20, command = lambda: self.change_order("down"))
        self.closeimage = ctk.CTkImage(Image.open(os.path.join(path,"close.png")), size=(20,20))
        self.closebutton = ctk.CTkButton(self.dataframe1, text="", image = self.closeimage, width=20, fg_color="red", command = self.remove_plot)
        self.graphlist.grid(column=0, columnspan=3, row=0, sticky="nsew", padx=5, pady=5)
        self.uparrow.grid(column=0, row=1, padx=(0,5), pady=5)
        self.downarrow.grid(column=1, row=1, padx=(0,5), pady=5)
        self.closebutton.grid(column=2, row=1, padx=(0,5), pady=5)

    
        self.load_topas_button = ctk.CTkButton(self.dataframe2, text = Text().loadsim[self.lang], command = self.load_topas, width=20)
        self.load_topas_button.grid(row=0, column=0, sticky="nsew", pady=(5,2), padx=5)
        
        self.load_mcc_button = ctk.CTkButton(self.dataframe2, text = Text().loadmeasurement[self.lang], command = self.load_measurement, width=20)
        self.load_mcc_button.grid(row=0, column=1, sticky="nsew", padx=5, pady=(5,2))
        
        self.load_raystation_button = ctk.CTkButton(self.dataframe2, text = Text().loadraystation[self.lang], command = self.load_raystation, width=20)
        self.load_raystation_button.grid(row=1, column=0, sticky="nsew", padx=5, pady=(5,2))
        
        self.load_radcalc_button = ctk.CTkButton(self.dataframe2, text = Text().loadradcalc[self.lang], command = self.load_radcalc, width=20)
        self.load_radcalc_button.grid(row=1, column=1, sticky="nsew", padx=5, pady=(5,2))
        
        self.showgrid = ctk.BooleanVar(value=self.p.get_attribute("grid"))

        self.gridoptions = ctk.StringVar(value=Text().gridoptions1[self.lang])
        self.showgrid_button = ctk.CTkCheckBox(self.dataframe2, text=Text().showgrid[self.lang], variable=self.showgrid, onvalue=True, offvalue=False, command = self.toggle_grid_options, font=("Bahnschrift",12, "bold"))
        self.showgrid_options = ctk.CTkOptionMenu(self.dataframe2, variable=self.gridoptions, values=[Text().gridoptions1[self.lang], Text().gridoptions2[self.lang]], command = self.toggle_grid_options)    
        self.showgrid_button.grid(column=0, row=4, padx=5, pady=2, sticky = "w")
        self.showgrid_options.grid(column=1, row=4, padx=5, pady=2, sticky = "w")   
        
        self.showlegend = ctk.BooleanVar(value = self.p.get_attribute("legend"))
        self.legendoptions = ctk.StringVar(value=Text().legendoptions1[self.lang]) 
        
        self.showlegend_button = ctk.CTkCheckBox(self.dataframe2, text=Text().showlegend[self.lang], variable=self.showlegend, onvalue=True, offvalue=False, command = self.toggle_legend_options, font=("Bahnschrift", 12, "bold"))
        self.showlegend_options = ctk.CTkOptionMenu(self.dataframe2, 
                                                    variable=self.legendoptions, 
                                                    values=[Text().legendoptions1[self.lang], 
                                                            Text().legendoptions2[self.lang], 
                                                            Text().legendoptions3[self.lang],
                                                            Text().legendoptions4[self.lang],
                                                            Text().legendoptions5[self.lang]],
                                                    command = self.toggle_legend_options)
        
        self.showlegend_button.grid(column=0, row=5, padx=5, pady=2, sticky="w")
        self.showlegend_options.grid(column=1, row=5, padx=5, pady=2, sticky="w")
        
        self.change_name_button = ctk.CTkButton(self.dataframe2, text=Text().edittabname[self.lang], command = self.change_name, width=20)
        self.close_tab_button = ctk.CTkButton(self.dataframe2, text=Text().closetab1[self.lang], command = lambda: self.parent.master.master.remove_tab(self.parent.master.master.tabnames.index(self.parent.name)), width=20, fg_color="red")
        self.close_tab_button.grid(row=6, column=1, sticky="new", pady=(5,2), padx=5)
        self.change_name_button.grid(row=6, column=0, sticky="new", pady=(5,2), padx=5)
        
        
        #######################################################################################################################
               
        self.tab(Text().settings1[self.lang]).rowconfigure(0, weight=1)
        self.tab(Text().settings1[self.lang]).columnconfigure(0, weight=1)     
        self.tab(Text().settings1[self.lang]).grid_propagate(False) 
        self.tab(Text().settings1[self.lang]).pack_propagate(False) 

        self.settings_scrollframe = ScrollFrame(self.tab(Text().settings1[self.lang]))
        self.settings_scrollframe.pack(fill="both", expand=True)
       
        self.graphsettingsframe = ctk.CTkFrame(self.settings_scrollframe.viewPort, border_color="black", border_width=1, fg_color=self.dataframe1.cget("fg_color"))
        self.graphsettingsframe.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        self.settings_scrollframe.configure(border_width=0)
        self.settings_scrollframe.canvas.configure(bg=self.dataframe1.cget("fg_color")[0])
        self.settings_scrollframe.configure(fg_color=self.dataframe1.cget("fg_color"))
        self.settings_scrollframe.viewPort.configure(fg_color=self.dataframe1.cget("fg_color")) 
        
        self.graphsettingsframe.columnconfigure(0, weight=1)
        self.graphsettingsframe.columnconfigure(1, weight=1)
        self.graphsettingsframe.grid_propagate(False)       
        
        self.graphsettingslabel = ctk.CTkLabel(self.graphsettingsframe, text=Text().graphsettings[self.lang], font=("Bahnschrift",16, "bold"))
        self.graphsettingslabel.grid(column=0, row=0, columnspan=2, sticky="nsew", padx=5, pady=(1,5))
        
        self.title = ctk.StringVar(value = self.p.get_attribute("graphtitle"))
        self.parent.ax.set_title(self.title.get())
        self.titleentry = ctk.CTkEntry(self.graphsettingsframe, textvariable=self.title, width=130)
        self.titleentry.bind("<Enter>", lambda x : self.on_enter(self.titleentry, self.rename_title, x))
        self.titleentry.bind("<Leave>", lambda x : self.on_leave(self.titleentry, x))
        self.titlebutton = ctk.CTkButton(self.graphsettingsframe, text=Text().renamet[self.lang], command = self.rename_title)
        self.titleentry.grid(column=0, row=1, padx=5, pady=2)
        self.titlebutton.grid(column=1, row=1, padx=5, pady=2)
        
        self.xtitle = ctk.StringVar(value = self.p.get_attribute("xaxislabel"))
        self.parent.ax.xaxis.set_label_text(self.xtitle.get())
        self.xentry = ctk.CTkEntry(self.graphsettingsframe, textvariable=self.xtitle, width=130)
        self.xentry.bind("<Enter>", lambda x : self.on_enter(self.xentry, self.rename_x, x))
        self.xentry.bind("<Leave>", lambda x : self.on_leave(self.xentry, x))
        self.xbutton = ctk.CTkButton(self.graphsettingsframe, text=Text().renamex[self.lang], command = self.rename_x)
        self.xentry.grid(column=0, row=2, padx=5, pady=2)
        self.xbutton.grid(column=1, row=2, padx=5, pady=2)
        
        self.ytitle = ctk.StringVar(value = self.p.get_attribute("yaxislabel"))
        self.parent.ax.yaxis.set_label_text(self.ytitle.get())
        self.yentry = ctk.CTkEntry(self.graphsettingsframe, textvariable=self.ytitle, width=130)
        self.yentry.bind("<Enter>", lambda x : self.on_enter(self.yentry, self.rename_y, x))
        self.yentry.bind("<Leave>", lambda x : self.on_leave(self.yentry, x))
        self.ybutton = ctk.CTkButton(self.graphsettingsframe, text=Text().renamey[self.lang], command = self.rename_y)
        self.yentry.grid(column=0, row=3, padx=5, pady=2)
        self.ybutton.grid(column=1, row=3, padx=5, pady=2)
        
        self.normalize=ctk.BooleanVar(value=self.p.get_attribute("normalize"))
        normtypedict = {"maximum":Text().maximum[self.lang], "plateau":Text().plateau[self.lang], "centeraxis":Text().centeraxis[self.lang]}
        self.normalization = ctk.StringVar(value=normtypedict[self.p.get_attribute("normtype")])
        self.normalize_button = ctk.CTkCheckBox(self.graphsettingsframe, text=Text().normalize[self.lang], variable=self.normalize, command=self.change_normalization, font=("Bahnschrift", 12, "bold"))
        self.normalize_options = ctk.CTkOptionMenu(self.graphsettingsframe, values=[Text().maximum[self.lang], Text().plateau[self.lang], Text().centeraxis[self.lang]], variable=self.normalization, command=self.change_normalization)
        self.normalize_button.grid(row=4, column=0, sticky="nsew", pady=2, padx=5)
        self.normalize_options.grid(row=4, column=1, sticky="ew", pady=2, padx=5)        
        
        self.spacerframe = ctk.CTkFrame(self.graphsettingsframe, fg_color = self.graphsettingsframe.cget("fg_color"))
        self.spacerframe.grid(row=5, column=0, columnspan=2, padx=2)
        self.spacerframe.columnconfigure(0, weight=2, minsize=115)
        self.spacerframe.columnconfigure(1, weight=1)
        self.spacerframe.columnconfigure(2, weight=2, minsize=90)
        self.spacerframe.rowconfigure(0, weight=1)
        
        self.caxcorrection = ctk.BooleanVar(value=self.p.get_attribute("caxcorrection"))

        self.cax_button = ctk.CTkCheckBox(self.spacerframe, text=Text().caxcorrection[self.lang], variable=self.caxcorrection, onvalue=True, offvalue=False, command = self.toggle_cax_correction, font=("Bahnschrift",12, "bold"))
        self.cax_button.grid(column=0, row=0, padx=2, pady=5, sticky = "nsew")
        
        self.show_points = ctk.BooleanVar(value=self.p.get_attribute("show_points"))
        self.pointsbutton = ctk.CTkCheckBox(self.spacerframe, text=Text().showpoints[self.lang], variable=self.show_points, command=self.change_points, font=("Bahnschrift", 12, "bold"))
        self.pointsbutton.grid(row=0, column=1, sticky="nsew", pady=2, padx=(0,2))
        
        self.show_error = ctk.BooleanVar(value=self.p.get_attribute("show_error"))
        self.errorbutton = ctk.CTkCheckBox(self.spacerframe, text=Text().showerror[self.lang], variable=self.show_error, command=self.change_error, font=("Bahnschrift", 12, "bold"))
        self.errorbutton.grid(row=0, column=2, sticky="nsew", pady=2, padx=(10,2))
        
        self.plotsettingsframe = ctk.CTkFrame(self.settings_scrollframe.viewPort, border_color="black", border_width=1, fg_color=self.graphsettingsframe.cget("fg_color"))
        self.plotsettingsframe.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        self.plotsettingsframe.columnconfigure(0, weight=1, minsize=144)
        self.plotsettingsframe.columnconfigure(1, weight=1)
        self.plotsettingsframe.grid_propagate(False)   
        
        self.plotsettingslabel = ctk.CTkLabel(self.plotsettingsframe, text=Text().plotsettings[self.lang], font=("Bahnschrift",16, "bold"))
        self.plotsettingslabel.grid(column=0, row=0, columnspan=2, sticky="nsew", padx=5, pady=(1,5))
        
        self.current_plot = ctk.StringVar(value="")
        self.plotselectorlabel = ctk.CTkLabel(self.plotsettingsframe, text=Text().plotselector[self.lang],  font=("Bahnschrift",14, "bold"))
        self.plotselectorlabel.grid(column=0, row=1, padx=5, pady=2, sticky="w")
        self.plotselector = ctk.CTkOptionMenu(self.plotsettingsframe, variable=self.current_plot, values=[], command = self.change_current_plot)
        self.plotselector.grid(column=1, row=1, padx=5, pady=2, sticky="nsew")
        
        self.plottitle = ctk.StringVar()
        self.plottitleentry = ctk.CTkEntry(self.plotsettingsframe, textvariable=self.plottitle, width=130)
        self.plottitleentry.bind("<Enter>", lambda x : self.on_enter(self.plottitleentry, self.rename_plot, x))
        self.plottitleentry.bind("<Leave>", lambda x : self.on_leave(self.plottitleentry, x))
        self.plottitlebutton = ctk.CTkButton(self.plotsettingsframe, text=Text().renameplot[self.lang], command = self.rename_plot)
        self.plottitleentry.grid(column=0, row=2, padx=5, pady=(3,1), sticky="nsew")
        self.plottitlebutton.grid(column=1, row=2, padx=5, pady=(3,1))
        
        self.linethicknesslabel = ctk.CTkLabel(self.plotsettingsframe, text=Text().linethickness[self.lang], font=("Bahnschrift",12, "bold"))
        self.linethicknesslabel.grid(column=0, row=3, padx=5, pady=2, sticky="w")
        self.linethickness = ctk.DoubleVar(value=self.p.get_attribute("linethickness"))
        self.linethicknessslider = ctk.CTkSlider(self.plotsettingsframe, from_=0, to=4, orientation="horizontal", number_of_steps=100, width=150, command = self.change_linethickness, variable=self.linethickness)
        self.linethicknessslider.grid(column=1, row=3, padx=5, pady=2, sticky="e")
        
        self.linestylelabel = ctk.CTkLabel(self.plotsettingsframe, text=Text().linestyle[self.lang], font=("Bahnschrift",12, "bold"))
        self.linestylelabel.grid(column=0, row=4, padx=5, pady=2, sticky="w")
        self.linestyledict = {"-.":Text().dashdot[self.lang], "-":Text().dash[self.lang], "dotted":Text().dot[self.lang], " ":Text().none[self.lang]}
        self.linestyle = ctk.StringVar(value=self.linestyledict[self.p.get_attribute("linestyle")])
        self.linestyleselector = ctk.CTkOptionMenu(self.plotsettingsframe, variable=self.linestyle, values=[Text().dashdot[self.lang], Text().dash[self.lang], Text().dot[self.lang], Text().none[self.lang]], command = self.change_linestyle)
        self.linestyleselector.grid(column=1, row=4, padx=5, pady=2, sticky="e")
        
        self.plotcolor = ctk.StringVar()
        self.linecolorlabel = ctk.CTkLabel(self.plotsettingsframe, text=Text().linecolor[self.lang], font=("Bahnschrift",12, "bold"))
        self.linecolorbutton = ctk.CTkButton(self.plotsettingsframe, text=Text().change[self.lang], command = self.choose_linecolor)
        self.linecolorlabel.grid(column=0, row=5, padx=5, pady=2, sticky="w")
        self.linecolorbutton.grid(column=1, row=5, padx=5, pady=2, sticky="e")

        self.figuresettingsframe = ctk.CTkFrame(self.settings_scrollframe.viewPort, border_color="black", border_width=1, fg_color=self.graphsettingsframe.cget("fg_color"), height=172)
        self.figuresettingsframe.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        self.figuresettingsframe.columnconfigure(0, weight=1, minsize=144)
        self.figuresettingsframe.columnconfigure(1, weight=1)
        self.figuresettingsframe.grid_propagate(False)   
        self.figuresettingslabel = ctk.CTkLabel(self.figuresettingsframe, text=Text().figuresettings[self.lang], font=("Bahnschrift",16, "bold"))
        self.figuresettingslabel.grid(column=0, row=0, columnspan=2, sticky="nsew", padx=5, pady=(1,5))

        self.dpilabel = ctk.CTkLabel(self.figuresettingsframe, text="DPI", font=("Bahnschrift",12, "bold"))
        self.dpilabel.grid(column=0, row=1, padx=5, pady=2, sticky="w")
        self.dpi = ctk.StringVar(value="600")
        self.dpiselector = ctk.CTkOptionMenu(self.figuresettingsframe, variable=self.dpi, values=["150", "300", "600"],)
        self.dpiselector.grid(column=1, row=1, padx=5, pady=2, sticky="e")

        self.figuresize_x = ctk.StringVar(value="5.5")
        self.figuresize_xentry = ctk.CTkEntry(self.figuresettingsframe, textvariable=self.figuresize_x, width=130)
        self.figuresize_xlabel = ctk.CTkLabel(self.figuresettingsframe, text=Text().figuresize_x[self.lang], font=("Bahnschrift",14, "bold"))
        self.figuresize_xentry.grid(column=1, row=2, padx=5, pady=(3,1), sticky="nsew")
        self.figuresize_xlabel.grid(column=0, row=2, padx=5, pady=(3,1), sticky="w")

        self.figuresize_y = ctk.StringVar(value="5.5")
        self.figuresize_yentry = ctk.CTkEntry(self.figuresettingsframe, textvariable=self.figuresize_y, width=130)
        self.figuresize_ylabel = ctk.CTkLabel(self.figuresettingsframe, text=Text().figuresize_y[self.lang],font=("Bahnschrift",14, "bold"))
        self.figuresize_yentry.grid(column=1, row=3, padx=5, pady=(3,1), sticky="nsew")
        self.figuresize_ylabel.grid(column=0, row=3, padx=5, pady=(3,1), sticky="w")

        self.preview_button =  ctk.CTkButton(self.figuresettingsframe, text=Text().preview[self.lang], command = self.preview, width=20)
        self.preview_button.grid(row=4, column=0, columnspan=2, sticky="s", padx=5, pady=5)
        
    ######################################################################################################################################################################
   
        self.tab(Text().parameters[self.lang]).columnconfigure(0, weight=1)
        self.tab(Text().parameters[self.lang]).rowconfigure(0, weight=1)
        self.tab(Text().parameters[self.lang]).grid_propagate(False)  
        self.tab(Text().parameters[self.lang]).configure(fg_color=self.dataframe1.cget("fg_color"))
        self.parameterframe = ctk.CTkFrame(self.tab(Text().parameters[self.lang]), border_color="black", border_width=1)
        self.parameterframe.grid(sticky="nsew", padx=5, pady=5)
        self.parameterframe.pack_propagate(False)
        self.paramslist = ScrollFrame(self.parameterframe)
        self.parameters = []
        self.paramslist.pack(fill="both", expand=True)

    ######################################################################################################################################################################

        self.tab(Text().analysis[self.lang]).configure(fg_color=self.dataframe1.cget("fg_color"))
        self.tab(Text().analysis[self.lang]).pack_propagate(False)
        self.analysis_scrollframe = ScrollFrame(self.tab(Text().analysis[self.lang]))
        self.analysis_scrollframe.configure(border_width=0)
        self.analysis_scrollframe.canvas.configure(bg=self.dataframe1.cget("fg_color")[0])
        self.analysis_scrollframe.configure(fg_color=self.dataframe1.cget("fg_color"))
        self.analysis_scrollframe.viewPort.configure(fg_color=self.dataframe1.cget("fg_color")) 
        self.analysis_scrollframe.pack(fill="both", expand=True)

        self.shiftframe = ctk.CTkFrame(self.analysis_scrollframe.viewPort, border_color="black", border_width=1)
        self.shiftframe.columnconfigure(0, weight=1, minsize=144)
        self.shiftframe.columnconfigure(1, weight=1)
        self.shiftframe.configure(fg_color=self.dataframe1.cget("fg_color"))
        
        self.shiftframetitle = ctk.CTkLabel(self.shiftframe, text=Text().shift[self.lang], font=("Bahnschrift",16, "bold"))
        self.shiftframetitle.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=(1,5))
        
        self.plotselectorlabel2 = ctk.CTkLabel(self.shiftframe, text=Text().plotselector[self.lang], font=("Bahnschrift",14, "bold"))
        self.plotselectorlabel2.grid(column=0, row=1, padx=5, pady=2, sticky="w")
        self.plotselector2 = ctk.CTkOptionMenu(self.shiftframe, variable=self.current_plot, values=[], command = self.change_current_plot)
        self.plotselector2.grid(column=1, row=1, padx=5, pady=2, sticky="nsew")

        self.spacerframe1 = ctk.CTkFrame(self.shiftframe, fg_color = self.shiftframe.cget("fg_color"))
        self.spacerframe1.grid(column=0, row=2, columnspan=2, sticky="nsew", padx=2)
        self.spacerframe1.rowconfigure(0, weight=1)
        self.spacerframe1.rowconfigure(1, weight=1)
        self.spacerframe1.columnconfigure(0, weight=1)
        self.spacerframe1.columnconfigure(1, weight=1)
        self.spacerframe1.columnconfigure(2, weight=1)

        self.doseshift = ctk.StringVar(value = self.p.get_attribute("doseoffset"))
        self.axshift = ctk.StringVar(value = self.p.get_attribute("axshift"))
        self.dosescale = ctk.StringVar(value = self.p.get_attribute("dosefactor"))
        self.flip = ctk.BooleanVar(value=self.p.get_attribute("flip"))
        
        self.dosescalelabel = ctk.CTkLabel(self.spacerframe1, text=Text().dosescale[self.lang], font=("Bahnschrift",12, "bold"))
        self.dosescaleentry = ctk.CTkEntry(self.spacerframe1, textvariable=self.dosescale, width=130)
        self.dosescaleentry.bind("<Enter>", lambda x : self.on_enter(self.dosescaleentry, self.apply, x))
        self.dosescaleentry.bind("<Leave>", lambda x : self.on_leave(self.dosescaleentry, x))
        
        self.doseshiftlabel = ctk.CTkLabel(self.spacerframe1, text=Text().doseshift[self.lang], font=("Bahnschrift",12, "bold"))
        self.axshiftlabel = ctk.CTkLabel(self.spacerframe1, text=Text().axshift[self.lang], font=("Bahnschrift",12, "bold"))
        self.doseshiftentry = ctk.CTkEntry(self.spacerframe1, textvariable=self.doseshift, width=130)
        self.doseshiftentry.bind("<Enter>", lambda x : self.on_enter(self.doseshiftentry, self.apply, x))
        self.doseshiftentry.bind("<Leave>", lambda x : self.on_leave(self.doseshiftentry, x))        
        self.axshiftentry = ctk.CTkEntry(self.spacerframe1, textvariable=self.axshift, width=130)
        self.axshiftentry.bind("<Enter>", lambda x : self.on_enter(self.axshiftentry, self.apply, x))
        self.axshiftentry.bind("<Leave>", lambda x : self.on_leave(self.axshiftentry, x))
        self.flipbutton = ctk.CTkCheckBox(self.shiftframe, variable=self.flip, text=Text().flip[self.lang], font=("Bahnschrift",12, "bold"))
        self.applybutton = ctk.CTkButton(self.shiftframe, text=Text().apply[self.lang], command = self.apply, fg_color="green")
        
        self.dosescalelabel.grid(column=0, row=0, padx=2, pady=2, sticky="n")
        self.dosescaleentry.grid(column=0, row=1, padx=2, pady=2, sticky="nsew")
        self.doseshiftlabel.grid(column=1, row=0, padx=2, pady=2, sticky="n")
        self.doseshiftentry.grid(column=1, row=1, padx=2, pady=2, sticky="nsew")
        self.axshiftlabel.grid(column=2, row=0, padx=2, pady=2, sticky="n")
        self.axshiftentry.grid(column=2, row=1, padx=2, pady=2, sticky="nsew")
        self.flipbutton.grid(column=0, row=3, padx=2, pady=2, sticky="ns")
        self.applybutton.grid(column=1, row=3, padx=5, pady=2, sticky="nsew")

        self.shiftframe.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        self.gammaframe = ctk.CTkFrame(self.analysis_scrollframe.viewPort, border_color="black", border_width=1)
        self.gammaframe.columnconfigure(0, weight=2, minsize=114)
        self.gammaframe.columnconfigure(1, weight=1)
        self.gammaframe.columnconfigure(2, weight=1)
        self.gammaframe.columnconfigure(3, weight=1)
        self.gammaframe.columnconfigure(4, weight=1)
        self.gammaframe.configure(fg_color=self.dataframe1.cget("fg_color"))
        
        self.gammaframetitle = ctk.CTkLabel(self.gammaframe, text=Text().gamma[self.lang], font=("Bahnschrift",16, "bold"))
        self.gammaframetitle.grid(row=0, column=0, columnspan=5, sticky="nsew", padx=5, pady=(1,5))
        
        self.reference = ctk.StringVar()
        self.referencelabel = ctk.CTkLabel(self.gammaframe, text=Text().reference[self.lang], font=("Bahnschrift",14, "bold"))
        self.referenceselector = ctk.CTkOptionMenu(self.gammaframe, variable=self.reference, values=[], command=self.clear_gamma)
        self.referencelabel.grid(column=0, row=1, padx=5, pady=1, sticky="nsw")
        self.referenceselector.grid(column=1, columnspan=4, row=1, padx=5, pady=1, sticky="nsew")
        
        self.test = ctk.StringVar()
        self.testlabel = ctk.CTkLabel(self.gammaframe, text=Text().test[self.lang], font=("Bahnschrift",14, "bold"))
        self.testselector = ctk.CTkOptionMenu(self.gammaframe, variable=self.test, values=[], command=self.clear_gamma)
        self.testlabel.grid(column=0, row=2, padx=5, pady=1, sticky="nsw")
        self.testselector.grid(column=1, columnspan=4, row=2, padx=5, pady=1, sticky="nsew")

        self.gammatype = ctk.BooleanVar(value=self.p.get_attribute("gammatype"))
        self.gammatypelabel = ctk.CTkLabel(self.gammaframe, text=Text().gammatype[self.lang], font=("Bahnschrift",12, "bold"))
        self.local = ctk.CTkRadioButton(self.gammaframe, text=Text().local[self.lang], variable=self.gammatype, value=True, font=("Bahnschrift",12, "bold"))
        self.globalg = ctk.CTkRadioButton(self.gammaframe, text=Text().globalg[self.lang], variable=self.gammatype, value=False, font=("Bahnschrift",12, "bold"))
        self.gammatypelabel.grid(column=0, row=3, padx=5, pady=1, sticky="nsw")
        self.local.grid(column=1, columnspan=2, row=3, padx=5, pady=(5,1), sticky="nsew")
        self.globalg.grid(column=3, columnspan=2,  row=3, padx=5, pady=(5,1), sticky="nsew")
        
        self.percent = ctk.StringVar(value=self.p.get_attribute("dd"))
        self.distance = ctk.StringVar(value=self.p.get_attribute("dta"))
        self.lowerthreshold = ctk.StringVar(value=self.p.get_attribute("lowerthreshold"))
        self.criterialabel = ctk.CTkLabel(self.gammaframe, text=Text().criterion[self.lang], font=("Bahnschrift",12, "bold"))
        self.percententry = ctk.CTkEntry(self.gammaframe, textvariable=self.percent, width=35)
        self.percentlabel = ctk.CTkLabel(self.gammaframe, text="% ", font=("Bahnschrift",14, "bold"))
        self.distanceentry = ctk.CTkEntry(self.gammaframe, textvariable=self.distance, width=35)
        self.distancelabel = ctk.CTkLabel(self.gammaframe, text="mm", font=("Bahnschrift",14, "bold"))
        self.lowerthresholdlabel = ctk.CTkLabel(self.gammaframe, text=Text().lowerthreshold[self.lang], font=("Bahnschrift",12, "bold"))
        self.lowerthresholdentry = ctk.CTkEntry(self.gammaframe, textvariable=self.lowerthreshold, width=35)
        
        self.criterialabel.grid(column=0, row=4, padx=5, pady=1, sticky="nsw")
        self.percententry.grid(column=1, row=4, padx=5, pady=1, sticky="nse")
        self.percentlabel.grid(column=2, row=4, padx=5, pady=1, sticky="nsw")
        self.distanceentry.grid(column=3, row=4, padx=5, pady=1, sticky="nse")
        self.distancelabel.grid(column=4, row=4, padx=5, pady=1, sticky="nsw")
        self.lowerthresholdlabel.grid(column=0, row=5, padx=5, pady=1, sticky="nsw")
        self.lowerthresholdentry.grid(column=1, columnspan=4, row=5, padx=5, pady=1, sticky="nsew")
        
        self.difference = ctk.BooleanVar(value=False)
        self.difference_button = ctk.CTkCheckBox(self.gammaframe, text=Text().difference[self.lang], variable=self.difference, font=("Bahnschrift",12, "bold"), command = self.clear_gam)
        self.difference_button.grid(column=0, row=6, padx=5, pady=2, sticky="nsw")
        self.plotgamma = ctk.BooleanVar(value=False)
        self.plotgamma_button = ctk.CTkCheckBox(self.gammaframe, text=Text().plotgamma[self.lang], variable=self.plotgamma, font=("Bahnschrift",12, "bold"), command = self.clear_diff)
        self.plotgamma_button.grid(column=1, columnspan=4, row=6, padx=5, pady=2, sticky="nsw")
        self.calc_gamma_button = ctk.CTkButton(self.gammaframe, text=Text().calculate[self.lang], command=self.calculate_gamma, font=("Bahnschrift",12, "bold"), fg_color="green")
        self.calc_gamma_button.grid(column=0, row=7, padx=5, pady=2, sticky="nsew")
        
        self.resultcanvas = ctk.CTkLabel(self.gammaframe, fg_color="white", text="", corner_radius=10, font=("Bahnschrift",14, "bold"))
        self.resultcanvas.grid(column=1, columnspan=4, row=7, padx=5, pady=2, sticky="nsew")
        
        self.gammaframe.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        draw = False
        if self.parent.plots != []:
            if self.showlegend.get():
                self.parent.ax.legend()
                draw = True
            if self.showgrid.get(): 
                self.parent.ax.grid(which="major", visible=True, axis="both", lw=1) 
                try: self.parent.ax2.grid(which="major", visible=True, axis="both", lw=1) 
                except Exception: pass
                draw = True
        if draw == True: self.parent.canvas.draw()
        self.disable_all_buttons()

        self.doseaddframe = ctk.CTkFrame(self.analysis_scrollframe.viewPort, border_color="black", border_width=1)
        self.doseaddframe.configure(fg_color=self.dataframe1.cget("fg_color"))
        self.doseaddframe.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        self.doseaddframe.columnconfigure(0, weight=1, minsize=80)
        self.doseaddframe.columnconfigure(1, weight=1)
        self.doseaddframetitle = ctk.CTkLabel(self.doseaddframe, text=Text().doseadd[self.lang], font=("Bahnschrift",16, "bold"))
        self.doseaddframetitle.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=(1,5))
        self.doseaddreference = ctk.StringVar()
        self.doseaddreferencelabel = ctk.CTkLabel(self.doseaddframe, text="Graph 1", font=("Bahnschrift",14, "bold"))
        self.doseaddreferenceselector = ctk.CTkOptionMenu(self.doseaddframe, variable=self.doseaddreference, values=[])
        self.doseaddreferencelabel.grid(column=0, row=1, padx=5, pady=1, sticky="nsw")
        self.doseaddreferenceselector.grid(column=1, row=1, padx=5, pady=1, sticky="nsew")
        self.doseaddtest = ctk.StringVar()
        self.doseaddtestlabel = ctk.CTkLabel(self.doseaddframe, text="Graph 2", font=("Bahnschrift",14, "bold"))
        self.doseaddtestselector = ctk.CTkOptionMenu(self.doseaddframe, variable=self.doseaddtest, values=[])
        self.doseaddtestlabel.grid(column=0, row=3, padx=5, pady=1, sticky="nsw")
        self.doseaddtestselector.grid(column=1, row=3, padx=5, pady=1, sticky="nsew")
        self.doseaddscale = ctk.StringVar(value="0.5")
        self.doseaddscalelabel = ctk.CTkLabel(self.doseaddframe, text=Text().scale[self.lang], font=("Bahnschrift",12, "bold"))
        self.doseaddscaleentry = ctk.CTkEntry(self.doseaddframe, textvariable=self.doseaddscale, width=70)
        self.doseaddscalelabel.grid(column=0, row=2, padx=5, pady=1, sticky="nsw")
        self.doseaddscaleentry.grid(column=1, row=2, padx=5, pady=1, sticky="nse")
        self.doseaddscale2 = ctk.StringVar(value="0.5")
        self.doseaddscalelabel2 = ctk.CTkLabel(self.doseaddframe, text=Text().scale[self.lang], font=("Bahnschrift",12, "bold"))
        self.doseaddscaleentry2 = ctk.CTkEntry(self.doseaddframe, textvariable=self.doseaddscale2, width=70)
        self.doseaddscalelabel2.grid(column=0, row=4, padx=5, pady=1, sticky="nsw")
        self.doseaddscaleentry2.grid(column=1, row=4, padx=5, pady=1, sticky="nse")
        self.doseaddbutton = ctk.CTkButton(self.doseaddframe, text=Text().apply[self.lang], fg_color="green", width=110, command = self.add_doses)
        self.doseaddbutton.grid(column=1, row=5, padx=5, pady=(5,2), sticky="nse")

    ######################################################################################################################################################################

    def add_doses(self):
        plot_labels = [plot.label for plot in self.parent.plots]
        reference_axes, reference_dose, _ = self.parent.plots[plot_labels.index(self.doseaddreference.get())].data(allow_normalization=False)
        evaluation_axes, evaluation_dose, _ = self.parent.plots[plot_labels.index(self.doseaddtest.get())].data(allow_normalization=False)

        akima_dose_interpolator = Akima1DInterpolator(evaluation_axes, evaluation_dose)
        evaluation_dose = akima_dose_interpolator.__call__(reference_axes)

        new_axis = reference_axes
        new_dose = float(self.doseaddscale.get())*np.array(reference_dose) + float(self.doseaddscale2.get())*np.array(evaluation_dose)
        new_filepath = self.parent.plots[plot_labels.index(self.doseaddreference.get())].dataObject.filepath + self.parent.plots[plot_labels.index(self.doseaddtest.get())].dataObject.filepath
        new_filename = f"{self.doseaddscale.get()}*" + self.parent.plots[plot_labels.index(self.doseaddreference.get())].dataObject.filename + " + " + f"{self.doseaddscale2.get()}*" + self.parent.plots[plot_labels.index(self.doseaddtest.get())].dataObject.filename
        if self.parent.plots[plot_labels.index(self.doseaddreference.get())].dataObject.direction == self.parent.plots[plot_labels.index(self.doseaddtest.get())].dataObject.direction:
            direction = self.parent.plots[plot_labels.index(self.doseaddreference.get())].dataObject.direction
        else: return
       
        class SummedDose:
            def __init__(self, filepath, filename, direction, axis, dose, plotlist, options, normalize):

                self.filepath = filepath
                self.lang = ProfileHandler().get_attribute("language")
                self.filename = filename
                self.dose = np.array(dose)
                self.axis = np.array(axis)
                self.direction = direction
                self.std_dev = np.array([0 for i in range(len(self.dose))])

                plotlist += [TGS_Plot(options, self, normalize = normalize)]
                options.parameters.append(Parameters(options.paramslist.viewPort, plotlist[-1], self.lang))
                options.parameters[-1].grid(row=len(options.parameters)-1, sticky="ew", padx=5, pady=5)
                options.plotbuttons.append(ctk.CTkRadioButton(options.graphlist.viewPort, text=plotlist[-1].label, variable=options.current_plot, text_color = plotlist[-1].linecolor, value=plotlist[-1].label, command=options.change_current_plot, font=("Bahnschrift", 14, "bold")))
                options.plotbuttons[-1].grid(sticky="w", padx=5, pady=5)
                options.filenames.append(self.filepath)
                if len(options.parent.plots) == 1:
                    options.enable_all_buttons()
                    
                try:
                    options.current_plot.set(plotlist[-1].label)
                    options.parent.saved = False
                    options.update_plotlist()
                    options.parent.update()
                except IndexError:
                    pass

            def params(self):
                if self.direction == "Z":
                    return pdd.calculate_parameters(
                        np.array(self.axis),
                        self.dose / max(self.dose),
                        [],
                    )
                else:
                    params = dp.calculate_parameters(
                        self.axis, self.dose / max(self.dose))
                    self.cax = params[1]
                    return params
                
        if new_filepath in self.filenames: 
            plot_label = [plot for plot in self.parent.plots if plot.dataObject.filepath == new_filepath][0].label
            current_plot = self.current_plot.get()
            self.current_plot.set(plot_label)
            self.remove_plot()
            SummedDose(new_filepath, new_filename, direction, new_axis, new_dose, self.parent.plots, self, normalize = self.normalize.get())
            self.current_plot.set(current_plot)
            self.change_current_plot()
        else:
            SummedDose(new_filepath, new_filename, direction, new_axis, new_dose, self.parent.plots, self, normalize = self.normalize.get())

    def clear_gam(self):
        self.plotgamma.set("False")
        
    def clear_diff(self):
        self.difference.set("False")

    def save(self):

        try:
            dpi = int(self.dpi.get())
            size_x = float(self.figuresize_x.get())
            size_y = float(self.figuresize_y.get())
        except Exception: self.bell()
        fname = fd.asksaveasfilename(title = Text().saveplottitle[self.lang], filetypes = (("PNG","*.png"),(Text().allfiles[self.lang],"*.*")))
        color = self.parent.figure.patch.get_facecolor()
        self.parent.figure.patch.set_facecolor("white")
        if self.parent.ax2 != None: 
            color2 = plt.gcf()._axstack.as_list()[0].get_facecolor()
            plt.gcf()._axstack.as_list()[0].set_facecolor("white")
            color3 = plt.gcf()._axstack.as_list()[1].get_facecolor()
            plt.gcf()._axstack.as_list()[1].set_facecolor("white")
        else:
            color2 = self.parent.ax.get_facecolor()
            self.parent.ax.set_facecolor("white")

        size = plt.gcf().get_size_inches()
        plt.gcf().set_size_inches(size_x, size_y)
        self.parent.figure.savefig(fname=fname, dpi=dpi)
        self.parent.figure.patch.set_facecolor(color)
        if self.parent.ax2 != None:
            plt.gcf()._axstack.as_list()[0].set_facecolor(color2)
            plt.gcf()._axstack.as_list()[1].set_facecolor(color3)
        else:
            self.parent.ax.set_facecolor(color2)
        self.parent.saved = True
        plt.gcf().set_size_inches(size)

    def preview(self):

        try:
            dpi = int(self.dpi.get())
            size_x = float(self.figuresize_x.get())
            size_y = float(self.figuresize_y.get())
        except Exception: self.bell()
        color = self.parent.figure.patch.get_facecolor()
        self.parent.figure.patch.set_facecolor("white")
        if self.parent.ax2 != None: 
            color2 = plt.gcf()._axstack.as_list()[0].get_facecolor()
            plt.gcf()._axstack.as_list()[0].set_facecolor("white")
            color3 = plt.gcf()._axstack.as_list()[1].get_facecolor()
            plt.gcf()._axstack.as_list()[1].set_facecolor("white")
        else:
            color2 = self.parent.ax.get_facecolor()
            self.parent.ax.set_facecolor("white")
        size = plt.gcf().get_size_inches()

        plt.gcf().set_size_inches(size_x, size_y)
        ps_buffer = io.BytesIO()
        self.parent.canvas.print_figure(ps_buffer, format="png", dpi=dpi)
        ps_buffer.seek(0)
        image = Image.open(ps_buffer)
        preview_window = ctk.CTkToplevel()
        preview_window.title("Preview")
        img_tk = ctk.CTkImage(light_image= image, size = image.size)
        label = ctk.CTkLabel(preview_window, image=img_tk, text="")
        label.image = img_tk
        label.pack()
        ps_buffer.close()
        preview_window.lift()

        self.parent.figure.patch.set_facecolor(color)
        if self.parent.ax2 != None:
            plt.gcf()._axstack.as_list()[0].set_facecolor(color2)
            plt.gcf()._axstack.as_list()[1].set_facecolor(color3)
        else:
            self.parent.ax.set_facecolor(color2)
        self.parent.saved = True
        plt.gcf().set_size_inches(size)
        return
    
    def on_enter(self, widget, command, event=None):
        widget.bind("<Return>", command)
            
    def on_leave(self, widget, event=None):
        widget.unbind("<Return>")
                  
    def change_order(self, direction):
        self.parent.saved = False
        plot_labels = [plot.label for plot in self.parent.plots]
        index = plot_labels.index(self.current_plot.get())
        
        if direction == "up":
            if index-1 >= 0:
                self.parent.plots[index], self.parent.plots[index-1] = self.parent.plots[index-1], self.parent.plots[index]
                self.plotbuttons[index], self.plotbuttons[index-1] = self.plotbuttons[index-1], self.plotbuttons[index]
                self.parameters[index], self.parameters[index-1] = self.parameters[index-1], self.parameters[index]
                self.filenames[index], self.filenames[index-1] = self.filenames[index-1], self.filenames[index]
                #[button.grid_forget() for button in self.plotbuttons]
                #[params.grid_forget() for params in self.parameters]
                [button.grid(row=i, padx=5, pady=5, sticky="w") for i, button in enumerate(self.plotbuttons)]
                [params.grid(row=i, sticky="ew", padx=5, pady=5) for i, params in enumerate(self.parameters)]
                self.update_plotlist()
        
        elif direction == "down":
            if index+1 < len(self.plotbuttons):
                self.parent.plots[index], self.parent.plots[index+1] = self.parent.plots[index+1], self.parent.plots[index]
                self.plotbuttons[index], self.plotbuttons[index+1] = self.plotbuttons[index+1], self.plotbuttons[index]
                self.parameters[index], self.parameters[index+1] = self.parameters[index+1], self.parameters[index]
                self.filenames[index], self.filenames[index+1] = self.filenames[index+1], self.filenames[index]
                #[button.grid_forget() for button in self.plotbuttons]
                #[params.grid_forget() for params in self.parameters]
                [button.grid(row=i, padx=5, pady=5, sticky="w") for i, button in enumerate(self.plotbuttons)]
                [params.grid(row=i, sticky="ew", padx=5, pady=5) for i, params in enumerate(self.parameters)]
                self.update_plotlist()
                
        self.parent.update()
        
    def disable_all_buttons(self):
        for tab in self.winfo_children():
            for frame in tab.winfo_children():
                for widget in frame.winfo_children():
                    try:
                        if widget.master != self.dataframe2:
                            widget.configure(state="disabled")
                    except ValueError:
                        pass
                    
                    try:
                        if widget.master != self.dataframe2:
                            for child in widget.winfo_children():
                                child.configure(state="disabled")
                    except Exception:
                        pass
            
    def enable_all_buttons(self):
        for tab in self.winfo_children():
            for frame in tab.winfo_children():
                for widget in frame.winfo_children():
                    try:
                        widget.configure(state="normal")
                    except ValueError:
                        pass
                
                    try:
                        for child in widget.winfo_children():
                            child.configure(state="normal")
                    except Exception:
                        pass
        
    def remove_plot(self):
        try: self.parent.ax2.clear()
        except AttributeError: pass
        self.parent.saved = False
        plot_labels = [plot.label for plot in self.parent.plots]
        index = plot_labels.index(self.current_plot.get())
        current_name = self.current_plot.get()
        if self.reference.get() == current_name:
            self.reference.set("")
            self.clear_gamma()
        if self.test.get() == current_name:
            self.test.set("")
            self.clear_gamma()
        if self.doseaddreference.get() == current_name:
            self.doseaddreference.set("")
        if self.doseaddtest.get() == current_name:
            self.doseaddtest.set("")
        self.plotbuttons[index].grid_forget()
        self.plotbuttons.pop(index)
        self.parent.plots.pop(index)
        self.parameters[index].grid_forget()
        self.parameters.pop(index)
        self.filenames.pop(index)
        if len(self.parent.plots) !=0:
            if index == 0:
                self.current_plot.set(self.parent.plots[0].label)
                self.parent.plots[0].set_tab_data()
            else:
                self.current_plot.set(self.parent.plots[index-1].label)
                self.parent.plots[index-1].set_tab_data()
        else:
            self.current_plot.set("")
            self.plottitleentry.delete(0, "end")
        self.update_plotlist()
        if len(self.parent.plots) == 0:
            self.disable_all_buttons()
        self.parent.update()

    def toggle_cax_correction(self, event=None):
        self.parent.saved = False
        for plot in self.parent.plots:
            plot.caxcorrection = self.caxcorrection.get()
        self.parent.update()
        
    def change_normalization(self, event=None):
        self.parent.saved = False
        for plot in self.parent.plots:
            plot.normalize = self.normalize.get()
            normtypedict = {Text().maximum[self.lang]:"maximum", Text().plateau[self.lang]:"plateau", Text().centeraxis[self.lang]:"centeraxis"}
            plot.normalization = normtypedict[self.normalization.get()]
        self.parent.update()

    def change_points(self, event=None):
        self.parent.saved = False
        for plot in self.parent.plots:
            plot.points = self.show_points.get()
        self.parent.update()
        
    def change_error(self, event=None):
        self.parent.saved = False
        for plot in self.parent.plots:
            plot.error = self.show_error.get()
        self.parent.update()
        
    def apply(self, event=None):
        try:
            plot_labels = [plot.label for plot in self.parent.plots]
            index = plot_labels.index(self.current_plot.get())
            current_plot = self.parent.plots[index]
            current_plot.dosefactor = float(self.dosescaleentry.get())
            current_plot.doseshift = float(self.doseshiftentry.get())
            current_plot.axshift = float(self.axshiftentry.get())
            current_plot.flip = self.flip.get()
            self.calculate_gamma()
            try: self.add_doses()
            except ValueError: pass
            self.parent.update()
        except ValueError:
            pass
        
    def clear_gamma(self, event=None):
        try: self.parent.ax2.yaxis.set_label_text("")
        except Exception: pass
        self.resultcanvas.configure(text="", fg_color="white")
        
    def calculate_gamma(self):
        try:
            percent = float(self.percent.get())
            distance = float(self.distance.get())
            local = self.gammatype.get()
            lower_percent_dose_cutoff = float(self.lowerthreshold.get())
            plot_labels = [plot.label for plot in self.parent.plots]
            reference_axes, reference_dose, _ = self.parent.plots[plot_labels.index(self.reference.get())].data()
            evaluation_axes, evaluation_dose, _ = self.parent.plots[plot_labels.index(self.test.get())].data()
            if self.caxcorrection.get():
                reference_axes = np.add(reference_axes, self.parent.plots[plot_labels.index(self.reference.get())].dataObject.params()[1])
                evaluation_axes = np.add(evaluation_axes, self.parent.plots[plot_labels.index(self.test.get())].dataObject.params()[1])
            try:
                g = gamma(axes_reference=reference_axes, dose_reference=reference_dose, axes_evaluation=evaluation_axes, dose_evaluation=evaluation_dose, dose_percent_threshold=percent, distance_mm_threshold=distance, local_gamma=local, lower_percent_dose_cutoff=lower_percent_dose_cutoff, max_gamma =4)
                g1 = np.array([i for i in g if np.isnan(i) == False])
                gamma_index = len(np.where(g1 <= 1)[0])/len(g1)*100
            except Exception:
                g = np.zeros(len(reference_axes))
                g1 = np.zeros(len(reference_axes))
                gamma_index = 0
            if gamma_index >= 95:
                self.resultcanvas.configure(fg_color="green")
            elif gamma_index <= 95 and gamma_index > 80:
                self.resultcanvas.configure(fg_color="yellow")
            else:
                self.resultcanvas.configure(fg_color="red")
                
            self.resultcanvas.configure(text=str(round(gamma_index, 3)) + "%")
            
            if self.difference.get():
                if self.parent.ax2 == None:
                    self.parent.figure, self.parent.ax = plt.subplots(nrows=2, ncols=1, sharex=True, height_ratios=[6, 2])
                    self.parent.ax, self.parent.ax2 = self.parent.ax
                    self.parent.canvas = FigureCanvasTkAgg(self.parent.figure, master=self.parent)
                    self.parent.navbar = NavigationToolbar2Tk(self.parent.canvas, self.parent, pack_toolbar=False) 
                    self.parent.slider1 = Slider(self.parent.navbar, self.parent.options.update_xlim)
                    self.parent.slider2 = Slider(self.parent.navbar, self.parent.options.update_xlim)
                    self.parent.slider1.pack(side="left", expand=False, padx=10)
                    self.parent.slider2.pack(side="left", expand=False)
                    self.parent.navbar._buttons["Save"].config(command=self.parent.options.save)
                    self.set_xlim()
                    self.update_xlim()
                    self.parent.master.master.parent.parent.set_theme() 
                    self.parent.config()
                    self.parent.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
                    self.parent.navbar.grid(row=1, column=0, sticky="nsew")
                self.parent.ax2.clear()
                evaluation_dose = np.interp(reference_axes, evaluation_axes, evaluation_dose)
                difference = 100*np.array([(reference_dose[i]-evaluation_dose[i])/reference_dose[i] for i in range(len(reference_dose))])
                self.parent.ax2.plot(reference_axes, difference, color="black", lw=1, linestyle="--", label=f"Ø-{Text().difference2[self.lang]}: {np.average(np.abs(difference)):.3f}%")
                self.parent.ax2.yaxis.set_label_text(Text().difference2[self.lang] + " %")
                self.parent.ax2.legend(loc="upper right", framealpha=0)
                self.parent.update()
                self.toggle_legend_options()
                
            elif self.plotgamma.get():
                if self.parent.ax2 == None:
                    self.parent.figure, self.parent.ax = plt.subplots(nrows=2, ncols=1, sharex=True, height_ratios=[6, 2])
                    self.parent.ax, self.parent.ax2 = self.parent.ax
                    
                    self.parent.canvas = FigureCanvasTkAgg(self.parent.figure, master=self.parent)
                    self.parent.navbar = NavigationToolbar2Tk(self.parent.canvas, self.parent, pack_toolbar=False)  
                    self.parent.slider1 = Slider(self.parent.navbar, self.update_xlim)
                    self.parent.slider2 = Slider(self.parent.navbar, self.update_xlim)
                    self.parent.slider1.pack(side="left", expand=False, padx=10)
                    self.parent.slider2.pack(side="left", expand=False)
                    self.parent.navbar._buttons["Save"].config(command=self.parent.options.save)
                    self.set_xlim()
                    self.update_xlim()
                    self.parent.master.master.parent.parent.set_theme() 
                    self.parent.config()
                    self.parent.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
                    self.parent.navbar.grid(row=1, column=0, sticky="nsew")
                self.parent.ax2.clear()
                self.parent.ax2.yaxis.set_label_text("Gamma-Index")
                self.parent.ax2.set_ylim(bottom=-0.2, top=4.2)
                self.parent.ax2.scatter(reference_axes, g, marker="x",c=g, cmap="jet", vmin=0, vmax=2, label = f"Ø-Gamma: {np.average(g1):.3f}")
                self.parent.ax2.legend(loc="upper right", framealpha=0)
                self.parent.update()
                self.toggle_legend_options()
                
            else:
                try: 
                    if self.parent.ax2 != None:
                        self.parent.ax2 = None
                        self.parent.figure, self.parent.ax = plt.subplots()
                        self.parent.canvas = FigureCanvasTkAgg(self.parent.figure, master=self.parent)
                        self.parent.navbar = NavigationToolbar2Tk(self.parent.canvas, self.parent, pack_toolbar=False)  
                        self.parent.slider1 = Slider(self.parent.navbar, self.parent.options.update_xlim)
                        self.parent.slider2 = Slider(self.parent.navbar, self.parent.options.update_xlim)
                        self.parent.slider1.pack(side="left", expand=False, padx=10)
                        self.parent.slider2.pack(side="left", expand=False)
                        self.parent.navbar._buttons["Save"].config(command=self.parent.options.save)
                        self.set_xlim()
                        self.update_xlim()
                        self.parent.master.master.parent.parent.set_theme() 
                        self.parent.config()
                        self.parent.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
                        self.parent.navbar.grid(row=1, column=0, sticky="nsew")    
                        self.parent.update()    
                        
            
                except AttributeError: pass
                
        except ValueError as e:
            pass
            
    def set_xlim(self, draw=True):
        self.parent.slider1.var.set(self.parent.ax.get_xlim()[0])
        self.parent.slider2.var.set(self.parent.ax.get_xlim()[1])
        self.parent.slider1.slider.configure(from_=self.parent.ax.get_xlim()[0], to=self.parent.ax.get_xlim()[1])
        self.parent.slider2.slider.configure(from_=self.parent.ax.get_xlim()[0], to=self.parent.ax.get_xlim()[1])
        self.parent.slider1.text.configure(text=str(round(self.parent.slider1.var.get(), 2)))
        self.parent.slider2.text.configure(text=str(round(self.parent.slider2.var.get(), 2)))
        
    def update_xlim(self):
        
        self.parent.ax.set_xlim(self.parent.slider1.var.get(), self.parent.slider2.var.get())
        self.parent.canvas.draw()

    def choose_linecolor(self):
        self.parent.saved = False
        color = colorchooser.askcolor()
        self.plotcolor.set(color[1])
        self.linecolorbutton.configure(fg_color = color[1])
        plot_labels = [plot.label for plot in self.parent.plots]
        index = plot_labels.index(self.current_plot.get())  
        line_labels = [line._label for line in self.parent.ax.lines]
        line_index = line_labels.index(self.current_plot.get())
        self.plotbuttons[index].configure(text_color=color[1])
        self.parameters[index].namelabel.configure(fg_color=color[1])
        current_plot = self.parent.plots[index]
        current_plot.linecolor = color[1]
        self.parent.ax.lines[line_index].set_color(color[1])
        self.toggle_legend_options()
        
    def rename_plot(self, event=None):
        self.parent.saved = False
        new_name = self.plottitleentry.get()
        plot_labels = [plot.label for plot in self.parent.plots]
        index = plot_labels.index(self.current_plot.get())
        current_name = self.parent.plots[index].label
        if self.reference.get() == current_name:
            self.reference.set(new_name)
        if self.test.get() == current_name:
            self.test.set(new_name)
        
        self.plotbuttons[index].configure(text=new_name)
        self.parameters[index].namelabel.configure(text=new_name)
        self.plotbuttons[index]._value = new_name
        current_plot = self.parent.plots[index]
        current_plot.label = new_name
        self.current_plot.set(new_name)
        self.update_plotlist()
        self.parent.update()    
        
    def change_linestyle(self, value):
        self.parent.saved = False
        plot_labels = [plot.label for plot in self.parent.plots]
        index = plot_labels.index(self.current_plot.get())
        line_labels = [line._label for line in self.parent.ax.lines]
        line_index = line_labels.index(self.current_plot.get())
        self.parent.plots[index].linestyle = {Text().dashdot[self.lang]:"-.", Text().dash[self.lang]:"-", Text().dot[self.lang]:"dotted", Text().none[self.lang]:" "}[value]
        self.parent.ax.lines[line_index].set_linestyle(self.parent.plots[index].linestyle)
        self.toggle_legend_options()
        
    def change_linethickness(self, value):
        self.parent.saved = False
        plot_labels = [plot.label for plot in self.parent.plots]
        line_labels = [line._label for line in self.parent.ax.lines]
        line_index = line_labels.index(self.current_plot.get())
        index = plot_labels.index(self.current_plot.get())
        self.parent.ax.lines[line_index].set_linewidth(value)
        self.parent.plots[index].linethickness = value
        self.toggle_legend_options()
        
    def rename_title(self, event=None):
        self.parent.saved = False
        self.parent.ax.set_title(self.title.get())
        self.parent.canvas.draw()
        
    def rename_x(self, event=None):
        self.parent.saved = False
        self.parent.ax.set_xlabel(self.xtitle.get())
        self.parent.canvas.draw()
        
    def rename_y(self, event=None):
        self.parent.saved = False
        self.parent.ax.set_ylabel(self.ytitle.get())
        self.parent.canvas.draw()
        
    def toggle_legend_options(self, draw=True):
        if self.parent.plots == []: return
        if self.showlegend.get():
            self.showlegend_options.configure(state="normal")
            which = {Text().legendoptions1[self.lang]:"best", 
                     Text().legendoptions2[self.lang]:"upper left",
                     Text().legendoptions3[self.lang]:"upper right",
                     Text().legendoptions4[self.lang]:"lower left",
                     Text().legendoptions5[self.lang]:"lower right"}.get(self.legendoptions.get())
            try: self.parent.ax.get_legend().remove()
            except AttributeError: pass
            self.parent.ax.legend(loc=which, reverse=True, framealpha=0)
            if draw: self.parent.canvas.draw()
        else:
            self.showlegend_options.configure(state="disabled")
            try: self.parent.ax.get_legend().remove()
            except AttributeError: pass
            if draw: self.parent.canvas.draw()
            
    def toggle_grid_options(self, draw=True):
        if self.showgrid.get():
            self.showgrid_options.configure(state="normal")
            which = {Text().gridoptions1[self.lang]:"major", Text().gridoptions2[self.lang]:"both"}.get(self.gridoptions.get())
            self.parent.ax.grid(False, which = "both", axis="both")
            self.parent.ax.grid(which="major", visible=True, axis="both", lw=1)
            try:
                self.parent.ax2.grid(False, which = "both", axis="both")
                self.parent.ax2.grid(which="major", visible=True, axis="both", lw=1)
            except AttributeError: pass
            if which == "both":
                self.parent.ax.grid(which="minor", visible=True, axis="both", lw=0.5)
                try: self.parent.ax2.grid(which="minor", visible=True, axis="both", lw=0.5)
                except AttributeError: pass
            if draw: self.parent.canvas.draw()
        else:
            self.showgrid_options.configure(state="disabled")
            self.parent.ax.grid(False, which = "both", axis="both")
            try: self.parent.ax2.grid(False, which = "both", axis="both")
            except AttributeError: pass
            if draw: self.parent.canvas.draw()
        
    def update_plotlist(self):
        plotnames = [plot.label for plot in self.parent.plots]
        self.plotselector.configure(values=plotnames)
        self.plotselector2.configure(values=plotnames)
        self.referenceselector.configure(values=plotnames)
        self.testselector.configure(values=plotnames)
        self.doseaddreferenceselector.configure(values=plotnames)
        self.doseaddtestselector.configure(values=plotnames)
        
    def set_ax_names(self, draw=True):
        self.parent.ax.set_title(self.title.get())
        self.parent.ax.set_xlabel(self.xtitle.get())
        self.parent.ax.set_ylabel(self.ytitle.get())
    
    def load_topas(self, path = None):
        if path == None:
            path = fd.askopenfilenames(filetypes=[("TOPAS files", "*.csv")])
        else:
            path = [path]
        if path == "" :
            return
        for p in path:
            if p not in self.filenames:
                
                sim = TGS_Plot(self, Simulation(p))
                if sim.fail == False:
                    self.parent.plots.append(sim)
                    self.filenames.append(p)
                    self.parameters.append(Parameters(self.paramslist.viewPort, sim, self.lang))
                    self.parameters[-1].grid(row=len(self.parameters)-1, sticky="ew", padx=5, pady=5)
                    self.current_plot.set(sim.label)
                    self.update_plotlist()     
                    self.plotbuttons.append(ctk.CTkRadioButton(self.graphlist.viewPort, text=sim.label, variable=self.current_plot, text_color = sim.linecolor, value=sim.label, command=self.change_current_plot, font=("Bahnschrift", 14, "bold")))
                    self.plotbuttons[-1].grid(sticky="w", padx=5, pady=5)
                    if len(self.parent.plots) == 1:
                        self.enable_all_buttons()
                
            self.parent.saved = False
            self.parent.update()
            
    def load_measurement(self, path = None):
        if path == None:
            path = fd.askopenfilename(filetypes=[("MCC files", "*.mcc")])
        
        if path != "" and path not in self.filenames:
            PTWMultimporter(path, self.tab(Text().data[self.lang]), self.parent.plots, self)
            
    def load_raystation(self, path = None):
        if path == None:
            path = fd.askopenfilename(filetypes=[("XLS files", "*.xls"), ("CSV Files", "*.csv")])
        
        if path != "" and path not in self.filenames:
            RayStationMultiImporter(path, self.tab(Text().data[self.lang]), self.parent.plots, self)
            
    def load_radcalc(self, path = None):
        if path == None:
            path = fd.askopenfilenames(filetypes=[("CSV files", "*.csv")])
        for p in path:
            if p != "" and p not in self.filenames:
                RadCalc(p, self.tab(Text().data[self.lang]), self.parent.plots, self)

    def load_eclipse(self, path = None):
        if path == None:
            path = fd.askopenfilenames(filetypes=[("DATA files", "*.data")])
        for p in path:
            if p != "" and p not in self.filenames:
                Eclipse(p, self.tab(Text().data[self.lang]), self.parent.plots, self)
            
            
    def load_txt(self, path = None, direction=None):
        if path == None:
            path = fd.askopenfilename(filetypes=[("TXT files", "*.txt")])
        if path not in self.filenames and path != "":
            with open(path, "r") as f:
                line = f.readline()
            if "Distance" in line:
                TXTImporter(path, self.tab(Text().data[self.lang]), self.parent.plots, self, "slicer",delimiter = "\t", skiprows=1)
            else:
                TXTImporter(path, self.tab(Text().data[self.lang]), self.parent.plots, self, "txt", delimiter = ",", direction=direction)

    def change_current_plot(self, event=None):
        plot_labels = [plot.label for plot in self.parent.plots]
        index = plot_labels.index(self.current_plot.get())
        self.parent.plots[index].set_tab_data()
            
    def change_name(self):
        
        root = self.parent.master.master.parent        
        window = ctk.CTkToplevel(root)
        window.overrideredirect(True)
        window.geometry(f"150x142+{root.winfo_rootx()+root.winfo_width()//2-75}+{root.winfo_rooty()+root.winfo_height()//2-71}")
        window.title("")
        
        def move(event):
            window.lift()
            entry.focus()
            window.geometry(f"150x142+{root.winfo_rootx()+root.winfo_width()//2-75}+{root.winfo_rooty()+root.winfo_height()//2-71}")
        
        def submit():
            self.newtabname = entry.get()
            window.destroy()
            if self.newtabname == "":
                return
     
            tab = self.newtabname
            self.newtabname = ""
            self.parent.master.master._current_name = tab
            
            self.parent.master.master.parent.parent.menubar.tabmenu.entryconfig(self.index+2, label=Text().closetab[self.lang].format(tab), 
                command = lambda: self.parent.master.master.remove_tab(self.index))
                                                                                
            frame = self.parent.master.master._tab_dict[self.parent.master.master._name_list[self.index]]
            self.parent.master.master._tab_dict.pop(self.parent.master.master._name_list[self.index])
            self.parent.master.master._tab_dict[tab] = frame
            self.parent.master.master._name_list[self.index] = tab
            self.parent.master.master._segmented_button._value_list[self.index] = tab
            button = self.parent.master.master._segmented_button._buttons_dict[self.parent.master.master.tabnames[self.index]]
            button.configure(text=tab)
            self.parent.master.master._segmented_button._buttons_dict.pop(self.parent.master.master.tabnames[self.index])
            self.parent.master.master._segmented_button._buttons_dict[tab] = button
            self.parent.master.master.tabnames[self.index] = tab
            self.parent.name = tab
            values = self.parent.master.master._segmented_button.cget("values")
            values[self.index] = tab
            self.parent.master.master._segmented_button.configure(values=values)
            self.parent.master.master._configure_tab_background_corners_by_name(tab)
            self.parent.master.master._segmented_button.set(tab)
            self.parent.master.master._draw()
            return
        def close():
            window.destroy()
            
        window.columnconfigure(0, weight=1)
        closebutton = ctk.CTkButton(window, text=" X ", command=close, width=2, height=1, font=("Bahnschrift", 12))
        closebutton.grid(row=0, column=0, sticky="ne", padx=(0, 4), pady=(4, 4))
        textlabel = ctk.CTkLabel(window, text=Text().newtabname[self.lang], font=("Bahnschrift", 16))
        textlabel.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        entry = ctk.CTkEntry(window, takefocus=True)
        submitbutton = ctk.CTkButton(window, text="OK", command=submit, width=30, font=("Bahnschrift", 12))
        entry.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        submitbutton.grid(row=3, column=0, sticky="ns", padx=5, pady=5)
        entry.focus()
        window.bind("<Configure>", move)
        window.bind("<Escape>", lambda event: window.destroy())
        window.bind("<Return>", lambda event: submit())