import json
import sys
import os


class ProfileHandler:
    def __init__(self):
        
        def resource_path(relative_path):
            """ Get absolute path to resource, works for dev and for PyInstaller """
            if hasattr(sys, '_MEIPASS'):
                return os.path.join(sys._MEIPASS, "TopasGraphSim", relative_path)

            return os.path.join(os.path.abspath("."), relative_path)

        self.profile_path = resource_path(os.path.join(
                "topasgraphsim",
                "src",
                "resources",
                "profile.json"))
        
        self.profile = self.read_data()

    def read_data(self):
        with open(self.profile_path) as profile:
            profile = json.load(profile)
            return profile

    def set_attribute(self, key, value):
        data = self.read_data()
        data[key] = value
        with open(self.profile_path, "w") as profile:
            json.dump(data, profile, indent=4)

    def get_attribute(self, key):
        data = self.read_data()
        value = data[f"{key}"]
        return value
