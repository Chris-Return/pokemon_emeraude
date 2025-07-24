from src.gameobjects.gameobject import GameObject
from src.gameobjects.behaviors.gameobjectbehavior import GameObjectBehavior
from src.animation.gridanimation import GridAnimation
from src.constants.constants import SCREEN_SCALE, GET_PNG

class GameObjectCharacter(GameObject):
    def __init__(self, game_object_mover, number):
        super().__init__()
        try:
            self.character_animation = GridAnimation(GET_PNG(number))
        except:
            print("Impossible de charger l'animation correspondante : "+number)
        self.game_object_mover = game_object_mover
        # Ne pas l'exécuter pour les personnages contrôlés par le joueur
        if(number > 1):
            self.game_object_behavior = GameObjectBehavior(self)

    def update(self, deltatime):
        super().update(deltatime)
        self.character_animation.update(deltatime)
        try:
            self.game_object_behavior.update(deltatime)
        except:
            pass

    def move_to(self, tab_directions):
        self.game_object_mover.add_object_to_move(self, tab_directions)
    
    def get_component(self):
        visible_component = self.character_animation.get_component()
        visible_component.set_position(self.get_position())
        return visible_component
    
    def set_position(self, position):
        self.position = position

    def teleport_at_map_position(self, position):
        self.set_position((position[0]*16*SCREEN_SCALE, position[1]*16*SCREEN_SCALE))
        self.set_map_position(position)
        try:
            self.game_object_behavior.set_center_position(position)
        except:
            pass

    def get_animation(self):
        return self.character_animation

    def get_position(self):
        return (self.character_animation.excent[0] + self.position[0], self.character_animation.excent[1] + self.position[1])
    
    def set_game_object_mover(self, game_object_mover):
        self.game_object_mover = game_object_mover

    def get_game_object_mover(self):
        return self.game_object_mover

    def set_direction(self, direction):
        self.character_animation.set_direction(direction)

    def get_direction(self):
        return self.character_animation.get_direction()
    
    def set_active(self, active):
        self.active = active
        self.game_object_behavior.set_active(active)

    def get_game_object_behavior(self):
        return self.game_object_behavior