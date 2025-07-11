from src.events.gameevent import GameEvent
from src.components.component import *
from src.data.playerdata import *

# ELEMENT PERMETTANT D'AFFICHER ET D'ANIMER UN CARACTERE
class WritableComponent():

    def __init__(self, writer, position):
        self.position = position
        self.character = ""
        self.writer = writer
        self.component = Component(None)
        self.component_shadow = Component(None)
        self.underline = Component(self.writer.render("-", True, (96,96,96)))
        self.underline_shadow = Component(self.writer.render("-", True, (208,208,208)))
        self.component.set_position((self.position[0], self.position[1]))
        self.component_shadow.set_position((self.position[0]+2, self.position[1]+2))
        self.underline.set_position((self.position[0], self.position[1]+20))
        self.underline_shadow.set_position((self.position[0]+2, self.position[1]+20+2))
        self.down = False
        self.deltatime_accumulator_animation = 0

    def update(self, deltatime):
        self.underline.set_position((self.position[0], self.position[1] + (20 if self.down else 30)))
        self.underline_shadow.set_position((self.position[0]+2, self.position[1] + (20 if self.down else 30)+2))
        self.deltatime_accumulator_animation += deltatime
        if(self.deltatime_accumulator_animation > 300):
            self.down = not self.down
            self.deltatime_accumulator_animation = 0

    def set_character(self, character):
        self.down = True
        self.underline.set_position((self.position[0], self.position[1] + (20 if self.down else 30)))
        self.underline_shadow.set_position((self.position[0]+2, self.position[1] + (20 if self.down else 30)+2))
        self.character = character
        self.component = Component(self.writer.render(self.character, True, (96,96,96)))
        self.component.set_position((self.position[0], self.position[1]))
        self.component_shadow = Component(self.writer.render(self.character, True, (208,208,208)))
        self.component_shadow.set_position((self.position[0]+2, self.position[1]+2))
        self.deltatime_accumulator_animation = 0

    def get_components(self):
        return [self.component_shadow, self.component, self.underline_shadow, self.underline]
    
    def get_letter_component(self):
        return self.component


