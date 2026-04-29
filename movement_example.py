import pygame
import math
import sys

# Initialize pygame
pygame.init()

# Set the window size and caption
screen_width, screen_height = 640, 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Example racing car')

# Set the background color
bg_color = (0, 0, 0)

# Create a clock to control the frame rate
clock = pygame.time.Clock()

# Load the original image
original_image = pygame.image.load("images/car_1.png")

# Get the dimensions of the original image
original_width, original_height = original_image.get_size()

# Set the desired width and height for the resized image
new_width = 50
new_height = 100

# Resize the image using the transform.scale() function
resized_image = pygame.transform.scale(original_image, (new_width, new_height))

# The resized image is now stored in the resized_image surface

# Create a car sprite
car_image = resized_image
car_rect = car_image.get_rect()

 # Set the initial position of the car
car_rect.centerx = screen_width // 2
car_rect.centery = screen_height // 2
# Set the speed of the car
speed = 5

# Set the direction of the car
direction = 0

# Set the keys that control the car
up_key = pygame.K_UP
down_key = pygame.K_DOWN
left_key = pygame.K_LEFT
right_key = pygame.K_RIGHT

# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
       if event.type == pygame.QUIT:

           pygame.quit()
           sys.exit()

    # Check if the up or down keys are pressed
    keys = pygame.key.get_pressed()
    if keys[up_key]:
        direction = 90
    elif keys[down_key]:
       direction = 270
    elif keys[left_key]:
       direction = 180
    elif keys[right_key]:
       direction = 0

    # Update the position of the car based on the direction and speed
    dx, dy = speed * math.cos(math.radians(direction)), -speed * math.sin(math.radians(direction))
    car_rect.centerx += dx
    car_rect.centery += dy

   # Keep the car within the screen bounds
    if car_rect.left < 0:
       car_rect.left = 0
    elif car_rect.right > screen_width:
       car_rect.right = screen_width
    if car_rect.top < 0:
       car_rect.top = 0
    elif car_rect.bottom > screen_height:
       car_rect.bottom = screen_height

    # Draw the background and car
    screen.fill(bg_color)
    screen.blit(car_image, car_rect)
    pygame.display.flip()

    # Limit the frame rate to 60 FPS
    clock.tick(60)
