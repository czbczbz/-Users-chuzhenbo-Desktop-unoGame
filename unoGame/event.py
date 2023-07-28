from enum import Enum


class EventType(Enum):
    UPDATE_PLAYER_LIST = 1
    fdsa = 2


class Event:
    def __init__(self, event_type):
        self.event_type = event_type
        self.updated_player_list=[]

