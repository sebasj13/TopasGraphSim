import numpy as np
from .profile import ProfileHandler
from ..resources.language import Text

class TGS_Plot():
    
    def __init__(self, Options, ImportedData):
        
        self.options = Options
        self.lang = self.options.lang
        self.dataObject = ImportedData
        self.direction = self.dataObject.direction
        self.p = ProfileHandler()
        
        self.normalize = self.p.get_attribute("normalize")
        self.normalization = "Maximum"
        
        self.label = self.dataObject.filename
        self.linethickness = self.p.get_attribute("linethickness")
        self.linestyle = self.p.get_attribute("linestyle")
        self.linecolor =  ProfileHandler().get_attribute("default_colors")[len(self.options.parent.plots)%len(ProfileHandler().get_attribute("default_colors"))]
        
        self.dosefactor = self.p.get_attribute("dosefactor")
        self.doseshift = self.p.get_attribute("doseoffset")
        self.axshift = self.p.get_attribute("axshift")
        self.flip = self.p.get_attribute("flip")
        
        self.set_tab_data()
        
    def set_tab_data(self):
        
        self.options.normalize.set(self.normalize)
        self.options.normalization.set(self.normalization)
        self.options.plottitle.set(self.label)
        self.options.linethicknessslider.set(self.linethickness)
        self.options.linestyle.set({"-.":Text().dashdot[self.lang], "-":Text().dash[self.lang], "dotted":Text().dot[self.lang]}[self.linestyle])
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
        ax.plot(axis, dose, label=self.label, lw=self.linethickness, color=self.linecolor, linestyle = self.linestyle)
        
        
        
        
        
    


