import pygame
import random

# Define constants for enemies
ENEMY_SIZE = 50  # Make sure this matches the size you want for your enemies
ENEMY_SPEED = 2
BULLET_SIZE = 10
BULLET_SPEED = 4
ENEMY_SHOOT_INTERVAL = 2000  # 2 seconds in milliseconds

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
        self.rect = pygame.Rect(screen_width, y_position, ENEMY_SIZE, ENEMY_SIZE)
        self.speed = ENEMY_SPEED
        self.last_shoot_time = pygame.time.get_ticks()

    def move(self):
        self.rect.x -= self.speed

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shoot_time > ENEMY_SHOOT_INTERVAL:
            self.last_shoot_time = current_time
            return Bullet(self.rect.left, self.rect.centery)
        return None

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), self.rect)  # Black color for enemies
