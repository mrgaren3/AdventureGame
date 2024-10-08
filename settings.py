import pygame,random,sys

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

# Colors
PLAYER_COLOR = (0, 0, 255)  # Blue
HEALTH_COLOR = (0, 255, 0)  # Green
SPEED_COLOR = (255, 255, 0)  # Yellow
ENEMY_COLOR = (0, 0, 0)  # Black
BULLET_COLOR = (255, 0, 0)  # Red
DOOR_COLOR = (0, 255, 0)  # Green

GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

def playerMethod(player):
    # Handle key presses for movement
    keys = pygame.key.get_pressed()
    player.handle_movement(keys)

    # Apply gravity
    player.apply_gravity()

    # Check for land collision
    player.check_land_collision()

    # Prevent player from going out of bounds
    player.prevent_out_of_bounds()

    # Update the player's health
    player.update_health()

    # Check speed boost expiration
    player.check_speed_boost()
