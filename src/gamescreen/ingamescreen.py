from src.gamescreen.gamescreen import GameScreen
from src.constants.constants import *
from src.gameobjects.player import Player
from src.maps.gamemap import GameMap
from src.maps.gameobjectmover import GameObjectMover
import pygame

class InGameScreen(GameScreen):
    def __init__(self):
        super().__init__()
        if(TEST_MODE):
            self.gamemap = GameMap(MAP_DE_CALIBRAGE)

        self.gameobjectmover = GameObjectMover()
        self.player = Player()

    def update(self, deltatime):
        self.player.update(deltatime)

    def get_components(self):
        return super().get_components() + self.gamemap.get_all_components() + [self.player.get_component()]
    
    def check_events(self, event):
        if(self.active and event.type == pygame.KEYDOWN):
                self.player.check_inputs(event)