
from src.components.component import *

class Animation(Component):

    def __init__(self, children):
        super().__init__(None)
        self.active = False
        self.ended = False
        self.deltatime_accumulator = 0
        self.animation_speed = 100
        self.children = children
        self.actual_frame = 0
        self.deltatime_animation_delay = 0
        self.actual_deltatime_animation_delay = 0
        self.dispose_on_end = False
        self.loop = False
        self.visible = True

        try:
            for comp in self.children:
                comp.set_visible(False)
        except:
            pass

    def update(self, deltatime):
        if(self.active):
            self.actual_deltatime_animation_delay += deltatime

        if(self.active and self.actual_deltatime_animation_delay > self.deltatime_animation_delay):
            self.deltatime_accumulator += deltatime
            if(self.deltatime_accumulator > self.animation_speed):
                for comp in self.children:
                    comp.set_visible(False)
                
                if(self.actual_frame < len(self.children)):
                    self.children[self.actual_frame].set_visible(True)
                    self.actual_frame += 1
                else:
                    # Si dernière frame
                    if(self.loop):
                        self.actual_frame = 0
                    else:
                        self.children[self.actual_frame-1].set_visible(not self.dispose_on_end)
                        self.active = False
                        self.ended = True

                self.deltatime_accumulator = 0

    def dispose(self):
        try:
            for comp in self.children:
                comp.set_visible(False)
        except:
            pass

    def play_loop(self):
        self.active = True
        self.loop = True
    
    def set_position(self, position):
        try:
            for comp in self.children:
                comp.set_position(position)
        except:
            pass

    def play(self):
        self.active = True

    def stop(self):
        self.active = False
        for frame in self.children:
            frame.set_visible(False)

    def set_speed(self, speed):
        self.animation_speed = speed

    def animation_begin_delay(self, deltatime):
        self.deltatime_animation_delay = deltatime

    def show_first_comp(self):
        self.children[0].set_visible(True)

    def set_dispose_on_end(self, bool):
        self.dispose_on_end = bool

    def get_active(self):
        return self.active
    
    def get_ended(self):
        return self.ended