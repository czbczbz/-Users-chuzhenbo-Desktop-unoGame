import random
import tkinter as tk
from tkinter.ttk import Combobox

from player import Player
from constant import *
from PIL import ImageTk, Image
from tkinter import Label
from card import *
from protocal import *
import tkinter.simpledialog as simpledialog


class PlayerView(tk.Frame):
    """
    In the main interface, the interface of each player in four directions
    """

    def __init__(self, master: tk.Tk, width, height, player: Player = None, bg=PLAYER_VIEW_BACKGROUND, position='top'):
        super().__init__(master, width=width, height=height)
        self.master = master
        self.width = width
        self.height = height
        self.player = player  # Corresponding player
        self.position = position  # 'top', 'bottom','left' or 'right'
        self.deck = None  # The deck in the middle of the main screen
        self.name_label = None  # type:[tk.Label]
        self.score_label = None  # type:[tk.Label]
        self.name_x = None  # Coordinate of name
        self.name_y = None
        self.score_x = None  # Coordinate of score
        self.score_y = None
        self.after_toggle_id = None  # Flash animation id
        self.line_canvas = None
        self.update_player()
        self.images = []
        self.image_labels = []  # type:[tk.Label]
        self.combobox = None

        self.turn = False

    def toggle_name_label_visibility(self):
        """
        When it was my turn to play on my own, the label of name and score flashed
        :return:
        """
        if self.turn:
            if self.name_label.winfo_viewable():
                self.name_label.place_forget()
                self.score_label.place_forget()
            else:
                self.name_label.place(x=self.name_x, y=self.name_y)
                self.score_label.place(x=self.score_x, y=self.score_y)
            self.after_toggle_id = self.after(500, self.toggle_name_label_visibility)
        else:
            if self.after_toggle_id is not None:
                self.after_cancel(self.after_toggle_id)
                self.after_toggle_id = None
            if not self.name_label.winfo_viewable():
                self.name_label.place(x=self.name_x, y=self.name_y)
                self.score_label.place(x=self.score_x, y=self.score_y)

    def update_player(self, player: Player = None):
        """
        Update the player information on the interface
        :param player:
        :return:
        """
        self.player = player
        if self.line_canvas is not None:
            self.line_canvas.place_forget()
            self.line_canvas = None
        if self.name_label is None:
            self.name_x = 25
            self.score_x = self.width - 100
            if self.position in ['top', 'bottom']:
                self.name_y = TOP_HEIGHT - int(30 * 0.6) if self.position == 'top' else BOTTOM_HEIGHT - int(60 * 0.6)
            else:
                self.name_y = (WINDOW_HEIGHT - TOP_HEIGHT - BOTTOM_HEIGHT) - 25
            self.score_y = self.name_y

            self.name_label = tk.Label(self, text=self.player.name if self.player is not None else '', font=('Arial', 10))
            self.name_label.place(x=self.name_x, y=self.name_y)

            self.score_label = tk.Label(self, text=f'Score: {self.player.score}' if self.player is not None else '', font=('Arial', 10))
            self.score_label.place(x=self.score_x, y=self.score_y)

            self.line_canvas = tk.Canvas(self, width=self.width - int(50 * 0.6), height=2)
            self.line_canvas.place(x=25, y=self.name_y - 2)
            self.line_canvas.create_line(0, 0, self.width - int(50 * 0.6), 0, width=5, fill='gray')
        else:
            self.line_canvas = tk.Canvas(self, width=self.width - int(50 * 0.6), height=2)
            self.line_canvas.place(x=25, y=self.name_y - 2)
            self.line_canvas.create_line(0, 0, self.width - int(50 * 0.6), 0, width=5, fill='black')
            self.name_label['text'] = player.name if player is not None else ''
            self.score_label['text'] = f'Score: {self.player.score}' if player is not None else ''

    def get_card_coords(self, card_number):
        """
        According to the number of cards, get the coordinates of each card in the interface
        :param card_number:
        :return:
        """
        if self.position in ['top', 'bottom']:
            left_top_x, left_top_y, bottom_right_x, bottom_right_y = 10, 10, WINDOW_WIDTH - 10, BOTTOM_HEIGHT - 10
            if self.position == 'top':
                left_top_y = 20
        else:
            left_top_x, left_top_y, bottom_right_x, bottom_right_y = 10, 20, LEFT_WIDTH - 10, WINDOW_HEIGHT - TOP_HEIGHT - BOTTOM_HEIGHT - 10
        total_width = bottom_right_x - left_top_x
        coords = []
        if card_number * CARD_WIDTH > total_width:
            interval = (total_width - CARD_WIDTH) / (card_number - 1)
            for i in range(card_number):
                coords.append([int(left_top_x + i * interval), left_top_y])
        else:
            start_x = (total_width - card_number * CARD_WIDTH) // 2
            for i in range(card_number):
                coords.append([left_top_x + start_x + i * CARD_WIDTH, left_top_y])
        return coords

    def update_view(self):
        """
        Update interface
        :return:
        """
        if self.turn is True:
            self.toggle_name_label_visibility()
        else:
            if not self.name_label.winfo_viewable():
                self.name_label.place(x=self.name_x, y=self.name_y)
                self.score_label.place(x=self.score_x, y=self.score_y)

        for image_label in self.image_labels:
            image_label.place_forget()
        self.image_labels.clear()
        if self.player is None:
            return
        self.score_label['text'] = f'Score: {self.player.score}'
        cards = self.player.cards_in_hand
        card_number = len(cards)
        if card_number == 0:
            return
        if self.position != 'bottom':
            cards = [Card(None, None, 'N.png') for _ in range(card_number)]
        coords = self.get_card_coords(card_number)
        for i in range(card_number):
            image = Image.open(cards[i].image_name)
            resized_image = image.resize((CARD_WIDTH, CARD_HEIGHT))
            image = ImageTk.PhotoImage(resized_image)
            self.images.append(image)
            label = tk.Label(self, image=image)
            label.place(x=coords[i][0], y=coords[i][1])
            if self.position == 'bottom':
                label.bind('<Button-1>', self.on_card_click)
            self.image_labels.append(label)

    def on_card_click(self, event):
        """
        The action that occurs when a card is clicked
        :param event:
        :return:
        """
        if not self.turn:
            return
        label_index = self.image_labels.index(event.widget)
        curr_clicked_card_id = self.player.cards_in_hand[label_index].id

        if not can_play(self.deck.curr_card_id, curr_clicked_card_id, self.deck.curr_card_color):
            return

        self.turn = False
        # Cancel name flashing
        if self.after_toggle_id is not None:
            self.after_cancel(self.after_toggle_id)
            self.after_toggle_id = None
        # Gets the color of the current click. If it is a wild card, a dialog box pops up and asks the user
        curr_clicked_card_color = None if is_wild_card(curr_clicked_card_id) else get_card_color_by_id(curr_clicked_card_id)
        if is_wild_card(curr_clicked_card_id):
            choice = simpledialog.askstring('Select an color', 'Input "b", "g", "r", or "y" for blue, green, red, yellow respectively:')
            while not choice or choice not in ['b', 'g', 'r', 'y']:
                choice = simpledialog.askstring('Select an color', 'Input "b", "g", "r", or "y" for blue, green, red, yellow respectively:')
            curr_clicked_card_color = ['b', 'g', 'r', 'y'].index(choice) + 1
        # Sends the click card information to the server
        packet = build_play_card_packet(self.player.name, self.player.room_name, curr_clicked_card_id, curr_clicked_card_color)
        self.player.client_socket.send(packet)
        # On the client side, remove played cards from the player's hand
        for card in self.player.cards_in_hand:
            if card.id == curr_clicked_card_id:
                self.player.cards_in_hand.remove(card)
                break
        # If there is only one card left, send a message to the server calling out UNO
        if len(self.player.cards_in_hand) == 1:
            packet = build_call_uno_packet(self.player.name, self.player.room_name)
            self.player.client_socket.send(packet)

    def set_deck(self, deck):
        """
        set deck
        :param deck:
        :return:
        """
        self.deck = deck

    def call_uno(self):
        toast = tk.Toplevel()
        toast.wm_overrideredirect(True)  # Remove window decorations
        toast.wm_geometry("+{}+{}".format(self.name_label.winfo_rootx() + 50, self.name_label.winfo_rooty() - 20))

        image = Image.open('images/LOGO.png')
        image = image.resize((60, 40))
        image = ImageTk.PhotoImage(image)

        label = tk.Label(toast, image=image)
        label.image = image
        label.pack(padx=10, pady=5)
        toast.after(2000, toast.destroy)
