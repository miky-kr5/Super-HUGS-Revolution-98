# Miguel Angel Astor Romero. Created on 7-1-2013. #
###################################################
import pygame

try:
   import android
except ImportError:
   android = None

from state import BaseState, VALID_STATES

class MenuState(BaseState):
    def __init__(self):
        self.count = 0
        self.rectangle = pygame.Rect(250, 350, 100, 100)
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
                self.next_transition = VALID_STATES['IN_GAME']
        return self.next_transition

    def render(self, canvas):
        pygame.draw.rect(canvas, (0, 255, 255), self.rectangle)
