import tkinter as tk
from player import Player
from constant import *


class PlayerView(tk.Frame):
    def __init__(self, master: tk.Tk, width, height, player: Player = None, bg=PLAYER_VIEW_BACKGROUND, position='top'):
        super().__init__(master, bg=bg, width=width, height=height)
        self.master = master
        self.width=width
        self.height=height
        self.player = player
        self.position = position

        self.angle = 0
        if position == 'top':
            self.angle = 180
        elif position == 'left':
            self.angle = 90
        elif position == 'right':
            self.angle = 270
