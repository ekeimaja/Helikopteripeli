import arcade
import pymunk
from src.constants import *
from src.physics import *


class Helicopter:
    """ For later use to make possible to make multiple players """
    def __init__(self, id, img, position_x, position_y, change_x, change_y, health):
        self.id = id
        self.img = img
        self.posx = position_x
        self.posy = position_y
        self.chgx = change_x
        self.chgy = change_y
        self.health = health
