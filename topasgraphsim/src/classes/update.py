import webbrowser
from tkinter import simpledialog as sd

import requests

from .profile import ProfileHandler


class CheckForUpdates:
    def __init__(self):

        currentVersion = "18.1.1"
        try:
            newestVersion = requests.get(
                "https://api.github.com/repos/sebasj13/topasgraphsim/releases/latest"
            ).json()["name"][1:]
        except Exception:
            return

        self.update = {
            "de": f"Eine neue Version ({newestVersion}) von TopasGraphSim ist verfügbar.\nAnsehen?",
            "en": f"A new version ({newestVersion}) of TopasGraphSim is available!\nView?",
        }

        if currentVersion != newestVersion:
            dialog = sd.messagebox.askokcancel(
                "", message=self.update[ProfileHandler().get_attribute("language")]
            )

            if dialog == True:
                try:
                    webbrowser.open("https://pypi.org/project/topasgraphsim/")
                except Exception:
                    return
