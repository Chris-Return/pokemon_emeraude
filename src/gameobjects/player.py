from src.gameobjects.gameobject import GameObject
from src.animation.gridanimation import GridAnimation
from src.constants.constants import *
from src.maps.gameobjectmover import GameObjectMover
import pygame

class Player(GameObject):
    def __init__(self):
        super().__init__()
        self.input_active = True
        self.character_animation = GridAnimation(ANIMATION_BUNDLE_PLAYER_MALE)
        self.character_animation.animation_speed = 150
        self.game_object_mover = GameObjectMover()

    def update(self, deltatime):
        super().update(deltatime)
        self.character_animation.update(deltatime)
        self.game_object_mover.update(deltatime)
        self.check_hold_press(pygame.key.get_pressed())

    def get_component(self):
        visible_component = self.character_animation.get_component()
        visible_component.set_position(self.get_position())
        return visible_component
    
    def check_inputs(self, event):
        pass

    def check_hold_press(self, key):
        if(self.input_active):
            if not any(key):
                self.character_animation.stop()
            if(key[pygame.K_DOWN]):
                self.game_object_mover.add_object_to_move(self, [0])
            elif(key[pygame.K_UP]):
                self.game_object_mover.add_object_to_move(self, [1])
            elif(key[pygame.K_LEFT]):
                self.game_object_mover.add_object_to_move(self, [2])
            elif(key[pygame.K_RIGHT]):
                self.game_object_mover.add_object_to_move(self, [3])