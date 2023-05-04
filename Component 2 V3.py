"""Car Assessment Game -- Compenent 2 Version 3
Version 3 to Print Driver car on screen
By Conor Smith"""

# Imports the Pygame library for graphics and the Time library for pausing
import pygame
import time

from pygame.sprite import AbstractGroup

pygame.init()

# Component 1 To Initlize Screen
screen = pygame.display.set_mode((700, 925))
pygame.display.set_caption("Car Driving Game")
game_icon = pygame.image.load('game_icon.png')
pygame.display.set_icon(game_icon)

# initialize clock to control frame rate
clock = pygame.time.Clock()

# class for player driven car
class Driver(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.image = pygame.transform.scale(pygame.image.load('driver_car.png'), (73, 125))
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
    
    def move_right(self):
        self.image.transform.rotate("", 30)
        self.x_pos += VELOCITY
    
    def move_left(self):
        self.image.transform.rotate("", -30)  # make car look like turning
        self.x_pos -= VELOCITY
    
    def move_up(self):
        self.image.transform.rotate("", 0)  # make car look like stright
        

# Game Variables and constants
game_over = False
VELOCITY = 5

driver_group = pygame.sprite.GroupSingle()

driver = Driver(350, 700)
driver_group.add(driver)



# Game Loop
while True:
    if not game_over:
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                pygame.quit()
                quit()
            
            driver = Driver(350, 700)
            driver_group.add(driver)

    if not game_over:
        driver_group.update()
        driver_group.draw(screen)
    

    clock.tick(60)
    pygame.display.update()