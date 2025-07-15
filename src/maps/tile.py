from src.components.component import Component
from src.data.datamanager import DataManager

class Tile(Component):

    number_of_tiles = 0

    def __init__(self, data_tab):
        super().__init__(None)
        self.vanilla_data = data_tab
        Tile.number_of_tiles += 1
        splited_data = self.vanilla_data.split(",")

        try:
            self.tileset_number = splited_data[0]
            self.x = splited_data[1]
            self.y = splited_data[2]
            self.collider = splited_data[3]
            self.sort_level = splited_data[4]
        except:
            print("Erreur de lecture de la tuile n°"+str(Tile.number_of_tiles))

        self.set_component(DataManager.get_tileset(self.tileset_number).get_tile_at(int(self.x), int(self.y)))