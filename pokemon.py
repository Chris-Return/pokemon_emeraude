import pygame
import time
import os
import sys
import ctypes
from src.gamescreen.gamemanager import GameManager
from src.constants.constants import MAIN_DIRECTORY, TITRE_FENETRE, LOGO_FENETRE, SCREEN_WIDTH, SCREEN_HEIGHT, NO_FRAME, TRANSPARENT
from src.data.datamanager import DataManager
from src.camera.camera import Camera

def get_components(components):
    list_components = []
    for comp in components:
        if(comp.get_visible()):
            list_components.append(comp)
            list_components += get_components(comp.get_children())

    return list_components

# RECURSIVE QUI ME PERMETTRA D'AFFICHER LES COMPOSANTS ENFANTS
def showComponent(component):
    try:
        if(component.get_modal()):
            screen.blit(component.get_component(), (component.get_position()[0], component.get_position()[1]))
        else:
            screen.blit(component.get_component(), (component.get_position()[0] - Camera.get_position()[0], component.get_position()[1] - Camera.get_position()[1]))
    except:
        pass

# Compter toutes les lignes de codes du projet
def compter_lignes_dossier(dossier):
    total_lignes = 0
    for racine, _, fichiers in os.walk(dossier):
        for fichier in fichiers:
            if fichier.endswith(".py"):
                chemin_fichier = os.path.join(racine, fichier)
                with open(chemin_fichier, "r", encoding="utf-8", errors="ignore") as f:
                    lignes = f.readlines()
                    total_lignes += len(lignes)
    return total_lignes

dossier_src = MAIN_DIRECTORY + "/src"
print(f"Total de lignes de code : {compter_lignes_dossier(dossier_src)}")

# Charger les données
DataManager.load()

# ------------ INITIALISATION ---------------------------------------------------------------
pygame.init()
pygame.display.set_caption(TITRE_FENETRE)
pygame.display.set_icon(pygame.image.load(LOGO_FENETRE))

if(not NO_FRAME):
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
else:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)

game_manager = GameManager()
# ------------ FIN INITIALISATION -----------------------------------------------------------

# ------------ DECLARATION DE LA GESTION DU TEMPS -------------------------------------------
begin_time_millis = round(time.time() * 1000)
end_time_millis = round(time.time() * 1000)
# ------------ FIN DECLARATION DE LA GESTION DU TEMPS ---------------------------------------

clock = pygame.time.Clock()
FPS_CAP = 100

if sys.platform == "win32" and TRANSPARENT:
    hwnd = pygame.display.get_wm_info()["window"]
    extended_style = ctypes.windll.user32.GetWindowLongW(hwnd, -20)
    ctypes.windll.user32.SetWindowLongW(hwnd, -20, extended_style | 0x80000 | 0x20)
    ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0x000000, 255, 0x2)

# BOUCLE DE GAMEPLAY
while(True):
    # PERMETTRE AUX ELEMENTS SE METTRE A JOUR EN FONCTION DU TEMPS
    game_manager.update(end_time_millis - begin_time_millis)

    # MISE A JOUR DU TEMPS DE DEBUT DE BOUCLE
    begin_time_millis = round(time.time() * 1000)

    components = game_manager.get_actual_gamescreen().get_components()
    # Trier les composants
    components = sorted(get_components(components), key=lambda x: x.sort_number)
    # AFFICHER LES COMPOSANTS
    for comp in components:
        showComponent(comp)

    # DESSINER L'ECRAN
    pygame.display.flip()
    # SUR FOND BLANC
    screen.fill((55,55,55))

    # GESTION DES EVENTS
    for event in pygame.event.get():
        game_manager.get_actual_gamescreen().check_events(event)
        # QUAND ON CLIQUE SUR LE BOUTON QUITTER DE LA FENETRE EN HAUT A DROITE
        if(event.type == pygame.QUIT):
            pygame.quit()

    # Supprimez cette ligne si vous ne voulez pas de FDP MAX, ou augmentez manuellement plus haut la valeur du
    # FPS CAP
    clock.tick(FPS_CAP)
    # TEMPS POUR ARRIVER EN FIN DE BOUCLE
    end_time_millis = round(time.time() * 1000)
