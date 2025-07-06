import pygame
from abc import abstractmethod

class GameEvent():
    
    def __init__(self):
        self.active = False
        self.components = []

    @abstractmethod
    def update(self, deltatime):
        pass

    @abstractmethod
    def run(self):
        self.active = True

    @abstractmethod
    def get_components(self):
        return self.components