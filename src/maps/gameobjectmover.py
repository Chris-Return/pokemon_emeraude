from src.maps.mapanalyser import MapAnalyser
from src.constants.constants import SCREEN_SCALE
from src.gameobjects.player import Player

class GameObjectMover():
    def __init__(self):
        self.stack_of_objects = {}
        self.destination_stack = {}
        self.deltatime_accumulator = 0
        self.speed = 2

    def update(self, deltatime):
        self.deltatime_accumulator += deltatime
        if(self.deltatime_accumulator > 7):
            to_remove = []

            # EFFECTUER LES DEPLACEMENTS NECESSAIRES
            for object in self.stack_of_objects:
                if(object.position == self.destination_stack[object]):
                    to_remove.append(object)
                else:
                    if(object.position[0] != self.destination_stack[object][0]):
                            object.set_position((object.position[0] + (self.speed if object.position[0] < self.destination_stack[object][0] else -self.speed), object.position[1]))
                    if(object.position[1] != self.destination_stack[object][1]):
                            object.set_position((object.position[0], object.position[1] + (self.speed if object.position[1] < self.destination_stack[object][1] else -self.speed)))
            self.deltatime_accumulator = 0

            for element in to_remove:
                MapAnalyser.define_element_position(element, self.stack_of_objects[element][0])
                # ENLEVER LES ELEMENTS QUI ONT TERMINÉ LEUR DEPLACEMENT
                if(not isinstance(element, Player)):
                    element.get_animation().stop()
                    
                self.stack_of_objects[element].pop(0)
                self.check_destination(element)

    def add_object_to_move(self, object, tab_directions):
        object.character_animation.play()
        object.input_active = False
        self.stack_of_objects[object] = tab_directions
        self.check_destination(object)
        
    def check_destination(self, object):
        try:
            object.character_animation.set_direction(self.stack_of_objects[object][0])
        except:
            pass
        
        # SI IL Y A ENCORE DES DESTINATIONS
        if(len(self.stack_of_objects[object]) > 0 and MapAnalyser.check_move(object, self.stack_of_objects[object][0])):
            MapAnalyser.lock_future_position(object, self.stack_of_objects[object][0])
            if(self.stack_of_objects[object][0] == 0):
                self.destination_stack[object] = (object.position[0],object.position[1]+(16*SCREEN_SCALE))
            elif(self.stack_of_objects[object][0] == 1):
                self.destination_stack[object] = (object.position[0],object.position[1]-(16*SCREEN_SCALE))
            elif(self.stack_of_objects[object][0] == 2):
                self.destination_stack[object] = (object.position[0]-(16*SCREEN_SCALE),object.position[1])
            elif(self.stack_of_objects[object][0] == 3):
                self.destination_stack[object] = (object.position[0]+(16*SCREEN_SCALE),object.position[1])
        else:
            object.input_active = True
            self.stack_of_objects.pop(object)
            if(not isinstance(object, Player)):
                object.character_animation.stop()