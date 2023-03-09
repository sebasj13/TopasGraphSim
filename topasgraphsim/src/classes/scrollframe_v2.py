import customtkinter as ctk
import tkinter as tk

# Adapted from https://gist.github.com/mp035/9f2027c3ef9172264532fcd6262f3b01


class ScrollFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, border_color="black", border_width=1)

        self.canvas = tk.Canvas(
            self,
            
        )
        self.viewPort = ctk.CTkFrame(
            self.canvas,
            corner_radius=0
        )
        self.scrollbar = ctk.CTkScrollbar(self, orientation="vertical",
                                    command=self.canvas.yview,
                                    width=15, corner_radius=10)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, minsize=15)
        self.rowconfigure(0, weight=1)
        self.canvas.grid(row=0, column=0, sticky="nsew", padx=(2,0), pady=2)
        self.scrollbar.grid(row=0, column=1, sticky="ns", padx=(0,2), pady=2)

        
        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.viewPort,
            anchor="nw",
            tags="self.viewPort",
            
        )

        self.viewPort.bind("<Configure>", self.onFrameConfigure)
        self.canvas.bind("<Configure>", self.onCanvasConfigure)

        self.viewPort.bind("<Enter>", self.onEnter)
        self.canvas.bind("<Leave>", self.onLeave)

        self.onFrameConfigure(None)

    def onFrameConfigure(self, event):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def onCanvasConfigure(self, event):
        """Reset the canvas window to encompass inner frame when required"""
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)

    def onMouseWheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def onEnter(self, event):
        self.canvas.bind_all("<MouseWheel>", self.onMouseWheel)

    def onLeave(self, event):
        self.canvas.unbind_all("<MouseWheel>")
