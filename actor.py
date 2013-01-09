###########################################
# Created on 1-9-2013. Miguel Angel Astor #
###########################################
import pygame
from animation import Animation

ACTOR_STATES = { 'IDLE': 0, 'MOVING': 1 }

class BaseActor:
    """ Represents any game object. This is the parent class for the actor 
    category of objects. It's behaviors are empty. """
    def __init__(self, name, visible, solid, position):
        """ Initializes the actor object. """
        # Conditions and parameters.
        self.name = name
        self.alive = True       # The Actor should be updated.
        self.animated = False   # The Actor has animations.
        self.visible = visible  # The Actor should be rendered.
        self.solid = solid      # The actor can collide with other actors
        # All sprites for an actor are stored as a list of pygame sprites.
        # The list starts empty. Sprites must be added with the add_sprite method.
        self.sprites = []
        # Animations are stored as a key (Animation angle),
        # value (Animation object) pairs. Animations are added with the
        # add_animation method.
        self.animations = {}
        # Parameters for direction and movement.
        self.position = list(position)
        self.speed = [0, 0]         # [X speed, Y speed].
        self.max_speed = [100, 100] # 100 pixels per second.
        self.acceleration = [0, 0]  # Ditto.
        # Collision detection information. AABB and Bounding circle.
        self.b_box = [0, 0] # [X length, Y length].
        self.radius = 0.0
        # Parameters for rendering.
        self.angle = 0
        self.scale = 1.0

    def is_alive(self):
        return self.alive

    def is_animated(self):
        return self.animated

    def is_visible(self):
        return self.visible

    def is_solid(self):
        return self.solid

    def destroy(self):
        self.alive = False

    def set_visible(self, visible):
        self.visible = visible

    def toggle_visible(self):
        self.visible = not self.visible

    def set_solid(self, solid):
        self.solid = solid

    def toggle_solid(self):
        self.solid = not self.solid

    def add_sprite(self, filename)
