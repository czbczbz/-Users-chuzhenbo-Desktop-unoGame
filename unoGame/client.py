import queue

from loginDialog import LoginDialog
from clientGui import ClientGUI
from event import Event, EventType


class Client:
    def __init__(self):
        self.gui = None
        self.player = None
        self.client_socket = None
        self.events = queue.Queue()  # type:queue.Queue[Event]

    def login(self):
        login_dialog = LoginDialog(self)
        login_dialog.show()
        if self.player is None:
            return False
        return True

    def play(self):
        self.gui = ClientGUI(self)
        print(self.player.is_admin)
        self.gui.show()


if __name__ == '__main__':
    client = Client()
    if client.login():
        print('login')
        client.play()
    else:
        print('not login')
