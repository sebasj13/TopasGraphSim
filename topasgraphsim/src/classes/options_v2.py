import customtkinter as ctk
import tkinter.filedialog as fd
from ..resources.language import Text
from ..classes.scrollframe_v2 import ScrollFrame
from tkinter import colorchooser

from ..classes.sim_import import Simulation

class Options(ctk.CTkTabview):
    
    """The options frame of the TGS application.
    """
    
    def __init__(self, parent, index, lang):
        
        self.parent = parent      
        self.index = index
        self.lang = lang  
        super().__init__(self.parent, width=200, border_color="black", border_width=1)
        
        self.newtabname = ""
        
        self.add(Text().data[self.lang])
        self.add(Text().analysis[self.lang])
        self.add(Text().parameters[self.lang])
        self.add(Text().settings[self.lang])
        

        self.tab(Text().data[self.lang]).rowconfigure(0, weight=1)
        self.tab(Text().data[self.lang]).rowconfigure(1, weight=1)  
        self.tab(Text().data[self.lang]).columnconfigure(0, weight=1)     
        self.tab(Text().data[self.lang]).grid_propagate(False)
               
        self.dataframe1 = ctk.CTkFrame(self.tab(Text().data[self.lang]))
        self.dataframe2 = ctk.CTkFrame(self.tab(Text().data[self.lang]), border_color="black", border_width=1)
        self.dataframe1.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.dataframe1.pack_propagate(False)
        self.dataframe2.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.dataframe2.grid_propagate(False)
        self.dataframe2.columnconfigure(0, weight=1)
        self.dataframe2.columnconfigure(1, weight=1)
        
        self.graphlist = ScrollFrame(self.dataframe1)
        self.graphlist.pack(fill="both", expand=True)
    
    
        self.load_topas_button = ctk.CTkButton(self.dataframe2, text = Text().loadsim[self.lang], command = self.load_topas, width=20)
        self.load_topas_button.grid(row=0, column=0, sticky="nsew", pady=5, padx=5)

        self.normalize=ctk.BooleanVar(value=True)
        self.normalization = ctk.StringVar(value=Text().maximum[self.lang])
        self.normalize_button = ctk.CTkCheckBox(self.dataframe2, text=Text().normalize[self.lang], variable=self.normalize, command=self.parent.update, font=("Bahnschrift", 12, "bold"))
        self.normalize_options = ctk.CTkOptionMenu(self.dataframe2, values=[Text().maximum[self.lang], Text().plateau[self.lang], Text().centeraxis[self.lang]], variable=self.normalization, command=self.parent.update)
        self.normalize_button.grid(row=2, column=0, sticky="nsew", pady=5, padx=5)
        self.normalize_options.grid(row=2, column=1, sticky="nsew", pady=5, padx=5)
        
        self.change_name_button = ctk.CTkButton(self.dataframe2, text=Text().edittabname[self.lang], command = self.change_name, width=20)
        self.close_tab_button = ctk.CTkButton(self.dataframe2, text=Text().closetab1[self.lang], command = lambda: self.parent.master.master.remove_tab(self.parent.master.master.tabnames.index(self.parent.name)), width=20, fg_color="red")
        self.close_tab_button.grid(row=4, column=1, sticky="nsew", pady=5, padx=5)
        self.change_name_button.grid(row=4, column=0, sticky="nsew", pady=5, padx=5)
        
        #######################################################################################################################
               
        self.tab(Text().settings[self.lang]).rowconfigure(0, weight=1)
        self.tab(Text().settings[self.lang]).rowconfigure(1, weight=1)  
        self.tab(Text().settings[self.lang]).columnconfigure(0, weight=1)     
        self.tab(Text().settings[self.lang]).grid_propagate(False)  
        
        self.graphsettingsframe = ctk.CTkFrame(self.tab(Text().settings[self.lang]), border_color="black", border_width=1)
        self.graphsettingsframe.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        self.graphsettingsframe.columnconfigure(0, weight=1)
        self.graphsettingsframe.columnconfigure(1, weight=1)
        self.graphsettingsframe.grid_propagate(False)       
        
        self.graphsettingslabel = ctk.CTkLabel(self.graphsettingsframe, text=Text().graphsettings[self.lang], font=("Bahnschrift",16, "bold"))
        self.graphsettingslabel.grid(column=0, row=0, columnspan=2, sticky="nsew", padx=5, pady=(1,5))
        
        self.title = ctk.StringVar()
        self.titleentry = ctk.CTkEntry(self.graphsettingsframe, textvariable=self.title, width=130)
        self.titlebutton = ctk.CTkButton(self.graphsettingsframe, text=Text().renamet[self.lang], command = self.rename_title)
        self.titleentry.grid(column=0, row=1, padx=5, pady=3)
        self.titlebutton.grid(column=1, row=1, padx=5, pady=3)
        
        self.xtitle = ctk.StringVar()
        self.xentry = ctk.CTkEntry(self.graphsettingsframe, textvariable=self.xtitle, width=130)
        self.xbutton = ctk.CTkButton(self.graphsettingsframe, text=Text().renamex[self.lang], command = self.rename_x)
        self.xentry.grid(column=0, row=2, padx=5, pady=3)
        self.xbutton.grid(column=1, row=2, padx=5, pady=3)
        
        self.ytitle = ctk.StringVar()
        self.yentry = ctk.CTkEntry(self.graphsettingsframe, textvariable=self.ytitle, width=130)
        self.ybutton = ctk.CTkButton(self.graphsettingsframe, text=Text().renamey[self.lang], command = self.rename_y)
        self.yentry.grid(column=0, row=3, padx=5, pady=3)
        self.ybutton.grid(column=1, row=3, padx=5, pady=3)
        
        self.showgrid = ctk.BooleanVar(value=False)
        self.gridoptions = ctk.StringVar(value=Text().gridoptions1[self.lang])
        
        self.showgrid_button = ctk.CTkCheckBox(self.graphsettingsframe, text=Text().showgrid[self.lang], variable=self.showgrid, onvalue=True, offvalue=False, command = self.toggle_grid_options, font=("Bahnschrift",12, "bold"))
        self.showgrid_options = ctk.CTkOptionMenu(self.graphsettingsframe, variable=self.gridoptions, values=[Text().gridoptions1[self.lang], Text().gridoptions2[self.lang]], state="disabled", command = lambda x: self.toggle_grid_options())
        
        self.showgrid_button.grid(column=0, row=4, padx=5, pady=3, sticky = "w")
        self.showgrid_options.grid(column=1, row=4, padx=5, pady=3, sticky = "w")   
        
        self.showlegend = ctk.BooleanVar()
        self.legendoptions = ctk.StringVar(value=Text().legendoptions1[self.lang])
        
        self.showlegend_button = ctk.CTkCheckBox(self.graphsettingsframe, text=Text().showlegend[self.lang], variable=self.showlegend, onvalue=True, offvalue=False, command = self.toggle_legend_options, font=("Bahnschrift", 12, "bold"))
        self.showlegend_options = ctk.CTkOptionMenu(self.graphsettingsframe, 
                                                    variable=self.legendoptions, 
                                                    values=[Text().legendoptions1[self.lang], 
                                                            Text().legendoptions2[self.lang], 
                                                            Text().legendoptions3[self.lang],
                                                            Text().legendoptions4[self.lang],
                                                            Text().legendoptions5[self.lang]],
                                                    state="disabled", command = lambda x: self.toggle_legend_options())
        
        self.showlegend_button.grid(column=0, row=5, padx=5, pady=(3,5), sticky="w")
        self.showlegend_options.grid(column=1, row=5, padx=5, pady=(3,5), sticky="w")
        
        self.plotsettingsframe = ctk.CTkFrame(self.tab(Text().settings[self.lang]), border_color="black", border_width=1)
        self.plotsettingsframe.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        self.plotsettingsframe.columnconfigure(0, weight=1)
        self.plotsettingsframe.columnconfigure(1, weight=1)
        self.plotsettingsframe.grid_propagate(False)   
        
        self.plotsettingslabel = ctk.CTkLabel(self.plotsettingsframe, text=Text().plotsettings[self.lang], font=("Bahnschrift",16, "bold"))
        self.plotsettingslabel.grid(column=0, row=0, columnspan=2, sticky="nsew", padx=5, pady=(1,5))
        
        self.current_plot = ctk.IntVar(value=0)
        self.plotselectorlabel = ctk.CTkLabel(self.plotsettingsframe, text=Text().plotselector[self.lang],  font=("Bahnschrift",14, "bold"))
        self.plotselectorlabel.grid(column=0, row=1, padx=5, pady=(3,5), sticky="w")
        self.plotselector = ctk.CTkOptionMenu(self.plotsettingsframe, variable=self.current_plot, values=[])
        self.plotselector.grid(column=1, row=1, padx=5, pady=(3,5), sticky="nsew")
        
        self.plottitle = ctk.StringVar()
        self.plottitleentry = ctk.CTkEntry(self.plotsettingsframe, textvariable=self.plottitle, width=130)
        self.plottitlebutton = ctk.CTkButton(self.plotsettingsframe, text=Text().renameplot[self.lang], command = self.rename_plot)
        self.plottitleentry.grid(column=0, row=2, padx=5, pady=(5,3))
        self.plottitlebutton.grid(column=1, row=2, padx=5, pady=(5,3))
        
        self.linethicknesslabel = ctk.CTkLabel(self.plotsettingsframe, text=Text().linethickness[self.lang], font=("Bahnschrift",12, "bold"))
        self.linethicknesslabel.grid(column=0, row=3, padx=5, pady=3, sticky="w")
        self.linethicknessslider = ctk.CTkSlider(self.plotsettingsframe, from_=0, to=4, orientation="horizontal", number_of_steps=100, width=150, command = self.change_linethickness)
        self.linethicknessslider.grid(column=1, row=3, padx=5, pady=3, sticky="e")
        
        self.linestylelabel = ctk.CTkLabel(self.plotsettingsframe, text=Text().linestyle[self.lang], font=("Bahnschrift",12, "bold"))
        self.linestylelabel.grid(column=0, row=4, padx=5, pady=3, sticky="w")
        self.linestyle = ctk.StringVar(value=Text().dashdot[self.lang])
        self.linestyleselector = ctk.CTkOptionMenu(self.plotsettingsframe, variable=self.linestyle, values=[Text().dashdot[self.lang], Text().dash[self.lang], Text().dot[self.lang]], command = self.change_linestyle)
        self.linestyleselector.grid(column=1, row=4, padx=5, pady=3, sticky="e")
        
        self.plotcolor = ctk.StringVar()
        self.linecolorlabel = ctk.CTkLabel(self.plotsettingsframe, text=Text().linecolor[self.lang], font=("Bahnschrift",12, "bold"))
        self.linecolorbutton = ctk.CTkButton(self.plotsettingsframe, text=Text().change[self.lang], command = self.choose_linecolor)
        self.linecolorlabel.grid(column=0, row=5, padx=5, pady=(3,5), sticky="w")
        self.linecolorbutton.grid(column=1, row=5, padx=5, pady=(3,5), sticky="e")
        
    ######################################################################################################################################################################
    
        self.tab(Text().analysis[self.lang]).rowconfigure(0, weight=1)
        self.tab(Text().analysis[self.lang]).rowconfigure(1, weight=1)  
        self.tab(Text().analysis[self.lang]).columnconfigure(0, weight=1)     
        self.tab(Text().analysis[self.lang]).grid_propagate(False)  
                
        self.shiftframe = ctk.CTkFrame(self.tab(Text().analysis[self.lang]), border_color="black", border_width=1)
        self.shiftframe.columnconfigure(0, weight=1, minsize=130)
        self.shiftframe.columnconfigure(1, weight=1)
        self.shiftframe.grid_propagate(False)  
        
        self.shiftframetitle = ctk.CTkLabel(self.shiftframe, text=Text().shift[self.lang], font=("Bahnschrift",16, "bold"))
        self.shiftframetitle.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=(1,5))
        
        self.plotselectorlabel2 = ctk.CTkLabel(self.shiftframe, text=Text().plotselector[self.lang], font=("Bahnschrift",14, "bold"))
        self.plotselectorlabel2.grid(column=0, row=1, padx=5, pady=(3,5), sticky="w")
        self.plotselector2 = ctk.CTkOptionMenu(self.shiftframe, variable=self.current_plot, values=[])
        self.plotselector2.grid(column=1, row=1, padx=5, pady=(3,5), sticky="nsew")


        self.doseshift = ctk.DoubleVar(value=0.0)
        self.axshift = ctk.DoubleVar(value= 0.0)
        self.dosescale = ctk.DoubleVar(value=1.0)
        
        self.doseshiftlabel = ctk.CTkLabel(self.shiftframe, text=Text().doseshift[self.lang], font=("Bahnschrift",12, "bold"))
        self. axshiftlabel = ctk.CTkLabel(self.shiftframe, text=Text().axshift[self.lang], font=("Bahnschrift",12, "bold"))
        self.doseshiftentry = ctk.CTkEntry(self.shiftframe, textvariable=self.doseshift, width=130)
        self. axshiftentry = ctk.CTkEntry(self.shiftframe, textvariable=self.axshift, width=130)
        self.dosescalelabel = ctk.CTkLabel(self.shiftframe, text=Text().dosescale[self.lang], font=("Bahnschrift",12, "bold"))
        self.dosescaleentry = ctk.CTkEntry(self.shiftframe, textvariable=self.dosescale, width=130)
        
        self.dosescalelabel.grid(column=0, row=2, padx=5, pady=3, sticky="w")
        self.dosescaleentry.grid(column=1, row=2, padx=5, pady=3, sticky="nsew")
        self.doseshiftlabel.grid(column=0, row=3, padx=5, pady=3, sticky="w")
        self.doseshiftentry.grid(column=1, row=3, padx=5, pady=3, sticky="nsew")
        self.axshiftlabel.grid(column=0, row=4, padx=5, pady=3, sticky="w")
        self.axshiftentry.grid(column=1, row=4, padx=5, pady=3, sticky="nsew")
        
        

        self.shiftframe.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        
        self.gammaframe = ctk.CTkFrame(self.tab(Text().analysis[self.lang]), border_color="black", border_width=1)
        self.gammaframe.columnconfigure(0, weight=1, minsize=130)
        self.gammaframe.columnconfigure(1, weight=1)
        self.gammaframe.columnconfigure(2, weight=1)
        self.gammaframe.columnconfigure(3, weight=1)
        self.gammaframe.columnconfigure(4, weight=1)
        self.gammaframe.grid_propagate(False)  
        
        self.gammaframetitle = ctk.CTkLabel(self.gammaframe, text=Text().gamma[self.lang], font=("Bahnschrift",16, "bold"))
        self.gammaframetitle.grid(row=0, column=0, columnspan=5, sticky="nsew", padx=5, pady=(1,5))
        
        self.reference = ctk.IntVar()
        self.referencelabel = ctk.CTkLabel(self.gammaframe, text=Text().reference[self.lang], font=("Bahnschrift",14, "bold"))
        self.referenceselector = ctk.CTkOptionMenu(self.gammaframe, variable=self.reference, values=[])
        self.referencelabel.grid(column=0, row=1, padx=5, pady=(3,5), sticky="w")
        self.referenceselector.grid(column=1, columnspan=4, row=1, padx=5, pady=(3,5), sticky="nsew")
        
        self.test = ctk.IntVar()
        self.testlabel = ctk.CTkLabel(self.gammaframe, text=Text().test[self.lang], font=("Bahnschrift",14, "bold"))
        self.testselector = ctk.CTkOptionMenu(self.gammaframe, variable=self.test, values=[])
        self.testlabel.grid(column=0, row=2, padx=5, pady=(3,5), sticky="w")
        self.testselector.grid(column=1, columnspan=4, row=2, padx=5, pady=(3,5), sticky="nsew")
        
        self.gammatype = ctk.StringVar(value=Text().local[self.lang])
        self.gammatypelabel = ctk.CTkLabel(self.gammaframe, text=Text().gammatype[self.lang], font=("Bahnschrift",12, "bold"))
        self.local = ctk.CTkRadioButton(self.gammaframe, text=Text().local[self.lang], variable=self.gammatype, value=Text().local[self.lang], font=("Bahnschrift",12, "bold"))
        self.globalg = ctk.CTkRadioButton(self.gammaframe, text=Text().globalg[self.lang], variable=self.gammatype, value=Text().globalg[self.lang], font=("Bahnschrift",12, "bold"))
        self.gammatypelabel.grid(column=0, row=3, padx=5, pady=(3,2), sticky="w")
        self.local.grid(column=1, columnspan=2, row=3, padx=5, pady=(2,5), sticky="nsew")
        self.globalg.grid(column=3, columnspan=2,  row=3, padx=5, pady=(2,5), sticky="nsew")
        
        self.percent = ctk.DoubleVar(value=3)
        self.distance = ctk.DoubleVar(value=3)
        self.criterialabel = ctk.CTkLabel(self.gammaframe, text=Text().criterion[self.lang], font=("Bahnschrift",12, "bold"))
        self.percententry = ctk.CTkEntry(self.gammaframe, textvariable=self.percent, width=35)
        self.percentlabel = ctk.CTkLabel(self.gammaframe, text="% ", font=("Bahnschrift",14, "bold"))
        self.distanceentry = ctk.CTkEntry(self.gammaframe, textvariable=self.distance, width=35)
        self.distancelabel = ctk.CTkLabel(self.gammaframe, text="mm", font=("Bahnschrift",14, "bold"))
        self.criterialabel.grid(column=0, row=4, padx=5, pady=(3,5), sticky="w")
        self.percententry.grid(column=1, row=4, padx=5, pady=(3,5), sticky="e")
        self.percentlabel.grid(column=2, row=4, padx=5, pady=(3,5), sticky="w")
        self.distanceentry.grid(column=3, row=4, padx=5, pady=(3,5), sticky="e")
        self.distancelabel.grid(column=4, row=4, padx=5, pady=(3,5), sticky="w")
        
        self.calc_gamma_button = ctk.CTkButton(self.gammaframe, text=Text().calculate[self.lang], command=self.calculate_gamma, font=("Bahnschrift",14, "bold"), fg_color="green")
        self.calc_gamma_button.grid(column=0, row=5, padx=5, pady=(3,5), sticky="nsew")
        
        self.resultcanvas = ctk.CTkLabel(self.gammaframe, fg_color="white", text="", corner_radius=10, font=("Bahnschrift",14, "bold"))
        self.resultcanvas.grid(column=1, columnspan=4, row=5, padx=5, pady=(3,5), sticky="nsew")
        
        
        self.gammaframe.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
    
    ######################################################################################################################################################################

        
    def calculate_gamma(self):
        percent = self.percent.get()
        distance = self.distance.get()
        print(percent,"%, ", distance, "mm")
        
        
    def choose_linecolor(self):
        color = colorchooser.askcolor()
        self.plotcolor.set(color[1])
        print(color)
        self.linecolorbutton.configure(fg_color = color[1])
        current_plot = self.current_plot.get()
        self.parent.update()
        
    def rename_plot(self):
        new_name = self.plottitleentry.get()
        print(new_name)
        current_plot = self.current_plot.get()
        self.parent.update()    
        
    def change_linestyle(self, value):
        print(value)
        current_plot = self.current_plot.get()
        self.parent.update()
        
    def change_linethickness(self, value):
        print(value)
        current_plot = self.current_plot.get()
        self.parent.update()
        
        
    def rename_title(self):
        self.parent.ax.set_title(self.title.get())
        self.parent.update()
        
    def rename_x(self):
        self.parent.ax.set_xlabel(self.xtitle.get())
        self.parent.update()
        
    def rename_y(self):
        self.parent.ax.set_ylabel(self.ytitle.get())
        self.parent.update()
        
    def toggle_legend_options(self):
        if self.showlegend.get():
            self.showlegend_options.configure(state="normal")
            which = {Text().legendoptions1[self.lang]:"best", 
                     Text().legendoptions2[self.lang]:"upper left",
                     Text().legendoptions3[self.lang]:"upper right",
                     Text().legendoptions4[self.lang]:"lower left",
                     Text().legendoptions5[self.lang]:"lower right"}.get(self.legendoptions.get())
            self.parent.ax.legend(loc=which)
            self.parent.update()
        else:
            self.showlegend_options.configure(state="disabled")
            try: self.parent.ax.get_legend().remove()
            except AttributeError: pass
            self.parent.update()
            
        
        
        
    def toggle_grid_options(self):
        if self.showgrid.get():
            self.showgrid_options.configure(state="normal")
            which = {Text().gridoptions1[self.lang]:"major", Text().gridoptions2[self.lang]:"both"}.get(self.gridoptions.get())
            self.parent.ax.grid(False, which = "both", axis="both")
            self.parent.ax.grid(which="major", visible=True, axis="both", lw=1)
            if which == "both":
                self.parent.ax.grid(which="minor", visible=True, axis="both", lw=0.5)
            self.parent.update()
        else:
            self.showgrid_options.configure(state="disabled")
            self.parent.ax.grid(False, which = "both", axis="both")
            self.parent.update()
        
    def load_topas(self):
        path = fd.askopenfilename(filetypes=[("TOPAS files", "*.csv")])
        
        if path != "":
            sim = Simulation(path)
            
            self.parent.ax.plot(sim.axis, sim.dose)
            self.parent.canvas.draw()
            
    def change_name(self):
        
        
        """Add a tab to the tabview.
        """
        root = self.parent.master.master.parent        
        window = ctk.CTkToplevel(root)
        window.wm_attributes("-toolwindow", True)
        window.geometry(f"180x120+{root.winfo_rootx()+root.winfo_width()//2-90}+{root.winfo_rooty()+root.winfo_height()//2-60}")
        window.title("")
        
        def move(event):
            window.lift()
            entry.focus()
            window.geometry(f"180x120+{root.winfo_rootx()+root.winfo_width()//2-90}+{root.winfo_rooty()+root.winfo_height()//2-60}")
        
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
        
        textlabel = ctk.CTkLabel(window, text=Text().newtabname[self.lang], font=("Bahnschrift", 16))
        textlabel.pack(padx=5, pady=5, fill="x", expand=True)
        entry = ctk.CTkEntry(window, takefocus=True)
        submitbutton = ctk.CTkButton(window, text="OK", command=submit, width=30, font=("Bahnschrift", 12))
        entry.pack(fill="x", expand=True, padx=5, pady=5)
        submitbutton.pack(padx=5, pady=5)
        entry.focus()
        window.bind("<Configure>", move)
        window.bind("<Escape>", lambda event: window.destroy())
        window.bind("<Return>", lambda event: submit())