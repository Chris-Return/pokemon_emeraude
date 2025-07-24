from src.components.component import Component
from src.data.datamanager import DataManager

class Tile(Component):

    def __init__(self, data_tab):
        super().__init__(None)
        self.vanilla_data = data_tab
        self.insert_all_datas()
        self.set_component(DataManager.get_tileset(self.tileset_number).get_tile_at(int(self.x), int(self.y)))


    def copy(self):
        return Tile(self.vanilla_data)
    
    def insert_all_datas(self):
        splited_data = self.vanilla_data.split(",")
        try:
            self.tileset_number = int(splited_data[0])
            self.x = int(splited_data[1])
            self.y = int(splited_data[2])
            self.collider = int(splited_data[3])
            self.sort_number = int(splited_data[4])
        except:
            print("Erreur de lecture de la tuile")
    
    def get_collision(self):
        return self.collider
    
    def get_vanilla_data(self):
        return self.vanilla_data
    
    def set_collider(self, number):
        self.collider = number

    def set_self(self, tile):
        self = tile        