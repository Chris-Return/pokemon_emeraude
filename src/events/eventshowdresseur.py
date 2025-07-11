from src.events.gameevent import *

class EventShowDresseur(GameEvent):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.deltatime_accumulator_show_dresseur = 0
        parent.player_sprite.set_position((300,100))

    def update(self, deltatime):
        self.deltatime_accumulator_show_dresseur += deltatime
        if(self.deltatime_accumulator_show_dresseur > 5):
            self.parent.prof_seko.get_component().set_alpha(self.parent.prof_seko.get_component().get_alpha()-3)
            self.deltatime_accumulator_show_dresseur = 0

            if(self.parent.prof_seko.get_component().get_alpha() <= 0):
                self.parent.prof_seko.set_visible(False)
                self.parent.player_sprite.get_component().set_alpha(self.parent.player_sprite.get_component().get_alpha()+3)

                if(self.parent.player_sprite.get_component().get_alpha() >= 255):
                    self.active = False