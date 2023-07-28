import socket
import struct
import threading
from room import Room
from player import Player
from constant import *

SERVER_ADDRESS = '0.0.0.0'
SERVER_PORT = 8888


class Server:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((SERVER_ADDRESS, SERVER_PORT))
        self.rooms = {}  # type:dict[str,Room]

    def room_exists(self, room_name):
        return room_name in self.rooms

    def handle_client(self, client_socket: socket.socket, client_address):

        while True:
            packet = client_socket.recv(1024)
            if len(packet) == 0:  # 对方关闭连接
                break
            print(len(packet))
            packet_type, len_room_name, len_player_name = struct.unpack('>III', packet[:12])
            print(packet_type, len_room_name, len_player_name)
            room_name = struct.unpack(f'{len_room_name}s', packet[12:12 + len_room_name])[0].decode('ASCII')
            player_name = struct.unpack(f'{len_player_name}s', packet[12 + len_room_name:12 + len_room_name + len_player_name])[0].decode('ASCII')
            print('room name:', room_name, 'player name:', player_name)
            if packet_type == PacketType.LOGIN.value:  # 登录
                if self.room_exists(room_name):
                    if self.rooms[room_name].started:
                        packet = struct.pack('>Ic', PacketType.LOGIN_FAILED_GAME_STARTED.value,b'N')
                        client_socket.send(packet)
                        client_socket.close()
                    if self.rooms[room_name].player_exists(player_name):
                        packet = struct.pack('>I', PacketType.LOGIN_FAILED_NAME_ALREADY_EXISTS.value,b'N')
                        client_socket.send(packet)
                        break
                    else:
                        player = Player(player_name, room_name, client_socket, client_address, False)
                        self.rooms[room_name].add_player(player)
                        packet = struct.pack('>Ic', PacketType.LOGIN_SUCCESS.value, b'N')
                        client_socket.send(packet)
                else:
                    print('login')
                    self.rooms[room_name] = Room(room_name)
                    player = Player(player_name, room_name, client_socket, client_address, True)
                    self.rooms[room_name].add_player(player)
                    packet = struct.pack('>Ic', PacketType.LOGIN_SUCCESS.value, b'A')
                    client_socket.send(packet)

    def start(self):
        self.server_socket.listen(1)

        while True:
            client_socket, client_address = self.server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address), daemon=True)
            client_thread.start()


if __name__ == '__main__':
    server = Server()
    server.start()
