
class GameEvent():
    
    def __init__(self, parent):
        self.active = False
        self.components = []
        self.type = None
        self.parent = parent
        self.map_freezer = True
        self.dead = False

    def update(self, deltatime):
        pass

    def run(self):
        self.active = True

    def get_components(self):
        return self.components
    
    def get_active(self):
        return self.active
    
    def check_inputs(self, event):
        pass

    def is_map_freezer(self):
        return self.map_freezer
    
    def is_dead(self):
        return self.dead
    
    def set_dead(self, dead):
        self.dead = dead