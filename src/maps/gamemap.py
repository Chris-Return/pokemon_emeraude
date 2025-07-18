from src.maps.tile import Tile
from warnings import deprecated
from src.components.component import Component
from src.constants.constants import *

# Données d'une carte
class GameMap():
    def __init__(self, file_path, additional_x, additional_y):
        try:
            with open(file_path, "r", encoding="utf-8") as fichier:
                self.file_data = fichier.readlines()
        except:
            print("Le fichier : "+file_path+" est introuvable")

        self.map_data = []
        self.repeat = []
        self.cartes_adjacentes = [None, None, None, None]
        self.excent_x = 0
        self.excent_y = 0
        self.additional_x = additional_x
        self.additional_y = additional_y
        self.read_adjacent_maps()

        self.read_layers(self.get_lines_after("layers"))
        self.repeat = self.read_repeat(self.get_lines_after("repeat"))
        self.repeat = [
                        [self.repeat[0], self.repeat[2]], 
                        [self.repeat[1], self.repeat[3]] ]

    @deprecated("À utiliser uniquement pour les tests. Il ne faut jamais afficher toutes les cases pour des raisons de performance.")
    def get_all_components(self):
        all_tiles = []
        for tiles in self.map_data:
            for tile in tiles:
                all_tiles.append(tile)
        
        return all_tiles
    
    def get_lines_after(self, word):
        lines = []
        begin_read = False
        for i in range(len(self.file_data)):
            if(begin_read and self.file_data[i].__contains__("break")):
                break

            if(begin_read):
                lines.append(self.file_data[i])

            if(self.file_data[i].__contains__(word)):
                begin_read = True
        
        return lines
    
    def read_layers(self, tab):
        for y in range (len(tab)):
            perfect_line = tab[y].strip()
            perfect_lines = perfect_line.split(";")
            for x in range (len(perfect_lines)):
                tile = Tile(perfect_lines[x])
                tile.set_position(((16 * SCREEN_SCALE * x) + (16 * SCREEN_SCALE * self.get_total_excent_x()),(16 * SCREEN_SCALE * y) + (16 * SCREEN_SCALE * self.get_additional_y())))
                try:
                    self.map_data[x].append(tile)
                except:
                    self.map_data.append([])
                    self.map_data[x].append(tile)

    def read_adjacent_maps(self):
        maps_name = ["map_down", "map_up", "map_left", "map_right"]
        for i in range(4):
            try:
                self.cartes_adjacentes[i] = self.get_lines_after(maps_name[i])[0].strip()
            except:
                pass

    def read_repeat(self, tab):
        tiles = []
        perfect_line = tab[0].strip()
        perfect_lines = perfect_line.split(";")
        for line in perfect_lines:
            tiles.append(Tile(line))

        return tiles
    
    def get(self, x, y):
        if(x >= self.get_map_width() or x < 0 or y >= self.get_map_height() or y < 0):
            return None
        return self.map_data[x][y]

    
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