import pygame,sys,random
from player.player import *
from settinges import *

# Initialize Pygame
pygame.init()

# Initialize the player
player = Player(SCREEN_WIDTH, LAND_Y_POSITION)

# Timer for spawning new power-ups
last_spawn_time = pygame.time.get_ticks()

# Main game loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

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

    # Reset player if needed
    player.reset_if_needed()

    # Check speed boost expiration
    player.check_speed_boost()

    # Check for collisions with power-ups
    for power_up in power_ups[:]:
        if player.rect.colliderect(power_up.rect):
            power_up.apply(player)
            power_ups.remove(power_up)

    # Spawn new power-ups every 5 seconds
    current_time = pygame.time.get_ticks()
    if current_time - last_spawn_time > POWER_UP_INTERVAL:
        last_spawn_time = current_time
        new_power_up_type = random.choice(['health', 'speed'])
        new_power_up_x = random.randint(0, SCREEN_WIDTH - POWER_UP_SIZE)
        new_power_up_y = LAND_Y_POSITION - POWER_UP_SIZE - random.randint(50, 150)
        new_power_up = PowerUp(new_power_up_x, new_power_up_y, new_power_up_type)
        power_ups.append(new_power_up)

    # Fill the screen with the background image
    screen.blit(background_image, (0, 0))

    # Draw the player and health bar
    player.draw(screen)

    # Draw power-ups
    for power_up in power_ups:
        power_up.draw(screen)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate to 60 FPS
    clock.tick(60)
