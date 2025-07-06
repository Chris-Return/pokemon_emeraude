from src.events.gameevent import GameEvent
from src.events.eventnenupiot import EventNenupiot
from src.constants.constants import *

class EventManager():
    def __init__(self):
        pass
    
    @staticmethod
    def getGameEvent(event):
        if(event.__contains__(EVENT_OPENNENUPIOT)):
            return EventNenupiot()
        
        return None