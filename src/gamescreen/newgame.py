from src.gamescreen.gamescreen import *
from src.components.component import *
from src.components.componentunscaled import *
from src.constants.constants import *
from src.components.dialogsystem import *
import pygame

class NewGameScreen(GameScreen):

    def __init__(self):
        super().__init__()
        self.next_screen_number = 4
        self.waiting_update_time = 10
        self.waiting_before_load = 1000
        self.deltatimebeforeload = 0
        self.deltatimegradiant = 0
        self.deltatimeprofground = 0
        self.deltatimeprofseko = 0
        self.deltatimeshowdialogbox = 0

        self.up_gradiant = Component(pygame.image.load(IMG_UP_GRADIANT_NEW_GAME))
        self.up_gradiant.get_component().set_alpha(0)

        self.prof_ground = Component(pygame.image.load(IMG_PROF_GROUND_NEW_GAME))
        self.prof_ground.get_component().set_alpha(0)

        self.prof_seko = Component(pygame.image.load(IMG_PROF_SEKO_NEW_GAME))
        self.prof_seko.get_component().set_alpha(0)
        self.prof_seko.set_position((335,80))

        self.dialogbox = DialogSystem(None, self)
        self.player_sprite = Component(None)
        self.player_sprite.set_position((510,110))

        self.components = [Component(pygame.image.load(IMG_BACKGROUND_NEW_GAME)),
                           self.up_gradiant,
                           self.prof_ground,
                           self.prof_seko]
        
        self.dialogbox.uploadParagraphs(PROF_SEKO_INTRO_1 if not TEST_MODE else TEST_PROF_SEKO_INTRO_1)

        if(TEST_MODE):
            self.deltatimebeforeload = 2025
            self.up_gradiant.get_component().set_alpha(255)
            self.prof_ground.get_component().set_alpha(255)
            self.prof_seko.get_component().set_alpha(255)

    def update(self, deltatime):
        self.update_before_load(deltatime)
        self.update_gradiant(deltatime)
        self.update_prof_ground(deltatime)
        self.update_prof_seko(deltatime)
        self.update_show_dialogbox(deltatime)
        self.dialogbox.update(deltatime)

    def update_before_load(self, deltatime):
        if(self.deltatimebeforeload < self.waiting_before_load):
            self.deltatimebeforeload += deltatime

    def update_gradiant(self, deltatime):
        # QUAND ON A ASSEZ ATTENDU
        if(self.deltatimebeforeload >= self.waiting_before_load and self.up_gradiant.get_component().get_alpha() < 255):
            self.deltatimegradiant += deltatime
            # TEMPS DE REFRESH + AUGMENTER L'OPACITAY
            if(self.deltatimegradiant > self.waiting_update_time):
                self.up_gradiant.get_component().set_alpha(self.up_gradiant.get_component().get_alpha()+1)
                self.deltatimegradiant = 0

    def update_prof_ground(self, deltatime):
        if(self.up_gradiant.get_component().get_alpha() == 255 and self.prof_ground.get_component().get_alpha() < 255):
            self.deltatimeprofground += deltatime
            if(self.deltatimeprofground > self.waiting_update_time):
                self.prof_ground.get_component().set_alpha(self.prof_ground.get_component().get_alpha()+1)
                self.deltatimeprofground = 0

    def update_prof_seko(self, deltatime):
        if(self.prof_ground.get_component().get_alpha() > 100 and self.prof_seko.get_component().get_alpha() < 255):
            self.deltatimeprofseko += deltatime
            if(self.deltatimeprofseko > self.waiting_update_time):
                self.prof_seko.get_component().set_alpha(self.prof_seko.get_component().get_alpha()+1)
                self.deltatimeprofseko = 0

    def update_show_dialogbox(self, deltatime):
        if(self.prof_seko.get_component().get_alpha() == 255):
            self.deltatimeshowdialogbox += deltatime
            if(self.deltatimeshowdialogbox > 2000):
                self.dialogbox.show()

    def check_events(self, event):
        self.dialogbox.check_events(event)

    def get_components(self):
        return self.components + [self.player_sprite, self.dialogbox]