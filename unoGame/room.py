import random
import struct
from typing import Dict

from card import read_cards_from_csv, Card
from constant import CARDS_CSV, PacketType
from player import Player


class Room:
    def __init__(self, name=None):
        self.room = None
        self.players = []  # type:list[Player]
        self.reset_cards()
        self.started = False

    def player_exists(self, player_name):
        for p in self.players:
            if p.name == player_name:
                return True
        return False

    def add_player(self, player):
        player.set_room(self)
        self.players.append(player)
        names_str = ''
        for player in self.players:
            names_str += player.name + ';'
        names_str = names_str[:-1]
        packet = struct.pack(f'>II{len(names_str)}s', PacketType.PLAYER_LIST.value, len(names_str), names_str.encode('ASCII'))
        for p in self.players:
            if p.name != player.name:
                p.client_socket.send(packet)

    def reset_cards(self):
        self.cards = read_cards_from_csv(CARDS_CSV)  # type:list[Card]
        random.shuffle(self.cards)

    # def deal_card(self):
