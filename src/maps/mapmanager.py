from src.maps.gamemap import GameMap
from src.maps.mapanalyser import MapAnalyser
from src.constants.constants import *

class MapManager():
    def __init__(self):
        self.loaded_maps = {}
        self.actualMap = None

    def set_actual_map(self, map_path):
        self.actualMap = self.loaded_maps[map_path]
        MapAnalyser.gamemap = self.actualMap

    def load_map(self, map_path, repeat, additional_x, additional_y):
        try:
            self.loaded_maps[map_path]
        except KeyError:
            self.loaded_maps[map_path] = GameMap(map_path, additional_x, additional_y)
            if(self.actualMap is None):
                self.set_actual_map(map_path)
            # Mon but ici est de charger la carte sur laquelle le joueur se trouve
            # ainsi que les cartes autours de celles-ci
            if(repeat):
                for i in range (len(self.loaded_maps[map_path].get_adjacent_maps())):
                    map = self.loaded_maps[map_path].get_adjacent_maps()[i]
                    if(map is not None): # POUR MOI, IL FAUDRAIT AUSSI RAJOUTER L'EXCENTRAGE TOTAL
                        if(i == 0): # EN BAS
                            self.load_map(eval(map), False, self.actualMap.get_total_excent_x(), self.actualMap.get_map_height() + self.actualMap.get_total_excent_y())
                        elif(i == 1): # EN HAUT
                            self.load_map(eval(map), False, self.actualMap.get_total_excent_x(), -self.actualMap.get_map_height() + self.actualMap.get_total_excent_y())
                        elif(i == 2): # A GAUCHE
                            self.load_map(eval(map), False, -self.actualMap.get_map_width() + self.actualMap.get_total_excent_x(), self.actualMap.get_total_excent_y())
                        elif(i == 3):# A DROITE
                            self.load_map(eval(map), False, self.actualMap.get_map_width() + self.actualMap.get_total_excent_x(), self.actualMap.get_total_excent_y())

    def get_limited_components(self, player):
        player_position = player.get_map_position() # LA BASE, C'EST LA POSITION DU BOUG
        rectLargeur = 18 # AFFICHER 18 CASES EN LARGEUR
        rectHauteur = 14 # AFFICHER 12 CASES EN HAUTEUR
        startRow = player_position[0] - int(rectLargeur/2) # CENTRER
        startCol = player_position[1] - int(rectHauteur/2) # CENTRER
        all_tiles = []

        for i in range(startRow, startRow + rectLargeur):
            for j in range(startCol, startCol + rectHauteur):
                try:
                    # J'EVITE LES ELEMENTS NEGATIFS POUR EVITER LES COMPORTEMENTS INATTENDUS
                    if(i < 0 or j < 0):
                        raise IndexError
                    all_tiles.append(self.actualMap.get_map_data()[i][j])
                except IndexError:
                    new_tile = None
                    if(j > self.actualMap.get_map_height() and self.actualMap.get_adjacent_maps()[0]):
                        # Carte en bas
                        map = self.loaded_maps[eval(self.actualMap.get_adjacent_maps()[0])]
                        new_tile = map.get_map_data()[i][-map.get_map_height()+j]
                    elif(j < 0 and self.actualMap.get_adjacent_maps()[1]):
                        # Carte en haut
                        map = self.loaded_maps[eval(self.actualMap.get_adjacent_maps()[1])]
                        #print("Value : ("+str(i)+","+str(map.get_map_height()+j)+")")
                        new_tile = map.get(i,map.get_map_height()+j)
                    elif(i < 0 and self.actualMap.get_adjacent_maps()[2]):
                        # Carte à gauche
                        map = self.loaded_maps[eval(self.actualMap.get_adjacent_maps()[2])]
                        new_tile = map.get_map_data()[-map.get_map_width()+i][j]
                    elif(i > self.actualMap.get_map_width() and self.actualMap.get_adjacent_maps()[3]):
                        # Carte à droite
                        map = self.loaded_maps[eval(self.actualMap.get_adjacent_maps()[3])]
                        new_tile = map.get_map_data()[map.get_map_width()+i][j]

                    # AFFICHAGE DU BACKGROUND REPETABLE
                    if(new_tile is None):
                        new_tile = self.actualMap.repeat[i%2][j%2].copy()
                        new_tile.set_position(((16 * SCREEN_SCALE * i),(16 * SCREEN_SCALE * j)))
                    
                    all_tiles.append(new_tile)

        return all_tiles

    def get_actual_map(self):
        return self.actualMap
