import socket
import struct
import threading
from client import Client
from constant import PacketType


def receive_message(client: 'Client'):
    while True:
        try:
            packet = client.client_socket.recv(1024)
            packet_type = struct.unpack('>I', packet[:4])
            if packet_type == PacketType.PLAYER_LIST.value:
                names_length=struct.unpack('>I',packet[4:8])[0]
                names=struct.unpack(f'>{names_length}s',packet[8:])[0].decode('ASCII')
                names=names.split(';')
                print(names)
        except ConnectionResetError:
            break
