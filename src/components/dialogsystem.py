import pygame
from src.components.component import *
from src.constants.constants import *
from src.events.eventmanager import *
from src.components.dialogvariables import *

class DialogSystem(Component):

    def __init__(self, pycomponent, parent):
        super().__init__(pycomponent)
        self.parent = parent
        self.visible = False
        # DEFINIR SI ON PEUT INTERAGIR AVEC LA DIALOGBOX
        self.active = False
        self.event_reading = False
        # BACKGROUND DE LA BOX
        self.img_dialogbox = Component(pygame.image.load(IMG_DIALOGBOX))
        self.img_dialogbox.set_position((0,335))

        # GENERATEUR DE ZONES DE TEXTE
        self.writer = pygame.font.Font(FONT_MAIN_DIALOGBOX, FONT_MAIN_DIALOGBOX_SIZE)

        self.children.append(self.img_dialogbox)
        # ENSEMBLE DES PARAGRAPHES A INTERPRETER
        self.paragraphs = []
        self.writedTexts = []
        # DEFINIR SI ON PEUT LANCER L'EXECUTION DE LA DIALOXBOX ( AFFICHAGE + DEFILEMENT DU TEXTE )
        self.run = False
        self.deltatime_accumulator = 0
        self.deltatime_cursor_next = 0

        self.comp_lines = [Component(None), Component(None), Component(None), Component(None)]
        self.comp_lines[1].set_position((45,360))
        self.comp_lines[0].set_position((47,362))
        self.comp_lines[3].set_position((45,410))
        self.comp_lines[2].set_position((47,412))

        for comp_line in self.comp_lines:
            self.children.append(comp_line)

        self.cursor_next = Component(pygame.image.load(IMG_CURSOR_NEXT))
        self.cursor_next.set_visible(False)
        self.children.append(self.cursor_next)

        self.actualLines = []

    def update(self, deltatime):
        self.update_event(deltatime)
        if(self.visible):
            self.deltatime_accumulator += deltatime
            if(self.deltatime_accumulator > 60):
                self.update_text()
                self.update_cursor_next(self.deltatime_accumulator)
                self.deltatime_accumulator = 0

    def update_event(self, deltatime):
        if(self.event_reading):
            self.game_event.update(deltatime)
            # QUAND L'EVENT VIENT TOUT JUSTE DE SE DESACTIVER
            if(not self.game_event.get_active()):
                self.event_reading = False
                self.next_line()

    def update_text(self):
        # Si tous les paragraphes n'ont pas été écrits
        if(not self.check_paragraphs()):
            # Désactiver les touches de clavier
            self.active = False
            # Boucler sur toutes les lignes à afficher
            try:
                for i in range(2):
                    if(self.actualLines[i] != self.writedTexts[i]):
                        self.writedTexts[i] += self.actualLines[i][len(self.writedTexts[i])]
                        self.comp_lines[i*2].set_component(self.writer.render(self.writedTexts[i], True, (208,208,200)))
                        self.comp_lines[i*2+1].set_component(self.getNewLine(self.writedTexts[i]))
                        break
            except:
                pass
        else:
            # Activer les touches du clavier
            if(not self.event_reading):
                self.active = True
    
    def update_cursor_next(self, deltatime):
        try:
            if(self.active):
                self.deltatime_cursor_next += deltatime
                self.cursor_next.set_visible(True)
                self.cursor_next.set_position((53 + self.comp_lines[0 if len(self.writedTexts) <= 1 else 2].get_component().get_size()[0], 360+(self.deltatime_cursor_next/30) + (50 * 1 if(len(self.writedTexts)) > 1 else 2)))

                if(self.deltatime_cursor_next >= 300):
                    self.deltatime_cursor_next = 0
            else:
                self.cursor_next.set_visible(False)
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

    def getNewLine(self, text):
        return self.writer.render(text, True, (96,96,96))

    def show(self):
        self.set_visible(True)

    def uploadParagraphs(self, str):
        # Ouvrir le contenu d'un fichier
        with open(str, "r", encoding="utf-8") as fichier:
            self.paragraphs = fichier.readlines()

        self.actualLines = self.paragraphs[0].split("|")
        # Enlever tous les retours à la ligne
        self.actualLines = [line.strip() for line in self.actualLines]
        # Initialiser à vide les éléments du tableau pour éviter les Exceptions
        self.writedTexts = ["" for i in range(len(self.actualLines))]

    def next_line(self):
        # EFFACER LES TEXTES RESIDUELS DANS LES COMPOSANTS
        for component in self.comp_lines:
            component.set_component(self.getNewLine(""))

        try:
            if(len(self.actualLines) > 2):
                self.actualLines.pop(0)
                self.writedTexts.pop(0)
                self.comp_lines[0].set_component(self.writer.render(self.writedTexts[0], True, (208,208,200)))
                self.comp_lines[1].set_component(self.getNewLine(self.writedTexts[0]))
            else:
                self.paragraphs.pop(0)
                if(self.check_line_content()):
                    self.init_normal_lines()
        except:
            self.actualLines = []
            self.writedTexts = []
            self.set_visible(False)
            self.active = False

    def check_line_content(self):
        self.paragraphs[0] = DialogVariables.get_variable(self.paragraphs[0])
        if(self.paragraphs[0].__contains__("[EVENT]")):
            self.game_event = EventManager.getGameEvent(self.paragraphs[0], self.parent)
            if(self.game_event != None):
                # SI UN EVENT A ETE DETECTE
                self.active = False
                self.event_reading = True
                self.game_event.run()

                # AFFICHER LES BOITES DE DIALOGUES AVEC LE TEXTE
                try:
                    for i in range(2):
                        self.writedTexts[i] = self.actualLines[i]
                        self.comp_lines[i*2].set_component(self.writer.render(self.writedTexts[i], True, (208,208,200)))
                        self.comp_lines[i*2+1].set_component(self.getNewLine(self.writedTexts[i]))
                except:
                    pass

                return False
        
        return True
    
    def init_normal_lines(self):
        self.actualLines = self.paragraphs[0].split("|")
        # Enlever tous les retours à la ligne
        self.actualLines = [line.strip() for line in self.actualLines]
        self.writedTexts = ["" for i in range(len(self.actualLines))]
        
    def check_events(self, event):
        # VERIFIER LES INPUTS DANS LES EVENTS
        if(self.game_event is not None):
            self.game_event.check_inputs(event)

        if(event.type == pygame.KEYDOWN):
            # APPUI SUR LA TOUCHE W DU CLAVIER
            if(event.key == pygame.K_w and self.visible and not self.event_reading):
                if(not self.check_paragraphs()):
                    try:
                    # SI ON APPUIE ALORS QUE TOUS LES PARAGRAPHES NE SONT PAS ENCORE AFFICHES
                        for i in range(2):
                            self.writedTexts[i] = self.actualLines[i]
                            self.comp_lines[i*2].set_component(self.writer.render(self.writedTexts[i], True, (208,208,200)))
                            self.comp_lines[i*2+1].set_component(self.getNewLine(self.writedTexts[i]))
                    except Exception:
                        pass
                # SI ON APPUIE ALORS QUE TOUT EST AFFICHÉ, ON PASSE AU DIALOGUE SUIVANT
                else:
                    self.next_line()
                    self.active = False

    def get_component(self):
        return super().get_component() + EventManager.get_game_components()
        