from src.constants.constants import CHARACTER_STEREOTYPE
from src.maps.mapreader import MapReader

class CharacterStereotype():

    map_reader = MapReader(CHARACTER_STEREOTYPE)
    tab_animations_info = {}

    def __init__(self):
        pass

    @staticmethod
    def load():
        CharacterStereotype.get_all_animations_info()
    
    @staticmethod
    def get_all_animations_info():
        tab_animations_info = None
        tab_animations_info = CharacterStereotype.map_reader.get_lines_after(str("animation_config:"))
        if(tab_animations_info is not None):
            for animation_info in tab_animations_info:
                striped_infos = animation_info.strip()
                couple_number_anim = striped_infos.split(":")
                CharacterStereotype.tab_animations_info[int(couple_number_anim[0])] = couple_number_anim[1].split(",")

    def animations_info_for(number):
        return CharacterStereotype.tab_animations_info[int(number)]