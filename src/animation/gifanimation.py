import pygame
from PIL import Image
from src.components.component import *

class GifAnimation(Component):
    def __init__(self, filepath):
        img = Image.open(filepath)
        frames = []
        try:
            while True:
                frame = img.copy().convert("RGBA")
                frames.append(pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode))
                img.seek(img.tell()+1)
        except Exception:
            pass

        print("Nenupiot frames : "+str(len(frames)))

        self.set_component(None)
        self.active = False
        self.ended = False
        self.deltatime_accumulator = 0
        self.animation_speed = 100
        self.children = [Component(frames[i]) for i in range(len(frames))]
        self.actual_frame = 0
        self.deltatime_animation_delay = 0
        self.actual_deltatime_animation_delay = 0
        self.dispose_on_end = False
        self.loop = False
        self.visible = True

        for comp in self.children:
            comp.set_visible(False)

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
        for comp in self.children:
            comp.set_visible(False)

    def play_loop(self):
        self.loop = True
    
    def set_position(self, position):
        for comp in self.children:
            comp.set_position(position)

    def play(self):
        self.active = True

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