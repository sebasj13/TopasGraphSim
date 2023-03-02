import tkinter as tk
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
        
        self.tabs = []
        self.newtabname = ""
        
    def add_tab(self):
        """Add a tab to the tabview.
        """
                
        window = ctk.CTkToplevel(self.parent.parent)
        window.geometry(f"180x90+{self.parent.parent.winfo_rootx()+self.parent.parent.winfo_width()//2-90}+{self.parent.parent.winfo_rooty()+self.parent.parent.winfo_height()//2-45}")
        window.wm_attributes("-toolwindow", True)
        window.title(Text().newtabname[self.lang])
        
        def move(event):
            window.lift()
            entry.focus()
            window.geometry(f"180x90+{self.parent.parent.winfo_rootx()+self.parent.parent.winfo_width()//2-90}+{self.parent.parent.winfo_rooty()+self.parent.parent.winfo_height()//2-45}")
        
        def submit():
            self.newtabname = entry.get()
            window.destroy()
            if self.newtabname == "" or self.newtabname in self.tabs:
                return

            tab = self.newtabname
            self.newtabname = ""
            self.add(tab)
            self.tabs.append(tab)
            tab = Tab(self.tab(tab), tab)
            self.parent.parent.set_theme()
            tab.pack(fill="both", expand=True)
            
            menu = tk.Menu(self.parent.parent.menubar, tearoff=False)
            menu.add_command(label=Text().closetab[self.lang], command=lambda: self.remove_tab(self.tabs.index(tab.name)))
            self.parent.parent.menubar.tabmenu.add_cascade(label=tab.name, menu=menu)
            self.set(self.tabs[-1])
        
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
        self.delete(self.tabs[index])
        self.tabs.pop(index)
        self.parent.parent.menubar.tabmenu.delete(index+1)