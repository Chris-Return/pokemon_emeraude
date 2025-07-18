import pygame
import time
import os
from src.gamescreen.gamemanager import GameManager
from src.constants.constants import *
from src.data.datamanager import DataManager
from src.camera.camera import Camera

# RECURSIVE QUI ME PERMETTRA D'AFFICHER LES COMPOSANTS ENFANTS
def showComponent(component):
    # Instruction pour une future caméra
    # screen.blit(sprite.image, camera.apply(sprite.rect))
    if(component.get_visible()):
        try:
            screen.blit(component.get_component(), (component.get_position()[0] - Camera.get_position()[0], component.get_position()[1] - Camera.get_position()[1]))
        except Exception:
            pass

        for child_component in component.get_children():
            showComponent(child_component)

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

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
game_manager = GameManager()
# ------------ FIN INITIALISATION -----------------------------------------------------------

# ------------ DECLARATION DE LA GESTION DU TEMPS -------------------------------------------
begin_time_millis = round(time.time() * 1000)
end_time_millis = round(time.time() * 1000)
# ------------ FIN DECLARATION DE LA GESTION DU TEMPS ---------------------------------------

clock = pygame.time.Clock()
FPS_CAP = 100

# BOUCLE DE GAMEPLAY
while(True):
    # PERMETTRE AUX ELEMENTS SE METTRE A JOUR EN FONCTION DU TEMPS
    game_manager.update(end_time_millis - begin_time_millis)

    # MISE A JOUR DU TEMPS DE DEBUT DE BOUCLE
    begin_time_millis = round(time.time() * 1000)

    # AFFICHER LES COMPOSANTS
    for comp in game_manager.get_actual_gamescreen().get_components():
        showComponent(comp)

    # DESSINER L'ECRAN
    pygame.display.flip()
    # SUR FOND BLANC
    screen.fill((255,255,255))

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
