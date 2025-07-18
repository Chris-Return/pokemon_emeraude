from src.gamescreen.gamescreen import GameScreen
from src.constants.constants import *
from src.gameobjects.player import Player
from src.maps.gamemap import GameMap
from src.maps.gameobjectmover import GameObjectMover
from src.maps.mapanalyser import MapAnalyser
from src.maps.mapmanager import MapManager
import pygame

class InGameScreen(GameScreen):
    def __init__(self):
        super().__init__()
        self.map_manager = MapManager()
        if(TEST_MODE):
            self.map_manager.load_map(MAP_BOURG_EN_VOL, True, 0, 0)

        self.gameobjectmover = GameObjectMover()
        self.player = Player()

        if(TEST_MODE):
            self.player.teleport_at_map_position((5,9))


    def update(self, deltatime):
        self.player.update(deltatime)

    def get_components(self):
        return super().get_components() + self.map_manager.get_limited_components(self.player) + [self.player.get_component()]
    
    def check_events(self, event):
        if(self.active and event.type == pygame.KEYDOWN):
                self.player.check_inputs(event)