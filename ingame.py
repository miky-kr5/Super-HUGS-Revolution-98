###########################################
# Created on 1-7-2013. Miguel Angel Astor #
###########################################
import pygame

try:
   import android
except ImportError:
   android = None

import player
import background
from state import BaseState, VALID_STATES

class InGameState(BaseState):
    def __init__(self):
       BaseState.__init__(self)

       self.next_transition = VALID_STATES['STAY']
       self.cursor_x = 0
       self.cursor_y = 0
       self.user_click = False

       screen_center = self.get_screen_center()
       self.rectangle = pygame.Rect(screen_center[0] - 50, screen_center[1] - 50, 100, 100)

       self.background = background.TiledBackground(1280, 1024, 'gfx/piso.png')

    def input(self):
       for event in pygame.event.get():
          if android:
             if android.check_pause():
                android.wait_for_resume()

          if event.type == pygame.KEYDOWN:
             if event.key == pygame.K_ESCAPE:
                self.next_transition = VALID_STATES['QUIT']
             self.user_click = True
          if event.type == pygame.QUIT:
             self.next_transition = VALID_STATES['QUIT']

          # Catch the position of a mouse click (or tap).
          if event.type == pygame.MOUSEBUTTONDOWN:
             (self.cursor_x, self.cursor_y) = event.pos
             self.user_click = True

    def update(self):
       if self.next_transition != VALID_STATES['QUIT']:
          if self.next_transition != VALID_STATES['STAY']:
             self.next_transition = VALID_STATES['STAY']

          if self.user_click:
             self.next_transition = VALID_STATES['SCORE']
             self.user_click = False

       return self.next_transition

    def render(self, canvas):
       self.background.draw(canvas)
       pygame.draw.rect(canvas, (255, 0, 255), self.rectangle)
