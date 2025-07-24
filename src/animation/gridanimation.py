from src.maps.tileset import Tileset
from src.animation.animation import Animation
from src.animation.characterstereotype import CharacterStereotype

class GridAnimation(Animation):

    def __init__(self, character_animation_path):
        super().__init__(None)
        self.stereotype = CharacterStereotype.animations_info_for(character_animation_path[1])
        self.animation_speed = int(self.stereotype[0])
        self.excent = (int(self.stereotype[1]),int(self.stereotype[2]))
        self.sort_number = 1
        self.direction = 0
        self.all_frames = Tileset.load_all_directions_object(character_animation_path[0], int(self.stereotype[3]), int(self.stereotype[4]), 4, 4)
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
        self.refresh_frame()

    def play(self):
        if(not self.active):
            self.active = True
            self.deltatime_accumulator = self.animation_speed + 1

    def set_direction(self, direction):
        if(direction != self.direction):
            self.direction = direction
            self.deltatime_accumulator = self.animation_speed + 1
            self.refresh_frame()
            
    
    def refresh_frame(self):
        for line in self.all_frames:
            for comp in line:
                comp.set_visible(False)

        self.visible_component = self.all_frames[self.direction][self.actual_frame]
        self.visible_component.set_visible(True)
    
    def get_direction(self):
        return self.direction

    def get_position(self):
        return (self.excent[0] + self.position[0], self.excent[1] + self.position[1])

    def get_component(self):
        return self.visible_component
    
    def set_animation_speed(self, speed):
        self.animation_speed = speed