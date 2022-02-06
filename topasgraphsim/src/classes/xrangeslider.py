import tkinter as tk
import tkinter.ttk as ttk
from ..resources.language import Text
from .profile import ProfileHandler
import time
from .RangeSlider import RangeSliderH


class XRangeSlider:
    def __init__(self, parent, slidervars, initial_limits):

        self.parent = parent
        self.window = tk.Toplevel()
        self.window.resizable(False, False)
        self.window.wm_overrideredirect(True)
        self.window.wm_attributes("-alpha", 0.6)
        self.window.bind("<Return>", self.submit)
        self.geometry = [
            self.parent.parent.winfo_rootx(),
            self.parent.parent.winfo_rooty(),
            self.parent.winfo_width(),
            self.parent.winfo_height(),
        ]
        self.height = 80
        self.window.geometry(
            f"{500}x{self.height}+{int(self.geometry[0]+self.geometry[2]//2) - 250}+{int(self.geometry[1]+0.8*self.geometry[1])}"
        )

        self.slider = RangeSliderH(
            self.window,
            variables=slidervars,
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
        slidervars[0].trace_add("write", self.update)
        slidervars[1].trace_add("write", self.update)
        self.stay_on_top()

        self.starttime = time.time()

    def update(self, *args):
        if time.time() > self.starttime + 0.5:
            self.parent.refresh()
            self.starttime = time.time()
        return

    def submit(self):
        self.parent.xlimmenu = False
        self.parent.parent.bind("<MouseWheel>", self.parent.change_x_limits)
        self.window.destroy()
        self.parent.refresh()
        return

    def stay_on_top(self):

        self.new_geometry = [
            self.parent.parent.winfo_rootx(),
            self.parent.parent.winfo_rooty(),
            self.parent.winfo_width(),
            self.parent.winfo_height(),
        ]
        self.window.lift()
        self.window.after(50, self.stay_on_top)
        if self.new_geometry == self.geometry:
            return

        self.geometry = self.new_geometry
        self.height = 80
        self.window.geometry(
            f"{500}x{self.height}+{int(self.geometry[0]+self.geometry[2]//2) - 250}+{int(self.geometry[1]+0.8*self.geometry[1])}"
        )
