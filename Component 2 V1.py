"""Car Assessment Game -- Compenent 2 Version 1
Version 1 to Create Running Game loop
By Conor Smith"""

# Imports the Pygame library for graphics and the Time library for pausing
import pygame
import time

pygame.init()

# Component 1 To Initlize Screen
screen = pygame.display.set_mode((700, 925))
pygame.display.set_caption("Car Driving Game")
game_icon = pygame.image.load('game_icon.png')
pygame.display.set_icon(game_icon)

# initialize clock to control frame rate
clock = pygame.time.Clock()

# Game Variables
game_over = False


# Game Loop
while True:
    if not game_over:
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                pygame.quit()
                quit()

    clock.tick(60)
    pygame.display.update()
    