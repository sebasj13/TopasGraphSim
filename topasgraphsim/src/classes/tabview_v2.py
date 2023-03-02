import os
from PIL import Image
import customtkinter as ctk

from .tab_v2 import Tab
from ..resources.language import Text


class TabView(ctk.CTkTabview):
    
    """The tabview of the TGS application.
    """
    
    def __init__(self, parent):
        
        self.parent = parent
        super().__init__(self.parent, border_color="black", border_width=1, )
        self.pack_propagate(False)
        
        self.lang = self.parent.parent.lang.get()
        
        self.tabnames = []
        self.newtabname = ""
        
        size = self.parent.winfo_screenwidth()//8
        self.logo = ctk.CTkImage(
            Image.open(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    "..",
                    "resources",
                    "icon.png",
                            )
                     ).resize((size, size), Image.LANCZOS), size=(size, size)
                                )
        
        self.logolabel = ctk.CTkLabel(self, text=Text().help[self.lang], image = self.logo, font=("Bahnschrift", 30), compound="top")
        self.logolabel.place(relx=0.5, rely=0.5, anchor="center")
        
    def add_tab(self):
        """Add a tab to the tabview.
        """
                
        window = ctk.CTkToplevel(self.parent.parent)
        window.wm_attributes("-toolwindow", True)
        window.title(Text().newtabname[self.lang])
        
        def move(event):
            window.lift()
            entry.focus()
            window.geometry(f"180x90+{self.parent.parent.winfo_rootx()+self.parent.parent.winfo_width()//2-90}+{self.parent.parent.winfo_rooty()+self.parent.parent.winfo_height()//2-45}")
        
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
            self.parent.parent.set_theme()
            tab.pack(fill="both", expand=True)

            self.parent.parent.menubar.tabmenu.add_command(label=Text().closetab[self.lang].format(tab.name), command=lambda: self.remove_tab(self.tabnames.index(tab.name)))
            self.set(self.tabnames[-1])
            
            if len (self.tabnames) == 1:
                self.logolabel.place_forget()
        
        entry = ctk.CTkEntry(window, takefocus=True)
        submitbutton = ctk.CTkButton(window, text="OK", command=submit)
        entry.pack(fill="x", expand=True, padx=5, pady=5)
        submitbutton.pack(padx=5, pady=5)
        entry.focus()
        window.bind("<Configure>", move)
        window.bind("<Escape>", lambda event: window.destroy())
        window.bind("<Return>", lambda event: submit())
    
    def remove_tab(self, index):
        """Remove a tab from the tabview.
        """
        self.delete(self.tabnames[index])
        self.tabnames.pop(index)
        if len(self.tabnames) == 0:
            self.logolabel.place(relx=0.5, rely=0.5, anchor="center")
        self.parent.parent.menubar.tabmenu.delete(index+2)