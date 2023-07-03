from PIL import Image, ImageDraw
import numpy as np

class Space:
    def __init__(self, settings):
        self.settings = settings

    def generate(self):
        # Create a new image with a black background
        image = Image.new('RGB', (self.settings.width, self.settings.height), 'black')
        draw = ImageDraw.Draw(image)

        # Function to draw stars with a twinkle
        def draw_star(x, y, diameter, color, draw):
            # Draw the star
            draw.ellipse([(x, y), (x + diameter, y + diameter)], fill=color)

            # Draw the twinkling effect
            if diameter > 2:
                for i in range(4):
                    dx = np.random.normal(scale=diameter)
                    dy = np.random.normal(scale=diameter)
                    draw.line([(x + dx, y + dy), (x + dx + diameter/2, y + dy + diameter/2)], fill=color)

        # Generate the stars
        for _ in range(self.settings.num_stars):
            # Determine the position and size of the star
            x_pos = np.random.randint(0, self.settings.width)
            y_pos = np.random.randint(0, self.settings.height)
            star_diameter = np.random.randint(self.settings.min_star_diameter, self.settings.max_star_diameter)
            star_color = self.settings.colors[star_diameter - self.settings.min_star_diameter] # assign color based on size

            # Draw the star
            draw_star(x_pos, y_pos, star_diameter, star_color, draw)

        # Generate the galaxies
        for _ in range(self.settings.num_galaxies):
            # Determine the position and size of the galaxy
            x_pos = np.random.randint(0, self.settings.width)
            y_pos = np.random.randint(0, self.settings.height)
            galaxy_diameter = np.random.randint(self.settings.min_galaxy_diameter, self.settings.max_galaxy_diameter)

            # Draw the galaxy with a radial gradient
            for i in range(galaxy_diameter):
                draw.ellipse([(x_pos - i, y_pos - i), (x_pos + i, y_pos + i)], outline=(255, 255, 255, max(0, 255 - i*3)))

        # Generate the shooting stars
        for _ in range(self.settings.num_shooting_stars):
            # Determine the start position and direction of the shooting star
            x_pos = np.random.randint(0, self.settings.width)
            y_pos = np.random.randint(0, self.settings.height)
            angle = np.random.uniform(0, 2*np.pi)

            # Draw the shooting star as a fading line
            for i in range(self.settings.shooting_star_length):
                x_offset = int(i * np.cos(angle))
                y_offset = int(i * np.sin(angle))
                draw.line([(x_pos + x_offset, y_pos + y_offset), (x_pos + x_offset + 1, y_pos + y_offset + 1)], fill=(255, 255, 255, max(0, 255 - i*5)))

            # Save the image
        image.save("background.jpeg")

        # Return the generated image
        return image