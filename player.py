import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Define constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PLAYER_SIZE = 50
GRAVITY = 0.8
JUMP_STRENGTH = 12
PLAYER_SPEED = 3
BOOST_SPEED = 6
POWER_UP_SIZE = 30
MAX_HEALTH = 100
SPEED_BOOST_DURATION = 5000  # in milliseconds
HEALTH_PACK_AMOUNT = 25
POWER_UP_INTERVAL = 5000  # 5 seconds in milliseconds

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Load the background image
background_image = pygame.image.load('background.jpg')
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Adventure Game")

# Determine the land area position
LAND_Y_POSITION = SCREEN_HEIGHT - 65

class PowerUp:
    def __init__(self, x, y, type):
        self.rect = pygame.Rect(x, y, POWER_UP_SIZE, POWER_UP_SIZE)
        self.type = type
        if type == 'health':
            self.color = GREEN
        elif type == 'speed':
            self.color = YELLOW

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

    def apply(self, player):
        if self.type == 'health':
            player.health = min(MAX_HEALTH, player.health + HEALTH_PACK_AMOUNT)
        elif self.type == 'speed':
            player.boost_speed()

class Player:
    def __init__(self):
        self.reset_player()
        self.resetting = False
        self.speed = PLAYER_SPEED
        self.boost_start_time = None

    def reset_player(self):
        self.rect = pygame.Rect(SCREEN_WIDTH//2 - PLAYER_SIZE//2, LAND_Y_POSITION - PLAYER_SIZE, PLAYER_SIZE, PLAYER_SIZE)
        self.velocity_y = 0
        self.can_jump = True
        self.has_double_jumped = False
        self.on_ground = False
        self.health = MAX_HEALTH
        self.resetting = False

    def handle_movement(self, keys):
        if self.resetting:
            return  # Ignore movement if resetting

        if keys[pygame.K_a]:  # Move left
            self.rect.x -= self.speed
        if keys[pygame.K_d]:  # Move right
            self.rect.x += self.speed

        # Jump logic
        if keys[pygame.K_SPACE] and self.can_jump:
            if self.on_ground:
                self.velocity_y = -JUMP_STRENGTH
                self.on_ground = False
                self.can_jump = False
            elif not self.has_double_jumped:
                self.velocity_y = -JUMP_STRENGTH
                self.has_double_jumped = True
                self.can_jump = False
        if not keys[pygame.K_SPACE]:  # Reset jump ability when space is released
            self.can_jump = True

    def apply_gravity(self):
        if self.resetting:
            return  # Skip gravity application if resetting

        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

    def check_land_collision(self):
        if self.resetting:
            return  # Skip collision check if resetting

        if self.rect.bottom > LAND_Y_POSITION:
            self.rect.bottom = LAND_Y_POSITION
            self.velocity_y = 0
            self.on_ground = True
            self.has_double_jumped = False

    def prevent_out_of_bounds(self):
        if self.resetting:
            return  # Skip bounds check if resetting

        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x + PLAYER_SIZE > SCREEN_WIDTH:
            self.rect.x = SCREEN_WIDTH - PLAYER_SIZE

        if self.rect.y < 0:
            self.rect.y = 0

    def update_health(self):
        if self.resetting:
            return  # Skip health update if resetting

        # Decrease health over time for demonstration purposes
        if self.health > 0:
            self.health -= 0.1
        else:
            self.health = 0
            self.resetting = True  # Set the resetting flag when health reaches 0

    def draw_health_bar(self):
        health_bar_width = 200
        health_bar_height = 20
        health_ratio = self.health / MAX_HEALTH
        health_bar_color = RED if health_ratio < 0.3 else GREEN

        # Draw the health bar border
        pygame.draw.rect(screen, BLACK, (10, 10, health_bar_width + 4, health_bar_height + 4))
        
        # Draw the health bar itself
        pygame.draw.rect(screen, health_bar_color, (12, 12, health_bar_width * health_ratio, health_bar_height))

    def draw(self):
        pygame.draw.rect(screen, BLUE, self.rect)
        self.draw_health_bar()

    def reset_if_needed(self):
        if self.resetting:
            self.reset_player()

    def boost_speed(self):
        self.speed = BOOST_SPEED
        self.boost_start_time = pygame.time.get_ticks()

    def check_speed_boost(self):
        if self.boost_start_time:
            elapsed_time = pygame.time.get_ticks() - self.boost_start_time
            if elapsed_time > SPEED_BOOST_DURATION:
                self.speed = PLAYER_SPEED
                self.boost_start_time = None


# Initialize the player
player = Player()

# Create initial power-ups
power_ups = [
    PowerUp(random.randint(0, SCREEN_WIDTH - POWER_UP_SIZE), LAND_Y_POSITION - POWER_UP_SIZE - 50, 'health'),
    PowerUp(random.randint(0, SCREEN_WIDTH - POWER_UP_SIZE), LAND_Y_POSITION - POWER_UP_SIZE - 150, 'speed')
]

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
    player.draw()

    # Draw power-ups
    for power_up in power_ups:
        power_up.draw()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate to 60 FPS
    clock.tick(60)
