"""program for single player racecar game - v4i
car move left and right
created by Charlotte"""

import pygame
import sys
import math
import time  # access sleep
pygame.init()

# create a clock to control the frame rate
clock = pygame.time.Clock()

# set the size of the display screen
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# upload racecar icon image in caption
game_icon = pygame.image.load("images/game_icon.png")
pygame.display.set_icon(game_icon)

# set the caption
pygame.display.set_caption("Racecar Game - by Charlotte")

grey = (50, 50, 50)  # background colour

road = pygame.image.load("images/road.png")

# resize car image
og_image = pygame.image.load("images/car_1.png").convert_alpha()
og_width, og_height = og_image.get_size()
new_width = 50
new_height = 100

resized_image = pygame.transform.scale(og_image, (new_width, new_height))

car_image = resized_image
car_rect = car_image.get_rect()

 # Set the initial position of the car
car_rect.centerx = screen_width // 2
car_rect.centery = screen_height // 2

# Set the speed of the car
speed = 5

# set car direction
direction = 0

# set keys that control car
left_key = pygame.K_LEFT
right_key = pygame.K_RIGHT

while True: # let user quit
    for event in pygame.event.get():
        # if user presses X button, game quits
        if event.type == pygame.QUIT:
            print("quit")
            pygame.quit()
            sys.exit()

    # Check if the up or down keys are pressed
    keys = pygame.key.get_pressed()
    if keys[left_key]:
        direction = 180
    elif keys[right_key]:
        direction = 0

    # update position of car based on direction and speed
    dx, dy = speed * math.cos(math.radians(direction)), -speed * math.sin(
        math.radians(direction))
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
    screen.fill(grey)
    screen.blit(road, (0, 0))
    screen.blit(car_image, car_rect)
    pygame.display.flip()

    # Limit the frame rate to 60 FPS
    clock.tick(60)
    pygame.display.update()
    clock.tick(60)
