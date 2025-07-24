from src.maps.mapreader import MapReader
from src.constants.constants import MAP_STEREOTYPE
from src.maps.tile import Tile

class MapStereotype():

    map_reader = MapReader(MAP_STEREOTYPE)
    tab_colliders = {}
    tab_replacer = {}

    def __init__(self):
        pass

    @staticmethod
    def load():
        MapStereotype.get_all_colliders(1)
        MapStereotype.get_all_replacer()

    @staticmethod
    def get_all_colliders(number):
        tab_colliders = None
        tab_colliders = MapStereotype.map_reader.get_lines_after(str("auto_collider:"+str(number)))
        if(tab_colliders != None):
            colliders = tab_colliders[0].split(";")
            for collider in colliders:
                MapStereotype.tab_colliders[collider] = number
            MapStereotype.get_all_colliders((number+1))

    @staticmethod
    def get_all_replacer():
        tab_replacer = None
        tab_replacer = MapStereotype.map_reader.get_lines_after("replacer:")
        if(tab_replacer != None):
            # Enlever les espaces
            tab_replacer[0].strip()
            datas = tab_replacer[0].split(";")
            # Boucler sur les couples "Tuile cible" : Tuiles de remplacement[]
            for data in datas:
                # couple[0] = Tuile cible
                couple = data.split(":")
                # couple[1] liste des tuiles de remplacement
                MapStereotype.tab_replacer[couple[0]] = couple[1].split("|")

    @staticmethod
    def get_collider_for(tile):
        try:
            return MapStereotype.tab_colliders[tile.vanilla_data]
        except:
            return tile.get_collision()

    @staticmethod
    def get_replacement_for(tile):
        try:
            tile_data = MapStereotype.tab_replacer[tile.get_vanilla_data()]
            main_tile = Tile(tile_data[0])
            main_tile.set_position(tile.get_position())
            for i in range(1, len(tile_data)):
                new_tile = Tile(tile_data[i])
                new_tile.set_position(main_tile.get_position())
                main_tile.get_children().append(new_tile)
                
            return main_tile
        except:
            return tile
        