"""program for single player racecar game - v1
beginning display screen
created by Charlotte"""

import pygame
import time  # access sleep
pygame.init()

# set the size of the display screen
screen = pygame.display.set_mode((640, 480))

# upload racecar icon image in caption
game_icon = pygame.image.load("images/game_icon.png")
pygame.display.set_icon(game_icon)

# set the caption
pygame.display.set_caption("Racecar Game - by Charlotte")

time.sleep(5)  # close display screen after 5 seconds
pygame.quit()
quit()
