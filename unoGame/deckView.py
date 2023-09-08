import tkinter as tk
from player import Player
from constant import *
from card import Card, read_cards_from_csv, get_card_by_id
import random
from PIL import ImageTk, Image
from protocal import *

BRIGHT_COLORS = ['#55afff', '#55aa55', '#ff5555', '#ffaa00']


class Deck(tk.Frame):
    """
    The frame of the display stack in the main interface
    """
    def __init__(self, master: tk.Tk, width, height, bg=PLAYER_VIEW_BACKGROUND):
        super().__init__(master, width=width, height=height)
        self.master = master
        self.width = width
        self.height = height
        self.player = None
        self.background_canvas = None
        self.curr_color_canvas = None
        self.color_rectangles_in_canvas = []
        self.content_frame = None
        # self.display_canvas = None

        self.deck_image = None
        self.deck_label = None
        self.curr_card_id = None
        self.curr_card_color = None
        self.curr_card_image = None
        self.curr_card_label = None
        self.first = True
        self.my_turn = False
        self.deck_clickable = False
        self.draw_background()

        self.content_frame = tk.Frame(self.background_canvas, width=self.width)
        self.content_frame.place(x=15, y=15)

        self.cards_num = 0
        self.all_cards = read_cards_from_csv()

    def draw_background(self):
        """
        Draw a rounded rectangle
        :return:
        """
        self.background_canvas = tk.Canvas(self, width=self.width, height=self.height)
        self.background_canvas.place(x=0, y=0)
        x1, y1 = 10, 10
        x2, y2 = self.width - 10, self.height - 35
        radius = 5
        outline_color = 'black'
        self.background_canvas.create_arc(x1, y1, x1 + radius * 2, y1 + radius * 2, start=90, extent=90, style="arc", width=3, outline=outline_color)
        self.background_canvas.create_arc(x2 - radius * 2, y1, x2, y1 + radius * 2, start=0, extent=90, style="arc", width=3, outline=outline_color)
        self.background_canvas.create_arc(x2 - radius * 2, y2 - radius * 2, x2, y2, start=270, extent=90, style="arc", width=3, outline=outline_color)
        self.background_canvas.create_arc(x1, y2 - radius * 2, x1 + radius * 2, y2, start=180, extent=90, style="arc", width=3, outline=outline_color)
        self.background_canvas.create_line(x1 + radius, y1, x2 - radius, y1, width=3, fill=outline_color)
        self.background_canvas.create_line(x2, y1 + radius, x2, y2 - radius, width=3, fill=outline_color)
        self.background_canvas.create_line(x2 - radius, y2, x1 + radius, y2, width=3, fill=outline_color)
        self.background_canvas.create_line(x1, y2 - radius, x1, y1 + radius, width=3, fill=outline_color)

    def draw_color_canvas(self):
        """
        Draws the color of the card currently played.
        :return:
        """
        if self.curr_color_canvas is not None:
            self.curr_color_canvas.place_forget()
        self.curr_color_canvas = tk.Canvas(self.background_canvas, width=15, height=CARD_HEIGHT, bg='white' if self.curr_card_color is None else BRIGHT_COLORS[self.curr_card_color - 1])
        self.curr_color_canvas.place(x=CARD_WIDTH+CARD_WIDTH+28, y=15)

    def draw_deck(self):
        """
        Draw the deck and add a click event
        :return:
        """
        image = Image.open(UNKNOWN_CARD_image_path)
        image = image.resize((CARD_WIDTH, CARD_HEIGHT))
        self.deck_image = ImageTk.PhotoImage(image)
        self.deck_label = tk.Label(self.content_frame, image=self.deck_image)
        self.deck_label.image = self.deck_image
        self.deck_label.pack(side=tk.LEFT)
        self.deck_label.bind('<Button-1>', self.on_deck_label_click)

    def on_deck_label_click(self, event):
        """
        The event that is triggered when the deck is clicked
        :param event:
        :return:
        """
        # If it's not my turn, or the deck is not clickable, go straight back.
        if not self.my_turn or not self.deck_clickable:
            return
        print('deck label clicked')
        # Build the event of clicking the deck and inform the server
        packet = build_draw_card_packet(self.player.name, self.player.room_name)
        self.player.client_socket.send(packet)

    def set_my_turn(self, new_turn):
        """
        set my_turn
        :param new_turn:
        :return:
        """

        self.my_turn = new_turn

    def update_view(self, cards_num, curr_card_id, curr_card_color):
        """
        Update the deck view
        :param cards_num:
        :param curr_card_id:
        :param curr_card_color:
        :return:
        """
        self.curr_card_id = curr_card_id
        self.curr_card_color = curr_card_color
        if cards_num == 0:
            self.deck_label.pack_forget()
            self.deck_label = None
        else:
            if self.deck_label is None:
                self.draw_deck()
        if self.curr_card_label is not None:
            self.curr_card_label.pack_forget()
            self.curr_card_label = None
            self.curr_card_image = None
        if curr_card_id is not None:
            card = get_card_by_id(curr_card_id, self.all_cards)
            image = Image.open(card.image_name)
            image = image.resize((CARD_WIDTH, CARD_HEIGHT))
            image = ImageTk.PhotoImage(image)
            self.curr_card_label = tk.Label(self.content_frame, image=image)
            self.curr_card_label.image = image
            self.curr_card_label.pack()
        self.draw_color_canvas()

    def set_clickable(self):
        self.deck_clickable = True
        pass
