import socket
import struct
import threading
from protocal import PacketType, unpack_cards_info_client
from event import Event, EventType


def receive_message(client: 'Client'):
    """
    A function in the client associated with a child thread used to receive data from the server
    :param client: the Client object
    :return:
    """

    while True:
        try:
            # Receives packet from the server
            packet = client.client_socket.recv(1024)
            # parse the type of the packet
            packet_type = struct.unpack('>I', packet[:4])[0]
            # Player list
            if packet_type == PacketType.PLAYER_LIST.value:
                names_length = struct.unpack('>I', packet[4:8])[0]
                names = struct.unpack(f'>{names_length}s', packet[8:])[0].decode('ASCII')
                names = names.split(';')
                # Create an event
                event = Event(EventType.UPDATE_PLAYER_LIST)
                event.updated_player_list = names
                # Adds the event to the event queue
                client.events.put(event)
            # A packet marking the start of the game
            elif packet_type == PacketType.START_GAME.value:
                event = Event(EventType.START_GAME)
                client.events.put(event)
            # Packet of cards information in the room
            elif packet_type == PacketType.PLAYER_CARDS_INFO.value:
                event = Event(EventType.GAME_STATE)
                event.cards_info = unpack_cards_info_client(packet)
                client.events.put(event)
            # One of the players called out uno
            elif packet_type == PacketType.CALL_UNO.value:
                packet_type, len_room_name, len_player_name = struct.unpack('>III', packet[:12])
                room_name = struct.unpack(f'{len_room_name}s', packet[12:12 + len_room_name])[0].decode('ASCII')
                player_name = struct.unpack(f'{len_player_name}s', packet[12 + len_room_name:12 + len_room_name + len_player_name])[0].decode('ASCII')
                event = Event(EventType.CALL_UNO)
                event.player_name = player_name
                client.events.put(event)
            #  marks the end of the game
            elif packet_type == PacketType.FINAL_WIN.value:
                name_length = struct.unpack('>I', packet[4:8])[0]
                player_name = struct.unpack(f'>{name_length}s', packet[8:8 + name_length])[0].decode('ASCII')
                event = Event(EventType.FINAL_WIN)
                event.player_name = player_name
                client.events.put(event)
            else:
                print('Unknown packet type')
        except ConnectionResetError:
            continue
