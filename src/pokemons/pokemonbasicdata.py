import json
import pygame
from src.constants.constants import *
from PIL import Image

class PokemonBasicData():
    def __init__(self, json_data):
        self.id = json_data["id"]
        self.name = json_data["name"]["french"]
        self.types = json_data["type"]
        self.hp = json_data["base"]["HP"]
        self.attack = json_data["base"]["Attack"]
        self.defense = json_data["base"]["Defense"]
        self.spe_attack = json_data["base"]["Sp. Attack"]
        self.spe_defense = json_data["base"]["Sp. Defense"]
        self.speed = json_data["base"]["Speed"]
        self.front_frames = []
        self.loadFrames()

    def show_values(self):
        for attr, valeur in self.__dict__.items():
            print(f"{attr} = {valeur}")

    def loadFrames(self):
        pil_gif = Image.open(ASSETS_POKEMONS + self.id + ".gif")
        try:
            while(True):
                frame = pil_gif.convert("RGBA")
                pygame_image = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
                self.front_frames.append(pygame_image.copy())
                pil_gif.seek(pil_gif.tell() + 1)
        except:
            pass