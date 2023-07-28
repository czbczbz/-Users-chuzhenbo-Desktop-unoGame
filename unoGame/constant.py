from enum import Enum
from PIL import ImageTk
from PIL.Image import Image

PLAYER_VIEW_BACKGROUND = '#ffffff'
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 1000
TOP_HEIGHT = 250
BOTTOM_HEIGHT = 250
LEFT_WIDTH = 300
RIGHT_WIDTH = 300
CARDS_CSV = 'images/cards.csv'
UNKNOWN_CARD_image_path = 'images/N.png'
CARD_HEIGHT = 240
CARD_WIDTH = 160


def init():
    global UNKNOWN_CARD
    UNKNOWN_CARD = ImageTk.PhotoImage(image=Image.open('images/N.png').resize(()))


class PacketType(Enum):
    LOGIN = 1
    LOGIN_SUCCESS = 2
    LOGIN_FAILED_NAME_ALREADY_EXISTS = 3
    LOGIN_FAILED_GAME_STARTED = 4
    PLAYER_LIST = 5
