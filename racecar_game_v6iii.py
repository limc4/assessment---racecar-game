"""program for single player racecar game - v6iii
allow user to use the up and down arrow keys to move
created by Charlotte"""

import pygame
import sys
import math
import random

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
up_key = pygame.K_UP
down_key = pygame.K_DOWN

speed = 8  # speed of car's turning

try:
    # icon and title
    game_icon = pygame.image.load("images/game_icon.png")
    pygame.display.set_icon(game_icon)
    pygame.display.set_caption("Racecar Game - by Charlotte")

    # road image (should be 640x480 for best results)
    ROAD_SURFACE = pygame.image.load("images/road_.png").convert()

    # car image
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
        """move road down screen"""
        self.y += self.speed

    def draw(self, surface):
        """draw road on screen"""
        surface.blit(self.image, (self.x, self.y))

class Car:
    def __init__(self, image, car_x, car_y, speed_):

        self.image = image
        # pick a random lane on the road
        self.x = car_x

        # start car at car_y (either below screen or middle of screen)
        self.y = car_y
        self.speed = speed_
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update(self):
        """move car up screen"""
        self.y -= self.speed
        self.rect.y = self.y

    def draw(self, surface):
        """draw image onto screen"""
        surface.blit(self.image, (self.x, self.y))

    def car_turn(self, current_direction):
        """handle car movement and return updated position"""
        current_speed = 0
        keys = pygame.key.get_pressed()

        if keys[left_key]:
            current_direction = 180
            current_speed = self.speed
        elif keys[right_key]:
            current_direction = 0
            current_speed = self.speed
        elif keys[up_key]:
            current_direction = 90
            current_speed = self.speed
        elif keys[down_key]:
            current_direction = 270
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
    """main loop"""
    # initialise objects
    # two road segments
    road1 = Road(0)
    road2 = Road(-SCREEN_HEIGHT)

    # create the object and its internal self.rect
    player_car = Car(player_car_surface, (SCREEN_WIDTH // 2),
                     player_car_surface.get_height(),speed)

    npc_cars = []  # list to store multiple npc cars

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

        # if last car has driven at least 200 pixels up from the bottom
        if len(npc_cars) == 0 or npc_cars[-1].y < (SCREEN_HEIGHT - 400):
            x_options = [SCREEN_WIDTH // 6, (SCREEN_WIDTH // 6 * 3),
                         (SCREEN_WIDTH // 6 * 5)]
            x_choice = random.choice(x_options)

            # randomize npc car image
            car_numbers = [2, 3, 4, 5, 6]
            car_choice = random.choice(car_numbers)

            og_image2 = pygame.image.load(
                f"images/car_{car_choice}.png").convert_alpha()

            # resize npc car image
            npc_surface = pygame.transform.scale(og_image2, (70, 140))

            # pass SCREEN_HEIGHT + 10 as starting y
            npc_cars.append(Car(npc_surface, x_choice, SCREEN_HEIGHT + 10,
                                random.randint(3, 8)))

        # draw things
        screen.fill(GREY)

        # draw roads first (background)
        road1.draw(screen)
        road2.draw(screen)

        # update or remove npc cars
        for car in npc_cars[:]:
            car.update()
            car.draw(screen)

            # remove cars if they leave the screen
            if car.y < 0:
                npc_cars.remove(car)

        # update car
        direction = Car.car_turn(player_car, direction)

        # check if road segments need to "leapfrog"
        if road1.y >= SCREEN_HEIGHT:
            road1.y = road2.y - SCREEN_HEIGHT
        if road2.y >= SCREEN_HEIGHT:
            road2.y = road1.y - SCREEN_HEIGHT

        # draw car second (foreground)
        screen.blit(player_car.image, player_car.rect)

        # refresh screen
        pygame.display.flip()
        clock.tick(FPS)

# main routine
if __name__ == "__main__":
    main()
