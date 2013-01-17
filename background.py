############################################
# Created on 1-16-2013. Miguel Angel Astor #
############################################
import pygame

import imloader
from constants import DEBUG
class TiledBackground():
    def __init__(self, width, height, texture_filename, position_x = 0, position_y = 0):
        self.w = width
        self.h = height
        self.position = (position_x, position_y)
        
        texture = imloader.cached_image_loader.get_image_to_screen_percent(texture_filename)
        img_w = texture.get_width()
        img_h = texture.get_height()

        rep_x = (self.w // img_w) + 1
        rep_y = (self.h // img_h) + 1
        if DEBUG:
            print '(' + str(rep_x) + ', ' + str(rep_y) + ')'

        self.image = pygame.Surface((self.w, self.h))
        render_x = 0
        render_y = 0
        for i in range(rep_x):
            render_x = i * img_w
            for j in range(rep_y):
                render_y = j * img_h
                self.image.blit(texture, (render_x, render_y))
            render_y = 0

    def get_width(self):
        return self.w

    def get_height(self):
        return self.h

    def get_position(self):
        return self.position

    def set_position(self, position):
        self.position = position

    def set_position_xy(self, position_x, position_y):
        self.position = (position_x, position_y)

    def draw(self, canvas):
        canvas.blit(self.image, self.position)
