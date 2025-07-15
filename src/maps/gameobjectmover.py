
class GameObjectMover():
    def __init__(self):
        self.stack_of_objects = {}
        self.destination_stack = {}
        self.deltatime_accumulator = 0
        self.speed = 1

    def update(self, deltatime):
        self.deltatime_accumulator += deltatime
        if(self.deltatime_accumulator > 5):
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
            
            # ENLEVER LES ELEMENTS QUI ONT TERMINÉ LEUR DEPLACEMENT
            for element in to_remove:
                self.stack_of_objects[element].pop(0)
                self.check_destination(element)

    def add_object_to_move(self, object, tab_directions):
        object.character_animation.play()
        object.input_active = False
        self.stack_of_objects[object] = tab_directions
        self.check_destination(object)
        
    def check_destination(self, object):
        # SI IL Y A ENCORE DES DESTINATIONS
        if(len(self.stack_of_objects[object]) > 0):
            if(self.stack_of_objects[object][0] == 0):
                self.destination_stack[object] = (object.position[0],object.position[1]+(16*3))
            elif(self.stack_of_objects[object][0] == 1):
                self.destination_stack[object] = (object.position[0],object.position[1]-(16*3))
            elif(self.stack_of_objects[object][0] == 2):
                self.destination_stack[object] = (object.position[0]-(16*3),object.position[1])
            elif(self.stack_of_objects[object][0] == 3):
                self.destination_stack[object] = (object.position[0]+(16*3),object.position[1])
            try:
                object.character_animation.set_direction(self.stack_of_objects[object][0])
            except:
                print("Impossible de modifier la direction du personnage")
        else:
            object.input_active = True
            #object.character_animation.stop()
            self.stack_of_objects.pop(object)