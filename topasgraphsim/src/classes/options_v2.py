import customtkinter as ctk
import tkinter.filedialog as fd
from ..resources.language import Text
from ..classes.scrollframe_v2 import ScrollFrame

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
        self.add(Text().settings[self.lang])
        self.add(Text().analysis[self.lang])

        self.tab(Text().data[self.lang]).rowconfigure(0, weight=1)
        self.tab(Text().data[self.lang]).rowconfigure(1, weight=1)  
        self.tab(Text().data[self.lang]).columnconfigure(0, weight=1)     
        self.tab(Text().data[self.lang]).grid_propagate(False)
        
        self.tab(Text().settings[self.lang]).columnconfigure(0, weight=1)
        self.tab(Text().settings[self.lang]).columnconfigure(1, weight=1)
        self.tab(Text().settings[self.lang]).grid_propagate(False)
        
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
        self.change_name_button = ctk.CTkButton(self.dataframe2, text=Text().edittabname[self.lang], command = self.change_name, width=20)
        self.close_tab_button = ctk.CTkButton(self.dataframe2, text=Text().closetab1[self.lang], command = lambda: self.parent.master.master.remove_tab(self.parent.master.master.tabnames.index(self.parent.name)), width=20, fg_color="red")
        self.close_tab_button.grid(row=1, column=1, sticky="nsew", pady=5, padx=5)
        self.change_name_button.grid(row=1, column=0, sticky="nsew", pady=5, padx=5)
        
        
        #######################################################################################################################
               
        self.title = ctk.StringVar()
        self.titleentry = ctk.CTkEntry(self.tab(Text().settings[self.lang]), textvariable=self.title, width=130)
        self.titlebutton = ctk.CTkButton(self.tab(Text().settings[self.lang]), text=Text().renamet[self.lang], command = self.rename_title)
        self.titleentry.grid(column=0, row=0, padx=5, pady=5)
        self.titlebutton.grid(column=1, row=0, padx=5, pady=5)
        
        self.xtitle = ctk.StringVar()
        self.xentry = ctk.CTkEntry(self.tab(Text().settings[self.lang]), textvariable=self.xtitle, width=130)
        self.xbutton = ctk.CTkButton(self.tab(Text().settings[self.lang]), text=Text().renamex[self.lang], command = self.rename_x)
        self.xentry.grid(column=0, row=1, padx=5, pady=5)
        self.xbutton.grid(column=1, row=1, padx=5, pady=5)
        
        self.ytitle = ctk.StringVar()
        self.yentry = ctk.CTkEntry(self.tab(Text().settings[self.lang]), textvariable=self.ytitle, width=130)
        self.ybutton = ctk.CTkButton(self.tab(Text().settings[self.lang]), text=Text().renamey[self.lang], command = self.rename_y)
        self.yentry.grid(column=0, row=2, padx=5, pady=5)
        self.ybutton.grid(column=1, row=2, padx=5, pady=5)
        
        self.showgrid = ctk.BooleanVar(value=False)
        self.gridoptions = ctk.StringVar(value=Text().gridoptions1[self.lang])
        
        self.showgrid_button = ctk.CTkCheckBox(self.tab(Text().settings[self.lang]), text=Text().showgrid[self.lang], variable=self.showgrid, onvalue=True, offvalue=False, command = self.toggle_grid_options)
        self.showgrid_options = ctk.CTkOptionMenu(self.tab(Text().settings[self.lang]), variable=self.gridoptions, values=[Text().gridoptions1[self.lang], Text().gridoptions2[self.lang]], state="disabled", command = lambda x: self.toggle_grid_options())
        
        self.showgrid_button.grid(column=0, row=3, padx=5, pady=5, sticky = "w")
        self.showgrid_options.grid(column=1, row=3, padx=5, pady=5, sticky = "w")   
        
        self.showlegend = ctk.BooleanVar()
        self.legendoptions = ctk.StringVar(value=Text().legendoptions1[self.lang])
        
        self.showlegend_button = ctk.CTkCheckBox(self.tab(Text().settings[self.lang]), text=Text().showlegend[self.lang], variable=self.showlegend, onvalue=True, offvalue=False, command = self.toggle_legend_options)
        self.showlegend_options = ctk.CTkOptionMenu(self.tab(Text().settings[self.lang]), 
                                                    variable=self.legendoptions, 
                                                    values=[Text().legendoptions1[self.lang], 
                                                            Text().legendoptions2[self.lang], 
                                                            Text().legendoptions3[self.lang],
                                                            Text().legendoptions4[self.lang],
                                                            Text().legendoptions5[self.lang]],
                                                    state="disabled", command = lambda x: self.toggle_legend_options())
        
        self.showlegend_button.grid(column=0, row=4, padx=5, pady=5, sticky="w")
        self.showlegend_options.grid(column=1, row=4, padx=5, pady=5, sticky="w")
        
        
        
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