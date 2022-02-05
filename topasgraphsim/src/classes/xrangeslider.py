import tkinter as tk
import tkinter.ttk as ttk
from ..resources.language import Text
from .profile import ProfileHandler
import numpy as np
from RangeSlider.RangeSlider import RangeSliderH


class XRangeSlider:
    def __init__(self, parent):

        self.parent = parent
        self.window = tk.Toplevel()
        self.window.resizable(False, False)
        self.window.wm_overrideredirect(True)
        self.geometry = [
            self.parent.parent.winfo_rootx(),
            self.parent.parent.winfo_rooty(),
            self.parent.winfo_width(),
            self.parent.winfo_height(),
        ]
        self.height = 80
        self.window.geometry(
            f"{500}x{self.height}+{int(self.geometry[0]+self.geometry[2]//2) - 250}+{self.geometry[1]+ self.geometry[3]}"
        )

        self.leftvar = tk.DoubleVar()

        self.rightvar = tk.DoubleVar()

        initial_limits = self.parent.DoseFigureHandler.initial_limits
        current_limits = self.parent.DoseFigureHandler.ax.get_xlim()
        self.leftvar.set(round(current_limits[0], 1))
        self.rightvar.set(round(current_limits[1], 1))
        self.slider = RangeSliderH(
            self.window,
            variables=[self.leftvar, self.rightvar],
            padX=100,
            valueSide="BOTTOM",
            Width=500,
            min_val=initial_limits[0],
            max_val=initial_limits[1],
            font_family="Helvetica",
            font_size=12,
            digit_precision=".0f",
            suffix=" mm",
        )

        self.submitbutton = ttk.Button(
            self.window,
            text=Text().submit[ProfileHandler().get_attribute("language")],
            command=self.submit,
        )
        self.submitbutton.grid(sticky="N")
        self.slider.grid(sticky="N")
        self.leftvar.trace_add("write", self.update)
        self.rightvar.trace_add("write", self.update)
        self.stay_on_top()

    def update(self, *args):
        self.current_limits = self.parent.DoseFigureHandler.ax.get_xlim()
        self.stretch = abs(self.current_limits[0]) + abs(self.current_limits[1])
        self.new_limits = [self.leftvar.get(), self.rightvar.get()]
        self.parent.new_limits = self.new_limits

        if (
            abs(self.current_limits[0] - self.new_limits[0]) > 0.05 * self.stretch
            or abs(self.current_limits[1] - self.new_limits[1]) > 0.05 * self.stretch
        ):
            self.parent.refresh()

    def submit(self):
        self.parent.refresh()
        self.parent.xlimmenu = False
        self.window.destroy()

    def stay_on_top(self):

        self.new_geometry = [
            self.parent.parent.winfo_rootx(),
            self.parent.parent.winfo_rooty(),
            self.parent.winfo_width(),
            self.parent.winfo_height(),
        ]
        self.window.after(50, self.stay_on_top)
        if self.new_geometry == self.geometry:
            return

        self.geometry = self.new_geometry
        self.height = 80
        self.window.geometry(
            f"{500}x{self.height}+{int(self.geometry[0]+self.geometry[2]//2) - 250}+{self.geometry[1]+ self.geometry[3]}"
        )
        self.window.lift()
