"""
This code creates the layout of level one.
"""
import pymunk

from src.physics import (
    PymunkSprite,
)
from src.constants import *


def create_floor(space, sprite_list):
    """ Create a bunch of blocks for the floor. """
    for x in range(-1000, 2000):
        y = SPRITE_SIZE / 2
        sprite = PymunkSprite("../images/bottom.png", x, y, scale=1.0, body_type=pymunk.Body.STATIC)
        sprite_list.append(sprite)
        space.add(sprite.body, sprite.shape)


def create_level_1(space, static_sprite_list, dynamic_sprite_list):
    """ Create level one. """
    create_floor(space, static_sprite_list)
