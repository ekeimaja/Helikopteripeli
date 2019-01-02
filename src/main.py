import timeit
import os
import arcade
import pymunk

from src.create_level import create_level_1
from src.physics import (
    PymunkSprite,
    check_grounding,
    resync_physics_sprites,
)

from src.constants import *


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Background image will be stored in this variable
        self.background = None

        # -- Pymunk
        self.space = pymunk.Space()
        self.space.gravity = GRAVITY

        # Lists of sprites
        self.dynamic_sprite_list = arcade.SpriteList()
        self.static_sprite_list = arcade.SpriteList()

        # Draw and processing timings
        self.draw_time = 0
        self.processing_time = 0

        # Current force applied to the player for movement by keyboard
        self.force = (0, 0)

        # Set the viewport boundaries
        # These numbers set where we have 'scrolled' to.
        self.view_left = 0
        self.view_bottom = 0

        create_level_1(self.space, self.static_sprite_list, self.dynamic_sprite_list)

        # Create player
        x = SCREEN_WIDTH / 4
        y = 150
        self.player = PymunkSprite("../images/heli.png", x, y, scale=1.0, moment=pymunk.inf, mass=DEFAULT_MASS)
        self.dynamic_sprite_list.append(self.player)
        self.space.add(self.player.body, self.player.shape)

        self.background = arcade.load_texture("../images/bg.png")

    def on_draw(self):
        """ Render the screen. """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Start timing how long this takes
        draw_start_time = timeit.default_timer()

        # Draw all the sprites
        self.static_sprite_list.draw()
        self.dynamic_sprite_list.draw()

        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT,
                                      self.background)

    def scroll_viewport(self):
        """ Manage scrolling of the viewport. """

        # Flipped to true if we need to scroll
        changed = False

        # Scroll left
        left_bndry = self.view_left + VIEWPORT_MARGIN
        if self.player.left < left_bndry:
            self.view_left -= left_bndry - self.player.left
            changed = True

        # Scroll right
        right_bndry = self.view_left + SCREEN_WIDTH - VIEWPORT_MARGIN
        if self.player.right > right_bndry:
            self.view_left += self.player.right - right_bndry
            changed = True

        # Scroll up
        top_bndry = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN
        if self.player.top > top_bndry:
            self.view_bottom += self.player.top - top_bndry
            changed = True

        # Scroll down
        bottom_bndry = self.view_bottom + VIEWPORT_MARGIN
        if self.player.bottom < bottom_bndry:
            self.view_bottom -= bottom_bndry - self.player.bottom
            changed = True

        if changed:
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)

    def update(self, delta_time):
        """ Update the sprites """

        # Keep track of how long this function takes.
        start_time = timeit.default_timer()

        # If we have force to apply to the player (from hitting the arrow
        # keys), apply it.
        self.player.body.apply_force_at_local_point(self.force, (0, 0))

        # check_collision(self.player)

        # See if the player is standing on an item.
        # If she is, apply opposite force to the item below her.
        # So if she moves left, the box below her will have
        # a force to move to the right.
        grounding = check_grounding(self.player)
        if self.force[0] and grounding and grounding['body']:
            grounding['body'].apply_force_at_world_point((-self.force[0], 0), grounding['position'])

        # Check for sprites that fall off the screen.
        # If so, get rid of them.
        for sprite in self.dynamic_sprite_list:
            if sprite.shape.body.position.y < 0:
                # Remove sprites from physics space
                self.space.remove(sprite.shape, sprite.shape.body)
                # Remove sprites from physics list
                sprite.kill()

        # Update physics
        self.space.step(1 / 60.0)

        # Resync the sprites to the physics objects that shadow them
        resync_physics_sprites(self.dynamic_sprite_list)

        # Scroll the viewport if needed
        self.scroll_viewport()

        # Save the time it took to do this.
        self.processing_time = timeit.default_timer() - start_time


def main():
    MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)

    arcade.run()


if __name__ == "__main__":
    main()
