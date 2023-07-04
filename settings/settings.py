import json
import os
from logger.logger import Logger


class Settings:
    def __init__(self):
        self.logger = None
        self.appdata_path = os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'WPGenerator')
        os.makedirs(self.appdata_path, exist_ok=True)
        self.settings_file = os.path.join(self.appdata_path, 'settings.json')

        # Define the image size
        self.width = 3840
        self.height = 1080

        # Define parameters for the stars
        self.min_star_diameter = 1
        self.max_star_diameter = 5
        self.num_stars = 500

        # Define parameters for the galaxies
        self.num_galaxies = 20
        self.min_galaxy_diameter = 10
        self.max_galaxy_diameter = 50

        # Define parameters for the shooting stars
        self.num_shooting_stars = 2
        self.shooting_star_length = 60

        # Define colors for the stars (these are RGB tuples)
        self.colors = [(255, 255, 255), (255, 240, 220), (255, 220, 180), (180, 220, 255)]

        # Define parameters for Perlin noise
        self.perlin_octaves = 16
        self.perlin_persistence = 0.1
        self.perlin_scale = 10

        # Define the save path
        self.save_path = self.load_save_path()

        # Initialize logging
        self.initialize_logging()

    def load_save_path(self):
        default_save_path = self.appdata_path
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    if "save_path" in settings:
                        save_path = settings["save_path"]
                        if self.validate_save_path(save_path):
                            return save_path
            except json.JSONDecodeError:
                pass  # Handle the JSON decoding error here

        # Create a new settings file with default values
        settings = {
            "save_path": default_save_path,
        }
        with open(self.settings_file, 'w') as f:
            json.dump(settings, f)

        return default_save_path

    def save_settings(self, settings):
        abs_settings_file = os.path.abspath(self.settings_file)
        settings_copy = settings.copy()
        settings_copy.pop('logger', None)  # Remove the 'logger' attribute
        with open(abs_settings_file, 'w') as f:
            json.dump(settings_copy, f)

    def validate_save_path(self, save_path):
        # Validate the save path
        if not os.path.isabs(save_path):
            return False
        if not os.path.exists(save_path):
            try:
                os.makedirs(save_path)
            except Exception:
                return False
        return True

    def initialize_logging(self):
        log_dir = os.path.join(self.appdata_path, 'logs')
        os.makedirs(log_dir, exist_ok=True)

        log_file = os.path.join(log_dir, 'app.log')

        logger = Logger()
        logger.configure_logging()
        logger.log_info('Application started')

        # Add the logger instance to the settings
        self.logger = logger

    # Methods for generator-specific settings

    def save_space_settings(self, settings):
        # Save Space generator settings to the settings file
        abs_settings_file = os.path.abspath(self.settings_file)
        with open(abs_settings_file, 'r') as f:
            settings_data = json.load(f)

        settings_data['space_settings'] = settings

        with open(abs_settings_file, 'w') as f:
            json.dump(settings_data, f)

    def load_space_settings(self):
        # Load Space generator settings from the settings file
        abs_settings_file = os.path.abspath(self.settings_file)
        with open(abs_settings_file, 'r') as f:
            settings_data = json.load(f)

        return settings_data.get('space_settings', {})

    def enable_space_setting(self, setting_name):
        # Enable Space generator setting
        space_settings = self.load_space_settings()
        space_settings[setting_name + "_enabled"] = True
        self.save_space_settings(space_settings)

    def disable_space_setting(self, setting_name):
        # Disable Space generator setting
        space_settings = self.load_space_settings()
        space_settings[setting_name + "_enabled"] = False
        self.save_space_settings(space_settings)

    def is_space_setting_enabled(self, setting_name):
        space_settings = self.load_space_settings()
        return space_settings.get(setting_name + "_enabled", False)
