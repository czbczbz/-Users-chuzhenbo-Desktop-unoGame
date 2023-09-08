import sys
import threading
import tkinter as tk
from tkinter import messagebox, simpledialog
import webbrowser
from constant import *
from player import Player
from playerView import PlayerView
from deckView import Deck
from clientBackgroundThread import receive_message
from event import Event, EventType
from protocal import *
from card import *

# Sets the maximum recursion depth of the program
sys.setrecursionlimit(10000000)


class ClientGUI:
    """
    Program main interface
    """

    def __init__(self, client):
        self.client = client  # client object
        self.root = tk.Tk()
        self.root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')
        self.root.resizable(width=False, height=False)  # The window size cannot be changed
        self.root.title('Uno Game')
        self.create_menu_bar()  # Create menu bar
        self.players_frames = []  # type:list[PlayerView]
        self.init_frames()

        self.background_listening_thread = threading.Thread(target=receive_message, args=(self.client,))
        self.background_listening_thread.daemon = True

    def show_help(self):
        webbrowser.open('gameInstructions.html')

    def show_about(self):
        messagebox.showinfo(title='about', message='Version 1.0\nAuthor: me')

    def init_frames(self):
        self.top_frame = PlayerView(self.root, width=WINDOW_WIDTH, height=TOP_HEIGHT, bg='red', position='top')
        self.top_frame.pack(side=tk.TOP)

        self.bottom_frame = PlayerView(self.root, width=WINDOW_WIDTH, height=BOTTOM_HEIGHT, bg="blue", position='bottom')
        self.bottom_frame.update_player(self.client.player)
        self.bottom_frame.pack(side=tk.BOTTOM)

        self.left_frame = PlayerView(self.root, width=LEFT_WIDTH, height=WINDOW_HEIGHT - TOP_HEIGHT - BOTTOM_HEIGHT, bg="green", position='left')
        self.left_frame.pack(side=tk.LEFT)

        self.right_frame = PlayerView(self.root, width=RIGHT_WIDTH, height=WINDOW_HEIGHT - TOP_HEIGHT - BOTTOM_HEIGHT, bg="yellow", position='right')
        self.right_frame.pack(side=tk.RIGHT)

        self.center_frame = Deck(self.root, width=WINDOW_WIDTH - LEFT_WIDTH - RIGHT_WIDTH, height=WINDOW_HEIGHT - TOP_HEIGHT - BOTTOM_HEIGHT, bg="orange")
        self.center_frame.pack(side=tk.TOP)
        self.center_frame.player = self.client.player

        self.players_frames = [self.bottom_frame, self.left_frame, self.top_frame, self.right_frame]

        for player_frame in self.players_frames:
            player_frame.set_deck(self.center_frame)

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
        self.root['menu'] = menu_bar

    def new_game(self):
        packet = get_start_game_packet_client(self.client.player.name, self.client.player.room_name)
        self.client.player.client_socket.send(packet)

    def show(self):
        # Start the background thread for receiving server-side packet
        self.background_listening_thread.start()
        # update_ui is executed every 100 milliseconds to pull events from the event queue to update the ui
        self.root.after(100, self.update_ui)
        self.root.mainloop()

    def update_ui(self):
        # Retrieve the event from the event queue and update the ui
        while self.client is not None and not self.client.events.empty():
            event = self.client.events.get(timeout=0.1)  # type:Event
            # When the event type is updating the player list
            if event.event_type == EventType.UPDATE_PLAYER_LIST:
                # Find my own serial number from the list
                myself_id = event.updated_player_list.index(self.client.player.name)
                # for players
                players = [self.client.player, None, None, None]
                # Place the other players in turn into Players
                for i, name in enumerate(event.updated_player_list):
                    if i == myself_id:
                        continue
                    players[i - myself_id] = Player(name)
                # Update the corresponding frames according to the players list
                for i, name in enumerate(players):
                    self.players_frames[i].update_player(players[i])
            # When the event type is to start the game
            elif event.event_type == EventType.START_GAME:
                self.center_frame.first = True
                # Empty the cards in the player's hand in the frames
                for player_view in self.players_frames:
                    player = player_view.player
                    if player is not None:
                        player.cards_in_hand.clear()
                        player_view.update_view()
            # When the event type indicates the game state
            elif event.event_type == EventType.GAME_STATE:
                print(event.cards_info)
                first = event.cards_info['first']
                self.center_frame.first = first
                # Update the deck information, as well as the cards currently played
                self.center_frame.update_view(event.cards_info['cards_num'], event.cards_info['curr_card_id'], event.cards_info['curr_card_color'])
                # Update the cards in each player's hand, as well as their respective scores, and change the turn of the player whose turn it is to true
                for player_info in event.cards_info['players']:
                    for player_view in self.players_frames:
                        if player_view.player is not None and player_view.player.name == player_info['name']:
                            player_view.turn = player_info['turn']
                            player_view.player.cards_in_hand = [get_card_by_id(card_id, self.center_frame.all_cards) for card_id in player_info['cards']]
                            player_view.player.score = player_info['score']
                            player_view.update_view()
                # First set the deck to unclickable
                self.center_frame.deck_clickable = False
                # bottom frame for my own. If it is currently my turn, change the frame's my_turn to true
                if self.bottom_frame.turn is True:
                    self.center_frame.my_turn = True
                    player_can_play = False
                    # Go through my own hand to see if there are any cards I can play
                    for card in self.bottom_frame.player.cards_in_hand:
                        card_id = card.id
                        if can_play(self.center_frame.curr_card_id, card_id, self.center_frame.curr_card_color):
                            player_can_play = True
                            break
                    # If there are no cards to play, set the deck to clickable
                    if not player_can_play:
                        self.center_frame.set_clickable()
                else:
                    self.center_frame.my_turn = False
                # If the first card in the game is wild, a dialog box pops up and asks the player to choose a color
                if self.center_frame.first and event.cards_info['curr_card_id'] == 80:
                    choice = simpledialog.askstring('Select an color', 'Input "b", "g", "r", or "y" for blue, green, red, yellow respectively:')
                    while not choice or choice not in ['b', 'g', 'r', 'y']:
                        choice = simpledialog.askstring('Select an color', 'Input "b", "g", "r", or "y" for blue, green, red, yellow respectively:')
                    self.center_frame.curr_card_color = ['b', 'g', 'r', 'y'].index(choice) + 1
            # If the event type is calling UNO
            elif event.event_type == EventType.CALL_UNO:
                # Find the frame of the player calling uno and call its call_uno function
                for player_view in self.players_frames:
                    if player_view.player is not None and player_view.player.name == event.player_name:
                        player_view.call_uno()
            # If the event type indicates final victory
            elif event.event_type == EventType.FINAL_WIN:
                # Empty the cards in each player's hand, set each player's turn to False, and a dialog box will pop up indicating the winning player
                for player_view in self.players_frames:
                    if player_view.player is not None:
                        player_view.player.cards_in_hand.clear()
                        player_view.turn = False
                        player_view.update_view()
                messagebox.showinfo('game over', message=f'The winner is {event.player_name}')
        # Recursive calls update the ui
        self.root.after(100, self.update_ui)
