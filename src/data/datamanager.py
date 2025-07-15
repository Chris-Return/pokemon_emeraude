from src.data.mapdata import MapData
from src.data.playerdatav2 import PlayerDataV2

class DataManager():

    data_holders = [MapData(), PlayerDataV2()]

    def __init__(self):
        pass

    @staticmethod
    def load():
        for data_holder in DataManager.data_holders:
            data_holder.loadData()

    def get_tileset(number):
        return DataManager.data_holders[0].data[int(number)]