import struct
from enum import Enum


class PacketType(Enum):
    LOGIN = 1
    LOGIN_SUCCESS = 2
    LOGIN_FAILED_NAME_ALREADY_EXISTS = 3
    LOGIN_FAILED_GAME_STARTED = 4
    PLAYER_LIST = 5
    ROOM_ALREADY_FULL = 6
    START_GAME = 7
    PLAYER_CARDS_INFO = 8
    PLAY_CARD = 9
    DRAW_CARD = 10
    CALL_UNO = 11
    FINAL_WIN = 12


def get_start_game_packet_server():
    """
    On the server side, build the packet that marks the start of the game
    :return:
    """
    return struct.pack('>I', PacketType.START_GAME.value)


def get_game_state_packet_server(room, first=False):
    """
    Package the game state into a sequence of bytes.
    :param room: Specific room
    :param first: Whether it is the first time to play
    :return:
    """
    # The current number of room deck
    packet = struct.pack('>III', PacketType.PLAYER_CARDS_INFO.value, len(room.cards), 1 if first else 0)
    # The card currently played
    curr_card = room.curr_card
    # The next player to play cards
    curr_player = room.curr_player
    if curr_card is not None:
        packet += struct.pack('>III', 1, curr_card.id, room.curr_card_color)
    else:
        packet += struct.pack('>I', 0)
    # number of players
    packet += struct.pack('>I', len(room.players))
    # Package information for each player
    for player in room.players:
        # The length of the player's name and the name
        packet += struct.pack(f'>I{len(player.name)}s', len(player.name), player.name.encode('ASCII'))
        # score of the player
        packet += struct.pack(f'>I', player.score)
        # Whether the player is the next player to play
        if curr_player is not None and curr_player.name == player.name:
            packet += struct.pack(f'>I', 1)
        else:
            packet += struct.pack(f'>I', 0)
        #The number of cards in a player's hand
        packet += struct.pack(f'>I', len(player.cards_in_hand))
        # Pack the cards in the player's hand
        for card in player.cards_in_hand:
            packet += struct.pack(f'>I', card.id)
    return packet


def unpack_cards_info_client(packet):
    """
    Unpack the packaged game state
    :param packet:
    :return:
    """
    result = {}
    offset = 4
    result['cards_num'] = struct.unpack('>I', packet[offset:offset + 4])[0]
    offset += 4
    if struct.unpack('>I', packet[offset:offset + 4])[0] == 1:
        result['first'] = True
    else:
        result['first'] = False
    offset += 4
    has_curr_card = struct.unpack('>I', packet[offset:offset + 4])[0]
    offset += 4
    if has_curr_card == 1:
        result['curr_card_id'], result['curr_card_color'] = struct.unpack('>II', packet[offset:offset + 8])
        offset += 8
    else:
        result['curr_card_id'] = None
    players_num = struct.unpack('>I', packet[offset:offset + 4])[0]
    offset += 4
    result['players'] = []
    for i in range(players_num):
        player_info = {}
        name_length = struct.unpack('>I', packet[offset:offset + 4])[0]
        offset += 4
        player_info['name'] = struct.unpack(f'>{name_length}s', packet[offset:offset + name_length])[0].decode('ASCII')
        offset += name_length
        player_info['score'] = struct.unpack(f'>I', packet[offset:offset + 4])[0]
        offset += 4
        player_info['turn'] = True if struct.unpack('>I', packet[offset:offset + 4])[0] == 1 else False
        offset += 4
        card_num = struct.unpack('>I', packet[offset:offset + 4])[0]
        offset += 4
        player_info['cards'] = []
        for j in range(card_num):
            card_id = struct.unpack('>I', packet[offset:offset + 4])[0]
            offset += 4
            player_info['cards'].append(card_id)
        result['players'].append(player_info)
    return result


def build_packet_header_client(packet_type, player_name, room_name):
    """
    When the player sends a packet to the server, the beginning of the packet includes the type of the packet, the name of the room, the name of the player
    :param packet_type:
    :param player_name:
    :param room_name:
    :return:
    """
    packet = struct.pack('>III', packet_type, len(room_name), len(player_name))
    packet += struct.pack(f'>{len(room_name)}s', room_name.encode('ASCII'))
    packet += struct.pack(f'>{len(player_name)}s', player_name.encode('ASCII'))
    return packet


def get_start_game_packet_client(player_name, room_name: str):
    """
    On the client side, build the packet that represents the start of the game
    :param player_name:
    :param room_name:
    :return:
    """
    return build_packet_header_client(PacketType.START_GAME.value, player_name, room_name)


def build_play_card_packet(player_name, room_name, card_id, card_color):
    """
    When a player plays a card, a packet is built to be sent to the server
    :param player_name:
    :param room_name:
    :param card_id:
    :param card_color:
    :return:
    """
    header = build_packet_header_client(PacketType.PLAY_CARD.value, player_name, room_name)
    return header + struct.pack('>II', card_id, card_color)


def build_draw_card_packet(player_name, room_name):
    """
    When a player draws cards from the deck, the packet is built
    :param player_name:
    :param room_name:
    :return:
    """
    return build_packet_header_client(PacketType.DRAW_CARD.value, player_name, room_name)


def build_call_uno_packet(player_name, room_name):
    """
    when a player call uno, the packet is build
    :param player_name:
    :param room_name:
    :return:
    """
    return build_packet_header_client(PacketType.CALL_UNO.value, player_name, room_name)


def build_game_over_packet_server(final_winner_player):
    """
    When the game ends, on the server side, a packet indicating the end of the game is built, containing the name of the player who won
    :param final_winner_player:
    :return:
    """

    packet = struct.pack('>I', PacketType.FINAL_WIN.value)
    packet += struct.pack('>I', len(final_winner_player.name))
    packet += struct.pack(f'>{len(final_winner_player.name)}s', final_winner_player.name.encode('ASCII'))
    return packet
