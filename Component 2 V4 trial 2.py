"""Car Assessment Game -- Component 2 Version 4
Version 4 to Create driver car controls trial 2
By Conor Smith"""

# Imports the Pygame library for graphics and the Time library for pausing
import pygame
import time
import math

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

# Game Variables and constants
game_over = False
VELOCITY = 5

driver_group = pygame.sprite.GroupSingle()

driver = Driver(350, 700)
driver_group.add(driver)

# Game Loop
while True:
    if not game_over:

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            driver.move_right()
        elif keys[pygame.K_LEFT]:
            driver.move_left()
        else:
            driver.move_up()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

    if not game_over:
        driver_group.update()
        screen.fill((255, 255, 255))  # Fill the screen with white before drawing the sprite
        driver_group.draw(screen)

    clock.tick(60)
    pygame.display.update()

# Quit pygame when the game loop is exited
pygame.quit()


# Code works perfectly fine