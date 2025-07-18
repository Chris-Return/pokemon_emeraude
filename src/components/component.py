import pygame
from src.constants.constants import *

class Component():

    def __init__(self, pycomponent):
        self.set_component(pycomponent)
        self.children = []
        self.visible = True
        self.position = (0,0)
        self.game_event = None

    def get_visible(self):
        return self.visible
    
    def set_visible(self, visible):
        self.visible = visible
    
    def get_position(self):
        return self.position
    
    def get_component(self):
        return self.component
    
    def set_component(self, new_component):
        self.component = new_component
        try:
            self.component = pygame.transform.scale_by(self.component, SCREEN_SCALE)
        except Exception:
            pass
    
    def set_position(self, position):
        self.position = position

    def get_children(self):
        try:
            return self.children + self.game_event.get_components()
        except:
            return self.children