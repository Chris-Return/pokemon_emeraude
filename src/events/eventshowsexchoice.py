from src.events.gameevent import GameEvent
from src.components.component import *
from src.data.playerdata import *

import pygame

class EventShowSexChoice(GameEvent):
    def __init__(self):
        super().__init__()
        self.components = [ Component(pygame.image.load(IMG_CHOIX_GARCON_FILLE)),
                            Component(pygame.image.load(IMG_FLECHE_CHOIX)),
                            Component(pygame.image.load(IMG_PLAYER_MALE)),
                            Component(pygame.image.load(IMG_PLAYER_FEMALE)) ]
        
        self.components[0].set_position((50,100))
        self.components[1].set_position((76,137))
        self.components[2].set_position((510,110))
        self.components[3].set_position((510,110))
        self.components[3].set_visible(False)

    def update(self, deltatime):
        pass

    def check_inputs(self, event):
        if(event.type == pygame.KEYDOWN and self.active):
            if(event.key == pygame.K_DOWN):
                self.components[3].set_visible(True)
                self.components[2].set_visible(False)
                self.components[1].set_position((76,184))
                PlayerData.sex = "F"

            if(event.key == pygame.K_UP):
                self.components[3].set_visible(False)
                self.components[2].set_visible(True)
                self.components[1].set_position((76,137))
                PlayerData.sex = "M"

            if(event.key == pygame.K_RETURN or event.key == pygame.K_w):
                self.components[0].set_visible(False)
                self.components[1].set_visible(False)
                self.active = False

            
