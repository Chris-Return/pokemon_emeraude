from abc import abstractmethod
from src.components.component import *

class GameScreen:

    @abstractmethod
    def __init__(self):
        self.components = []
        self.active = True
        self.next_screen_number = 0
    
    @abstractmethod
    def update(self, deltaTime):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def get_components(self):
        return self.components
    
    @abstractmethod
    def check_events(self, event):
        pass

    def get_active(self):
        return self.active
    
    def get_next_screen_number(self):
        return self.next_screen_number