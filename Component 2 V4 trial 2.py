"""Car Assessment Game -- Component 2 Version 3
Version 4 to Create driver car controls
By Conor Smith"""

# Imports the Pygame library for graphics and the Time library for pausing
import pygame
import time

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
        self.image = pygame.transform.scale(pygame.image.load('driver_car.png'), (73, 125))
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def move_right(self):
        self.image = pygame.transform.rotate(self.image, -30)
        self.x_pos += VELOCITY

    def move_left(self):
        self.image = pygame.transform.rotate(self.image, 30)  # make car look like turning
        self.x_pos -= VELOCITY

    def move_up(self):
        self.image = pygame.transform.rotate(self.image, 0)  # make car look like stright


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
        if keys[pygame.K_LEFT]:
            driver.move_left()

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


# code currently amkes car spiral off screen