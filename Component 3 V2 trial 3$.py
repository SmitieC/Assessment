"""Car Assessment Game -- Component 3 Version 2
Version 2 to make obstacles
trial 2 to spawn obstacles in lanes without stacking
By Conor Smith"""

# Imports the Pygame library for graphics and the Time library for pausing
import pygame
import time
import math
import random

from pygame.sprite import AbstractGroup

pygame.init()

# Component 1 To Initialize Screen
screen = pygame.display.set_mode((700, 925))
pygame.display.set_caption("Car Driving Game")
game_icon = pygame.image.load('game_icon.png')
pygame.display.set_icon(game_icon)

# Initialize clock to control frame rate
clock = pygame.time.Clock()

# Class for player driven car
class Driver(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.orig_image = pygame.transform.scale(pygame.image.load('driver_car.png'), (73, 125))
        self.image = self.orig_image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.angle = 0

    def move_right(self):
        self.angle = -15
        if self.x_pos < 700 - VELOCITY:  # check if car is within screen
            self.x_pos += VELOCITY

    def move_left(self):
        self.angle = 15  # make car look like turning
        if self.x_pos > VELOCITY:  # check if car is within screen
            self.x_pos -= VELOCITY

    def move_up(self):
        self.angle = 0  # make car look like straight

    def update(self):
        self.image = pygame.transform.rotate(self.orig_image, self.angle)
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.rect = self.rect.clamp(screen.get_rect())

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.running_sprites = []
        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("car_2.png"), (73, 125)))
        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("car_3.png"), (73, 125)))
        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("car_4.png"), (73, 125)))
        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("car_5.png"), (73, 125)))
        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("car_6.png"), (73, 125)))
        
        self.image = random.choice(self.running_sprites)
        if self.x_pos > 400:
            self.image = pygame.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    
    def update(self):
        self.y_pos += VELOCITY  # Move obstacle downwards
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        if self.y_pos > 950:
            self.kill()
    
            

# Game Variables and constants
game_over = False
VELOCITY = 5
game_speed = 5
lane_pos = []
lane_pos.append(115)
lane_pos.append(253)
lane_pos.append(436)
lane_pos.append(593)

road = pygame.image.load('Road-1.png')
road = pygame.transform.rotate(road, 90)
road = pygame.transform.scale(road, (700, 925))

driver_group = pygame.sprite.GroupSingle()
obstacle_group = pygame.sprite.Group()

driver = Driver(350, 700)
driver_group.add(driver)

# Initialize y-position of road
road_y = -925

# Game Loop
while not game_over:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # Handle input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
        driver.move_right()
    elif keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
        driver.move_left()
    else:
        driver.move_up()

    # Spawn obstacles
    # Spawn obstacles
    if random.random() < 0.02 and len(obstacle_group) < 4:  # Increase probability of obstacles spawning
        obstacle_x = random.choice(lane_pos)
        obstacle_y = -100  # Spawn obstacles at the top of the screen
        while any(abs(obstacle_x - obstacle.x_pos) < 73 for obstacle in obstacle_group):
            obstacle_x = random.choice(lane_pos) # Generate new x_pos for obstacle until it's not on top of another one
        obstacle = Obstacle(obstacle_x, obstacle_y)
        obstacle_group.add(obstacle)


    # Update game objects
    driver_group.update()
    obstacle_group.update()  # Update obstacle positions

    # Draw game objects
    screen.fill((255, 255, 255))
    screen.blit(road, (0, road_y))
    screen.blit(road, (0, road_y + 925))
    #driver_group.draw(screen)
    obstacle_group.draw(screen)

    # Update display
    pygame.display.update()

    # Move road
    road_y += VELOCITY
    if road_y >= 0:
        road_y = -925

    # Control frame rate
    clock.tick(60)

    pygame.display.update()