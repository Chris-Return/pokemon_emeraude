import pygame

class Camera:
    def __init__(self, width, height):
        self.offset = pygame.Vector2(0, 0)
        self.width = width
        self.height = height

    def apply(self, target_rect):
        return target_rect.move(-self.offset.x, -self.offset.y)

    def move_to(self, target):
        self.offset.x = target.centerx - self.width // 2
        self.offset.y = target.centery - self.height // 2