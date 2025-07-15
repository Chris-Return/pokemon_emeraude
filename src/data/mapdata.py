from src.data.dataholder import DataHolder
from src.maps.tileset import Tileset
from src.constants.constants import *

class MapData(DataHolder):

    def __init__(self):
        super().__init__()

    def loadData(self):
        super().loadData()
        self.data = [Tileset(TILESET_OUTDOORS),
                     Tileset(TILESET_INDOORS)]