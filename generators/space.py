from PIL import Image, ImageDraw
import numpy as np
import noise
from logger.logger import Logger


class Space:
    def __init__(self, logger, settings):
        self.logger = logger
        self.settings = settings
        self.space_settings = self.settings.load_space_settings()

    def generate(self):
        self.logger.log_info('Generating space image...')

        try:
            # Save the updated settings before generating the image
            self.settings.save_space_settings(self.space_settings)

            settings = self.settings  # Use the settings object directly

            # Create a new image with a black background
            image = Image.new('RGB', (settings.width, settings.height), 'black')
            draw = ImageDraw.Draw(image)

            # Function to draw stars with a twinkle
            def draw_star(x, y, diameter, color, draw):
                # Draw the star
                draw.ellipse([(x, y), (x + diameter, y + diameter)], fill=color)

                # Draw the twinkling effect
                if diameter > 2:
                    for _ in range(4):
                        dx = np.random.normal(scale=diameter)
                        dy = np.random.normal(scale=diameter)
                        draw.line([(x + dx, y + dy), (x + dx + diameter / 2, y + dy + diameter / 2)], fill=color)

            # Generate the stars
            for _ in range(settings.num_stars):
                # Determine the position and size of the star
                x_pos = np.random.randint(0, settings.width)
                y_pos = np.random.randint(0, settings.height)
                star_diameter = np.random.randint(settings.min_star_diameter, settings.max_star_diameter)
                star_color = settings.colors[
                    star_diameter - settings.min_star_diameter]  # assign color based on size

                # Draw the star
                draw_star(x_pos, y_pos, star_diameter, star_color, draw)

            # Generate the galaxies
            if settings.is_space_setting_enabled("galaxies"):
                num_galaxies = int(self.space_settings.get("num_galaxies", 0))
                min_galaxy_diameter = int(self.space_settings.get("min_galaxy_diameter", 0))
                max_galaxy_diameter = int(self.space_settings.get("max_galaxy_diameter", 0))
                colors = self.space_settings.get("colors", [])

                for _ in range(num_galaxies):
                    # Determine the position and size of the galaxy
                    x_pos = np.random.randint(0, settings.width)
                    y_pos = np.random.randint(0, settings.height)
                    galaxy_diameter = np.random.randint(min_galaxy_diameter, max_galaxy_diameter)

                    # Draw the galaxy with a radial gradient
                    for i in range(galaxy_diameter):
                        draw.ellipse([(x_pos - i, y_pos - i), (x_pos + i, y_pos + i)],
                                     outline=(255, 255, 255, max(0, 255 - i * 3)))

            # Generate the shooting stars
            if settings.is_space_setting_enabled("shooting_stars"):
                num_shooting_stars = int(self.space_settings.get("num_shooting_stars", 0))
                shooting_star_length = int(self.space_settings.get("shooting_star_length", 0))

                for _ in range(num_shooting_stars):
                    # Determine the start position and direction of the shooting star
                    x_pos = np.random.randint(0, settings.width)
                    y_pos = np.random.randint(0, settings.height)
                    angle = np.random.uniform(0, 2 * np.pi)

                    # Draw the shooting star as a fading line
                    for i in range(shooting_star_length):
                        x_offset = int(i * np.cos(angle))
                        y_offset = int(i * np.sin(angle))
                        draw.line([(x_pos + x_offset, y_pos + y_offset), (x_pos + x_offset + 1, y_pos + y_offset + 1)],
                                  fill=(255, 255, 255, max(0, 255 - i * 5)))

            # Generate the space background using Perlin noise
            if settings.is_space_setting_enabled("perlin_noise"):
                perlin_octaves = int(self.space_settings.get("perlin_octaves", 0))
                perlin_persistence = float(self.space_settings.get("perlin_persistence", 0.0))
                perlin_scale = int(self.space_settings.get("perlin_scale", 0))

                noise_array = self.generate_perlin_noise(perlin_octaves, perlin_persistence, perlin_scale, settings)
                self.draw_space_background(noise_array, draw, settings)

            self.logger.log_info('Space image generated successfully.')
            return image

        except Exception as e:
            error_message = f'Error occurred while generating space image: {str(e)}'
            self.logger.log_error(error_message)
            raise

    def generate_perlin_noise(self, octaves, persistence, scale, settings):
        # Generate Perlin noise for the space background
        noise_array = np.zeros((settings.width, settings.height))

        for x in range(settings.width):
            for y in range(settings.height):
                noise_value = noise.snoise2(
                    x / scale,
                    y / scale,
                    octaves=octaves,
                    persistence=persistence
                )
                noise_array[x, y] = noise_value

        return noise_array

    def draw_space_background(self, noise_array, draw, settings):
        # Draw the space background using the Perlin noise
        for x in range(settings.width):
            for y in range(settings.height):
                value = int((noise_array[x, y] + 1) * 127.5)
                color = (value, value, value)
                draw.point((x, y), fill=color)

    def enable_space_setting(self, setting_name):
        # Enable Space generator setting
        self.settings.enable_space_setting(setting_name)

    def disable_space_setting(self, setting_name):
        # Disable Space generator setting
        self.settings.disable_space_setting(setting_name)

    def is_space_setting_enabled(self, setting_name):
        return self.settings.is_space_setting_enabled(setting_name)
