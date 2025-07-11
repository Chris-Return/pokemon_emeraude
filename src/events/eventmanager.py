from src.events.gameevent import GameEvent
from src.events.eventnenupiot import EventNenupiot
from src.events.eventchoosesex import EventChooseSex
from src.events.eventshowsexchoice import EventShowSexChoice
from src.events.eventwriteplayername import EventWritePlayerName
from src.events.eventshowprofandnenupiot import EventShowProfAndNenupiot
from src.events.eventshowdresseur import EventShowDresseur
from src.constants.constants import *

class EventManager():

    event_nenupiot = None
    event_choose_sex = None
    components = []

    def __init__(self):
        pass
    
    @staticmethod
    def getGameEvent(event, parent):
        try:
            if(event.__contains__(EVENT_OPENNENUPIOT)):
                EventManager.event_nenupiot = EventNenupiot()
                EventManager.components.append(EventManager.event_nenupiot)
                return EventManager.event_nenupiot
            
            if(event.__contains__(EVENT_CHOOSE_SEX)):
                EventManager.event_choose_sex = EventChooseSex(EventManager.event_nenupiot, parent)
                EventManager.components.append(EventManager.event_choose_sex)
                return EventManager.event_choose_sex
            
            if(event.__contains__(EVENT_SHOW_PROF_AND_NENUPIOT)):
                return EventShowProfAndNenupiot(EventManager.event_nenupiot, parent)

            if(event.__contains__(EVENT_SHOW_SEX_CHOICE)):
                return EventShowSexChoice(parent)

            if(event.__contains__(EVENT_WRITE_PLAYER_NAME)):
                return EventWritePlayerName()
            
            if(event.__contains__(EVENT_SHOW_DRESSEUR)):
                return EventShowDresseur(parent)
                
        except Exception as e:
            print(e)

    @staticmethod
    def get_game_components():
        comp_to_return = []
        for comp in EventManager.components:
            for c in comp.get_components():
                comp_to_return.append(c)

        return comp_to_return