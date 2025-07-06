import json
from src.constants.constants import *

class JSONData():

    def __init__(self):
        self.json_to_load = [JSON_POKEMON_BASIC_DATA]
        self.data = []

    def loadAll(self):
        for file in self.json_to_load:
            with open(file, "r", encoding="utf-8") as fichier:
                self.data.append(json.load(fichier))

    def getLoadedDatas(self):
        return self.data