import pygame,random
from player.player import *

# Define constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
LAND_Y_POSITION = SCREEN_HEIGHT - 65
POWER_UP_SIZE = 30
POWER_UP_INTERVAL = 5000  # 5 seconds in milliseconds
ENEMY_SPAWN_INTERVAL_MIN = 4000  # 4 seconds in milliseconds
ENEMY_SPAWN_INTERVAL_MAX = 7000  # 7 seconds in milliseconds

# Load the background image
background_image = pygame.image.load('background.jpg')
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Adventure Game")