class EventWritePlayerName(GameEvent):
    def __init__(self):
        super().__init__()
        self.number_of_characters_max = 10
        self.majuscules = [ ("A", "B", "C", "D", "", "E", "F", "G", "H", "", ".", "SWITCH"),
                            ("I", "J", "K", "L", "", "M", "N", "O", "P", "", ",", "SWITCH"),
                            ("Q", "R", "S", "T", "", "U", "V", "W", "X", "", " ", "RETURN"),
                            ("Y", "Z", "" , "" , "", "-", "" , "" , "" , "", "" , "OK")]
        
        self.minuscule = [  ("a", "b", "c", "d", "", "e", "f", "g", "h", "", ".", "SWITCH"),
                            ("i", "j", "k", "l", "", "m", "n", "o", "p", "", ",", "SWITCH"),
                            ("q", "r", "s", "t", "", "u", "v", "w", "x", "", " ", "RETURN"),
                            ("y", "z", "" , "" , "", "-", "" , "" , "" , "", "" , "OK")]

        self.reftable = self.majuscules
        self.animation_switch_characters = False
        
        self.name_elements = []
        
        self.writer = pygame.font.Font(FONT_MAIN_DIALOGBOX, FONT_MAIN_DIALOGBOX_SIZE)
        self.writedName = ""
        self.selector_position = (0,0)

        # INITIALISATION DES ELEMENTS VISUELS DE SAISIE
        self.elements_visuels = [WritableComponent(self.writer, (310 + (i*20),140)) for i in range(self.number_of_characters_max)]

        for comp in self.elements_visuels:
            for all_comp in comp.get_components():
                all_comp.set_visible(False)

        self.background_component = Component(pygame.image.load(IMG_BACKGROUND_NEW_GAME))
        self.actualkeyboard = Component(pygame.image.load(IMG_CLAVIER_MAJUSCULE))
        self.backgroundkeyboard = Component(pygame.image.load(IMG_CLAVIER_MINUSCULES))

        self.components = [
            Component(pygame.image.load(IMG_NEW_GAME_SELECT_PLAYER_NAME)),
            Component(pygame.image.load(IMG_CLAVIER_OVERLAY)),
            self.backgroundkeyboard,
            self.actualkeyboard,
            Component(pygame.image.load(IMG_CLAVIER_SIDE_BUTTONS)),
            Component(pygame.image.load(IMG_LETTER_SELECTION_RED)),
            Component(pygame.image.load(IMG_LETTER_SELECTION_WHITE)),
            Component(pygame.image.load(IMG_NAME_CURSOR)),
            Component(pygame.image.load(IMG_SELECTOR_WIDE))]

        self.backgroundkeyboard.set_position((50,225))
        self.actualkeyboard.set_position((50,225))
        self.components[4].set_position((550,225))
        self.components[5].set_position((94, 243))
        self.components[6].set_position((94, 243))
        self.components[7].set_position((260, 150))
        self.components[8].set_position((562, 231))

        # Tous les composants qui possèdent un canal Alpha doivent apparaître
        for comp in self.components:
            comp.set_visible(False)
            try:
                comp.get_component().set_alpha(255)
            except:
                pass

        self.background_component.set_visible(True)
        self.background_component.get_component().set_alpha(0)
        self.deltatime_accumulator_alpha = 0
        self.deltatime_accumulator_selector = 0
        self.deltatime_accumulator_cursor = 0
        self.deltatime_accumulator_wide_selector = 0
        self.deltatime_accumulator_animation_switch = 0
        self.go_full_red = False
        self.show_background = True
        self.go_full_white = True
        self.end_selection = False

    def update(self, deltatime):
        try:
            self.elements_visuels[len(self.writedName)].update(deltatime)
        except:
            pass

        self.update_selector(deltatime)
        self.update_name_cursor(deltatime)
        self.update_wide_selector(deltatime)
        self.update_switch(deltatime)

        self.deltatime_accumulator_alpha += deltatime
        if(self.deltatime_accumulator_alpha > 5 and self.background_component.get_component().get_alpha() < 255 and self.show_background):
            self.background_component.get_component().set_alpha(self.background_component.get_component().get_alpha()+2)
            self.deltatime_accumulator_alpha = 0

            if(self.background_component.get_component().get_alpha() >= 255):
                for comp in self.components:
                    comp.set_visible(not self.end_selection)

                for comp in self.elements_visuels:
                    for all_comp in comp.get_components():
                        all_comp.set_visible(not self.end_selection)

                self.show_background = False

        if(self.deltatime_accumulator_alpha > 5 and self.background_component.get_component().get_alpha() > 0 and not self.show_background):
            self.background_component.get_component().set_alpha(self.background_component.get_component().get_alpha()-2)
            self.deltatime_accumulator_alpha = 0
            
            if(self.background_component.get_component().get_alpha() <= 0):
                self.show_background = None
                if(self.end_selection):
                    self.active = False

    def update_switch(self, deltatime):
        self.deltatime_accumulator_animation_switch += deltatime
        if(self.animation_switch_characters):
            if(self.deltatime_accumulator_animation_switch > 5 and self.actualkeyboard.get_position()[1] > 100):
                self.actualkeyboard.set_position((self.actualkeyboard.get_position()[0], self.actualkeyboard.get_position()[1]-3))
                self.backgroundkeyboard.set_position((self.backgroundkeyboard.get_position()[0], self.backgroundkeyboard.get_position()[1]+3))
                self.deltatime_accumulator_animation_switch = 0

                # INVERSER LES DEUX COMPOSANTS QUAND OK
                if(self.actualkeyboard.get_position()[1] <= 100):
                    self.animation_switch_characters = False
                    self.reftable = self.majuscules if self.reftable == self.minuscule else self.minuscule
                    component_copy = self.actualkeyboard
                    self.actualkeyboard = self.backgroundkeyboard
                    self.backgroundkeyboard = component_copy
        else:
            if(self.deltatime_accumulator_animation_switch > 10 and self.backgroundkeyboard.get_position()[1] < 225):
                self.backgroundkeyboard.set_position((self.backgroundkeyboard.get_position()[0], self.backgroundkeyboard.get_position()[1]+3))
                self.actualkeyboard.set_position((self.actualkeyboard.get_position()[0], self.actualkeyboard.get_position()[1]-3))
                self.deltatime_accumulator_animation_switch = 0

                if(self.backgroundkeyboard.get_position()[1] >= 225):
                    for comp in self.elements_visuels:
                        for all_comp in comp.get_components():
                            all_comp.set_visible(True)
                    
                    self.components[7].set_visible(True)
        
            
    def update_selector(self, deltatime):
        if(not self.show_background and not self.end_selection):
            self.deltatime_accumulator_selector += deltatime
            self.components[5].set_visible(True if self.selector_position[1] < 11 else False)
            self.components[6].set_visible(True if self.selector_position[1] < 11 else False)

            if(self.deltatime_accumulator_selector > 5):
                if(self.components[6].get_component().get_alpha() >= 255):
                    self.go_full_red = True

                if(self.components[6].get_component().get_alpha() <= 0):
                    self.go_full_red = False

                self.components[6].get_component().set_alpha(self.components[6].get_component().get_alpha() + (-5 if self.go_full_red else +5))
                self.deltatime_accumulator_selector = 0

    def update_wide_selector(self, deltatime):
        if(not self.show_background and not self.end_selection):
            self.deltatime_accumulator_wide_selector += deltatime
            self.components[8].set_visible(True if self.selector_position[1] == 11 else False)
            if(self.deltatime_accumulator_wide_selector > 5):
                if(self.components[8].get_component().get_alpha() >= 255):
                    self.go_full_white = False
                
                if(self.components[8].get_component().get_alpha() <= 0):
                    self.go_full_white = True

                self.components[8].get_component().set_alpha(self.components[8].get_component().get_alpha() + (3 if self.go_full_white else -3))


    def update_name_cursor(self, deltatime):
        self.deltatime_accumulator_cursor += deltatime
        if(self.deltatime_accumulator_cursor > 20):
            self.components[7].set_position((self.components[7].get_position()[0]+1, 150))
            if(self.components[7].get_position()[0] > 280):
                self.components[7].set_position((260, 150))
            self.deltatime_accumulator_cursor = 0

    def modify_name(self):
        if(len(self.reftable[self.selector_position[0]][self.selector_position[1]]) == 1 and len(self.writedName) < self.number_of_characters_max):
            self.elements_visuels[len(self.writedName)].set_character(self.reftable[self.selector_position[0]][self.selector_position[1]])
            self.writedName += self.reftable[self.selector_position[0]][self.selector_position[1]]
        else:
            if(self.reftable[self.selector_position[0]][self.selector_position[1]].__contains__("SWITCH")):
                self.animation_switch_characters = True
                for comp in self.elements_visuels:
                    for all_comp in comp.get_components():
                        all_comp.set_visible(False)
                
                self.components[7].set_visible(False)

            elif(self.reftable[self.selector_position[0]][self.selector_position[1]].__contains__("RETURN")):
                if(len(self.writedName) > 0):
                    self.elements_visuels[len(self.writedName)-1].set_character("")
                    self.writedName = self.writedName[:-1]
                    try:
                        self.elements_visuels[len(self.writedName)+1].set_character("")
                    except:
                        pass
            
            elif(self.reftable[self.selector_position[0]][self.selector_position[1]].__contains__("OK") and len(self.writedName) > 0):
                self.show_background = True
                self.end_selection = True
                PlayerData.name = self.writedName

    def try_move_selector(self, x, y):
        new_selector_position = self.selector_position
        new_selector_position = (new_selector_position[0]+x, new_selector_position[1]+y)

        security_counter = 0
        while(security_counter < 10):
            security_counter += 1
            try:
                # Python étant ce qu'il est, je vérifie moi-même que x et y ne sont pas négatifs
                # Explication : Python accepte les valeurs négatives dans une tentative d'accès à une liste
                if(new_selector_position[0] < 0 or new_selector_position[1] < 0):
                    raise IndexError

                character_selected = self.reftable[new_selector_position[0]][new_selector_position[1]]
                if(character_selected == ""):
                    # Si on veut aller à droite, on skip le caractère vide
                    if(y>0):
                        new_selector_position = (new_selector_position[0], new_selector_position[1]+1)
                    # Si on veut aller à gauche
                    if(y<0):
                        new_selector_position = (new_selector_position[0], new_selector_position[1]-1)
                    # Si on veut aller en haut
                    if(x>0):
                        new_selector_position = (new_selector_position[0]+1, new_selector_position[1])
                    # Si on veut aller en bas
                    if(x<0):
                        new_selector_position = (new_selector_position[0]-1, new_selector_position[1])
                else:
                    break
            except IndexError:
                if(new_selector_position[1] >= len(self.reftable[self.selector_position[0]])):
                    new_selector_position = (new_selector_position[0], 0)
                if(new_selector_position[1] < 0):
                    new_selector_position = (new_selector_position[0], len(self.reftable[self.selector_position[0]])-1)
                if(new_selector_position[0] >= len(self.reftable)):
                    new_selector_position = (0, new_selector_position[1])
                if(new_selector_position[0] < 0):
                    new_selector_position = (len(self.reftable)-1, new_selector_position[1])

        if(security_counter == 10):
            print("Boucle infinie stoppée")

        self.selector_position = new_selector_position

        if(new_selector_position[1] == 11):
            self.try_move_wide_selector(new_selector_position, x, y)

        self.components[5].set_position((94 + (37*self.selector_position[1]), 243 + (47*self.selector_position[0])))
        self.components[6].set_position((94 + (37*self.selector_position[1]), 243 + (47*self.selector_position[0])))

    def try_move_wide_selector(self, position, x, y):
        # CODER LE SKIP SWITCH -> SWITCH
        if(position[0] == 1 and x > 0):
            position = (position[0]+1, position[1])
        elif(position[0] == 1 and x < 0):
            position = (position[0]-1, position[1])
        elif(position[0] == 1 and y != 0):
            position = (0, position[1])

        self.selector_position = position

        if(position[0] == 0 or position[0] == 1):
            self.components[8].set_position((562, 231))
        elif(position[0] == 2):
            self.components[8].set_position((562, 318))
        elif(position[0] == 3):
            self.components[8].set_position((562, 384))

    def check_inputs(self, event):
        if(event.type == pygame.KEYDOWN and self.active and self.background_component.get_component().get_alpha() <= 0):
            if(event.key == pygame.K_DOWN):
                self.try_move_selector(1, 0)

            if(event.key == pygame.K_UP):
                self.try_move_selector(-1, 0)

            if(event.key == pygame.K_LEFT):
                self.try_move_selector(0, -1)

            if(event.key == pygame.K_RIGHT):
                self.try_move_selector(0, 1)

            if(event.key == pygame.K_w or event.key == pygame.K_RETURN):
                self.modify_name()

    def get_components(self):
            list_comp = []
            for ev in self.elements_visuels:
                for comp in ev.get_components():
                    list_comp.append(comp)

            list_main_comp = []
            for i in range(len(self.components)):
                if(i==2):
                    list_main_comp.append(self.backgroundkeyboard)
                elif(i==3):
                    list_main_comp.append(self.actualkeyboard)
                else:
                    list_main_comp.append(self.components[i])

            return list_main_comp + list_comp + [self.background_component]