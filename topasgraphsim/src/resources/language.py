class Text:

    """
    Contains all translatable text in the program.
    """

    def __init__(self):

        self.absolute = {"de": "Absolut", "en": "Absolute"}
        self.about = {"de": "Über TGS", "en": "About"}
        self.add = {"de": "Daten hinzufügen", "en": "Add Data"}
        self.axis = {"de": "Achse", "en": "Axis"}
        self.calcfail = {
            "de": "Parameter konnten nicht berechnen werden!",
            "en": "Parameters could not be calculated!",
        }
        self.calcparams = {"de": "Parameter berechnen", "en": "Calculate parameters"}
        self.caxcorrection = {
            "de": "Zentralstrahlkorrektur",
            "en": "Center axis correction",
        }
        self.centeraxis = {"de": "Zentralstrahl", "en": "Center axis"}
        self.changefilename = {"de": "Neuer Name:", "en": "New Name:"}
        self.changeerr = {"de": "Darstellung ändern", "en": "Switch view"}
        self.choosenormalization = {"de": "Normieren auf ...", "en": "Normalize to ..."}
        self.close = {
            "de": "Derzeitige Ansicht schließen",
            "en": "Close current project",
        }
        self.closeprompt = {
            "de": "Graph wurde noch nicht gespeichert. Trotzdem Schließen?",
            "en": "Graph was not saved. Close anyways?",
        }
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
        self.dp = {"de": "Dosisquerverteilung", "en": "Dose profile"}
        self.egs = {"de": "EGS Simulationsdateien", "en": "EGS Simulation Data"}
        self.egsunit = {"de": "Dosis [Gy/Historie]", "en": "Dose [Gy/History]"}
        self.end = {"de": "Beenden", "en": "Close"}
        self.english = {"de": "Englisch", "en": "English"}
        self.error = {"de": "Abweichung", "en": "Difference"}
        self.errorbars = {"de": "Fehlerbalken anzeigen", "en": "Show error bars"}
        self.errlimmenu = {"de": "Fehlergrenze einstellen", "en": "Change error limits"}
        self.file = {"de": "Datei", "en": "File"}
        self.flank = {"de": "Flanke", "en": "Flank"}
        self.fullscreen = {"de": "Vollbild", "en": "Fullscreen"}
        self.fwhm = {"de": "HWB", "en": "FWHM"}
        self.german = {"de": "Deutsch", "en": "German"}
        self.half = {"de": "Halbe Querverteilung anzeigen", "en": "Show half profile"}
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
        self.languageset = {
            "en": "Das geöffnete Projekt wird geschlossen. Fortfahren?",
            "de": "The current project will be closed. Continue?",
        }
        self.light = {"de": "Hell", "en": "Light"}
        self.loadmeasurement = {"de": "Messung laden", "en": "Load measurement"}
        self.loadsim = {"de": "Simulationsergebnis laden", "en": "Load simulation"}

        self.marker = {"de": "Symbolgröße", "en": "Marker Size"}
        self.markerline = {"de": "Liniendicke", "en": "Line Width"}
        self.measurement = {"de": "Messung", "en": "Measurement"}
        self.measurementdata = {"de": "Messdaten", "en": "Measurement Data"}
        self.maximum = {"de": "Maximum", "en": "Maximum"}
        self.normalize = {"de": "Normieren", "en": "Normalize"}
        self.normunit = {"de": "Relative Dosis", "en": "Relative Dose"}
        self.normalization = {"de": "Normierung", "en": "Normalization"}
        self.options = {"de": "Optionen", "en": "Options"}
        self.orr = {"de": "oder", "en": "or"}
        self.percentage = {"de": "Prozentual", "en": "Percentage"}
        self.pdd = {"de": "Tiefendosiskurve", "en": "Depth dose"}
        self.ptw = {"de": "PTW tbaScan", "en": "PTW tbaScan"}
        self.revert = {"de": "Rückgängig", "en": "Undo"}
        self.reset = {"de": "Zurücksetzen", "en": "Reset"}
        self.resetcolors = {"de": "Farbschema zurücksetzen", "en": "Reset colorscheme"}
        self.save = {"de": "Graph abspeichern", "en": "Save graph"}
        self.scanaxis = {
            "de": "Scanrichtung: [X = Ja | Y = Nein]",
            "en": "Scan axis: [X = Yes | Y = No]",
        }
        self.simulation = {"de": "Simulation", "en": "Simulation"}
        self.startdark = {"de": "Im dunklen Modus starten", "en": "Start in dark mode"}
        self.submit = {"de": "Fertig", "en": "Submit"}
        self.symmetry = {"de": "Symmetrie", "en": "Symmetry"}
        self.topas = {"de": "TOPAS Simulationsdateien", "en": "TOPAS Simulation Data"}
        self.topasunit = {"de": "Dosis", "en": "Dose"}
        self.view = {"de": "Ansicht", "en": "View"}
        self.window_title = {
            "de": "TopasMC Simulationsauswertung",
            "en": "TopasMC Simulation Analysis",
        }
        self.zoom = {"de": "Zoomfenster anzeigen", "en": "Show zoom view"}
