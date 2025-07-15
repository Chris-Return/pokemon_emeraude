import pygame
from src.components.component import Component

class Tileset():
    def __init__(self, img_path):
        self.img_path = img_path
        self.img = pygame.image.load(img_path)
        # Taille d'une tuile par rapport à l'image de référence
        self.size_per_tile = [16,16]

    def get_tile_at(self, x, y):
        rect = pygame.Rect(int(x*self.size_per_tile[0]), int(y*self.size_per_tile[1]), self.size_per_tile[0], self.size_per_tile[1])
        return self.img.subsurface(rect)
    
    @staticmethod
    # LA DIRECTION EST VERTICALE PAR DEFAUT
    def load_all_directions_object(path, size_x, size_y, width, height):
        img = pygame.image.load(path)
        img_list = []
        for i in range(width):
            img_range = []
            for y in range(height):
                rect = pygame.Rect(int(i*size_x), int(y*size_y), size_x, size_y)
                img_range.append(Component(img.subsurface(rect)))

            img_list.append(img_range)

        return img_list