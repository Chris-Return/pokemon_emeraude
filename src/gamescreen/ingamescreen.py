from src.gamescreen.gamescreen import GameScreen
from src.constants.constants import TEST_MODE, MAP_BOURG_EN_VOL
from src.gameobjects.player import Player
from src.maps.mapanalyser import MapAnalyser
from src.maps.mapmanager import MapManager
from src.maps.mapstereotype import MapStereotype
from src.animation.characterstereotype import CharacterStereotype
from src.maps.mapinteraction import MapInteraction
import pygame

class InGameScreen(GameScreen):
    def __init__(self):
        super().__init__()
        MapStereotype.load()
        CharacterStereotype.load()
        self.map_manager = MapManager()
        
        if(TEST_MODE):
            self.map_manager.load_map(MAP_BOURG_EN_VOL, True, 0, 0)

        self.player = Player(self.map_manager.get_game_object_mover())
        MapAnalyser.player = self.player
        MapAnalyser.set_map_manager(self.map_manager)

        if(TEST_MODE):
            self.player.teleport_at_map_position((5,9))

        self.map_interaction = MapInteraction(self.map_manager, self.player)


    def update(self, deltatime):
        self.map_interaction.update(deltatime)
        self.player.update(deltatime)
        self.map_manager.update(deltatime)

    def get_components(self):
        characters = self.map_manager.get_characters_components() + [self.player.get_component()]
        characters = sorted(characters, key=lambda x: x.get_position()[1])
        return super().get_components() + self.map_manager.get_limited_components(self.player) + characters + self.map_interaction.get_components()
    
    def check_events(self, event):
        if(self.active and event.type == pygame.KEYDOWN):
            self.player.check_inputs(event)
            self.map_interaction.check_inputs(event)