"""program for single player racecar game - v2
initialise player car
created by Charlotte"""

import pygame
import time  # access sleep
pygame.init()

# set the size of the display screen
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# upload racecar icon image in caption
game_icon = pygame.image.load("images/game_icon.png")
pygame.display.set_icon(game_icon)

# set the caption
pygame.display.set_caption("Racecar Game - by Charlotte")

bg_color = (0, 0, 0)  # background colour

# create a clock to control the frame rate
clock = pygame.time.Clock()

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

# Set the direction of the car
direction = 0

screen.fill(bg_color)
screen.blit(car_image, car_rect)
pygame.display.flip()

time.sleep(5)  # close display screen after 5 seconds
pygame.quit()
quit()
