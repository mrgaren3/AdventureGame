import pygame

# Define constants
PLAYER_SIZE = 50
GRAVITY = 0.8
JUMP_STRENGTH = 14
PLAYER_SPEED = 4
BOOST_SPEED = 8
POWER_UP_SIZE = 30
MAX_HEALTH = 100
SPEED_BOOST_DURATION = 8000  # in milliseconds
HEALTH_PACK_AMOUNT = 35

# Colors
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

class PowerUp:
    def __init__(self, x, y, type):
        self.rect = pygame.Rect(x, y, POWER_UP_SIZE, POWER_UP_SIZE)
        self.type = type
        if type == 'health':
            self.color = GREEN
        elif type == 'speed':
            self.color = YELLOW

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def apply(self, player):
        if self.type == 'health':
            player.health = min(MAX_HEALTH, player.health + HEALTH_PACK_AMOUNT)
        elif self.type == 'speed':
            player.boost_speed()

class Player:
    def __init__(self, screen_width, land_y_position):
        self.screen_width = screen_width
        self.land_y_position = land_y_position
        self.speed = PLAYER_SPEED
        self.boost_start_time = None

        # Load player images
        self.load_images()

        # Initialize player
        self.reset_player()

    def load_images(self):
        # Load the player idle image
        full_image = pygame.image.load('playerIdle.png').convert_alpha()

        # Check the dimensions of the loaded image
        img_width, img_height = full_image.get_size()
        print(f"Loaded image size: {img_width}x{img_height}")

        # Extract the first frame (33x32) from the sprite sheet
        if img_width >= 33 and img_height >= 32:
            self.idle_image = full_image.subsurface(pygame.Rect(0, 0, 33, 32))
        else:
            raise ValueError("The loaded image is smaller than the expected dimensions of 33x32.")

        # Scale the image while maintaining the aspect ratio
        scale_factor = PLAYER_SIZE / self.idle_image.get_height()
        new_width = int(self.idle_image.get_width() * scale_factor)
        self.idle_image = pygame.transform.scale(self.idle_image, (new_width, PLAYER_SIZE))

        # Create the flipped image for left direction
        self.idle_image_right = self.idle_image
        self.idle_image_left = pygame.transform.flip(self.idle_image_right, True, False)

    def reset_player(self):
        self.rect = pygame.Rect(self.screen_width // 2 - self.idle_image.get_width() // 2, 
                                self.land_y_position - PLAYER_SIZE, 
                                self.idle_image.get_width(), 
                                PLAYER_SIZE)
        self.velocity_y = 0
        self.can_jump = True
        self.has_double_jumped = False
        self.on_ground = False
        self.health = MAX_HEALTH
        self.resetting = False
        self.facing_right = True  # Initial facing direction

    def handle_movement(self, keys):
        if self.resetting:
            return  # Ignore movement if resetting

        if keys[pygame.K_a]:  # Move left
            self.rect.x -= self.speed
            self.facing_right = False
        if keys[pygame.K_d]:  # Move right
            self.rect.x += self.speed
            self.facing_right = True

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

        if self.rect.bottom > self.land_y_position:
            self.rect.bottom = self.land_y_position
            self.velocity_y = 0
            self.on_ground = True
            self.has_double_jumped = False

    def prevent_out_of_bounds(self):
        if self.resetting:
            return  # Skip bounds check if resetting

        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x + self.rect.width > self.screen_width:
            self.rect.x = self.screen_width - self.rect.width

        if self.rect.y < 0:
            self.rect.y = 0

    def update_health(self):
        if self.resetting:
            return  # Skip health update if resetting

        if self.health < 0:
            self.health = 0
            self.resetting = True  # Set the resetting flag when health reaches 0

    def draw_health_bar(self, screen):
        health_bar_width = 200
        health_bar_height = 20
        health_ratio = self.health / MAX_HEALTH
        health_bar_color = RED if health_ratio < 0.3 else GREEN

        # Draw the health bar border
        pygame.draw.rect(screen, BLACK, (10, 10, health_bar_width + 4, health_bar_height + 4))
        
        # Draw the health bar itself
        pygame.draw.rect(screen, health_bar_color, (12, 12, health_bar_width * health_ratio, health_bar_height))

    def draw(self, screen):
        if self.facing_right:
            screen.blit(self.idle_image_right, self.rect)
        else:
            screen.blit(self.idle_image_left, self.rect)
        self.draw_health_bar(screen)

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
