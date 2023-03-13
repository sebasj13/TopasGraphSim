import os
import tkinterDnD as tkdnd
import customtkinter as ctk
from tkinter import StringVar

from .src.resources.language import Text
from .src.classes.menubar_v2 import MenuBar
from .src.classes.profile import ProfileHandler
from .src.classes.main_viewer_v2 import MainViewer

class Tk(ctk.CTk, tkdnd.dnd.DnDWrapper):
    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)
        self.TkDnDVersion = tkdnd.tk._init_tkdnd(self)


class TopasGraphSim(Tk):
    
    """GUI to visualize and analyse the results of TOPASMC simulations.
    """
    
    def __init__(self):      
        
        super().__init__()
        
        self.appname = "TopasGraphSim"
        self.version = "23.0.0"
        self.author = "Sebastian Schäfer"
        self.affiliation = "UK Halle\nMLU Halle-Wittenberg\nUK Hamburg-Eppendorf"
        self.title(f"{self.appname} - v.{self.version}")
        self.lang = StringVar()
        self.lang.set(ProfileHandler().get_attribute("language"))
        self.iconpath = os.path.join(os.path.dirname(__file__), "src", "resources","icon.ico")
        self.iconbitmap(self.iconpath)
        
        self.colorscheme = StringVar(value=ProfileHandler().get_attribute("color_scheme"))
        ctk.set_appearance_mode(self.colorscheme.get())
        ctk.set_default_color_theme("blue")
        
        self.menubar = MenuBar(self)
        self.config(menu=self.menubar)

        self.frame = MainViewer(self)
        
        self.set_theme()
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width = screen_width // 2
        height = screen_height // 2
        self.minsize(width, height)
        self.pack_propagate(False)
        
        
        self.state(ProfileHandler().get_attribute("state"))
        try:
            self.geometry(ProfileHandler().get_attribute("geometry"))
        except Exception:
            x = screen_width // 2 - width // 2
            y = screen_height // 2 - height // 2
            self.geometry(f"{width}x{height}+{x-25}+{y}")
            
           
        self.protocol("WM_DELETE_WINDOW", self.exit)
                
        self.mainloop()
        
    def settings(self):
        try:
            self.frame.tabview.add_settings()
        except ValueError:
            self.frame.tabview.set(Text().settings[self.lang.get()])
        
    def set_language(self):
        ProfileHandler().set_attribute("language", self.lang.get())
        
        self.bell()
        window = ctk.CTkToplevel(self)
        window.wm_attributes("-toolwindow", True)
        window.geometry(f"220x80+{self.winfo_rootx()+self.winfo_width()//2-110}+{self.winfo_rooty()+self.winfo_height()//2-40}")
        window.title("")
        
        def move(event):
            window.lift()
            window.geometry(f"220x80+{self.winfo_rootx()+self.winfo_width()//2-110}+{self.winfo_rooty()+self.winfo_height()//2-40}")
        
        def submit():
            window.destroy()
        label = ctk.CTkLabel(window, text=Text().restart[self.lang.get()], font=("Bahnschrift", 16))
        okbutton = ctk.CTkButton(window, text="OK", command=submit, width=30)
        label.pack()
        okbutton.pack(padx=5, pady=5)
        window.bind("<Configure>", move)
        window.bind("<Escape>", lambda event: window.destroy())
        window.bind("<Return>", lambda event: submit())
        
    def set_theme(self):
        self.frame.pack_forget()
        ProfileHandler().set_attribute("color_scheme", self.colorscheme.get())
        ctk.set_appearance_mode(ProfileHandler().get_attribute("color_scheme"))
        colors = {"light": "#D9D9D9", "dark":"#1C1C1C"}
        colors2 = {"light": "#E5E5E5", "dark":"#212121"}
        colors3 = {"light": "#DBDBDB", "dark":"#2B2B2B"}
        fontcolors = {"light": "black", "dark":"white"}
        color = colors[ProfileHandler().get_attribute("color_scheme")]
        color2 = colors2[ProfileHandler().get_attribute("color_scheme")]
        color3 = colors3[ProfileHandler().get_attribute("color_scheme")]
        fontcolor = fontcolors[ProfileHandler().get_attribute("color_scheme")]
        self.frame.configure(bg=color2)
        for tab in self.frame.tabview.tabnames:
            if tab != Text().settings[self.lang.get()]:
                self.frame.tabview.tab(tab).tab.options.configure(bg_color=color2)
                self.frame.tabview.tab(tab).tab.options.graphlist.configure(fg_color=color2)
                self.frame.tabview.tab(tab).tab.options.graphlist.canvas.configure(bg=color3, highlightbackground=color3)
                self.frame.tabview.tab(tab).tab.options.graphlist.scrollbar.configure(fg_color=color3)
                for w in self.frame.tabview.tab(tab).winfo_children():
                    if hasattr(w, "figure"):
                        if w.options.showlegend.get():
                            for text in w.ax.get_legend().get_texts():
                                text.set_color(fontcolor)
                        w.ax.set_title(w.ax.get_title(), color=fontcolor)
                        w.ax.set_xlabel(w.ax.get_xlabel(), color=fontcolor)
                        w.ax.set_ylabel(w.ax.get_ylabel(), color=fontcolor)
                        w.figure.patch.set_facecolor(color2)
                for w in self.frame.tabview.tab(tab).winfo_children():
                    self.frame.tabview.tab(tab).tab.options.configure(bg_color=color2)
                    self.frame.tabview.tab(tab).tab.options.graphlist.configure(fg_color=color2)
                    self.frame.tabview.tab(tab).tab.options.graphlist.canvas.configure(bg=color3, highlightbackground=color3)
                    self.frame.tabview.tab(tab).tab.options.graphlist.scrollbar.configure(fg_color=color3)
                    if hasattr(w, "figure"):
                        if w.options.showlegend.get():
                            for text in w.ax.get_legend().get_texts():
                                text.set_color(fontcolor)
                        w.ax.set_title(w.ax.get_title(), color=fontcolor)
                        w.ax.set_xlabel(w.ax.get_xlabel(), color=fontcolor)
                        w.ax.set_ylabel(w.ax.get_ylabel(), color=fontcolor)
                        w.figure.patch.set_facecolor(color2)
                        w.ax.set_facecolor(color)
                        w.ax.spines["bottom"].set_color(fontcolor)
                        w.ax.spines["top"].set_color(fontcolor)
                        w.ax.spines["right"].set_color(fontcolor)
                        w.ax.spines["left"].set_color(fontcolor)
                        w.ax.tick_params(axis="x", colors=fontcolor)
                        w.ax.tick_params(axis="y", colors=fontcolor)
                        w.navbar.config(background=color2)
                        w.navbar._message_label.config(background=color)
                        for t in w.navbar.winfo_children():
                            t.config(background=color2)
                            if t.winfo_class() != "Frame":
                                t.config(foreground=fontcolor)
                        w.navbar.update()
                        w.canvas.draw()
        self.frame.pack(fill="both", expand=True)

    def exit(self):
        ProfileHandler().set_attribute("state", self.state())
        if self.state() == "zoomed":
            ProfileHandler().set_attribute("geometry", " ")
        else:
            ProfileHandler().set_attribute("geometry", self.geometry())

        saved = [self.frame.tabview.tab(w).tab.saved for w in self.frame.tabview.tabnames]
        if saved != [] or False in saved:

            self.bell()
            window = ctk.CTkToplevel(self)
            window.wm_attributes("-toolwindow", True)
            window.title("")
            
            def move(event):
                window.lift()
                window.geometry(f"200x100+{self.winfo_rootx()+self.winfo_width()//2-100}+{self.winfo_rooty()+self.winfo_height()//2-50}")
            
            def submit():
                window.destroy()
                self.quit()
            
            def cancel():
                window.destroy()
            
            window.rowconfigure(0, weight=1)
            window.columnconfigure(0, weight=1)
            window.columnconfigure(1, weight=1)
            textlabel = ctk.CTkLabel(window, text=Text().unsavedchanges1[self.lang.get()], font=("Bahnschrift", 16))
            submitbutton = ctk.CTkButton(window, text=Text().yes[self.lang.get()], command=submit, width=40, font=("Bahnschrift", 12))
            cancelbutton = ctk.CTkButton(window, text=Text().no[self.lang.get()], command=cancel, width = 40, font=("Bahnschrift", 12))
            textlabel.grid(row=0, columnspan=2, padx=5, pady=5, sticky="nsew")
            submitbutton.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
            cancelbutton.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
            window.bind("<Configure>", move)
            window.bind("<Escape>", lambda event: window.destroy())
            window.bind("<Return>", lambda event: submit())
        else:
            self.quit()
                
if __name__ == "__main__":
    TopasGraphSim()