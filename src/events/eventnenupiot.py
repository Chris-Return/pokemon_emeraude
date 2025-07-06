from src.events.gameevent import GameEvent
from src.constants.constants import *
from src.components.component import *
from src.components.componentunscaled import *
from src.animation.animation import *
from src.animation.gifanimation import *

class EventNenupiot(GameEvent):
    
    def __init__(self):
        super().__init__()

        self.pokeball_animation = Animation([
            Component(pygame.image.load(IMG_POKEBALL_CLASSIC)),
            Component(pygame.image.load(IMG_POKEBALL_CLASSIC_OPEN)),
            Component(pygame.image.load(IMG_POKEBALL_CLASSIC_FULL_OPEN))
        ])

        self.flash_pokeball = Animation([ ComponentUnscaled(pygame.image.load(IMG_FLASH_POKEBALL+str(i)+".png")) for i in range (8) ])
        self.flash_pokeball.set_position((-10,-190))
        self.flash_pokeball.set_speed(50)
        self.flash_pokeball.set_dispose_on_end(True)

        self.pokeball_animation.set_position((335, 150))
        self.pokeball_animation.animation_begin_delay(800)
        self.pokeball_animation.show_first_comp()

        self.nenupiot = GifAnimation(GET_FRONT_POKEMON(270))
        self.nenupiot.set_speed(20)
        self.nenupiot.set_position((160,80))

        self.components = [self.pokeball_animation, 
                           self.flash_pokeball,
                           self.nenupiot]

    def update(self, deltatime):
        if(self.active):
            if(self.pokeball_animation.get_active()):
                self.pokeball_animation.update(deltatime)

            # Si l'animation de la pokeball est terminée
            if(not self.pokeball_animation.get_active()):
                self.flash_pokeball.active = True
                self.flash_pokeball.update(deltatime)

            if(self.flash_pokeball.get_ended()):
                self.pokeball_animation.dispose()
                self.nenupiot.active = True
                self.nenupiot.update(deltatime)

            if(self.nenupiot.get_ended()):
                self.active = False

    def get_components(self):
        return self.components
    
    def run(self):
        self.active = True
        self.pokeball_animation.active = True

    def get_active(self):
        return self.active