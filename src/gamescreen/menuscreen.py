from src.gamescreen.gamescreen import *
from src.components.component import *
from src.constants.constants import *
import math
import pygame



class MenuScreen(GameScreen):

    def __init__(self):
        super().__init__()
        self.next_screen_number = 1
        self.background_image = Component(pygame.image.load(IMG_BACKGROUND_MAIN_MENU_2))
        self.background_image.get_component().set_alpha(255)
        self.deltaTimeBackground = 0
        self.deltaTimePressStart = 0
        self.background_image_ascending = False

        self.pokemon_logo = Component(pygame.image.load(IMG_POKEMON_TITLE))
        self.pokemon_logo.set_position((75,0))

        self.pokemon_credit = Component(pygame.image.load(IMG_CREDITS))
        self.pokemon_credit.set_position((0,425))

        self.press_start = Component(pygame.image.load(IMG_PRESS_START))
        self.press_start.set_position((150,310))

        self.brume = Component(pygame.image.load(IMG_BRUME))
        self.brume.get_component().set_alpha(100)
        
        self.components = [ Component(pygame.image.load(IMG_BACKGROUND_MAIN_MENU_1)),
                            self.background_image,
                            self.brume,
                            self.pokemon_logo,
                            self.pokemon_credit,
                            self.press_start ]

    def update(self, deltatime):
        super().update(deltatime)
        self.update_rayquaza(deltatime)
        self.update_press_start(deltatime)

    def update_rayquaza(self, deltatime):
        self.deltaTimeBackground += deltatime

        if(self.deltaTimeBackground > 5):

            if(self.background_image.get_component().get_alpha() == 255):
                self.background_image_ascending = False

            if(self.background_image.get_component().get_alpha() == 0):
                self.background_image_ascending = True

            self.background_image.get_component().set_alpha(int(self.background_image.get_component().get_alpha())+1 if self.background_image_ascending else int(self.background_image.get_component().get_alpha())-1)
            self.deltaTimeBackground = 0

    def update_press_start(self, deltatime):
        self.deltaTimePressStart += deltatime
        if(self.deltaTimePressStart > 350):
            self.press_start.set_visible(not self.press_start.get_visible())
            self.deltaTimePressStart = 0
    
    def check_events(self, event):
        if(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_RETURN):
                self.active = False