import json
import os


class ProfileHandler:
    def __init__(self):

        self.profile_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                os.pardir,
                "resources",
                "profile.json",)
        
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
