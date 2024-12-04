import os
import sys
from PIL import Image
import customtkinter as ctk

from .tab import Tab
from .settings import Settings
from ..resources.language import Text


class TabView(ctk.CTkTabview):
    
    """The tabview of the TGS application.
    """
    
    def __init__(self, parent):
        
        self.parent = parent
        super().__init__(self.parent, border_color="black", border_width=1)
        self.pack_propagate(False)
        self.grid_propagate(False)
        
        self.lang = self.parent.parent.lang.get()
        
        self.tabnames = []
        self.newtabname = ""
        
        def resource_path(relative_path):
            """ Get absolute path to resource, works for dev and for PyInstaller """
            if hasattr(sys, '_MEIPASS'):
                return os.path.join(sys._MEIPASS, "TopasGraphSim", relative_path)

            return os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir, os.pardir, relative_path)
        
        size = self.parent.winfo_screenwidth()//8
        self.logo = ctk.CTkImage(
            Image.open(
                resource_path(os.path.join(
                    "topasgraphsim",
                    "src",
                    "resources",
                    "images",
                    "icon.png",
                            ))
                     ).resize((size, size), Image.LANCZOS), size=(size, size)
                                )
        
        self.logolabel = ctk.CTkLabel(self, text=Text().help[self.lang], image = self.logo, font=("Bahnschrift", 30), compound="top")
        self.logolabel.place(relx=0.5, rely=0.5, anchor="center")
        
    def add_tab(self, name = None):
        """Add a tab to the tabview.
        """
        if name != None:
            if type(name) == str:
                tab = name
            else:
                tab = Text().untitled[self.lang]
            self.newtabname = ""
            self.add(tab)
            self.tabnames.append(tab)
            tab = Tab(self.tab(tab), tab, len(self.tabnames)-1, self.lang)
            setattr(self.tab(tab.name), "tab", tab)
            self.parent.parent.set_theme()
            tab.pack(fill="both", expand=True)
            tab.grid_propagate(False)
            tab.pack_propagate(False)

            self.parent.parent.menubar.tabmenu.add_command(label=Text().closetab[self.lang].format(tab.name), command=lambda: self.remove_tab(self.tabnames.index(tab.name)))
            self.set(self.tabnames[-1])
            
            if len (self.tabnames) == 1:
                self.logolabel.place_forget()
                
        else:       
            window = ctk.CTkToplevel(self.parent.parent)
            window.overrideredirect(True)
            window.title("")
            
            def move(event):
                window.lift()
                entry.focus()
                window.geometry(f"150x142+{self.parent.parent.winfo_rootx()+self.parent.parent.winfo_width()//2-75}+{self.parent.parent.winfo_rooty()+self.parent.parent.winfo_height()//2-71}")
            
            def submit():
                self.newtabname = entry.get()
                window.destroy()
                if self.newtabname == "" or self.newtabname in self.tabnames:
                    return

                tab = self.newtabname
                self.newtabname = ""
                self.add(tab)
                self.tabnames.append(tab)
                tab = Tab(self.tab(tab), tab, len(self.tabnames)-1, self.lang)
                setattr(self.tab(tab.name), "tab", tab)
                self.parent.parent.set_theme()
                tab.pack(fill="both", expand=True)

                self.parent.parent.menubar.tabmenu.add_command(label=Text().closetab[self.lang].format(tab.name), command=lambda: self.remove_tab(self.tabnames.index(tab.name)))
                self.set(self.tabnames[-1])
                
                if len (self.tabnames) == 1:
                    self.logolabel.place_forget()
                    
            def close():
                window.destroy()
            
            self.columnconfigure(0, weight=1)
            self.closebutton = ctk.CTkButton(window, text=" X ", command=close, width=2, height=1, font=("Bahnschrift", 12))
            self.closebutton.grid(row=0, column=0, sticky="ne", padx=(0, 4), pady=(4, 4))
            textlabel = ctk.CTkLabel(window, text=Text().newtabname[self.lang], font=("Bahnschrift", 16))
            textlabel.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
            entry = ctk.CTkEntry(window, takefocus=True)
            submitbutton = ctk.CTkButton(window, text="OK", command=submit, font=("Bahnschrift", 12), width=30)
            entry.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
            submitbutton.grid(row=3, column=0, sticky="ns", padx=5, pady=5)
            entry.focus()
            window.bind("<Configure>", move)
            window.bind("<Escape>", lambda event: window.destroy())
            window.bind("<Return>", lambda event: submit())
    
    def remove_tab(self, index):
        """Remove a tab from the tabview.
        """
        
        if self.tab(self.tabnames[index]).tab.saved == False:
            
            self.parent.parent.bell()
            window = ctk.CTkToplevel(self.parent.parent)
            window.wm_attributes("-toolwindow", True)
            window.title("")
            
            def move(event):
                window.lift()
                window.geometry(f"200x100+{self.parent.parent.winfo_rootx()+self.parent.parent.winfo_width()//2-100}+{self.parent.parent.winfo_rooty()+self.parent.parent.winfo_height()//2-50}")
            
            def submit():
                window.destroy()
                self.delete(self.tabnames[index])
                self.tabnames.pop(index)
                if len(self.tabnames) == 0:
                    self.logolabel.place(relx=0.5, rely=0.5, anchor="center")
                self.parent.parent.menubar.tabmenu.delete(index+2)
            
            def cancel():
                window.destroy()
            
            window.rowconfigure(0, weight=1)
            window.columnconfigure(0, weight=1)
            window.columnconfigure(1, weight=1)
            textlabel = ctk.CTkLabel(window, text=Text().unsavedchanges[self.lang], font=("Bahnschrift", 16))
            submitbutton = ctk.CTkButton(window, text=Text().yes[self.lang], command=submit, width=40, font=("Bahnschrift", 12))
            cancelbutton = ctk.CTkButton(window, text=Text().no[self.lang], command=cancel, width = 40, font=("Bahnschrift", 12))
            textlabel.grid(row=0, columnspan=2, padx=5, pady=5, sticky="nsew")
            submitbutton.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
            cancelbutton.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
            window.bind("<Configure>", move)
            window.bind("<Escape>", lambda event: window.destroy())
            window.bind("<Return>", lambda event: submit())
        
        else:
            self.delete(self.tabnames[index])
            self.tabnames.pop(index)
            if len(self.tabnames) == 0:
                self.logolabel.place(relx=0.5, rely=0.5, anchor="center")
            self.parent.parent.menubar.tabmenu.delete(index+2)
            
    def add_settings(self):
        
        tabname = Text().settings[self.lang]
        self.add(tabname)
        self.tabnames.append(tabname)
        tab = Settings(self.tab(tabname), tabname, len(self.tabnames)-1, self.lang)
        setattr(self.tab(tabname), "tab", tab)
        self.parent.parent.set_theme()
        tab.pack(fill="both", expand=True)

        self.parent.parent.menubar.tabmenu.add_command(label=Text().closetab[self.lang].format(tab.name), command=lambda: self.remove_tab(self.tabnames.index(tab.name)))
        self.set(self.tabnames[-1])
        
        if len (self.tabnames) == 1:
            self.logolabel.place_forget()