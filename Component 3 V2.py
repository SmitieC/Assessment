"""Car Assessment Game -- Component 3 Version 2
Version 2 to make obstacles
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
        self.all_cars = [
            pygame.transform.scale(
                pygame.image.load("car_2.png"), (50, 90)
            )
        ]
        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("car_3.png"), (50, 90)))
        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("car_4.png"), (50, 90)))
        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("car_5.png"), (50, 90)))
        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("car_6.png"), (50, 90)))
        
        self.image = random.choice(self.all_cars)
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.x_pos -= game_speed
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

# Game Variables and constants
game_over = False
VELOCITY = 5
game_speed = 5

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
while True:
    if not game_over:

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            driver.move_right()
        elif keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            driver.move_left()
        else:
            driver.move_up()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        # Decrease y-position of road to make it move downwards
        road_y += VELOCITY
        if road_y >= 0:
            road_y = -925
 # Add obstacles to the group randomly based on a probability distribution
        if random.random() < 0.01:
            obstacle_x = random.randint(0, 700)
            obstacle_y = random.randint(-1000, -100)
            obstacle = Obstacle(obstacle_x, obstacle_y)
            obstacle_group.add(obstacle)

    if not game_over:
        driver_group.update()
        screen.fill((255, 255, 255))  # Fill the screen with white before drawing the sprite

        # Draw the road at its current y-position
        screen.blit(road, (0, road_y))
        screen.blit(road, (0, road_y + 925))

        # Update and draw obstacles in the group
        obstacle_group.update()
        obstacle_group.draw(screen)

        driver_group.draw(screen)

    clock.tick(60)
    pygame.display.update()