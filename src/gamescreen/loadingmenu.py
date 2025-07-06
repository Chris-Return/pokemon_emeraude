from src.gamescreen.gamescreen import *
from src.components.component import *
from src.constants.constants import *
import pygame

class LoadingMenu(GameScreen):

    def __init__(self):
        super().__init__()
        self.next_screen_number = 2
        self.selection = 0
        self.bouton_option = Component(pygame.image.load(IMG_OPTIONS_INACTIVE))
        self.bouton_option.set_position((0,100))

        self.bouton_option_active = Component(pygame.image.load(IMG_OPTIONS))
        self.bouton_option_active.set_position((0,100))
        self.bouton_option_active.set_visible(False)

        self.bouton_nouvelle_partie = Component(pygame.image.load(IMG_NOUVELLE_PARTIE))
        self.bouton_nouvelle_partie.set_position((0,5))

        self.bouton_nouvelle_partie_inactive = Component(pygame.image.load(IMG_NOUVELLE_PARTIE_INACTIVE))
        self.bouton_nouvelle_partie_inactive.set_position((0,5))
        self.bouton_nouvelle_partie_inactive.set_visible(False)

        self.components = [Component(pygame.image.load(IMG_BACKGROUND_LOADING_SCREEN)),
                           self.bouton_nouvelle_partie,
                           self.bouton_nouvelle_partie_inactive,
                           self.bouton_option_active,
                           self.bouton_option]

    def update(self, deltatime):
        pass

    def check_events(self, event):
        if(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_DOWN):
                self.bouton_nouvelle_partie.set_visible(False)
                self.bouton_nouvelle_partie_inactive.set_visible(True)
                self.bouton_option.set_visible(False)
                self.bouton_option_active.set_visible(True)
                self.selection = 1

            if(event.key == pygame.K_UP):
                self.bouton_nouvelle_partie.set_visible(True)
                self.bouton_nouvelle_partie_inactive.set_visible(False)
                self.bouton_option.set_visible(True)
                self.bouton_option_active.set_visible(False)
                self.selection = 0

            if(event.key == pygame.K_RETURN and self.selection == 0):
                self.next_screen_number = 2
                self.active = False