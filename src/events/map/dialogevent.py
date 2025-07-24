import pygame
from src.events.gameevent import GameEvent
from src.components.component import Component
from src.constants.constants import IMG_CURSOR_NEXT, IMG_DIALOGBOX, FONT_MAIN_DIALOGBOX, FONT_MAIN_DIALOGBOX_SIZE, INTERFACE_SORT_LEVEL
from src.components.dialogvariables import DialogVariables

class DialogEvent(GameEvent):

    # --- Déclaration des composants ---
    # BACKGROUND DE LA BOX
    img_dialogbox = Component(pygame.image.load(IMG_DIALOGBOX))
    img_dialogbox.set_position((0,335))
    img_dialogbox.set_sort_number(INTERFACE_SORT_LEVEL)
    img_dialogbox.set_modal(True)

    comp_lines = [Component(None), Component(None), Component(None), Component(None)]
    comp_lines[1].set_position((45,360))
    comp_lines[1].set_modal(True)
    comp_lines[1].set_sort_number(INTERFACE_SORT_LEVEL+2)
    comp_lines[0].set_position((47,362))
    comp_lines[0].set_modal(True)
    comp_lines[0].set_sort_number(INTERFACE_SORT_LEVEL+1)
    comp_lines[3].set_position((45,410))
    comp_lines[3].set_modal(True)
    comp_lines[3].set_sort_number(INTERFACE_SORT_LEVEL+2)
    comp_lines[2].set_position((47,412))
    comp_lines[2].set_modal(True)
    comp_lines[2].set_sort_number(INTERFACE_SORT_LEVEL+1)

    cursor_next = Component(pygame.image.load(IMG_CURSOR_NEXT))
    cursor_next.set_modal(True)
    cursor_next.set_sort_number(INTERFACE_SORT_LEVEL+1)
    cursor_next.set_visible(False)

    def __init__(self, parent, lines):
        super().__init__(parent)
        self.active = True
        self.paragraphs = lines
        self.actualLines = []
        self.writedTexts = []
        self.writing_end = False

        self.deltatime_accumulator = 0
        self.deltatime_cursor_next = 0

        # GENERATEUR DE ZONES DE TEXTE
        self.writer = pygame.font.Font(FONT_MAIN_DIALOGBOX, FONT_MAIN_DIALOGBOX_SIZE)
        self.components.append(DialogEvent.img_dialogbox)
        self.components.append(DialogEvent.cursor_next)
        self.init_normal_lines()

    def update(self, deltatime):
        super().update(deltatime)
        self.deltatime_accumulator += deltatime
        if(self.deltatime_accumulator > 60):
            self.update_text()
            self.update_cursor_next(deltatime)
            self.deltatime_accumulator = 0

    def update_text(self):
        # Si tous les paragraphes n'ont pas été écrits
        if(not self.check_paragraphs()):
            # Désactiver les touches de clavier
            self.writing_end = False
            # Boucler sur toutes les lignes à afficher
            try:
                for i in range(2):
                    if(self.actualLines[i] != self.writedTexts[i]):
                        self.writedTexts[i] += self.actualLines[i][len(self.writedTexts[i])]
                        DialogEvent.comp_lines[i*2].set_component(self.writer.render(self.writedTexts[i], True, (208,208,200)))
                        DialogEvent.comp_lines[i*2+1].set_component(self.getNewLine(self.writedTexts[i]))
                        break
            except:
                pass
        else:
            self.writing_end = True
    
    def getNewLine(self, text):
        return self.writer.render(text, True, (96,96,96))

    def update_cursor_next(self, deltatime):
        try:
            if(self.writing_end):
                self.deltatime_cursor_next += deltatime
                DialogEvent.cursor_next.set_visible(True)
                DialogEvent.cursor_next.set_position((53 + DialogEvent.comp_lines[0 if len(self.writedTexts) <= 1 else 2].get_component().get_size()[0], 360+(self.deltatime_cursor_next/30) + (50 * 1 if(len(self.writedTexts)) > 1 else 2)))

                if(self.deltatime_cursor_next >= 300):
                    self.deltatime_cursor_next = 0
            else:
                DialogEvent.cursor_next.set_visible(False)
        except:
            pass
    
    # Vérifier si les paragraphes sont complets
    def check_paragraphs(self):
        try:
            for i in range(2 if len(self.writedTexts) > 1 else 1):
                if(self.writedTexts[i] != self.actualLines[i]):
                    return False
            return True
        except:
            return True
        
    def next_line(self):
        # EFFACER LES TEXTES RESIDUELS DANS LES COMPOSANTS
        for component in self.comp_lines:
            component.set_component(self.getNewLine(""))

        try:
            if(len(self.actualLines) > 2):
                self.actualLines.pop(0)
                self.writedTexts.pop(0)
                DialogEvent.comp_lines[0].set_component(self.writer.render(self.writedTexts[0], True, (208,208,200)))
                DialogEvent.comp_lines[1].set_component(self.getNewLine(self.writedTexts[0]))
            else:
                self.paragraphs.pop(0)
                self.init_normal_lines()
        except:
            self.actualLines = []
            self.writedTexts = []
            self.active = False
            self.set_dead(True)
            self.writing_end = False
    
    def check_line_content(self):
        self.paragraphs[0] = DialogVariables.get_variable(self.paragraphs[0])

    def init_normal_lines(self):
        self.actualLines = self.paragraphs[0].split("|")
        # Enlever tous les retours à la ligne
        self.actualLines = [line.strip() for line in self.actualLines]
        self.writedTexts = ["" for i in range(len(self.actualLines))]

    def check_inputs(self, event):
        if(event.key == pygame.K_w):
            if(not self.check_paragraphs()):
                try:
                # SI ON APPUIE ALORS QUE TOUS LES PARAGRAPHES NE SONT PAS ENCORE AFFICHES
                    for i in range(2):
                        self.writedTexts[i] = self.actualLines[i]
                        DialogEvent.comp_lines[i*2].set_component(self.writer.render(self.writedTexts[i], True, (208,208,200)))
                        DialogEvent.comp_lines[i*2+1].set_component(self.getNewLine(self.writedTexts[i]))
                except Exception:
                    pass
            # SI ON APPUIE ALORS QUE TOUT EST AFFICHÉ, ON PASSE AU DIALOGUE SUIVANT
            else:
                self.next_line()
                self.writing_end = False

    def get_components(self):
        return self.components + DialogEvent.comp_lines