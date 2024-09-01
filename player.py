import pygame
import sys

# Initialize Pygame
pygame.init()

# Define constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
LAND_HEIGHT = 100
PLAYER_SIZE = 50
GRAVITY = 0.8
JUMP_STRENGTH = 12
PLAYER_SPEED = 3

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Adventure Game")

# Create the land (a green rectangle at the bottom of the screen)
land = pygame.Rect(0, SCREEN_HEIGHT - LAND_HEIGHT, SCREEN_WIDTH, LAND_HEIGHT)

# Create the player (a blue square)
player = pygame.Rect(SCREEN_WIDTH//2 - PLAYER_SIZE//2, SCREEN_HEIGHT - LAND_HEIGHT - PLAYER_SIZE, PLAYER_SIZE, PLAYER_SIZE)
player_velocity_y = 0
can_jump = True
has_double_jumped = False
on_ground = False

# Main game loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Handle key presses for movement
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_a]:  # Move left
        player.x -= PLAYER_SPEED
    if keys[pygame.K_d]:  # Move right
        player.x += PLAYER_SPEED
    if keys[pygame.K_s]:  # Move down (optional for vertical movement)
        player.y += PLAYER_SPEED
    
    # Jump logic
    if keys[pygame.K_SPACE] and can_jump:
        if on_ground:
            player_velocity_y = -JUMP_STRENGTH
            on_ground = False
            can_jump = False
        elif not has_double_jumped:
            player_velocity_y = -JUMP_STRENGTH
            has_double_jumped = True
            can_jump = False
    if not keys[pygame.K_SPACE]:  # Reset jump ability when space is released
        can_jump = True

    # Apply gravity
    player_velocity_y += GRAVITY
    player.y += player_velocity_y

    # Check if the player is on the land
    if player.colliderect(land):
        player.y = SCREEN_HEIGHT - LAND_HEIGHT - PLAYER_SIZE
        player_velocity_y = 0
        on_ground = True
        has_double_jumped = False  # Reset double jump ability when landing

    # Prevent the player from going out of bounds
    if player.x < 0:
        player.x = 0
    elif player.x + PLAYER_SIZE > SCREEN_WIDTH:
        player.x = SCREEN_WIDTH - PLAYER_SIZE

    if player.y < 0:
        player.y = 0

    # Fill the screen with white
    screen.fill(WHITE)

    # Draw the land
    pygame.draw.rect(screen, GREEN, land)

    # Draw the player
    pygame.draw.rect(screen, BLUE, player)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate to 60 FPS
    clock.tick(60)
