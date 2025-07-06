from src.gamescreen.menuscreen import *
from src.gamescreen.loadingmenu import *
from src.gamescreen.newgame import *
from src.data.jsondata import JSONData

class GameManager:
    def __init__(self):
        self.actualGameScreen = self.get_screen(BEGIN_SCREEN_GAME)
        self.json_data = JSONData()
        self.json_data.loadAll()

    def update(self, deltaTime):
        if(self.actualGameScreen.active):
            self.actualGameScreen.update(deltaTime)
        else:
            self.actualGameScreen = self.get_screen(self.actualGameScreen.get_next_screen_number())

    def get_screen(self, number):
        match number:
            case 0: return MenuScreen()
            case 1: return LoadingMenu()
            case 2: return NewGameScreen()
            case _: 
                print("Aucun écran ne correspond au numéro : "+number)
                return 0
             
    def get_actual_gamescreen(self):
         return self.actualGameScreen