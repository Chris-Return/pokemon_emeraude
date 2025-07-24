
class MapAnalyser():

    map_manager = None
    gamemap = None
    locked_map_positions = []
    player = None

    def __init__(self):
        pass

    @staticmethod
    def check_move(gameobject, direction):
        # Données de la carte 
        map_data = MapAnalyser.gamemap.get_map_data()
        gameobject_position = gameobject.get_map_position()
        future_position = MapAnalyser.get_future_position(gameobject, direction)

        # Vérifier si la carte est ok
        if(not MapAnalyser.check_mapobject_out(gameobject_position, direction) and MapAnalyser.gamemap.get_adjacent_maps()[direction] is None):
            return False
        
        # Vérifier si la carte interdit le déplacement
        no_map_collision = MapAnalyser.check_mapobject_collision(map_data, gameobject, direction)

        # Vérifier si la case est bloquée en vue d'un objet actuellement en mouvement
        unlocked_destination = True
        if future_position in MapAnalyser.locked_map_positions:
            unlocked_destination = False

        # Vérifier si il y a un joueur/pnj actuellement sur la route
        character_free = MapAnalyser.is_character_free(future_position)

        return no_map_collision and unlocked_destination and character_free
    
    def is_character_free(future_position):
        characters = MapAnalyser.gamemap.get_characters()
        for character in characters:
            if(character.get_map_position() == future_position):
                return False
            
        if(MapAnalyser.player.get_map_position() == future_position):
            return False
        
        return True
    
    @staticmethod
    def define_element_position(element, direction):
        # Si on ne sort pas de la carte
        old_position = element.get_map_position()
        element.set_map_position(MapAnalyser.get_future_position(element, direction))

        if(not MapAnalyser.check_mapobject_out(old_position, direction)):
            MapAnalyser.map_manager.set_actual_map_direction(direction)
        
        MapAnalyser.unlock_position(element.get_map_position())

    def get_future_position(element, direction):
        future_position = None
        if(MapAnalyser.check_mapobject_out(element.get_map_position(), direction)):
            if(direction == 0):
                future_position = (element.get_map_position()[0], element.get_map_position()[1]+1)
            elif(direction == 1):
                future_position = (element.get_map_position()[0], element.get_map_position()[1]-1)
            elif(direction == 2):
                future_position = (element.get_map_position()[0]-1, element.get_map_position()[1])
            elif(direction == 3):
                future_position = (element.get_map_position()[0]+1, element.get_map_position()[1])
        else:
            # Récupérer la carte dans la direction nécessaire et replacer le joueur
            if(MapAnalyser.map_manager.get_map(direction) == None and (direction == 1 or direction == 2)):
                return None
            
            if(direction == 0): 
                future_position = (element.get_map_position()[0], 0)
            elif(direction == 1):
                future_position = (element.get_map_position()[0], MapAnalyser.map_manager.get_map(direction).get_map_height()-1)
            elif(direction == 2):
                future_position = (MapAnalyser.map_manager.get_map(direction).get_map_width()-1, element.get_map_position()[1])
            elif(direction == 3):
                future_position = (0, element.get_map_position()[1])

        return future_position


    def lock_future_position(element, direction):
        MapAnalyser.locked_map_positions.append(MapAnalyser.get_future_position(element, direction))
    
    @staticmethod
    def unlock_position(position):
        MapAnalyser.locked_map_positions.remove(position)

    # Vérifier si on ne dépasse pas la limite de la carte
    @staticmethod
    def check_mapobject_out(gameobject_position, direction):
        if(gameobject_position[0] == 0 and direction == 2):
            return False
        elif(gameobject_position[0] == MapAnalyser.gamemap.get_map_width()-1 and direction == 3):
            return False
        elif(gameobject_position[1] == MapAnalyser.gamemap.get_map_height()-1 and direction == 0):
            return False
        elif(gameobject_position[1] == 0 and direction == 1):
            return False
        return True
    
    # Vérification simple des collisions sans carte adjacente
    @staticmethod
    def check_mapobject_collision(map_data, gameobject, direction):
        position = MapAnalyser.get_future_position(gameobject, direction)
        if(map_data[position[0]][position[1]].get_collision() == 1):
            return False
        return True

    @staticmethod
    def set_map_manager(map_manager):
        MapAnalyser.map_manager = map_manager
        MapAnalyser.gamemap = map_manager.get_actual_map()

    def set_player(player):
        MapAnalyser.player = player