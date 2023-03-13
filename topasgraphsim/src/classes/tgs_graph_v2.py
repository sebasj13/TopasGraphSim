import numpy as np
from .profile import ProfileHandler
from ..resources.language import Text

class TGS_Plot():
    
    def __init__(self, Options, ImportedData):
        
        self.options = Options
        self.lang = self.options.lang
        self.dataObject = ImportedData
        self.direction = self.dataObject.direction
        
        self.normalize = False
        self.normalization = "Maximum"
        
        self.label = self.dataObject.filename
        self.linethickness = 1
        self.linestyle = Text().dashdot[self.lang]
        self.linestyledict = {Text().dashdot[self.lang]:"-.", Text().dash[self.lang]:"-", Text().dot[self.lang]:"dotted"}
        self.linecolor =  ProfileHandler().get_attribute("default_colors")[len(self.options.parent.plots)]
        
        self.dosefactor = 1
        self.doseshift = 0
        self.axshift = 0 
        self.flip = False
        
        self.set_tab_data()
        
    def set_tab_data(self):
        
        self.options.normalize.set(self.normalize)
        self.options.normalization.set(self.normalization)
        self.options.plottitle.set(self.label)
        self.options.linethicknessslider.set(self.linethickness)
        self.options.linestyle.set(self.linestyle)
        self.options.plotcolor.set(self.linecolor)
        self.options.linecolorbutton.configure(fg_color=self.linecolor)
        self.options.doseshift.set(self.doseshift)
        self.options.axshift.set(self.axshift)
        self.options.dosescale.set(self.dosefactor)
        self.options.flip.set(self.flip)
        
    def data(self):
        
        axis = np.add(self.dataObject.axis,self.axshift)
        dose = self.dataObject.dose.copy()
        if self.normalize:
            dose /= np.max(dose)

        dose = np.add(dose * self.dosefactor, self.doseshift)
        if self.flip:
            dose = np.flip(dose)
            
        return axis, dose
        
    def plot(self, ax):
    
        axis, dose = self.data()
        ax.plot(axis, dose, label=self.label, lw=self.linethickness, color=self.linecolor, linestyle = self.linestyledict[self.linestyle])
        
        
        
        
        
    


