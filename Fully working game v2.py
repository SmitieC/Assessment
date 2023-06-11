"""Car Assessment Game
Fully working Game
By Conor Smith"""

import pygame
import random
import sys
from pygame.sprite import AbstractGroup

pygame.init()

VELOCITY = 5


# class for player controlled car
class Driver(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.orig_image = pygame.transform.scale(
            pygame.image.load('Assessment/Driver_car.png'), (73, 125))
        self.image = self.orig_image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.angle = 0

    def move_right(self):
        self.angle = -15  # make car look like turning
        if self.x_pos < 700 - VELOCITY:  # check if car is within screen
            self.x_pos += VELOCITY

    def move_left(self):
        self.angle = 15  # make car look like turning
        if self.x_pos > VELOCITY:  # check if car is within screen
            self.x_pos -= VELOCITY

    def move_up(self):
        self.angle = 0  # make car look like straight

    def update(self):  # update car position on screen
        self.image = pygame.transform.rotate(self.orig_image, self.angle)
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.rect = self.rect.clamp(screen.get_rect())


# class for obstacle cars
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.running_sprites = []
        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("Assessment/car_2.png"), (73, 125)))
        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("Assessment/car_3.png"), (73, 125)))
        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("Assessment/car_4.png"), (73, 125)))
        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("Assessment/car_5.png"), (73, 125)))
        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("Assessment/car_6.png"), (73, 125)))

        self.image = random.choice(self.running_sprites)
        if self.x_pos > 400:
            self.image = pygame.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.speed = random.randint(10, 15)
        self.added_to_score = False  # initialize added_to_score to False

    def update(self):
        self.y_pos += self.speed  # Move obstacle downwards
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        if self.y_pos > 950:  # if obstacle is off the screen, kill
            self.kill()

        if not self.added_to_score and self.y_pos >= 750:
            global score
            score += 1
            self.added_to_score = True


# game loop function so game can be restarted
def game_loop():
    # Component 1 To Initialize Screen
    global screen
    screen = pygame.display.set_mode((700, 925))
    pygame.display.set_caption("Car Driving Game")
    game_icon = pygame.image.load('Assessment/game_icon.png')
    pygame.display.set_icon(game_icon)

    # Initialize clock to control frame rate
    clock = pygame.time.Clock()

    # Initialize score and font
    global score
    score = 0
    font = pygame.font.Font(None, 36)

    # Game Variables and constants
    lane_pos = [115, 253, 436, 593]
    player_moved = False

    # Initialize sprites
    road = pygame.image.load('Assessment/Road-1.png')
    road = pygame.transform.rotate(road, 90)
    road = pygame.transform.scale(road, (700, 925))

    driver_group = pygame.sprite.GroupSingle()
    obstacle_group = pygame.sprite.Group()

    driver = Driver(253, 700)
    driver_group.add(driver)

    # Initialize y-position of road
    road_y = -925

    # Game Loop
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open("Assessment/high_score.txt", "r") as f:
                    high_score_str = f.read().strip()
                    # Remove leading/trailing whitespace
                if high_score_str:
                    try:
                        high_score = int(high_score_str)
                    except ValueError:
                        high_score = 0
                else:
                    high_score = 0  # Set to a default value if file is empty
                if score > high_score:
                    high_score = score
                    with open("Assessment/high_score.txt", "w") as f:
                        f.write(str(high_score))
                pygame.quit()
                sys.exit()

        # Handle input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            driver.move_right()
            player_moved = True
        elif keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            driver.move_left()
            player_moved = True
        else:
            driver.move_up()

        # Check for collisions
        if pygame.sprite.spritecollide(driver, obstacle_group, False):
            game_over_screen()

        # Spawn obstacles
        if player_moved and random.random() < 0.02 and len(obstacle_group) < 4:
            # Increase probability of obstacles spawning
            obstacle_x = random.choice(lane_pos)
            obstacle_y = -100  # Spawn obstacles at the top of the screen
            while any(abs(obstacle_x - obstacle.x_pos) < 73 for
                      obstacle in obstacle_group):
                obstacle_x = random.choice(lane_pos)
                # Generate new x_pos for obstacle until
                # it's not on top of another one
            obstacle = Obstacle(obstacle_x, obstacle_y)
            obstacle_group.add(obstacle)

        # Update game objects
        driver_group.update()
        obstacle_group.update()  # Update obstacle positions

        # Draw game objects
        screen.fill((255, 255, 255))
        screen.blit(road, (0, road_y))
        screen.blit(road, (0, road_y + 925))
        driver_group.draw(screen)
        obstacle_group.draw(screen)

        # display player score on screen
        player_score_text = font.render(f"Score: {score}", True,
                                        (255, 255, 255))
        screen.blit(player_score_text, (55, 10))

        # Update display
        pygame.display.update()

        # Move road
        road_y += 8
        if road_y >= 0:
            road_y = -925

        # Control frame rate
        clock.tick(60)

        pygame.display.update()


def game_over_screen():
    # Game Over Screen
    font = pygame.font.Font(None, 36)
    screen.fill((255, 255, 255))
    game_over_text = font.render("Game Over!", True, (0, 0, 0))
    game_over_text2 = font.render("Would you like to restart or quit?", True,
                                  (0, 0, 0))
    game_over_text3 = font.render("(Press R or Q)", True, (0, 0, 0))
    screen.blit(game_over_text, (150, 400))
    screen.blit(game_over_text2, (150, 550))
    screen.blit(game_over_text3, (150, 600))

    # Scoring
    with open("Assessment/high_score.txt", "r") as f:
        high_score_str = f.read().strip()  # Remove leading/trailing whitespace
    if high_score_str:
        try:
            high_score = int(high_score_str)
        except ValueError:
            high_score = 0
    else:
        high_score = 0  # Set to a default value if file is empty
    score_text = font.render(f"Your score was: {score}", True, (0, 0, 0))
    if score > high_score:
        high_score = score
        with open("Assessment/high_score.txt", "w") as f:
            f.write(str(high_score))
    high_score_text = font.render(f"High score: {high_score}", True, (0, 0, 0))
    screen.blit(score_text, (150, 450))
    screen.blit(high_score_text, (150, 500))
    pygame.display.update()

    # Ask user to restart or quit
    restart = False
    while not restart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_loop()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                return


game_loop()
