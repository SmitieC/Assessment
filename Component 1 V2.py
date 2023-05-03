"""Car Assessment Game -- Compenent 1 Version 2
Version 2 to Set Game Name
By Conor Smith"""

# Imports the Pygame library for graphics and the Time library for pausing
import pygame
import time

pygame.init()

# Creates a Pygame window with a size of 700 pixels wide and 925 pixels tall
screen = pygame.display.set_mode((700, 925))

# Set Window Name to be Car Driving Game
pygame.display.set_caption("Car Driving Game")

# Pauses the program for 5 seconds before it closes for testing purposes
time.sleep(5)
