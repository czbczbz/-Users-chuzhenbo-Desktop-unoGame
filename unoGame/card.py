import csv
import os

from PIL import ImageTk, Image
from typing import Tuple


class Card:
    def __init__(self, id, name, image_name):
        self.id = id
        self.name = name
        self.image_name = os.path.join('images',image_name)
        # self.image = ImageTk.PhotoImage(image=Image.open(self.image_name))

    def resize_image(self, size: Tuple[int, int]):
        self.image = ImageTk.PhotoImage(image=Image.open(self.image_name).resize(size))


def read_cards_from_csv(file_name):
    cards = []
    with open(file_name, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)
        for row in reader:
            name, id, image_name, num = row[0], int(row[1]), row[2], row[3]
            for _ in num:
                cards.append(Card(id, name, image_name))
    return cards

if __name__ == '__main__':
    read_cards_from_csv('images/cards.csv')
