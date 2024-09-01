import pygame,random
from player.player import *

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
LAND_Y_POSITION = SCREEN_HEIGHT - 100
POWER_UP_SIZE = 30
POWER_UP_INTERVAL = 5000  # 5 seconds in milliseconds

# Load the background image
background_image = pygame.image.load('background.jpg')
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Adventure Game")

# Create initial power-ups
power_ups = [
    PowerUp(random.randint(0, SCREEN_WIDTH - POWER_UP_SIZE), LAND_Y_POSITION - POWER_UP_SIZE - 50, 'health'),
    PowerUp(random.randint(0, SCREEN_WIDTH - POWER_UP_SIZE), LAND_Y_POSITION - POWER_UP_SIZE - 150, 'speed')
]
