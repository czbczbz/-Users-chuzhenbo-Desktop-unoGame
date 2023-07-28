import tkinter as tk
from player import Player
from constant import *
from card import Card, read_cards_from_csv
import random
from PIL import ImageTk, Image


class Deck(tk.Frame):
    def __init__(self, master: tk.Tk, width, height, bg=PLAYER_VIEW_BACKGROUND):
        super().__init__(master, width=width, height=height)
        self.master = master
        self.width = width
        self.height = height
        self.background_canvas = None
        self.content_frame = None
        self.display_canvas = None
        self.deck_image = None
        self.deck_label = None
        self.my_turn = False
        self.draw_background()
        self.draw_content_1()
        self.cards = read_cards_from_csv(CARDS_CSV)  # type:list[Card]
        random.shuffle(self.cards)

    def draw_background(self):
        self.background_canvas = tk.Canvas(self, width=self.width, height=self.height)
        self.background_canvas.pack()
        x1, y1 = 20, 20
        x2, y2 = self.width - 20, self.height - 20
        radius = 10
        outline_color = 'blue'
        self.background_canvas.create_arc(x1, y1, x1 + radius * 2, y1 + radius * 2, start=90, extent=90, style="arc", width=5, outline=outline_color)
        self.background_canvas.create_arc(x2 - radius * 2, y1, x2, y1 + radius * 2, start=0, extent=90, style="arc", width=5, outline=outline_color)
        self.background_canvas.create_arc(x2 - radius * 2, y2 - radius * 2, x2, y2, start=270, extent=90, style="arc", width=5, outline=outline_color)
        self.background_canvas.create_arc(x1, y2 - radius * 2, x1 + radius * 2, y2, start=180, extent=90, style="arc", width=5, outline=outline_color)
        self.background_canvas.create_line(x1 + radius, y1, x2 - radius, y1, width=5, fill=outline_color)
        self.background_canvas.create_line(x2, y1 + radius, x2, y2 - radius, width=5, fill=outline_color)
        self.background_canvas.create_line(x2 - radius, y2, x1 + radius, y2, width=5, fill=outline_color)
        self.background_canvas.create_line(x1, y2 - radius, x1, y1 + radius, width=5, fill=outline_color)

    def draw_content_1(self):
        self.content_frame = tk.Frame(self.background_canvas)
        self.content_frame.place(x=30, y=30)

        image = Image.open(UNKNOWN_CARD_image_path)
        resized_image = image.resize((CARD_WIDTH, CARD_HEIGHT))
        deck_image = ImageTk.PhotoImage(resized_image)
        self.deck_label = tk.Label(self.content_frame, image=deck_image)
        self.deck_label.image = deck_image
        self.deck_label.pack()
        self.deck_label.bind('<Button-1>', self.on_deck_label_click)

    def on_deck_label_click(self, event):
        if not self.my_turn:
            return
        print('deck label clicked')

    def set_my_turn(self, new_turn):
        self.my_turn = new_turn

    def pop(self):
        if len(self.cards) == 0:
            return None
        front = self.cards.pop(0)
        return front
