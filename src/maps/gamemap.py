from src.maps.mapreader import MapReader
from src.gameobjects.gameobjectcharacter import GameObjectCharacter

# Données d'une carte
class GameMap():
    def __init__(self, file_path, additional_x, additional_y):
        # ici, le active est utilisé uniquement pour activer les activités des objets liés
        self.active = False
        self.map_reader = MapReader(file_path)
        self.cartes_adjacentes = self.map_reader.read_adjacent_maps()
        characters_data = self.map_reader.read_characters()
        self.characters = []

        for data in characters_data:
            character = GameObjectCharacter(None, int(data[0]))
            character.teleport_at_map_position((int(data[1]), int(data[2])))
            self.characters.append(character)

        self.excent_x = 0
        self.excent_y = 0
        self.additional_x = additional_x
        self.additional_y = additional_y
        self.map_data = self.map_reader.read_layers(self.map_reader.get_lines_after("layers"), self.get_total_excent_x(), self.additional_y)
        self.repeat = self.map_reader.read_repeat(self.map_reader.get_lines_after("repeat"))
        self.repeat = [ [self.repeat[0], self.repeat[2]], 
                        [self.repeat[1], self.repeat[3]] ]

    def get_all_components(self):
        all_tiles = []
        for tiles in self.map_data:
            for tile in tiles:
                all_tiles.append(tile)
        
        return all_tiles
    
    def get_characters_components(self):
        all_tiles = []
        for character in self.characters:
            all_tiles.append(character.get_component())
        return all_tiles
    
    def get(self, x, y):
        if(x >= self.get_map_width() or x < 0 or y >= self.get_map_height() or y < 0):
            return None
        return self.map_data[x][y]
    
    def set_all_game_object_mover(self, go):
        try:
            for c in self.characters:
                c.set_game_object_mover(go)
        except:
            pass

    def get_characters(self):
        return self.characters
    
    def get_total_excent_x(self):
        return self.additional_x + self.excent_x
    
    def get_total_excent_y(self):
        return self.additional_y + self.excent_y
    
    def get_additional_x(self):
        return self.additional_x
    
    def get_additional_y(self):
        return self.additional_y
    
    def get_map_data(self):
        return self.map_data

    def get_tile_at(self,x,y):
        return self.map_data[x][y]
    
    def get_map_width(self):
        return len(self.map_data[0])
    
    def get_map_height(self):
        return len(self.map_data)
    
    def get_repeat(self):
        return self.repeat
    
    def get_map_data(self):
        return self.map_data
    
    def get_adjacent_maps(self):
        return self.cartes_adjacentes