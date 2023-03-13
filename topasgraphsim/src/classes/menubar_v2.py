import tkinter as tk

from .profile import ProfileHandler
from ..resources.language import Text
from ..resources.info_v2 import show_info

class MenuBar(tk.Menu):
    
    """The menubar of the TGS application.
    """

    def __init__(self, parent):
        
        self.parent = parent
        text = Text()
        l = self.parent.lang.get()
        super().__init__(self.parent)
        
        self.filemenu = tk.Menu(self, tearoff=False)
        
        self.languagemenu = tk.Menu(self, tearoff=False)
        self.languagemenu.add_radiobutton(label=text.english[l], command=self.set_language, variable=self.parent.lang, value="en")
        self.languagemenu.add_radiobutton(label=text.german[l], command=self.set_language, variable=self.parent.lang, value="de")
        self.filemenu.add_command(command=self.load_topas, label=text.loadsim[l], accelerator="Ctrl+O")
        self.filemenu.add_separator()
        self.filemenu.add_cascade(label=text.language[l], menu=self.languagemenu)
        self.filemenu.add_command(label=text.settings[l], command=self.parent.settings)
        self.filemenu.add_command(label = text.end[l], command=self.parent.exit)
    
        self.viewmenu = tk.Menu(self, tearoff=False)
        
        self.tabmenu = tk.Menu(self, tearoff=False)
        self.tabmenu.add_command(label=text.newtab[l], command=lambda: self.parent.frame.tabview.add_tab(), accelerator="Ctrl+N")
        self.parent.bind("<Control-n>", lambda e: self.parent.frame.tabview.add_tab())
        self.tabmenu.add_separator()
        self.viewmenu.add_cascade(label=text.tabnames[l], menu=self.tabmenu)
        
        self.viewmenu.add_separator()
        self.thememenu = tk.Menu(self, tearoff=False)
        self.thememenu.add_radiobutton(label=text.light[l], command=self.set_theme, variable=self.parent.colorscheme, value="light")
        self.thememenu.add_radiobutton(label=text.dark[l], command=self.set_theme, variable=self.parent.colorscheme, value="dark")
        self.viewmenu.add_cascade(label=text.themeselection[l], menu=self.thememenu)
        
        self.fullscreen = tk.BooleanVar(value=ProfileHandler().get_attribute("fullscreen"))
        self.viewmenu.add_checkbutton(label=text.fullscreen[l], command=self.toggle_fullscreen, variable=self.fullscreen, accelerator="F11")
        self.parent.bind("<F11>", lambda e: self.toggle_fullscreen(e))
        
        self.add_cascade(label=text.file[l], menu = self.filemenu)
        self.add_cascade(label=text.view[l], menu=self.viewmenu)
        self.add_command(label=text.about[l], command=lambda: show_info(self.parent))
        
    def set_theme(self):
        """Switch between light and dark theme.
        """
        self.parent.set_theme()
            
    def set_language(self):
        """Switch between english and german language.
        """
        self.parent.set_language()
        
    def toggle_fullscreen(self, event=None): 
        """Toggle fullscreen mode.
        """
        
        if event != None:
            self.fullscreen.set(not self.fullscreen.get())
            ProfileHandler().set_attribute("fullscreen", self.fullscreen.get())
            self.parent.attributes("-fullscreen", self.fullscreen.get())
            
        else:
            ProfileHandler().set_attribute("fullscreen", self.fullscreen.get())
            self.parent.attributes("-fullscreen", self.fullscreen.get())
            
    def load_topas(self):
        current_tab = self.parent.frame.tabview.get()
        if current_tab == "":
            self.parent.frame.tabview.add_tab(name = True)
            current_tab = self.parent.frame.tabview.get()
        self.parent.frame.tabview.tab(current_tab).tab.options.load_topas()
