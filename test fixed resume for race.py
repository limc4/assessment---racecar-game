import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# --- CONSTANTS ---
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FPS = 60

GREY = (128, 128, 128)
WHITE = (255, 255, 255)
RED = (230, 5, 65)

# Fonts
msg_font = pygame.font.SysFont("lucida console", 20)

# Setup Display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# --- ASSETS ---
try:
    pygame.display.set_caption("Racecar Game - by Charlotte")

    # Road
    ROAD_SURFACE = pygame.image.load("images/road_.png").convert()

    # Player Car
    og_image = pygame.image.load("images/car_1.png").convert_alpha()
    player_car_surface = pygame.transform.scale(og_image, (70, 140))

    # NPC Car Options
    car_options = [
        pygame.image.load(f"images/car_{i}.png").convert_alpha()
        for i in range(2, 7)
    ]
except Exception as e:
    print(f"Error loading images: {e}")
    pygame.quit()
    sys.exit()


# --- CLASSES ---

class Road:
    def __init__(self, y_position):
        self.image = ROAD_SURFACE
        self.x = 0
        self.y = y_position
        self.speed = 5

    def update(self):
        self.y += self.speed

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))


class Car:
    def __init__(self, image, car_x, car_y, speed_):
        self.image = image
        self.speed = speed_
        self.rect = self.image.get_rect(topleft=(car_x, car_y))

    def update_npc(self):
        """NPCs drive up the screen"""
        self.rect.y -= self.speed

    def car_turn(self, player_speed):
        """Handle player movement"""
        current_speed = 0
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            direction = 180
            current_speed = player_speed
        elif keys[pygame.K_RIGHT]:
            direction = 0
            current_speed = player_speed
        elif keys[pygame.K_UP]:
            direction = 90
            current_speed = player_speed
        elif keys[pygame.K_DOWN]:
            direction = 270
            current_speed = player_speed
        else:
            return  # No key pressed, no movement

        dx = current_speed * math.cos(math.radians(direction))
        dy = -current_speed * math.sin(math.radians(direction))

        self.rect.x += dx
        self.rect.y += dy

        # Screen Bounds
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH: self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT: self.rect.bottom = SCREEN_HEIGHT

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# --- UTILS ---

def message(msg, txt_colour, center_pos):
    txt = msg_font.render(msg, True, txt_colour)
    screen.blit(txt, txt.get_rect(center=center_pos))


# --- MAIN GAME FUNCTION ---

def main():
    road1 = Road(0)
    road2 = Road(-SCREEN_HEIGHT)

    player_car = Car(player_car_surface, SCREEN_WIDTH // 2 - 35,
                     SCREEN_HEIGHT - 160, 8)
    npc_cars = []

    play = True
    game_over = False
    game_paused = False

    while play:
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    game_paused = not game_paused
                elif event.key == pygame.K_r:
                    main()  # Restart
                elif event.key == pygame.K_q:
                    play = False

        # 2. Update Logic (Only if running)
        if not game_paused and not game_over:
            # Update Roads
            road1.update()
            road2.update()
            if road1.y >= SCREEN_HEIGHT: road1.y = road2.y - SCREEN_HEIGHT
            if road2.y >= SCREEN_HEIGHT: road2.y = road1.y - SCREEN_HEIGHT

            # Update Player
            player_car.car_turn(8)

            # Spawn NPCs
            if len(npc_cars) == 0 or npc_cars[-1].rect.y < (
                    SCREEN_HEIGHT - 300):
                x_pos = random.choice(
                    [100, SCREEN_WIDTH // 2 - 35, SCREEN_WIDTH - 170])
                img = pygame.transform.scale(random.choice(car_options),
                                             (70, 140))
                npc_cars.append(
                    Car(img, x_pos, SCREEN_HEIGHT + 10, random.randint(7, 10)))

            # Update NPCs & Collisions
            for car in npc_cars[:]:
                car.update_npc()
                if player_car.rect.inflate(-20, -20).colliderect(
                        car.rect.inflate(-10, -10)):
                    game_over = True
                if car.rect.y < -150:
                    npc_cars.remove(car)

        # 3. Drawing Section (Always draws current state)
        screen.fill(GREY)
        road1.draw(screen)
        road2.draw(screen)

        for car in npc_cars:
            car.draw(screen)

        player_car.draw(screen)

        # 4. Overlays
        if game_over or game_paused:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(150)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

            if game_over:
                message("CRASHED!", RED,
                        (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
                message("Press 'R' to Restart", WHITE,
                        (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
            else:
                message("PAUSED", WHITE,
                        (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
                message("SPACE to Resume | 'R' to Reset", WHITE,
                        (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()