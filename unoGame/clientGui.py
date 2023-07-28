import socket
import struct
import tkinter as tk
from tkinter import messagebox
from tkinterhtml import HtmlFrame
import webbrowser
from constant import *
from player import Player
from player_view import PlayerView
from deck import Deck


class ClientGUI:
    def __init__(self, client):
        self.client = client
        self.root = tk.Tk()
        self.root.after(100, self.update_ui)
        self.root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')
        self.root.resizable(width=False, height=False)
        self.root.title('Uno Game')
        self.create_menu_bar()
        self.init_frames()

    def show_help(self):
        webbrowser.open('gameInstructions.html')

    def show_about(self):
        messagebox.showinfo(title='about', message='Version 1.0\nAuthor: me')

    def init_frames(self):
        self.top_frame = PlayerView(self.root, width=WINDOW_WIDTH, height=TOP_HEIGHT, bg='red', position='top')
        self.top_frame.pack(side=tk.TOP)

        self.bottom_frame = PlayerView(self.root, width=WINDOW_WIDTH, height=BOTTOM_HEIGHT, bg="blue", position='bottom')
        self.bottom_frame.pack(side=tk.BOTTOM)

        self.left_frame = PlayerView(self.root, width=LEFT_WIDTH, height=WINDOW_HEIGHT - TOP_HEIGHT - BOTTOM_HEIGHT, bg="green", position='left')
        self.left_frame.pack(side=tk.LEFT)

        self.right_frame = PlayerView(self.root, width=RIGHT_WIDTH, height=WINDOW_HEIGHT - TOP_HEIGHT - BOTTOM_HEIGHT, bg="yellow", position='right')
        self.right_frame.pack(side=tk.RIGHT)

        self.center_frame = Deck(self.root, width=WINDOW_WIDTH - LEFT_WIDTH - RIGHT_WIDTH, height=WINDOW_HEIGHT - TOP_HEIGHT - BOTTOM_HEIGHT, bg="orange")
        self.center_frame.pack(side=tk.TOP)

    def create_menu_bar(self):
        menu_bar = tk.Menu(self.root)
        if self.client is not None and self.client.player.is_admin:
            game_menu = tk.Menu(menu_bar, tearoff=0)
            game_menu.add_command(label='New game', command=self.new_game)
            menu_bar.add_cascade(label='Game', menu=game_menu)
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label='How to play', command=self.show_help)
        help_menu.add_command(label='About', command=self.show_about)
        menu_bar.add_cascade(label='Help', menu=help_menu)
        self.root.config(menu=menu_bar)

    def new_game(self):
        pass

    def show(self):
        self.root.mainloop()

    def update_ui(self):
        while self.client is not None and not self.client.events.empty():
            event = self.client.events.get()
            print(event.event_type)


if __name__ == '__main__':
    gui = ClientGUI(None)
    gui.show()
