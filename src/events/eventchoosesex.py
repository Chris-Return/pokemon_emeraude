from src.events.gameevent import GameEvent

class EventChooseSex(GameEvent):
    def __init__(self, eventNenupiot, parent):
        super().__init__()
        self.eventNenupiot = eventNenupiot
        self.parent = parent
        self.deltatime_accumulator_fade = 0
        self.deltatime_accumulator_ground = 0

    def update(self, deltatime):
        if(self.active):
            self.deltatime_accumulator_fade += deltatime
            # EFFACER LES ELEMENTS
            if(self.deltatime_accumulator_fade > 5 and self.eventNenupiot.nenupiot.get_final_frame().get_component().get_alpha() != 0):
                self.eventNenupiot.nenupiot.get_final_frame().get_component().set_alpha(self.eventNenupiot.nenupiot.get_final_frame().get_component().get_alpha()-1)
                self.parent.prof_seko.get_component().set_alpha(self.eventNenupiot.nenupiot.get_final_frame().get_component().get_alpha())
                self.deltatime_accumulator_fade = 0

                if(self.parent.prof_seko.get_component().get_alpha() == 0):
                    self.parent.prof_seko.set_visible(False)

            # BOUGER + FADE DU SOL
            if(self.eventNenupiot.nenupiot.get_final_frame().get_component().get_alpha() < 200):
                self.deltatime_accumulator_ground += deltatime
                if(self.deltatime_accumulator_ground > 5 and self.parent.prof_ground.get_component().get_alpha() >= 0):
                    self.parent.prof_ground.get_component().set_alpha(self.parent.prof_ground.get_component().get_alpha()-3)
                    self.parent.prof_ground.set_position((self.parent.prof_ground.get_position()[0]+1, self.parent.prof_ground.get_position()[1]))
                    self.deltatime_accumulator_ground = 0
                
            if(self.parent.prof_ground.get_component().get_alpha() <= 0 and self.parent.prof_seko.get_component().get_alpha() <= 0):
                self.active = False