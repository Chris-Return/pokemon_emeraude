from src.components.component import Component
from src.data.datamanager import DataManager

class Tile(Component):

    def __init__(self, data_tab):
        super().__init__(None)
        self.vanilla_data = data_tab
        splited_data = self.vanilla_data.split(",")

        try:
            self.tileset_number = int(splited_data[0])
            self.x = int(splited_data[1])
            self.y = int(splited_data[2])
            self.collider = int(splited_data[3])
            self.sort_level = int(splited_data[4])
        except:
            print("Erreur de lecture de la tuile")

        self.set_component(DataManager.get_tileset(self.tileset_number).get_tile_at(int(self.x), int(self.y)))


    def copy(self):
        return Tile(self.vanilla_data)
    
    def get_collision(self):
        return self.collider