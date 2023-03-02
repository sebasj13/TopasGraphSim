import customtkinter as ctk

from ..resources.language import Text

class Options(ctk.CTkFrame):
    
    """The options frame of the TGS application.
    """
    
    def __init__(self, parent, index, lang):
        
        self.parent = parent      
        self.index = index
        self.lang = lang  
        super().__init__(self.parent, border_color="black", border_width=1)
        
        self.newtabname = ""
        
        self.change_name_button = ctk.CTkButton(self, text="Edit tab name", command = self.change_name)
        self.change_name_button.pack(pady=5, padx=5, fill="x")
        
    def change_name(self):
        
        
        """Add a tab to the tabview.
        """
        root = self.parent.master.master.parent        
        window = ctk.CTkToplevel(root)
        window.wm_attributes("-toolwindow", True)
        window.geometry(f"180x90+{root.winfo_rootx()+root.winfo_width()//2-90}+{root.winfo_rooty()+root.winfo_height()//2-45}")
        window.title(Text().newtabname[self.lang])
        
        def move(event):
            window.lift()
            entry.focus()
            window.geometry(f"180x90+{root.winfo_rootx()+root.winfo_width()//2-90}+{root.winfo_rooty()+root.winfo_height()//2-45}")
        
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
            values = self.parent.master.master._segmented_button.cget("values")
            values[self.index] = tab
            self.parent.master.master._segmented_button.configure(values=values)
            self.parent.master.master._configure_tab_background_corners_by_name(tab)
            self.parent.master.master._segmented_button.set(tab)
            self.parent.master.master._draw()
            return
            
        entry = ctk.CTkEntry(window, takefocus=True)
        submitbutton = ctk.CTkButton(window, text="OK", command=submit)
        entry.pack(fill="x", expand=True, padx=5, pady=5)
        submitbutton.pack(padx=5, pady=5)
        entry.focus()
        window.bind("<Configure>", move)
        window.bind("<Escape>", lambda event: window.destroy())
        window.bind("<Return>", lambda event: submit())