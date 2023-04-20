import customtkinter as ctk
from threading import Thread

class Slider(ctk.CTkFrame):
    def __init__(self, parent, update):
        self.parent = parent
        self.update = update
        super().__init__(self.parent)
        self.var = ctk.DoubleVar(value=0.0)
        self.slider = ctk.CTkSlider(self, orientation = "horizontal", width=80, variable=self.var, command = self.update_text, from_=0.0, to=100, number_of_steps=100)
        self.text = ctk.CTkLabel(self, text="0.0")
        self.slider.grid(row=0, column=0)
        self.text.grid(row=0, column=1)
        self.columnconfigure(0, minsize=100)
        self.columnconfigure(1, minsize=30)
        self.rowconfigure(0)
        
    def update_text(self, event):
        self.text.configure(text=str(round(self.var.get(), 2)))
        self.update()
        
        
    