###########################################
# Created on 1-7-2013. Miguel Angel Astor #
###########################################
import pygame

try:
   import android
except ImportError:
   android = None

import player
from state import BaseState, VALID_STATES

class InGameState(BaseState):
    def __init__(self):
       BaseState.__init__(self)

       self.count = 0
       screen_center = self.get_screen_center()
       self.rectangle = pygame.Rect(screen_center[0] - 50, screen_center[1] - 50, 100, 100)
       self.next_transition = VALID_STATES['STAY']

    def input(self):
       for event in pygame.event.get():
          if android:
             if android.check_pause():
                android.wait_for_resume()

          if event.type == pygame.KEYDOWN:
             if event.key == pygame.K_ESCAPE:
                self.next_transition = VALID_STATES['QUIT']
          if event.type == pygame.QUIT:
             self.next_transition = VALID_STATES['QUIT']

    def update(self):
       if self.next_transition != VALID_STATES['QUIT']:
          if self.count < 120:
             self.count += 1
             self.next_transition = VALID_STATES['STAY']
          else:
             self.count = 0
             self.next_transition = VALID_STATES['SCORE']
       return self.next_transition

    def render(self, canvas):
       canvas.fill(self.background_color)
       pygame.draw.rect(canvas, (255, 0, 255), self.rectangle)
