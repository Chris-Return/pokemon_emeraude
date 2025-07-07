from src.events.gameevent import GameEvent
from src.events.eventnenupiot import EventNenupiot
from src.events.eventchoosesex import EventChooseSex
from src.events.eventshowsexchoice import EventShowSexChoice
from src.events.eventwriteplayername import EventWritePlayerName
from src.constants.constants import *

class EventManager():

    event_nenupiot = ""

    def __init__(self):
        pass
    
    @staticmethod
    def getGameEvent(event, parent):
        try:
            if(event.__contains__(EVENT_OPENNENUPIOT)):
                EventManager.event_nenupiot = EventNenupiot()
                return EventManager.event_nenupiot
            
            if(event.__contains__(EVENT_CHOOSE_SEX)):
                return EventChooseSex(EventManager.event_nenupiot, parent)

            if(event.__contains__(EVENT_SHOW_SEX_CHOICE)):
                return EventShowSexChoice()

            if(event.__contains__(EVENT_WRITE_PLAYER_NAME)):
                return EventWritePlayerName()
                
        except Exception as e:
            print(e)