from src.constants.constants import SCREEN_SCALE
from src.maps.tile import Tile

class MapReader():
    def __init__(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as fichier:
                self.file_data = fichier.readlines()
        except:
            print("Le fichier : "+file_path+" est introuvable")

    def get_lines_after(self, word):
        lines = []
        begin_read = False
        for i in range(len(self.file_data)):
            self.file_data[i] = self.file_data[i].strip()
            if(begin_read and self.file_data[i].__contains__("break")):
                break

            if(begin_read):
                lines.append(self.file_data[i])

            if(self.file_data[i].__contains__(word)):
                begin_read = True

        return lines if len(lines) > 0 else None
    
    def read_layers(self, tab, total_excent_x, additional_y):
        map_data = []
        for y in range (len(tab)):
            perfect_line = tab[y].strip()
            perfect_lines = perfect_line.split(";")
            for x in range (len(perfect_lines)):
                tile = Tile(perfect_lines[x])
                tile.set_position(((16 * SCREEN_SCALE * x) + (16 * SCREEN_SCALE * total_excent_x),(16 * SCREEN_SCALE * y) + (16 * SCREEN_SCALE * additional_y)))
                try:
                    map_data[x].append(tile)
                except:
                    map_data.append([])
                    map_data[x].append(tile)

        return map_data
    
    def read_adjacent_maps(self):
        cartes_adjacentes = [None, None, None, None]
        maps_name = ["map_down", "map_up", "map_left", "map_right"]
        for i in range(4):
            try:
                cartes_adjacentes[i] = self.get_lines_after(maps_name[i])[0].strip()
            except:
                pass
        
        return cartes_adjacentes
    
    def read_characters(self):
        characters = []
        characters_data = self.get_lines_after("characters")
        try:
            for character_data in characters_data:
                data = character_data.strip()
                data = data.split(",")
                characters.append(data)
        except:
            pass

        return characters

    
    def read_repeat(self, tab):
        tiles = []
        perfect_line = tab[0].strip()
        perfect_lines = perfect_line.split(";")
        for line in perfect_lines:
            tiles.append(Tile(line))

        return tiles