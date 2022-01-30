class Text:

    """
    Contains all translatable text in the program.
    """

    def __init__(self):

        self.add = {"de": "Daten hinzufügen", "en": "Add Data"}
        self.axis = {"de": "Achse", "en": "Axis"}
        self.caxcorrection = {
            "de": "Zentralstrahlkorrektur",
            "en": "Center axis correction",
        }
        self.centeraxis = {"de": "Zentralstrahl", "en": "Center axis"}
        self.changefilename = {"de": "Neuer Name:", "en": "New Name:"}
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
        self.dp = {"de": "Dosisquerverteilung", "en": "Dose profile"}
        self.egs = {"de": "EGS Simulationsdateien", "en": "EGS Simulation Data"}
        self.end = {"de": "Beenden", "en": "Close"}
        self.english = {"de": "Englisch", "en": "English"}
        self.errorbars = {"de": "Fehlerbalken anzeigen", "en": "Show error bars"}
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
        self.normalization = {"de": "Normierung", "en": "Normalization"}
        self.options = {"de": "Optionen", "en": "Options"}
        self.orr = {"de": "oder", "en": "or"}
        self.pdd = {"de": "Tiefendosiskurve", "en": "Depth dose"}
        self.ptw = {"de": "PTW tbaScan", "en": "PTW tbaScan"}
        self.revert = {"de": "Rückgängig", "en": "Undo"}
        self.save = {"de": "Graph abspeichern", "en": "Save graph"}
        self.simulation = {"de": "Simulation", "en": "Simulation"}
        self.startdark = {"de": "Im dunklen Modus starten", "en": "Start in dark mode"}
        self.submit = {"de": "Fertig", "en": "Sumbit"}
        self.symmetry = {"de": "Symmetrie", "en": "Symmetry"}
        self.topas = {"de": "TOPAS Simulationsdateien", "en": "TOPAS Simulation Data"}
        self.view = {"de": "Ansicht", "en": "View"}
        self.window_title = {
            "de": "TopasMC Simulationsauswertung",
            "en": "TopasMC Simulation Analysis",
        }
        self.zoom = {"de": "Zoomfenster anzeigen", "en": "Show zoom view"}
