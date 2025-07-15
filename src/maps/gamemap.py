from src.maps.tile import Tile
from warnings import deprecated

# Données d'une carte
class GameMap():
    def __init__(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as fichier:
                self.file_data = fichier.readlines()
        except:
            print("Le fichier : "+file_path+" est introuvable")

        self.map_data = []

        for y in range (len(self.file_data)):
            perfect_line = self.file_data[y].strip()
            perfect_lines = perfect_line.split(";")
            for x in range (len(perfect_lines)):
                tile = Tile(perfect_lines[x])
                tile.set_position(((16*3 * x),(16*3 * y)))
                try:
                    self.map_data[x].append(tile)
                except:
                    self.map_data.append([])
                    self.map_data[x].append(tile)

    @deprecated("À utiliser uniquement pour les tests. Il ne faut jamais afficher toutes les cases pour des raisons de performance.")
    def get_all_components(self):
        all_tiles = []
        for tiles in self.map_data:
            for tile in tiles:
                all_tiles.append(tile)
        
        return all_tiles
    
    # X et Y étant la position du joueur
    def get_around_tiles(self, x, y):
        pass

    def get_tile_at(self,x,y):
        return self.map_data[x][y]
    
    def get_map_width(self):
        return len(self.map_data[0])
    
    def get_map_height(self):
        return len(self.map_data)