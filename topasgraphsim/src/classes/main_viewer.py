from tkinter import Frame
from .tabview import TabView

class MainViewer(Frame):
    
    """The main viewer of the TGS application.
    """
    
    def __init__(self, parent):
        
        self.parent = parent
        super().__init__(self.parent, border=1, bg="#E5E5E5")
        self.tabview = TabView(self)
        self.tabview.pack(fill="both", expand=True)
        self.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.register_drop_target("*")
        self.bind("<<Drop>>", self.drop)

    def add_file(self, path):
        if len(self.tabview.tabnames) == 0:
            self.tabview.add_tab(name = True)
            if path[-4:] == ".csv":
                self.tabview.tab(self.tabview.tabnames[-1]).tab.options.load_topas(path)
            elif path[-4:] == ".mcc":
                self.tabview.tab(self.tabview.tabnames[-1]).tab.options.load_measurement(path)
            
        else:
            if path[-4:] == ".csv":
                self.tabview.tab(self.tabview.tabnames[self.tabview.tabnames.index(self.tabview.get())]).tab.options.load_topas(path)
            elif path[-4:] == ".mcc":
                self.tabview.tab(self.tabview.tabnames[self.tabview.tabnames.index(self.tabview.get())]).tab.options.load_measurement(path)

    def drop(self, event):
        if "}" in event.data:
            paths = event.data.split("}")
        else:
            paths = event.data.split(" ")
        for path in paths:
            print(path)
            if path != "":
                path = path.strip()
                if "{" in path:
                    path = path.replace("{", "")
                if path[-4:] == ".csv":
                    if len(self.tabview.tabnames) == 0:
                        self.tabview.add_tab(name = True)
                    with open(path,"r") as f:
                        l = f.readline()
                    if "Machine" in l:
                        self.tabview.tab(self.tabview.tabnames[-1]).tab.options.load_radcalc([path])
                    else:
                        self.tabview.tab(self.tabview.tabnames[-1]).tab.options.load_topas(path)
                elif path[-4:] == ".mcc":
                    if len(self.tabview.tabnames) == 0:
                        self.tabview.add_tab(name = True)
                    self.tabview.tab(self.tabview.tabnames[-1]).tab.options.load_measurement(path)
                    
                elif path[-4:] == ".txt":
                    if len(self.tabview.tabnames) == 0:
                        self.tabview.add_tab(name = True)
                    self.tabview.tab(self.tabview.tabnames[-1]).tab.options.load_txt(path)

                elif path[-5:] == ".data":
                    if len(self.tabview.tabnames) == 0:
                        self.tabview.add_tab(name = True)
                    self.tabview.tab(self.tabview.tabnames[-1]).tab.options.load_eclipse([path])