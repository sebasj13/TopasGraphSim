class Text:

    """
    Contains all translatable text in the program.
    """

    def __init__(self):

        self.absolute = {"de": "Absolut", "en": "Absolute"}
        self.allfiles = {"de": "Alle Dateien", "en": "All files"}
        self.analysis = {"de": "Analyse", "en": "Analysis"}
        self.about = {"de": "Über TGS", "en": "About"}
        self.add = {"de": "Daten hinzufügen", "en": "Add Data"}
        self.adddescriptors = {
            "de": "Beschriftungen hinzufügen",
            "en": "Add descriptors",
        }
        self.axis = {"de": "Achse", "en": "Axis"}
        self.calcfail = {
            "de": "Parameter konnten nicht berechnen werden!",
            "en": "Parameters could not be calculated!",
        }
        self.bins = {"de": "Klassenanzahl", "en": "Number of bins"}
        self.binsize = {"de": "Klassenbreite", "en": "Bin size"}
        self.min = {"de": "Minimum", "en": "Minimum"}
        self.max = {"de": "Maximum", "en": "Maximum"}
        self.criterion = {"de": "Kriterium", "en": "Criterion"}
        self.calcparams = {"de": "Parameter berechnen", "en": "Calculate parameters"}
        self.calculate = {"de": "Berechnen", "en": "Calculate"}
        self.caxcorrection = {
            "de": "CAX-Korrektur",
            "en": "CAX correction",
        }
        self.beamquality = {"de":"Strahlungsqualitätsindex", "en":"Beam quality index"}
        self.zmax = {"de":"Maximumstiefe", "en":"Depth of maximum"}
        self.centeraxis = {"de": "Zentralstrahl", "en": "Center axis"}
        self.cax = {"de":"Zentralstrahlabweichung", "en":"Center axis deviation"}
        self.changefilename = {"de": "Neuer Name:", "en": "New Name:"}
        self.change = {"de": "Ändern", "en": "Change"}
        self.changeerr = {"de": "Darstellung ändern", "en": "Switch view"}
        self.choosenormalization = {"de": "Normieren auf ...", "en": "Normalize to ..."}
        self.close = {
            "de": "Derzeitige Ansicht schließen",
            "en": "Close current project",
        }
        self.closetab = {"de": "Tab '{}' schließen", "en": "Close tab '{}'"}
        self.closetab1 = {"de": "Tab schließen", "en": "Close tab"}
        self.closeprompt = {
            "de": "Graph wurde noch nicht gespeichert. Trotzdem Schließen?",
            "en": "Graph was not saved. Close anyways?",
        }
        self.difference2 = {"de": "Differenz", "en": "Difference"}
        self.dark = {"de": "Dunkel", "en": "Dark"}
        self.decrease = {"de": "Verkleinern", "en": "Decrease"}
        self.decreaseupper = {
            "de": "Obere Grenze verkleinern",
            "en": "Decrease upper limit",
        }
        self.decreaselower = {
            "de": "Untere Grenze verkleinern",
            "en": "Decrease lower limit",
        }
        self.differenceplot = {
            "de": "Differenzgraph anzeigen",
            "en": "Show difference plot",
        }
        self.direction = {"de": "Richtung asuwählen...", "en": "Select direction..."}
        self.data = {"de": "Daten", "en": "Data"}
        self.gammasettings = {"de": "Gamma", "en": "Gamma"}
        self.generalsettings = {"de": "Allgemein", "en": "General"}
        self.axshift = {"de": "Achsenoffset", "en": "Axis shift"}
        self.apply = {"de":"Anwenden", "en":"Apply"}
        self.doseshift = {"de":"Dosisoffset", "en": "Dose offset"}
        self.dosescale = {"de":"Dosisfaktor", "en": "Dose factor"}
        self.flatkrieger = {"de":"Flatness (Krieger)", "en":"Flatness (Krieger)"}
        self.flatstddev = {"de":"Flatness (StdAbw)", "en":"Flatness (StdDev)"}
        self.leftpenumbra = {"de":"Penumbra (Links)", "en": "Penumbra (left)"}
        self.rightpenumbra = {"de":"Penumbra (Rechts)", "en": "Penumbra (right)"}
        self.leftintegral = {"de":"Integral (Links)", "en": "Integral (left)"}
        self.rightintegral = {"de":"Integral (Rechts)", "en": "Integral (right)"}
        self.dp = {"de": "Dosisquerverteilungen", "en": "Dose profiles"}
        self.defaulttitle = {"de": "Neuer Graph", "en": "New graph"}
        self.defaulttitlelabel = {"de": "Graphtitel", "en": "Graph title"}
        self.defaultxaxis = {"de": "X-Achse", "en": "X-Axis"}
        self.defaultxaxislabel = {"de": "X-Achse", "en": "X-Axis label"}
        self.defaultyaxis = {"de": "Y-Achse", "en": "Y-Axis"}
        self.defaultyaxislabel = {"de": "Y-Achse", "en": "Y-Axis label"}
        self.linestyle = {"de": "Linienart", "en": "Line type"}
        self.dash = {"de": "Linie", "en": "Line"}
        self.dashdot = {"de": "Punkt-Linie", "en": "Dash-Dot"}
        self.dot = {"de": "Punkt", "en": "Dot"}
        self.egs = {"de": "EGS Simulationsdateien", "en": "EGS Simulation Data"}
        self.egsunit = {"de": "Dosis [Gy/Historie]", "en": "Dose [Gy/History]"}
        self.end = {"de": "Beenden", "en": "Close"}
        self.edittabname = {"de": "Tab umbenennen", "en": "Rename tab"}
        self.english = {"de": "Englisch", "en": "English"}
        self.error = {"de": "Abweichung", "en": "Difference"}
        self.error1 = {"de": "Fehler bei der Parameterberechnung!", "en": "Failed to calculate parameters!"}
        self.errorbars = {"de": "Fehlerbalken", "en": "Errorbars"}
        self.errlimmenu = {"de": "Fehlergrenze einstellen", "en": "Change error limits"}
        self.file = {"de": "Datei", "en": "File"}
        self.flip = {"de": "Daten umkehren", "en": "Flip data"}
        self.fileerror = {"de": "Datei konnte nicht geladen werden!", "en": "File could not be loaded!"}
        self.plateau = {"de": "Plateau", "en": "Plateau"}
        self.fullscreen = {"de": "Vollbild", "en": "Fullscreen"}
        self.saveplottitle = {"de": "Dateinahmen wählen...", "en": "Choose filename..."}
        self.fwhm = {"de": "HWB", "en": "FWHM"}
        self.gamma = {"de": "Gammaanalyse", "en": "Gamma analysis"}
        self.gammamenu = {"de": "Gamma-Index", "en": "Gamma-Index"}
        self.german = {"de": "Deutsch", "en": "German"}
        self.half = {"de": "Halbe Querverteilung anzeigen", "en": "Show half profile"}
        self.graphinfo = {"de": "Werte über Maus anzeigen", "en": "Show value on hover"}
        self.graphsettings = {"de": "Grapheinstellungen", "en": "Graph settings"}
        self.help = {"de": "Füge einen neuen Tab hinzu [Ctrl+N],\noder ziehe eine Datei in das Fenster, um anzufangen!", "en": "Add a new tab [Ctrl+N],\nor drag and drop a file to begin!"}
        self.histnum = {
            "de": "Anzahl der Historien in der Simulation:",
            "en": "Histories in Simulation:",
        }
        self.histories = {"de": "Historien", "en": "Histories"}
        self.image = {"de": "Bilder", "en": "Images"}
        self.increase = {"de": "Vergrößern", "en": "Increase"}
        self.increaseupper = {
            "de": "Obere Grenze vergrößern",
            "en": "Increase upper limit",
        }
        self.increselower = {
            "de": "Untere Grenze vergrößern",
            "en": "Increase lower limit",
        }
        self.incordata = {
            "de": {
                1: " wurde nicht importiert - unpassender Messtyp!",
                2: " wurden nicht importiert - unpassende Messtypen!",
            },
            "en": {
                1: " was not imported - incompatible measurement!",
                2: " were not imported - incompatible measurements!",
            },
        }
        self.language = {"de": "Sprache", "en": "Language"}
        self.shift = {"de": "Linie verschieben/skalieren", "en": "Shift/rescale graph"}
        self.showpoints = {"de": "Punkte", "en": "Points"}
        self.settings = {"de": "Standardeinstellungen", "en": "Default settings"}
        self.settings1 = {"de":"Einstellungen", "en":"Settings"}
        self.savesettings = {"de": "Einstellungen speichern", "en": "Save settings"}
        self.languageset = {
            "en": "Das geöffnete Projekt wird geschlossen. Fortfahren?",
            "de": "The current project will be closed. Continue?",
        }
        self.none = {"de": "Keine", "en": "None"}
        self.light = {"de": "Hell", "en": "Light"}
        self.linethickness = {"de": "Linienstärke", "en": "Line thickness"}
        self.linecolor = {"de": "Linienfarbe", "en": "Line color"}
        self.loadmeasurement = {"de": "Messung laden", "en": "Load measurement"}
        self.local = {"de": "Lokal", "en": "Local"}
        self.globalg = {"de": "Global", "en": "Global"}
        self.gammatype = {"de": "Gamma-Typ", "en": "Gamma type"}
        self.loadsim = {"de": "Simulation laden", "en": "Load simulation"}

        self.marker = {"de": "Symbolgröße", "en": "Marker Size"}
        self.markerline = {"de": "Liniendicke", "en": "Line width"}
        self.measurement = {"de": "Messung", "en": "Measurement"}
        self.measurementdata = {"de": "Messdaten", "en": "Measurement Data"}
        self.metric = {"de": "Metrik", "en": "Metric"}
        self.maximum = {"de": "Maximum", "en": "Maximum"}
        self.newtab = {"de": "Neuer Tab", "en": "New Tab"}
        self.newtabname = {"de": "Name des neuen Tabs:", "en": "Name of new tab:"}
        self.normalize = {"de": "Normieren", "en": "Normalize"}
        self.normunit = {"de": "Relative Dosis", "en": "Relative Dose"}
        self.normalization = {"de": "Normierung", "en": "Normalization"}
        self.options = {"de": "Optionen", "en": "Options"}
        self.orr = {"de": "oder", "en": "or"}
        self.parameters = {"de": "Parameter", "en": "Parameters"}
        self.plotsettings = {"de": "Linien", "en": "Plot"}
        self.percentage = {"de": "Prozentual", "en": "Percentage"}
        self.pdd = {"de": "TDK", "en": "PDD"}
        self.ptw = {"de": "PTW tbaScan", "en": "PTW tbaScan"}
        self.restart = {"de": "Neu starten, um Änderungen\nzu übernehmen!", "en":"Restart the application to\napply the changes!"}
        self.radcalc = {"de": "RadCalc", "en": "RadCalc"}
        self.recent = {"de": "Zuletzt verwendet", "en": "Recent files"}
        self.renamet = {"de": "Titel ändern", "en": "Rename title"}
        self.renamex = {"de": "X-Achse umbenennen", "en": "Rename X-axis"}
        self.renamey = {"de": "Y-Achse umbenennen", "en": "Rename Y-axis"}
        self.renameplot = {"de": "Linie umbenennen", "en": "Rename plot"}
        self.plotselector = {"de": "Linie auswählen:", "en": "Select plot:"}
        self.revert = {"de": "Rückgängig", "en": "Undo"}
        self.reset = {"de": "Zurücksetzen", "en": "Reset"}
        self.resetcolors = {"de": "Farbschema zurücksetzen", "en": "Reset color scheme"}
        self.resetmarkers = {
            "de": "Markerstil zurücksetzen",
            "en": "Reset marker styles",
        }
        self.save = {"de": "Graph abspeichern", "en": "Save graph"}
        self.scanaxis = {
            "de": "Scanrichtung: [X = Ja | Y = Nein]",
            "en": "Scan axis: [X = Yes | Y = No]",
        }
        self.lowerthreshold = {"de": "Dosislimit", "en": "Dose threshold"}
        self.difference = {"de": "Differenzplot", "en": "Plot difference"}
        self.plotgamma = {"de": "Gamma-Plot", "en": "Plot gamma"}
        self.showtable = {"de": "Wertetabelle anzeigen", "en": "Show parameter table"}
        self.select = {"de": "Messungen auswählen ...", "en": "Select measurements ..."}
        
        self.showerror = {"de": "Fehler", "en": "Errorbars"}
        self.showgrid = {"de": "Raster anzeigen", "en": "Show grid"}
        self.gridoptions1 = {"de": "Große Gitterlinien", "en": "Large gridlines"}
        self.gridoptions2 = {"de":"Alle Gitterlinien", "en":"All gridlines"}
        self.showlegend = {"de": "Legende anzeigen", "en": "Show legend"}
        self.legendoptions1 = {"de": "Auto", "en": "Auto"}
        self.legendoptions2 = {"de": "Oben Links", "en": "Top left"}
        self.legendoptions3 = {"de": "Oben Rechts", "en": "Top right"}
        self.legendoptions4 = {"de": "Unten Links", "en": "Bottom left"}
        self.legendoptions5 = {"de": "Unten Rechts", "en": "Bottom right"}
        self.simulation = {"de": "Simulation", "en": "Simulation"}
        self.startdark = {"de": "Im dunklen Modus starten", "en": "Start in dark mode"}
        self.submit = {"de": "Fertig", "en": "Submit"}
        self.symmetry = {"de": "Symmetrie", "en": "Symmetry"}
        self.tabnames = {"de": "Tabs", "en": "Tabs"}
        self.reference = {"de": "Referenzlinie:", "en": "Reference plot:"}
        self.test = {"de":"Auswertungslinie:", "en":"Evaluation plot:"}
        self.topas = {"de": "TOPAS Simulationsdateien", "en": "TOPAS Simulation Data"}
        self.topasunit = {"de": "Dosis", "en": "Dose"}
        self.themeselection = {"de": "Farbschema", "en": "Color Scheme"}
        self.view = {"de": "Ansicht", "en": "View"}
        self.window_title = {
            "de": "TopasMC Simulationsauswertung",
            "en": "TopasMC Simulation Analysis",
        }
        self.unsavedchanges = {"de": "Ungespeicherte Daten!\nTab trotzdem schließen?", "en": "Unsaved changes!\nClose tab anyway?"}
        self.unsavedchanges1 = {"de": "Ungespeicherte Daten!\nTrotzdem schließen?", "en": "Unsaved changes!\nClose anyway?"}
        self.untitled = {"de": "Unbenannt", "en": "Untitled"}
        self.zoom = {"de": "Zoomfenster anzeigen", "en": "Show zoom view"}
        self.yes = {"de": "Ja", "en": "Yes"}
        self.no = {"de": "Nein", "en": "No"}
