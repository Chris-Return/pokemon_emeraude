from src.components.component import Component

class GameObject(Component):
    def __init__(self):
        super().__init__(None)
        self.active = True
        self.map_position = (0,0)
        self.input_active = False
        self.character_animation = None

    def update(self, deltatime):
        pass

    def get_map_position(self):
        return self.map_position
    
    def set_map_position(self, position):
        self.map_position = position