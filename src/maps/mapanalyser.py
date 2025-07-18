
class MapAnalyser():

    gamemap = None
    locked_map_positions = []

    def __init__(self):
        pass

    @staticmethod
    def check_move(gameobject, direction):
        # Données de la carte 
        map_data = MapAnalyser.gamemap.get_map_data()
        gameobject_position = gameobject.get_map_position()

        # Vérifier si la carte est ok
        if(not MapAnalyser.check_mapobject_out(map_data, gameobject_position, direction) and
            MapAnalyser.gamemap.get_adjacent_maps()[direction] is None):
            return False

        map_collision = MapAnalyser.check_mapobject_collision(map_data, gameobject_position, direction)

        return map_collision
    
    # Vérifier si on ne dépasse pas la limite de la carte
    def check_mapobject_out(map_data, gameobject_position, direction):
        no_border = True
        if(gameobject_position[0] == 0 and direction == 2):
            no_border = False
        if(gameobject_position[0] == MapAnalyser.gamemap.get_map_width()-1 and direction == 3):
            no_border = False
        if(gameobject_position[1] == MapAnalyser.gamemap.get_map_height()-1 and direction == 0):
            no_border = False
        if(gameobject_position[1] == 0 and direction == 1):
            no_border = False
        # MapAnalyser.gamemap.get_adjacent_maps()[direction]
        return no_border
    
    # Vérification simple des collisions sans carte adjacente
    # TODO : Modifier pour prendre en compte les cartes adjacentes dans une future update
    @staticmethod
    def check_mapobject_collision(map_data, gameobject_position, direction):
        if(direction == 0 and map_data[gameobject_position[0]][gameobject_position[1]+1].get_collision() == 1):
            return False
        elif(direction == 1 and map_data[gameobject_position[0]][gameobject_position[1]-1].get_collision() == 1):
            return False
        elif(direction == 2 and map_data[gameobject_position[0]-1][gameobject_position[1]].get_collision() == 1):
            return False
        elif(direction == 3 and map_data[gameobject_position[0]+1][gameobject_position[1]].get_collision() == 1):
            return False
        
        return True