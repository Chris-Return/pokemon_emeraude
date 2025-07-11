from src.events.gameevent import *
from src.components.component import *
from src.data.playerdata import *

class EventShowProfAndNenupiot(GameEvent):
    def __init__(self, eventNenupiot, parent):
        super().__init__()
        self.eventNenupiot = eventNenupiot
        self.parent = parent
        self.deltatime_accumulator_move_ground = 0
        self.parent.player_sprite.get_component().set_alpha(255)
        self.fade_to_black = True

    def update(self, deltatime):
        if(self.active):
            self.deltatime_accumulator_move_ground += deltatime
            if(self.deltatime_accumulator_move_ground > 5 and self.parent.prof_ground.get_component().get_alpha() > 0 and self.fade_to_black):
                self.parent.player_sprite.get_component().set_alpha(self.parent.player_sprite.get_component().get_alpha() -3)
                self.parent.prof_ground.get_component().set_alpha(self.parent.prof_ground.get_component().get_alpha()-3)
                self.deltatime_accumulator_move_ground = 0

                if(self.parent.prof_ground.get_component().get_alpha() <= 0):
                    self.parent.prof_seko.get_component().set_alpha(0)
                    self.parent.prof_seko.set_visible(True)
                    self.parent.prof_ground.set_position((0,0))
                    self.fade_to_black = False

            if(self.deltatime_accumulator_move_ground > 5 and self.parent.prof_ground.get_component().get_alpha() < 255):
                self.parent.prof_seko.get_component().set_alpha(self.parent.prof_seko.get_component().get_alpha() + 3)
                self.deltatime_accumulator_move_ground = 0

                if(self.parent.prof_seko.get_component().get_alpha() >= 255):
                    self.active = False