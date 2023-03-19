import customtkinter as ctk
from ..resources.language import Text

class Parameters(ctk.CTkFrame):
    
    def __init__(self, parent, tgs_graph, lang):
        
        self.parent = parent
        self.graph = tgs_graph
        self.lang = lang
        self.text = Text()
        self.font = ("Bahnschrift", 12)
        super().__init__(self.parent, border_color="black", border_width=1)
        
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight=2)
        
        try: self.parameters = self.graph.dataObject.params()
        except Exception:
            pass
        
        self.namelabel = ctk.CTkLabel(self, text=self.graph.label, font=("Bahnschrift", 14, "bold"), fg_color=self.graph.linecolor)
        
        if self.graph.direction == "Z":
            self.beamqualitylabel = ctk.CTkLabel(self, text=self.text.beamquality[self.lang], font=self.font, height=14)
            self.zmaxlabel = ctk.CTkLabel(self, text=self.text.zmax[self.lang], font=self.font, height=14)
            
            self.beamquality = ctk.CTkLabel(self, text=str(self.parameters[0]) + " ± " + str(self.parameters[1]), font=self.font, height=14)
            self.zmax = ctk.CTkLabel(self, text= str(self.parameters[2]), font=self.font, height=14)
        
            self.namelabel.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=2, pady=2)
            self.beamqualitylabel.grid(row=1, column=0, sticky="w", padx=2, pady=2)
            self.zmaxlabel.grid(row=2, column=0, sticky="w", padx=2, pady=2)
            
            self.beamquality.grid(row=1, column=1, sticky="nsew", padx=2, pady=2)
            self.zmax.grid(row=2, column=1, sticky="nsew", padx=2, pady=2)
        
        else:
            self.halfwidthlabel = ctk.CTkLabel(self, text=self.text.fwhm[self.lang], font=self.font, height=14)
            self.caxlabel = ctk.CTkLabel(self, text=self.text.cax[self.lang], font = self.font, height=14)
            self.flatklabel = ctk.CTkLabel(self, text=self.text.flatkrieger[self.lang], font = self.font, height=14)
            self.flatslabel = ctk.CTkLabel(self, text=self.text.flatstddev[self.lang], font = self.font, height=14)
            self.symmetrylabel = ctk.CTkLabel(self, text = self.text.symmetry[self.lang], font = self.font, height=14)
            self.lpenumbralabel = ctk.CTkLabel(self, text= self.text.leftpenumbra[self.lang], font=self.font, height=14)
            self.rpenumbralabel = ctk.CTkLabel(self, text= self.text.rightpenumbra[self.lang], font=self.font, height=14)
            self.lintegrallabel = ctk.CTkLabel(self, text= self.text.leftintegral[self.lang], font=self.font, height=14)
            self.rintegrallabel = ctk.CTkLabel(self, text= self.text.rightintegral[self.lang], font=self.font, height=14)
            
            self.halfwidth = ctk.CTkLabel(self, text=str(self.parameters[0]), font=self.font, height=14)
            self.cax = ctk.CTkLabel(self, text=str(self.parameters[1]), font=self.font, height=14)
            self.flatk = ctk.CTkLabel(self, text=str(self.parameters[2]), font=self.font, height=14)
            self.flats = ctk.CTkLabel(self, text=str(self.parameters[3]), font=self.font, height=14)
            self.symmetry = ctk.CTkLabel(self, text=str(self.parameters[4]), font=self.font, height=14)
            self.lpenumbra = ctk.CTkLabel(self, text=str(self.parameters[5]), font=self.font, height=14)
            self.rpenumbra = ctk.CTkLabel(self, text=str(self.parameters[6]), font=self.font, height=14)
            self.lintegral = ctk.CTkLabel(self, text=str(self.parameters[7]), font=self.font, height=14)
            self.rintegral = ctk.CTkLabel(self, text=str(self.parameters[8]), font=self.font, height=14)
            
            self.namelabel.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=2, pady=2)
            self.halfwidthlabel.grid(row=1, column=0, sticky="w", padx=2, pady=2)
            self.caxlabel.grid(row=2, column=0, sticky="w", padx=2, pady=2)
            self.flatklabel.grid(row=3, column=0, sticky="w", padx=2, pady=2)
            self.flatslabel.grid(row=4, column=0, sticky="w", padx=2, pady=2)
            self.symmetrylabel.grid(row=5, column=0, sticky="w", padx=2, pady=2)
            self.lpenumbralabel.grid(row=6, column=0, sticky="w", padx=2, pady=2)
            self.rpenumbralabel.grid(row=7, column=0, sticky="w", padx=2, pady=2)
            self.lintegrallabel.grid(row=8, column=0, sticky="w", padx=2, pady=2)
            self.rintegrallabel.grid(row=9, column=0, sticky="w", padx=2, pady=2)
            
            self.halfwidth.grid(row=1, column=1, sticky="nsew", padx=2, pady=2)
            self.cax.grid(row=2, column=1, sticky="nsew", padx=2, pady=2)
            self.flatk.grid(row=3, column=1, sticky="nsew", padx=2, pady=2)
            self.flats.grid(row=4, column=1, sticky="nsew", padx=2, pady=2)
            self.symmetry.grid(row=5, column=1, sticky="nsew", padx=2, pady=2)
            self.lpenumbra.grid(row=6, column=1, sticky="nsew", padx=2, pady=2)
            self.rpenumbra.grid(row=7, column=1, sticky="nsew", padx=2, pady=2)
            self.lintegral.grid(row=8, column=1, sticky="nsew", padx=2, pady=2)
            self.rintegral.grid(row=9, column=1, sticky="nsew", padx=2, pady=2)
            
                
        """
        HWB,
        CAXdev,
        flat_krieger,
        flat_stddev,
        S,
        Lpenumbra,
        Rpenumbra,
        Lintegral,
        Rintegral,
        """
            