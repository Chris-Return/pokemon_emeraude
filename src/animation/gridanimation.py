from src.maps.tileset import Tileset
from src.animation.animation import Animation

class GridAnimation(Animation):

    def __init__(self, character_animation_path):
        super().__init__(None)
        self.direction = 0
        self.all_frames = Tileset.load_all_directions_object(character_animation_path, 15, 22, 4, 4)
        self.loop = True
        self.visible_component = self.all_frames[self.direction][self.actual_frame]

    def update(self, deltatime):
        if(self.active):
            self.deltatime_accumulator += deltatime
            if(self.deltatime_accumulator > self.animation_speed):
                # Rendre invisible toutes les frames
                for frame in self.all_frames[self.direction]:
                    frame.set_visible(False)

                self.all_frames[self.direction][self.actual_frame].set_visible(True)
                self.visible_component = self.all_frames[self.direction][self.actual_frame]
                self.actual_frame += 1

                if(self.actual_frame == len(self.all_frames[self.direction])):
                    self.actual_frame = 0
        
                self.deltatime_accumulator = 0

    def stop(self):
        self.active = False
        self.actual_frame = 0
        for line in self.all_frames:
            for comp in line:
                comp.set_visible(False)

        self.visible_component = self.all_frames[self.direction][self.actual_frame]
        self.visible_component.set_visible(True)

    def play(self):
        if(not self.active):
            self.active = True
            self.deltatime_accumulator = self.animation_speed + 1

    def set_direction(self, direction):
        if(direction != self.direction):
            self.direction = direction
            self.deltatime_accumulator = self.animation_speed + 1

    def get_component(self):
        return self.visible_component