from tkinter import simpledialog as sd
import requests
import webbrowser
from .profile import ProfileHandler


class CheckForUpdates:
    def __init__(self):

        currentVersion = "17.2.4"
        newestVersion = requests.get(
            "https://api.github.com/repos/sebasj13/topasgraphsim/releases/latest"
        ).json()["name"][1:]

        self.update = {
            "de": f"Eine neue Version ({newestVersion}) von TopasGraphSim ist verfügbar.\nAnsehen?",
            "en": f"A new version ({newestVersion}) of TopasGraphSim is available!\nView?",
        }

        if currentVersion != newestVersion:
            dialog = sd.messagebox.askokcancel(
                "", message=self.update[ProfileHandler().get_attribute("language")]
            )

            if dialog == True:
                webbrowser.open("https://pypi.org/project/topasgraphsim/")
