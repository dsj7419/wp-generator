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
max_star_diameter = 5
num_stars = 3000

# Define parameters for the galaxies
num_galaxies = 100
min_galaxy_diameter = 15
max_galaxy_diameter = 40

# Define parameters for the shooting stars
num_shooting_stars = 5
shooting_star_length = 100

# Define colors for the stars (these are RGB tuples)
colors = [(255, 255, 255), (255, 240, 220), (255, 220, 180), (180, 220, 255)]

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
for _ in range(num_stars):
    # Determine the position and size of the star
    x_pos = np.random.randint(0, width)
    y_pos = np.random.randint(0, height)
    star_diameter = np.random.randint(min_star_diameter, max_star_diameter)
    star_color = colors[star_diameter - min_star_diameter] # assign color based on size

    # Draw the star
    draw_star(x_pos, y_pos, star_diameter, star_color, draw)

# Generate the galaxies
for _ in range(num_galaxies):
    # Determine the position and size of the galaxy
    x_pos = np.random.randint(0, width)
    y_pos = np.random.randint(0, height)
    galaxy_diameter = np.random.randint(min_galaxy_diameter, max_galaxy_diameter)

    # Draw the galaxy as a faint, fuzzy point
    for i in range(galaxy_diameter):
        draw.ellipse([(x_pos - i/2, y_pos - i/2), (x_pos + i/2, y_pos + i/2)], fill=(255, 255, 255, 255 - i*5))

# Generate the shooting stars
for _ in range(num_shooting_stars):
    # Determine the start position and direction of the shooting star
    x_pos = np.random.randint(0, width)
    y_pos = np.random.randint(0, height)
    angle = np.random.uniform(0, 2*np.pi)

    # Draw the shooting star as a fading line
    for i in range(shooting_star_length):
        x_offset = int(i * np.cos(angle))
        y_offset = int(i * np.sin(angle))
        draw.line([(x_pos + x_offset, y_pos + y_offset), (x_pos + x_offset + 1, y_pos + y_offset + 1)], fill=(255, 255, 255, 255 - i*2))

# Save the image
image.save("background.jpeg")
