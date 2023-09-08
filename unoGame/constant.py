from enum import Enum
from PIL import ImageTk
from PIL.Image import Image

"""
Some constant Settings
"""
# 1920*1080
# 625*500
PLAYER_VIEW_BACKGROUND = '#ffffff'
WINDOW_HEIGHT = int(800*0.6)
WINDOW_WIDTH = int(1000*0.6)
TOP_HEIGHT = int(250*0.6)
BOTTOM_HEIGHT = int(300*0.6)
LEFT_WIDTH = int(350*0.6)
RIGHT_WIDTH = int(350*0.6)
CARDS_CSV = 'images/cards.csv'
UNKNOWN_CARD_image_path = 'images/N.png'
CARD_HEIGHT = int(150*0.6)
CARD_WIDTH = int(100*0.6)


def init():
    global UNKNOWN_CARD
    UNKNOWN_CARD = ImageTk.PhotoImage(image=Image.open('images/N.png').resize(()))



