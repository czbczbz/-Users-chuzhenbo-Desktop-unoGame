import socket


class Player:
    """

    """
    def __init__(self, name=None, room_name=None, client_socket=None, client_address=None, is_admin=False):
        """

        :param name: name of the player
        :param room_name: the name of the room where the player is
        :param client_socket: The socket associated with the player
        :param client_address: The address of the socket associated with the player
        :param is_admin: # Whether the player is the administrator of the room he is in
        """
        self.name = name  # type:str
        self.client_socket = client_socket  # type:socket.socket
        self.client_address = client_address
        self.room_name = room_name
        self.room = None
        self.score = 0
        self.cards_in_hand = []
        self.is_admin = is_admin

    def set_room(self, room):
        """
        Set the room the player is in
        :param room: a room object
        :return: None
        """
        self.room = room

    def __eq__(self, other):
        """
        Determine if two players are the same
        :param other: other player
        :return: True or False
        """
        return self.name == other.name
