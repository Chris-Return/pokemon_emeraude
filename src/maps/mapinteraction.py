import pygame
from src.maps.mapanalyser import MapAnalyser
from src.events.map.gameeventmanager import GameEventManager

class MapInteraction():
    def __init__(self, map_manager, player):
        self.active = True
        self.map_manager = map_manager
        self.player = player
        self.game_event = None

    def update(self, deltatime):
        if(self.game_event is not None and self.game_event.get_active()):
            self.game_event.update(deltatime)

        if(self.game_event is not None and self.game_event.is_dead()):
            self.game_event = None
            all_game_objects = self.map_manager.get_all_game_objects()
            self.player.set_input_active(True)
            [go.set_active(True) for go in all_game_objects]


    def check_inputs(self, event):
        if(self.game_event == None and event.key == pygame.K_w):
            self.find_interaction_at(MapAnalyser.get_future_position(self.player, self.player.get_direction()))
        elif(self.game_event is not None):
            self.game_event.check_inputs(event)

    def find_interaction_at(self, map_position):
        all_game_objects = self.map_manager.get_all_game_objects()
        game_event = GameEventManager.get_generated_game_event_at(all_game_objects, map_position)
        if(game_event is not None):
            if(game_event.is_map_freezer()):
                self.player.set_input_active(False)
                [go.set_active(False) for go in all_game_objects]

            self.game_event = game_event
            self.game_event.run()

    def get_components(self):
        try:
            return self.game_event.get_components()
        except:
            return []