class Settings:
    def __init__(self):
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