"""program for single player racecar game - v5
scrolling road and car movement
Created by Charlotte"""

import pygame
import sys
import math

pygame.init()

# constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

GREY = (50, 50, 50)

try:
    # Icon and Title
    game_icon = pygame.image.load("images/game_icon.png")
    pygame.display.set_icon(game_icon)
    pygame.display.set_caption("Racecar Game - by Charlotte")

    # Road Image (Should be 640x480 for best results)
    ROAD_SURFACE = pygame.image.load("images/road_.png").convert()

    # Car Image
    og_image = pygame.image.load("images/car_1.png").convert_alpha()
    car_image = pygame.transform.scale(og_image, (70, 140))
    car_rect = car_image.get_rect()
except Exception as e:
    print(f"Error loading assets: {e}")
    pygame.quit()
    sys.exit()

class Road:
    def __init__(self, y_pos):
        self.image = ROAD_SURFACE
        self.x = 0
        self.y = y_pos
        self.speed = 5

    def update(self):
        # Move down
        self.y += self.speed

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

def car_turn(rect, current_direction):
    """Handles car movement and returns updated position"""
    current_speed = 0
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        current_direction = 180
        current_speed = 8
    elif keys[pygame.K_RIGHT]:
        current_direction = 0
        current_speed = 8

    # calculate movement
    dx = current_speed * math.cos(math.radians(current_direction))
    dy = -current_speed * math.sin(math.radians(current_direction))

    car_rect.centerx += dx
    car_rect.centery += dy

    # check boundaries of screen
    if car_rect.left < 0: rect.left = 0
    if car_rect.right > SCREEN_WIDTH: rect.right = SCREEN_WIDTH

    return current_direction

def main():
    # initialise objects
    # two road segments
    road1 = Road(0)
    road2 = Road(-SCREEN_HEIGHT)

    # set car position
    car_rect.centerx = SCREEN_WIDTH // 2
    car_rect.centery = SCREEN_HEIGHT // 2
    direction = 0

    while True:
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # update roads
        road1.update()
        road2.update()

        # check if road segments need to "leapfrog"
        if road1.y >= SCREEN_HEIGHT:
            road1.y = road2.y - SCREEN_HEIGHT
        if road2.y >= SCREEN_HEIGHT:
            road2.y = road1.y - SCREEN_HEIGHT

        # update car
        direction = car_turn(car_rect, direction)

        # draw things
        screen.fill(GREY)

        # draw roads first (background)
        road1.draw(screen)
        road2.draw(screen)

        # draw car second (foreground)
        screen.blit(car_image, car_rect)

        # refresh screen
        pygame.display.flip()
        clock.tick(FPS)

# main routine
if __name__ == "__main__":
    main()
