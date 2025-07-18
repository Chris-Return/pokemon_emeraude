from src.constants.constants import *

class Camera:

    camera_position = (0,0)

    def __init__(self):
        pass
    
    @staticmethod
    def apply(self, position):
        return (position[0] + Camera.camera_position[0], position[1] + Camera.camera_position[1])
    
    @staticmethod
    def get_position():
        return Camera.camera_position
    
    @staticmethod
    def set_position(position):
        new_position = (position[0] + 25 - SCREEN_WIDTH/2, position[1] + 25 - SCREEN_HEIGHT/2)
        Camera.camera_position = new_position