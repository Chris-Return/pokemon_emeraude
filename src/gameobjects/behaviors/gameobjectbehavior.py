from src.gameobjects.behaviors.movebehavior import MoveBehavior
from src.gameobjects.behaviors.directionalbehavior import DirectionalBehavior
from src.maps.mapanalyser import MapAnalyser

class GameObjectBehavior():
    def __init__(self, parent):
        # Définir si actif
        self.active = True
        # Propriétaire du comportement
        self.parent = parent
        # Vérifier si l'objet peut bouger sur la carte
        self.allow_movement = True
        # Vérifier si l'objet est autorisé à changer de direction
        self.allow_directional_change = True
        # Rayon de déplacement (seulement si autorisé)
        self.movement_length = 2
        # Point central du comportement
        self.center_point = parent.get_map_position()
        # Si le joueur possède le flag, on passe au behavior suivant
        self.flag = None
        # Déclencher ce behavior si flag ok sur le joueur
        self.sub_behavior = None
        # Lignes de dialogues liées à ce behavior
        self.dialog = ["Test d'un texte en première|ligne du jeu.", "Et ceci est un second texte."]
        # Pokémons que possèdent le PNJ
        self.pokemons = []
        # Vision du personnage
        self.vision_length = 0
        # Type d'Event
        self.type = None

        # Accumulateurs de temps
        self.deltatime_accumulator_movement = 0
        self.deltatime_accumulator_direction = 0

        self.random_deltatime_accumulator_movement = 1000
        self.random_deltatime_accumulator_direction = 2000


    def update(self, deltatime):
        if(self.active):
            MoveBehavior.update(deltatime, self.get_behavior())
            DirectionalBehavior.update(deltatime, self.get_behavior())

    # TODO Modifier par rapport aux données du joueur
    def get_behavior(self):
        return self.sub_behavior if self.sub_behavior is not None else self
    
    # Vérifier si le mouvement désiré n'est pas en dehors de la zone de circulation
    def get_movement_out_of_scope(self, direction):
        future_positon = MapAnalyser.get_future_position(self.parent, direction)
        if((direction == 0 or direction == 1) and abs(self.center_point[1] - future_positon[1]) > self.movement_length):
            return False
        elif((direction == 2 or direction == 3) and abs(self.center_point[0] - future_positon[0]) > self.movement_length):
            return False
        return True
    
    def get_parent(self):
        return self.parent
    
    def set_active(self, active):
        self.active = active

    def set_center_position(self, position):
        self.center_point = position

    def as_dialog(self):
        return len(self.dialog) > 0
    
    def get_dialog(self):
        return self.dialog