from PIL import Image, ImageDraw
import numpy as np

# Define the image size
width = 3840
height = 1080

# Create a new image with a black background
image = Image.new('RGB', (width, height), 'black')
draw = ImageDraw.Draw(image)

# Define parameters for the stars
min_star_diameter = 1
max_star_diameter = 3
num_stars = 5000

# Generate the stars
for _ in range(num_stars):
    # Determine the position and size of the star
    x_pos = np.random.randint(0, width)
    y_pos = np.random.randint(0, height)
    star_diameter = np.random.randint(min_star_diameter, max_star_diameter)

    # Draw the star
    draw.ellipse([(x_pos, y_pos), (x_pos + star_diameter, y_pos + star_diameter)], fill='white')

# Save the image
image.save("background.jpeg")
