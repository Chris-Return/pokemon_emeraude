from src.gameobjects.gameobjectcharacter import GameObjectCharacter
from src.animation.gridanimation import GridAnimation
from src.constants.constants import SCREEN_SCALE, GET_PNG
from src.camera.camera import Camera
import pygame

class Player(GameObjectCharacter):
    def __init__(self, game_object_mover):
        super().__init__(game_object_mover, 0)
        self.input_active = True
        self.character_animation = GridAnimation(GET_PNG(0))

    def update(self, deltatime):
        super().update(deltatime)
        self.check_hold_press(pygame.key.get_pressed())
    
    def set_position(self, position):
        self.position = position
        Camera.set_position(position)

    def teleport_at_map_position(self, position):
        self.set_position((position[0]*16*SCREEN_SCALE, position[1]*16*SCREEN_SCALE))
        self.set_map_position(position)

    def check_inputs(self, event):
        pass

    def set_input_active(self, active):
        self.input_active = active

    def check_hold_press(self, key):
        if(self.input_active):
            if not key[pygame.K_DOWN] and not key[pygame.K_UP] and not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
                self.character_animation.stop()
            if(key[pygame.K_DOWN]):
                self.game_object_mover.add_object_to_move(self, [0])
            elif(key[pygame.K_UP]):
                self.game_object_mover.add_object_to_move(self, [1])
            elif(key[pygame.K_LEFT]):
                self.game_object_mover.add_object_to_move(self, [2])
            elif(key[pygame.K_RIGHT]):
                self.game_object_mover.add_object_to_move(self, [3])