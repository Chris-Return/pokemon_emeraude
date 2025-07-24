from src.components.component import Component

class GameObject(Component):
    def __init__(self):
        super().__init__(None)
        self.active = False
        self.map_position = (0,0)
        self.input_active = True
        self.character_animation = None

    def update(self, deltatime):
        pass

    def get_map_position(self):
        return self.map_position
    
    def set_map_position(self, position):
        self.map_position = position

    def get_input_active(self):
        return self.input_active
    
    def set_active(self, active):
        self.active = active