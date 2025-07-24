from src.gameobjects.gameobjectcharacter import GameObjectCharacter
from src.events.map.dialogevent import DialogEvent

class GameEventManager():
    def __init__(self):
        pass

    @staticmethod
    def get_generated_game_event_at(gameobjects, map_position):
        for gameobject in gameobjects:
            # Verifier la position de l'objet
            if(gameobject.get_map_position() == map_position):
                if(isinstance(gameobject, GameObjectCharacter)):
                    behavior = gameobject.get_game_object_behavior()
                    # Calculer les events
                    return GameEventManager.generate_game_event(gameobject, behavior)
        
        return None

    @staticmethod
    def generate_game_event(gameobject, behavior):
        if(behavior.as_dialog()):
            lines = behavior.get_dialog().copy()
            return DialogEvent(gameobject, lines)
        return None