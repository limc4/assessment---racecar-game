"""program for single player racecar game - v9
player score
created by Charlotte"""

import pygame
import sys
import math
import random

from pygame import K_SPACE

pygame.init()

# constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FPS = 60

GREY = (128, 128, 128)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (230, 5, 65)
TRANSPARENCY = 100

msg_font = pygame.font.SysFont("lucida console", 20)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

score_tick = pygame.USEREVENT + 1  # unique event ID for score
pygame.time.set_timer(score_tick, 1000)

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

    # npc car images
    car2_surface = pygame.image.load("images/car_2.png").convert_alpha()
    car3_surface = pygame.image.load("images/car_3.png").convert_alpha()
    car4_surface = pygame.image.load("images/car_4.png").convert_alpha()
    car5_surface = pygame.image.load("images/car_5.png").convert_alpha()
    car6_surface = pygame.image.load("images/car_6.png").convert_alpha()

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
        # surface.blit(self.image, (self.x, self.y))
        surface.blit(self.image, self.rect)

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

def message(msg, txt_colour, center_):
    """display messages"""
    txt = msg_font.render(msg, True, txt_colour)

    text_box = txt.get_rect(center=center_)

    screen.blit(txt, text_box)

def main():
    """main loop"""
    # initialise objects
    # two road segments
    road1 = Road(0)
    road2 = Road(-SCREEN_HEIGHT)

    # create the player car object and its internal self.rect
    player_car = Car(player_car_surface, (SCREEN_WIDTH // 2),
                     player_car_surface.get_height(),speed)

    npc_cars = []  # list to store multiple npc cars

    # set the starting position on the object's rect
    player_car.rect.centerx = SCREEN_WIDTH // 2
    player_car.rect.centery = SCREEN_HEIGHT // 2
    direction = 0  # initially isn't turning

    # non-object variables
    score = 0000
    play = True
    game_over = False
    game_paused = False

    while play:
        for event in pygame.event.get():
            # handle X button
            if event.type == pygame.QUIT:
                if not game_paused and not game_over:
                    # first click: pause the game
                    game_paused = True
                    break  # stop checking other events in the list
                elif game_paused or game_over:
                    # second click (or clicking while crashed): actually quit
                    play = False
                    break
            elif event.type == score_tick:
                if not game_paused and not game_over:
                    score += 1  # increase score every second

            # handle keyboard
            if event.type == pygame.KEYDOWN:
                # SPACE to resume
                if event.key == pygame.K_SPACE:
                    game_paused = False

                # 'r' to restart
                elif event.key == pygame.K_r:
                    main()

                # 'q' to quit
                elif event.key == pygame.K_q:
                    play = False

        if not game_paused and not game_over:
            # update roads
            road1.update()
            road2.update()

            # check if road segments need to "leapfrog"
            if road1.y >= SCREEN_HEIGHT:
                road1.y = road2.y - SCREEN_HEIGHT
            if road2.y >= SCREEN_HEIGHT:
                road2.y = road1.y - SCREEN_HEIGHT

            # if last car has driven at least 200 pixels up from the bottom
            if len(npc_cars) == 0 or npc_cars[-1].y < (SCREEN_HEIGHT - 350):
                x_options = [SCREEN_WIDTH // 6, (SCREEN_WIDTH // 6 * 3),
                             (SCREEN_WIDTH // 6 * 5)]
                x_choice = random.choice(x_options)

                # randomize npc car image
                car_options = [car2_surface, car3_surface, car4_surface,
                               car5_surface, car6_surface]
                car_choice = random.choice(car_options)
                og_image_npc = car_choice

                # resize npc car image
                npc_surface = pygame.transform.scale(og_image_npc,
                                                     (70, 140))

                # pass SCREEN_HEIGHT + 10 as starting y
                npc_cars.append(Car(npc_surface, x_choice, SCREEN_HEIGHT + 10,
                                    random.randint(3, 8)))

            # update or remove npc cars
            for car in npc_cars[:]:
                car.update()  # math happens here

                # check for collision
                if player_car.rect.inflate(-20, -20).colliderect(
                        car.rect.inflate(-10, -10)):
                    game_over = True

                # remove cars if they leave the screen
                if car.y < -140:
                    npc_cars.remove(car)

            # update car
            direction = Car.car_turn(player_car, direction)

        # draw things all the time while play
        screen.fill(GREY)

        # draw roads first (background)
        road1.draw(screen)
        road2.draw(screen)

        # draw npc cars second
        for car in npc_cars[:]:
            car.draw(screen)

        # draw car third (foreground)
        screen.blit(player_car.image, player_car.rect)

        # update score
        message(str(f"Score: {score:04}"), WHITE, (550, 25))

        if game_over:
            grey_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            grey_screen.set_alpha(TRANSPARENCY)  # make grey transparent
            screen.blit(grey_screen, (0, 0))

            message(f"You crashed! Your score was {score}", RED,
                    (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
            message("Press 'r' to restart or the", WHITE,
                    (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            message("top right X button to exit.", WHITE,
                    (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))

        if game_paused:
            grey_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            grey_screen.set_alpha(TRANSPARENCY)  # make grey transparent
            screen.blit(grey_screen, (0, 0))

            instructions1 = "Exit: click X again or"
            instructions2 = "'q' to quit, SPACE to resume,"
            instructions3 = "'r' to reset"
            message(instructions1, WHITE, (SCREEN_WIDTH // 2,
                                          SCREEN_HEIGHT // 2 - 20))
            message(instructions2, WHITE, (SCREEN_WIDTH // 2,
                                           SCREEN_HEIGHT // 2))
            message(instructions3, WHITE, (SCREEN_WIDTH // 2,
                                           SCREEN_HEIGHT // 2 + 20))

        # refresh screen
        pygame.display.flip()
        clock.tick(FPS)

# main routine
if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()
