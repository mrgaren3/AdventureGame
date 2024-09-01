import pygame
import sys
import random
from player.player import Player, PowerUp
from Enemy.enemy import Enemy, ENEMY_SIZE

# Initialize Pygame
pygame.init()

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

def reset_game():
    global last_spawn_time, last_enemy_spawn_time, enemy_spawn_interval, power_ups, enemies, bullets, player

    # Reset the player
    player.reset_if_needed()

    # Clear existing power-ups and enemies
    power_ups = []
    enemies = []
    bullets = []

    # Reset spawn timers
    last_spawn_time = pygame.time.get_ticks()
    last_enemy_spawn_time = pygame.time.get_ticks()
    enemy_spawn_interval = random.randint(ENEMY_SPAWN_INTERVAL_MIN, ENEMY_SPAWN_INTERVAL_MAX)

# Initialize the player
player = Player(SCREEN_WIDTH, LAND_Y_POSITION)

# Create initial power-ups
power_ups = []

# Timer for spawning new power-ups
last_spawn_time = pygame.time.get_ticks()

# Timer for spawning new enemies
last_enemy_spawn_time = pygame.time.get_ticks()
enemy_spawn_interval = random.randint(ENEMY_SPAWN_INTERVAL_MIN, ENEMY_SPAWN_INTERVAL_MAX)

# Create lists for enemies and bullets
enemies = []
bullets = []

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

    # Check speed boost expiration
    player.check_speed_boost()

    # Check for collisions with power-ups
    for power_up in power_ups[:]:
        if player.rect.colliderect(power_up.rect):
            power_up.apply(player)
            power_ups.remove(power_up)

    # Spawn new power-ups every 5 seconds, if the game is not in the resetting state
    current_time = pygame.time.get_ticks()
    if not player.resetting and current_time - last_spawn_time > POWER_UP_INTERVAL:
        last_spawn_time = current_time
        new_power_up_type = random.choice(['health', 'speed'])
        new_power_up_x = random.randint(0, SCREEN_WIDTH - POWER_UP_SIZE)
        new_power_up_y = LAND_Y_POSITION - POWER_UP_SIZE - random.randint(50, 150)
        new_power_up = PowerUp(new_power_up_x, new_power_up_y, new_power_up_type)
        power_ups.append(new_power_up)

    # Spawn new enemies every 4-7 seconds, if the game is not in the resetting state
    if not player.resetting and current_time - last_enemy_spawn_time > enemy_spawn_interval:
        last_enemy_spawn_time = current_time
        enemy_y_position = LAND_Y_POSITION - ENEMY_SIZE
        enemies.append(Enemy(SCREEN_WIDTH, enemy_y_position))
        enemy_spawn_interval = random.randint(ENEMY_SPAWN_INTERVAL_MIN, ENEMY_SPAWN_INTERVAL_MAX)

    # Move and draw enemies and bullets
    for enemy in enemies[:]:
        enemy.move()
        bullet = enemy.shoot()
        if bullet:
            bullets.append(bullet)
        if enemy.rect.right < 0:
            enemies.remove(enemy)

    for bullet in bullets[:]:
        bullet.move()
        if bullet.rect.right < 0:
            bullets.remove(bullet)

    # Check for collisions between player and enemies
    for enemy in enemies[:]:
        if player.rect.colliderect(enemy.rect):
            player.health = 0  # Player hit by enemy
            player.resetting = True
            reset_game()  # Reset game state

    # Check for collisions between bullets and player
    for bullet in bullets[:]:
        if player.rect.colliderect(bullet.rect):
            player.health -= 10
            bullets.remove(bullet)
            if player.health <= 0:
                player.resetting = True
                reset_game()  # Reset game state

    # Fill the screen with the background image
    screen.blit(background_image, (0, 0))

    # Draw the player and health bar
    player.draw(screen)

    # Draw power-ups
    for power_up in power_ups:
        power_up.draw(screen)

    # Draw enemies
    for enemy in enemies:
        enemy.draw(screen)

    # Draw bullets
    for bullet in bullets:
        bullet.draw(screen)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate to 60 FPS
    clock.tick(60)
