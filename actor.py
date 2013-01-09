###########################################
# Created on 1-9-2013. Miguel Angel Astor #
###########################################
import pygame
from animation import Animation

class Actor:
    """ Represents any game object. """
    def __init__(self):
        """ Initializes the actor object. """
        # All sprites for an actor are stored as a list of pygame sprites.
        self.sprites = []
        # Animations are stored as a key (animation name),
        # value (list of sprite indices) pairs.
        self.animations = {}
        # Parameters.
        self.angle = 0
        self.speed = [0, 0] # [X speed, Y speed].
        self.acceleration = [0, 0] # Ditto.
        self.b_box = [0, 0] # [X length, Y length].
