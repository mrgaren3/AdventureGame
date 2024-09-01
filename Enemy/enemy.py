import pygame,os

# Define constants for enemies
ENEMY_SIZE = 50  # Make sure this matches the size you want for your enemies
ENEMY_SPEED = 2
BULLET_SIZE = 10
BULLET_SPEED = 4
ENEMY_SHOOT_INTERVAL = 2000  # 2 seconds in milliseconds
DIR = r'Enemy/FlyingMonster'
enemy_image_paths = []
for i in os.listdir(DIR):
    enemy_image_paths.append(i)

class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BULLET_SIZE, BULLET_SIZE)
        self.speed = BULLET_SPEED
        self.color = (255, 0, 0)  # Red color for bullets

    def move(self):
        self.rect.x -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Enemy:
    def __init__(self, screen_width, y_position):
        # Load all animation frames
        self.Bigimage = [pygame.image.load(os.path.join(DIR, image_path)) for image_path in enemy_image_paths]
        self.flipImage = [pygame.transform.flip(image, True, False) for image in self.Bigimage]
        self.images = [pygame.transform.scale(image, (50, 50)) for image in self.flipImage]
        self.current_frame = 0
        self.animation_speed = 100  # Time in milliseconds to show each frame
        self.last_update_time = pygame.time.get_ticks()

        self.rect = self.images[0].get_rect(topleft=(screen_width, y_position))
        self.speed = ENEMY_SPEED
        self.last_shoot_time = pygame.time.get_ticks()

    def move(self):
        self.rect.x -= self.speed

    def animate(self):
        # Update to the next frame if enough time has passed
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time > self.animation_speed:
            self.last_update_time = current_time
            self.current_frame = (self.current_frame + 1) % len(self.images)

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shoot_time > ENEMY_SHOOT_INTERVAL:
            self.last_shoot_time = current_time
            return Bullet(self.rect.left, self.rect.centery)
        return None

    def draw(self, screen):
        # Draw the current frame
        self.animate()
        screen.blit(self.images[self.current_frame], self.rect)
