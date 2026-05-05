"""program for single player racecar game - v4ii
car move left and right function
created by Charlotte"""

import pygame
import sys
import math
import time  # access sleep
pygame.init()

# set up and constants
# clock to control the frame rate
clock = pygame.time.Clock()

# set the size of the display screen
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# upload racecar icon image in caption
GAME_ICON = pygame.image.load("images/game_icon.png")
pygame.display.set_icon(GAME_ICON)

# set the caption
pygame.display.set_caption("Racecar Game - by Charlotte")

GREY = (50, 50, 50)  # background colour
ROAD = pygame.image.load("images/road2.png")  # background image

try:
    og_image = pygame.image.load("images/car_1.png").convert_alpha()
    og_width, og_height = og_image.get_size()

    # optional: rescale images
    new_width = 70
    new_height = 140
    resized_image = pygame.transform.scale(og_image, (new_width,
                                                      new_height))
    car_image = resized_image
    car_rect = car_image.get_rect()
except:
    print("Error: PNG files were not found! Please check folder!")
    pygame.quit()
    sys.exit()

# set the initial position of the car
car_rect.centerx = SCREEN_WIDTH // 2
car_rect.centery = SCREEN_HEIGHT // 2

speed = 8  # speed of car's turning

direction = 0  # direction of car's movement

# set keys that control car
left_key = pygame.K_LEFT
right_key = pygame.K_RIGHT

def car_turn(current_speed, direction):
    """check if arrow keys are pressed and return direction of car"""
    # check if keys are pressed
    keys = pygame.key.get_pressed()
    if keys[left_key]:
        direction = 180
        current_speed = speed  # Set speed only when key is held
    elif keys[right_key]:
        direction = 0
        current_speed = speed  # Set speed only when key is held

    # update position using current_speed
    dx = current_speed * math.cos(math.radians(direction))
    dy = -current_speed * math.sin(math.radians(direction))

    car_rect.centerx += dx
    car_rect.centery += dy

    # Keep the car within the screen bounds
    if car_rect.left < 0:
        car_rect.left = 0
    elif car_rect.right > SCREEN_WIDTH:
        car_rect.right = SCREEN_WIDTH
    if car_rect.top < 0:
        car_rect.top = 0
    elif car_rect.bottom > SCREEN_HEIGHT:
        car_rect.bottom = SCREEN_HEIGHT

    return car_rect.centerx, car_rect.centery

# main routine
while True: # let user quit
    for event in pygame.event.get():
        # if user presses X button, game quits
        if event.type == pygame.QUIT:
            print("quit")
            pygame.quit()
            sys.exit()

    # start with 0 movement every frame
    current_speed = 0
    car_rect.centerx, car_rect.centery = car_turn(current_speed, direction)

    # Draw the background and car
    screen.fill(GREY)
    screen.blit(ROAD, (0, 0))
    screen.blit(car_image, car_rect)
    pygame.display.flip()

    pygame.display.update()
    clock.tick(60)  # 60 fps
