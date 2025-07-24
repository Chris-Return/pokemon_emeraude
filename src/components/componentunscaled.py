from src.components.component import *

class ComponentUnscaled(Component):

    def __init__(self, pycomponent):
        self.set_component(pycomponent)
        self.children = []
        self.visible = True
        self.position = (0,0)
        self.sort_number = 0

    def get_visible(self):
        return self.visible
    
    def set_visible(self, visible):
        self.visible = visible
    
    def get_position(self):
        return self.position
    
    def get_component(self):
        return self.component
    
    def set_component(self, new_component):
        self.component = new_component
    
    def set_position(self, position):
        self.position = position

    def get_children(self):
        return self.children