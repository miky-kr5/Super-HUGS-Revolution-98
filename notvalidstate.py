# Miguel Angel Astor Romero. Created on 7-1-2013. #
###################################################
import pygame

try:
   import android
except ImportError:
   android = None

from state import BaseState, VALID_STATES

class NotValidState(BaseState):
    def __init__(self):
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
        return self.next_transition

    def render(self, canvas):
        pygame.draw.rect(canvas, (0, 0, 0), self.rectangle)
