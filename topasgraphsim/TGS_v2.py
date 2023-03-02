import os
from tkinter.dialog import Dialog
import customtkinter as ctk
from tkinter import StringVar
from src.resources.language import Text
from src.classes.menubar_v2 import MenuBar
from src.classes.profile import ProfileHandler
from src.classes.main_viewer_v2 import MainViewer


class TopasGraphSim(ctk.CTk):
    
    """GUI to visualize and analyse the results of TOPASMC simulations.
    """
    
    def __init__(self):
        super().__init__()
        
        self.appname = "TopasGraphSim"
        self.version = "23.0.0"
        self.author = "Sebastian Schäfer"
        self.title(f"{self.appname} - v.{self.version}")
        self.lang = StringVar()
        self.lang.set(ProfileHandler().get_attribute("language"))
        self.iconpath = os.path.join(os.path.dirname(__file__), "src", "resources","icon.ico")
        self.iconbitmap(self.iconpath)
        
        self.colorscheme = StringVar(value=ProfileHandler().get_attribute("color_scheme"))
        ctk.set_appearance_mode(self.colorscheme.get())
        ctk.set_default_color_theme("dark-blue")
        
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
            
        self.protocol("WM_DELETE_WINDOW", self.quit)
                
        self.mainloop()
        
    def set_language(self):
        ProfileHandler().set_attribute("language", self.lang.get())
        
        self.bell()
        window = ctk.CTkToplevel(self)
        window.wm_attributes("-toolwindow", True)
        window.geometry(f"260x60+{self.winfo_rootx()+self.winfo_width()//2-130}+{self.winfo_rooty()+self.winfo_height()//2-30}")
        window.title("")
        
        def move(event):
            window.lift()
            window.geometry(f"260x60+{self.winfo_rootx()+self.winfo_width()//2-130}+{self.winfo_rooty()+self.winfo_height()//2-30}")
        
        def submit():
            window.destroy()
        label = ctk.CTkLabel(window, text=Text().restart[self.lang.get()])
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
        colors = {"light": "#D9D9D9", "dark":"#292929"}
        fontcolors = {"light": "black", "dark":"white"}
        color = colors[ProfileHandler().get_attribute("color_scheme")]
        fontcolor = fontcolors[ProfileHandler().get_attribute("color_scheme")]
        for tab in self.frame.tabview.tabnames:
            for w in self.frame.tabview.tab(tab).winfo_children():
                if hasattr(w, "figure"):
                    w.figure.patch.set_facecolor(color)
                    w.ax.set_facecolor(color)
                    w.ax.spines["bottom"].set_color(fontcolor)
                    w.ax.spines["top"].set_color(fontcolor)
                    w.ax.spines["right"].set_color(fontcolor)
                    w.ax.spines["left"].set_color(fontcolor)
                    w.ax.tick_params(axis="x", colors=fontcolor)
                    w.ax.tick_params(axis="y", colors=fontcolor)
                    w.navbar.config(background=color)
                    w.navbar._message_label.config(background=color)
                    for t in w.navbar.winfo_children():
                        t.config(background=color)
                        if t.winfo_class() != "Frame":
                            t.config(foreground=fontcolor)
                    w.navbar.update()
                    w.canvas.draw()
        self.frame.pack(fill="both", expand=True)

    def quit(self):
        ProfileHandler().set_attribute("state", self.state())
        if self.state() == "zoomed":
            ProfileHandler().set_attribute("geometry", " ")
        else:
            ProfileHandler().set_attribute("geometry", self.geometry())
        super().quit()
                
if __name__ == "__main__":
    TopasGraphSim()