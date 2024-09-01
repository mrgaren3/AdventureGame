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
MAX_HEALTH = 100  # Maximum health for the player

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Adventure Game")

# Create the land (a green rectangle at the bottom of the screen)
land = pygame.Rect(0, SCREEN_HEIGHT - LAND_HEIGHT, SCREEN_WIDTH, LAND_HEIGHT)


class Player:
    def __init__(self):
        self.reset_player()
        self.resetting = False

    def reset_player(self):
        self.rect = pygame.Rect(SCREEN_WIDTH//2 - PLAYER_SIZE//2, SCREEN_HEIGHT - LAND_HEIGHT - PLAYER_SIZE, PLAYER_SIZE, PLAYER_SIZE)
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
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_d]:  # Move right
            self.rect.x += PLAYER_SPEED
        if keys[pygame.K_s]:  # Move down (optional for vertical movement)
            self.rect.y += PLAYER_SPEED

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

        if self.rect.colliderect(land):
            self.rect.y = SCREEN_HEIGHT - LAND_HEIGHT - PLAYER_SIZE
            self.velocity_y = 0
            self.on_ground = True
            self.has_double_jumped = False  # Reset double jump ability when landing

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


# Initialize the player
player = Player()

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

    # Fill the screen with white
    screen.fill(WHITE)

    # Draw the land
    pygame.draw.rect(screen, GREEN, land)

    # Draw the player and health bar
    player.draw()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate to 60 FPS
    clock.tick(60)
