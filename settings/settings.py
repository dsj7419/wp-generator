import json
import os

class Settings:
    def __init__(self):
        self.appdata_path = os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'WPGenerator')
        os.makedirs(self.appdata_path, exist_ok=True)
        self.settings_file = os.path.join(self.appdata_path, 'settings.json')

        # Define the image size
        self.width = 3840
        self.height = 1080

        # Define parameters for the stars
        self.min_star_diameter = 1
        self.max_star_diameter = 5
        self.num_stars = 3000

        # Define parameters for the galaxies
        self.num_galaxies = 50
        self.min_galaxy_diameter = 40
        self.max_galaxy_diameter = 80

        # Define parameters for the shooting stars
        self.num_shooting_stars = 2
        self.shooting_star_length = 100

        # Define colors for the stars (these are RGB tuples)
        self.colors = [(255, 255, 255), (255, 240, 220), (255, 220, 180), (180, 220, 255)]

        # Define the save path
        self.save_path = self.load_save_path()

    def load_save_path(self):
        default_save_path = self.appdata_path
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as f:
                settings = json.load(f)
                if "save_path" in settings:
                    return settings["save_path"]
        return default_save_path

    def save_settings(self):
        settings = {"save_path": self.save_path}
        with open(self.settings_file, 'w') as f:
            json.dump(settings, f)
