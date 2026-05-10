"""program for single player racecar game - v6i
Car class with turning function inside
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

# set keys that control car
left_key = pygame.K_LEFT
right_key = pygame.K_RIGHT

speed = 8  # speed of car's turning

try:
    # Icon and Title
    game_icon = pygame.image.load("images/game_icon.png")
    pygame.display.set_icon(game_icon)
    pygame.display.set_caption("Racecar Game - by Charlotte")

    # Road Image (Should be 640x480 for best results)
    ROAD_SURFACE = pygame.image.load("images/road_.png").convert()

    # Car Image
    og_image = pygame.image.load("images/car_1.png").convert_alpha()
    player_car_surface = pygame.transform.scale(og_image, (70, 140))
    player_car_rect = player_car_surface.get_rect()
except Exception as e:
    print(f"Error loading assets: {e}")
    pygame.quit()
    sys.exit()

class Road:
    def __init__(self, y_position):
        self.image = ROAD_SURFACE
        self.x = 0
        self.y = y_position
        self.speed = 5

    def update(self):
        # Move down
        self.y += self.speed

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

class Car:
    def __init__(self, image, speed):
        self.image = image
        self.x = SCREEN_WIDTH
        self.y = SCREEN_HEIGHT - self.image.get_height() - 10
        self.speed = speed
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update(self):
        # move up
        self.y -= self.speed

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def car_turn(self, current_direction):
        """Handles car movement and returns updated position"""
        current_speed = 0
        keys = pygame.key.get_pressed()

        if keys[left_key]:
            current_direction = 180
            current_speed = self.speed
        elif keys[right_key]:
            current_direction = 0
            current_speed = self.speed

        # calculate movement
        dx = current_speed * math.cos(math.radians(current_direction))
        dy = -current_speed * math.sin(math.radians(current_direction))

        self.rect.centerx += dx
        self.rect.centery += dy

        # keep the car within the screen bounds
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH: self.rect.right = SCREEN_WIDTH

        return current_direction

def main():
    # initialise objects
    # two road segments
    road1 = Road(0)
    road2 = Road(-SCREEN_HEIGHT)

    # create the object and its internal self.rect
    player_car = Car(player_car_surface, speed)

    # set the starting position on the object's rect
    player_car.rect.centerx = SCREEN_WIDTH // 2
    player_car.rect.centery = SCREEN_HEIGHT // 2
    direction = 0  # initially isn't turning

    while True:
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # update roads
        road1.update()
        road2.update()

        # update car
        direction = Car.car_turn(player_car, direction)

        # check if road segments need to "leapfrog"
        if road1.y >= SCREEN_HEIGHT:
            road1.y = road2.y - SCREEN_HEIGHT
        if road2.y >= SCREEN_HEIGHT:
            road2.y = road1.y - SCREEN_HEIGHT

        # draw things
        screen.fill(GREY)

        # draw roads first (background)
        road1.draw(screen)
        road2.draw(screen)

        # draw car second (foreground)
        screen.blit(player_car.image, player_car.rect)

        # refresh screen
        pygame.display.flip()
        clock.tick(FPS)

# main routine
if __name__ == "__main__":
    main()
