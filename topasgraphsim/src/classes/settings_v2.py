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
        self.p = ProfileHandler()
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
        
        #############################
        
        self.generalframe.columnconfigure(0, weight=1)
        self.generalframe.columnconfigure(1, weight=1)
        
        self.generallabel = ctk.CTkLabel(self.generalframe, text=Text().generalsettings[self.lang], font=("Bahnschrift", 24))
        self.generallabel.grid(row=0, column=0, columnspan=2, pady=5, sticky="nsew", padx=5)
               
        self.defaulttitle = ctk.StringVar(value=self.p.get_attribute("graphtitle"))
        self.defaulttitlelabel = ctk.CTkLabel(self.generalframe, text=Text().defaulttitlelabel[self.lang], font=("Bahnschrift", 16))
        self.defaulttitleentry = ctk.CTkEntry(self.generalframe, textvariable=self.defaulttitle)
        self.defaulttitlelabel.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.defaulttitleentry.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        
        self.defaulxaxis = ctk.StringVar(value=self.p.get_attribute("xaxislabel") )
        self.defaulxaxislabel = ctk.CTkLabel(self.generalframe, text=Text().defaultxaxislabel[self.lang], font=("Bahnschrift", 16))
        self.defaulxaxisentry = ctk.CTkEntry(self.generalframe, textvariable=self.defaulxaxis)
        self.defaulxaxislabel.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.defaulxaxisentry.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
        
        self.defaulyaxis = ctk.StringVar(value=self.p.get_attribute("yaxislabel") )
        self.defaulyaxislabel = ctk.CTkLabel(self.generalframe, text=Text().defaultyaxislabel[self.lang], font=("Bahnschrift", 16))
        self.defaulyaxisentry = ctk.CTkEntry(self.generalframe, textvariable=self.defaulyaxis)
        self.defaulyaxislabel.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.defaulyaxisentry.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")
        
        self.normalize = ctk.BooleanVar(value=ProfileHandler().get_attribute("normalize"))
        self.normalizebutton = ctk.CTkCheckBox(self.generalframe, text=Text().normalize[self.lang], variable=self.normalize, font=("Bahnschrift", 16))
        normtypedict = {"maximum":Text().maximum[self.lang], "plateau":Text().plateau[self.lang], "centeraxis":Text().centeraxis[self.lang]}
        self.normtype = ctk.StringVar(value=normtypedict[ProfileHandler().get_attribute("normtype")])
        self.normalize_options = ctk.CTkOptionMenu(self.generalframe, values=[Text().maximum[self.lang], Text().plateau[self.lang], Text().centeraxis[self.lang]], variable=self.normtype)
        self.normalizebutton.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.normalize_options.grid(row=4, column=1, padx=5, pady=5)
        
        self.show_points = ctk.BooleanVar(value=ProfileHandler().get_attribute("show_points"))
        self.pointsbutton = ctk.CTkCheckBox(self.generalframe, text=Text().showpoints[self.lang], variable=self.show_points, font=("Bahnschrift", 16))
        self.pointsbutton.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        
        self.showgrid = ctk.BooleanVar(value=ProfileHandler().get_attribute("grid"))
        self.gridbutton = ctk.CTkCheckBox(self.generalframe, text=Text().showgrid[self.lang], variable=self.showgrid, font=("Bahnschrift", 16))
        self.gridbutton.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        
        self.showlegend = ctk.BooleanVar(value=ProfileHandler().get_attribute("legend"))
        self.legendbutton = ctk.CTkCheckBox(self.generalframe, text=Text().showlegend[self.lang], variable=self.showlegend, font=("Bahnschrift", 16))
        self.legendbutton.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        
        ############################
        
        self.plotframe.columnconfigure(0, weight=1, minsize=130)
        self.plotframe.columnconfigure(1, weight=1)
        self.plotframe.grid_propagate(False) 
        
        self.plotlabel = ctk.CTkLabel(self.plotframe, text=Text().plotsettings[self.lang], font=("Bahnschrift", 24))
        self.plotlabel.grid(pady=5, columnspan=2, row=0, sticky="nsew", padx=5)
        
        self.doseshift = ctk.StringVar(value="0")
        self.axshift = ctk.StringVar(value= "0")
        self.dosescale = ctk.StringVar(value="1")
        self.flip = ctk.BooleanVar(value=False)
        
        self.linethicknesslabel = ctk.CTkLabel(self.plotframe, text=Text().linethickness[self.lang], font=("Bahnschrift",16))
        self.linethicknesslabel.grid(column=0, row=1, padx=5, pady=5, sticky="w")
        self.linethickness = ctk.DoubleVar(value = self.p.get_attribute("linethickness"))
        self.linethicknessslider = ctk.CTkSlider(self.plotframe, from_=0, to=4, orientation="horizontal", number_of_steps=100, width=150, variable=self.linethickness)
        self.linethicknessslider.grid(column=1, row=1, padx=5, pady=5, sticky="ew")
        
        self.linestylelabel = ctk.CTkLabel(self.plotframe, text=Text().linestyle[self.lang], font=("Bahnschrift",16))
        self.linestylelabel.grid(column=0, row=2, padx=5, pady=5, sticky="w")
        self.linestyledict = {"-.":Text().dashdot[self.lang], "-":Text().dash[self.lang], "dotted":Text().dot[self.lang], " ":Text().none[self.lang]}
        self.linestyle = ctk.StringVar(value = self.linestyledict[self.p.get_attribute("linestyle")])
        self.linestyleselector = ctk.CTkOptionMenu(self.plotframe, variable=self.linestyle, values=[Text().dashdot[self.lang], Text().dash[self.lang], Text().dot[self.lang], Text().none[self.lang]])
        self.linestyleselector.grid(column=1, row=2, padx=5, pady=5, sticky="ew")
        
        self.dosescale = ctk.StringVar(value=self.p.get_attribute("dosefactor"))
        self.dosescalelabel = ctk.CTkLabel(self.plotframe, text=Text().dosescale[self.lang], font=("Bahnschrift",16))
        self.dosescaleentry = ctk.CTkEntry(self.plotframe, textvariable=self.dosescale, width=130)
        self.doseshift = ctk.StringVar(value=self.p.get_attribute("doseoffset"))
        self.doseshiftlabel = ctk.CTkLabel(self.plotframe, text=Text().doseshift[self.lang], font=("Bahnschrift",16))
        self.axshiftlabel = ctk.CTkLabel(self.plotframe, text=Text().axshift[self.lang], font=("Bahnschrift",16))
        self.doseshiftentry = ctk.CTkEntry(self.plotframe, textvariable=self.doseshift, width=130)    
        self.axshift = ctk.StringVar(value=self.p.get_attribute("axshift"))       
        self.axshiftentry = ctk.CTkEntry(self.plotframe, textvariable=self.axshift, width=130)
        self.flipbutton = ctk.CTkCheckBox(self.plotframe, variable=self.flip, text=Text().flip[self.lang], font=("Bahnschrift",16))
        
        self.dosescalelabel.grid(column=0, row=3, padx=5, pady=5, sticky="w")
        self.dosescaleentry.grid(column=1, row=3, padx=5, pady=5, sticky="nsew")
        self.doseshiftlabel.grid(column=0, row=4, padx=5, pady=5, sticky="w")
        self.doseshiftentry.grid(column=1, row=4, padx=5, pady=5, sticky="nsew")
        self.axshiftlabel.grid(column=0, row=5, padx=5, pady=5, sticky="w")
        self.axshiftentry.grid(column=1, row=5, padx=5, pady=5, sticky="nsew")
        self.flipbutton.grid(column=0, row=6, columnspan=2, padx=5, pady=5, sticky="nsew")
        
        
        ############################
        
        self.gammalabel = ctk.CTkLabel(self.gammaframe, text=Text().gammasettings[self.lang], font=("Bahnschrift", 24))
        self.gammalabel.grid(columnspan=5, pady = 5, sticky="nsew", padx=5)
        self.gammaframe.columnconfigure(0, weight=1, minsize=115)
        self.gammaframe.columnconfigure(1, weight=1)
        self.gammaframe.columnconfigure(2, weight=1)
        self.gammaframe.columnconfigure(3, weight=1)
        self.gammaframe.columnconfigure(4, weight=1)
        
        self.gammatype = ctk.BooleanVar(value=self.p.get_attribute("gammatype"))
        self.gammatypelabel = ctk.CTkLabel(self.gammaframe, text=Text().gammatype[self.lang], font=("Bahnschrift",16))
        self.local = ctk.CTkRadioButton(self.gammaframe, text=Text().local[self.lang], variable=self.gammatype, value=True, font=("Bahnschrift",16,))
        self.globalg = ctk.CTkRadioButton(self.gammaframe, text=Text().globalg[self.lang], variable=self.gammatype, value=False, font=("Bahnschrift",16))
        self.gammatypelabel.grid(column=0, row=3, padx=5, pady=(3,2), sticky="w")
        self.local.grid(column=1, columnspan=2, row=3, padx=5, pady=(2,5), sticky="nsew")
        self.globalg.grid(column=3, columnspan=2,  row=3, padx=5, pady=(2,5), sticky="nsew")
        
        self.percent = ctk.StringVar(value=self.p.get_attribute("dd"))
        self.distance = ctk.StringVar(value=self.p.get_attribute("dta"))
        self.criterialabel = ctk.CTkLabel(self.gammaframe, text=Text().criterion[self.lang], font=("Bahnschrift",16))
        self.percententry = ctk.CTkEntry(self.gammaframe, textvariable=self.percent)
        self.percentlabel = ctk.CTkLabel(self.gammaframe, text="% ", font=("Bahnschrift",16))
        self.distanceentry = ctk.CTkEntry(self.gammaframe, textvariable=self.distance)
        self.distancelabel = ctk.CTkLabel(self.gammaframe, text="mm", font=("Bahnschrift",16))
        self.criterialabel.grid(column=0, row=4, padx=5, pady=5, sticky="w")
        self.percententry.grid(column=1, row=4, padx=5, pady=5, sticky="e")
        self.percentlabel.grid(column=2, row=4, padx=5, pady=5, sticky="w")
        self.distanceentry.grid(column=3, row=4, padx=5, pady=5, sticky="e")
        self.distancelabel.grid(column=4, row=4, padx=5, pady=5, sticky="w")
        
        ############################
        
        self.settingslabel.grid(row=0, columnspan=3, padx=5, pady=5, sticky="nsew")
        self.generalframe.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.plotframe.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        self.gammaframe.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")
        self.closetabbutton.grid(row=2, column=2, padx=5, pady=5, sticky="nsew")
        self.revertbutton.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
        self.savebutton.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
        
    def save(self):
        
        self.parent.master.master.bell()
        self.p.set_attribute("graphtitle", self.defaulttitle.get())
        self.p.set_attribute("xaxislabel", self.defaulxaxis.get())
        self.p.set_attribute("yaxislabel", self.defaulyaxis.get())
        self.p.set_attribute("normalize"    , self.normalize.get())
        self.p.set_attribute("show_points"   , self.show_points.get())
        normtypedict = {Text().maximum[self.lang]:"maximum", Text().plateau[self.lang]:"plateau", Text().centeraxis[self.lang]:"centeraxis"}
        self.p.set_attribute("normtype", normtypedict[self.normtype.get()])
        self.p.set_attribute("legend"   , self.showlegend.get())
        self.p.set_attribute("grid"     , self.showgrid.get())
        
        try: self.p.set_attribute("linethickness", round(float(self.linethickness.get()),2))
        except ValueError: pass
        linestyledict = {Text().dashdot[self.lang]:"-.", Text().dash[self.lang]:"-", Text().dot[self.lang]:"dotted", Text().none[self.lang]:" "}
        self.p.set_attribute("linestyle", linestyledict[self.linestyle.get()])
        try: self.p.set_attribute("dosefactor", float(self.dosescale.get()))
        except ValueError: pass
        try: self.p.set_attribute("doseoffset", float(self.doseshift.get()))
        except ValueError: pass
        try: self.p.set_attribute("axshift", float(self.axshift.get()))
        except ValueError: pass
        self.p.set_attribute("flip", self.flip.get())
        
        self.p.set_attribute("gammatype", self.gammatype.get())
        self.p.set_attribute("dd", self.percent.get())
        self.p.set_attribute("dta", self.distance.get())
        
        self.saved = True

    def reset(self):
        
        self.defaulttitle.set(self.p.get_attribute("graphtitle"))
        self.defaulxaxis.set(self.p.get_attribute("xaxislabel"))
        self.defaulyaxis.set(self.p.get_attribute("yaxislabel"))
        self.normalize.set(self.p.get_attribute("normalize"))
        self.show_points.set(self.p.get_attribute("show_points"))
        normtypedict = {"maximum":Text().maximum[self.lang], "plateau":Text().plateau[self.lang], "centeraxis":Text().centeraxis[self.lang]}
        self.normtype.set(normtypedict[self.p.get_attribute("normtype")])
        self.showgrid.set(self.p.get_attribute("grid"))
        self.showlegend.set(self.p.get_attribute("legend"))
        
        self.linethickness.set(self.p.get_attribute("linethickness"))
        linestyledict = {"-.":Text().dashdot[self.lang], "-":Text().dash[self.lang], "dotted":Text().dot[self.lang], " ":Text().none[self.lang]}
        self.linestyle.set(linestyledict[self.p.get_attribute("linestyle")])
        self.dosescale.set(self.p.get_attribute("dosefactor"))
        self.doseshift.set(self.p.get_attribute("doseoffset"))
        self.axshift.set(self.p.get_attribute("axshift"))
        self.flip.set(self.p.get_attribute("flip"))
        
        self.gammatype.set(self.p.get_attribute("gammatype"))
        self.percent.set(self.p.get_attribute("dd"))
        self.distance.set(self.p.get_attribute("dta"))
        self.saved = True
    
    def close(self):
        self.parent.master.remove_tab(self.index)
        