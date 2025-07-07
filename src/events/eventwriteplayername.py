from src.events.gameevent import GameEvent
from src.components.component import *

class EventWritePlayerName(GameEvent):
    def __init__(self):
        super().__init__()
        self.background_component_number = 7
        self.components = [
            Component(pygame.image.load(IMG_NEW_GAME_SELECT_PLAYER_NAME)),
            Component(pygame.image.load(IMG_CLAVIER_OVERLAY)),
            Component(pygame.image.load(IMG_CLAVIER_MINUSCULES)),
            Component(pygame.image.load(IMG_CLAVIER_MAJUSCULE)),
            Component(pygame.image.load(IMG_CLAVIER_SIDE_BUTTONS)),
            Component(pygame.image.load(IMG_LETTER_SELECTION_RED)),
            Component(pygame.image.load(IMG_LETTER_SELECTION_WHITE)),
            Component(pygame.image.load(IMG_BACKGROUND_NEW_GAME)),
        ]

        self.components[2].set_position((50,225))
        self.components[3].set_position((50,225))
        self.components[4].set_position((550,225))
        self.components[5].set_position((94, 243))
        self.components[6].set_position((94, 243))

        for comp in self.components:
            comp.set_visible(False)
            comp.get_component().set_alpha(255)

        self.components[self.background_component_number].set_visible(True)
        self.components[self.background_component_number].get_component().set_alpha(0)
        self.deltatime_accumulator_alpha = 0
        self.deltatime_accumulator_selector = 0
        self.go_full_red = False
        self.show_background = True

    def update(self, deltatime):
        self.update_selector(deltatime)
        self.deltatime_accumulator_alpha += deltatime
        if(self.deltatime_accumulator_alpha > 5 and self.components[self.background_component_number].get_component().get_alpha() < 255 and self.show_background):
            self.components[self.background_component_number].get_component().set_alpha(self.components[self.background_component_number].get_component().get_alpha()+2)
            self.deltatime_accumulator_alpha = 0

            if(self.components[self.background_component_number].get_component().get_alpha() >= 255):
                for comp in self.components:
                    comp.set_visible(True)

                self.show_background = False

        if(self.deltatime_accumulator_alpha > 5 and self.components[self.background_component_number].get_component().get_alpha() > 0 and not self.show_background):
            self.components[self.background_component_number].get_component().set_alpha(self.components[self.background_component_number].get_component().get_alpha()-2)
            self.deltatime_accumulator_alpha = 0
            
            if(self.components[self.background_component_number].get_component().get_alpha() <= 0):
                self.show_background = None

    def update_selector(self, deltatime):
        self.deltatime_accumulator_selector += deltatime
        if(self.deltatime_accumulator_selector > 5):
            if(self.components[6].get_component().get_alpha() >= 255):
                self.go_full_red = True

            if(self.components[6].get_component().get_alpha() <= 0):
                self.go_full_red = False

            self.components[6].get_component().set_alpha(self.components[6].get_component().get_alpha() + (-5 if self.go_full_red else +5))


            self.deltatime_accumulator_selector = 0