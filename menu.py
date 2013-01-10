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
       BaseState.__init__(self)

       self.count = 0
       screen_center = self.get_screen_center()
       self.rectangle = pygame.Rect(screen_center[0] - 50, screen_center[1] - 50, 100, 100)
       self.next_transition = VALID_STATES['STAY']

       # Load main menu buttons.

       # Load main menu labels.
       
       # Load score menu buttons.
       
       # Load score menu labels.
       
       # Load story screen sprites.

       # Add sound support.

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

          # Detect mouse clicks (taps)

    def update(self):
       # Check collisions with current buttons.
       
       # Switch submenu if able.
       # If switching to score submenu, load scores database.
       # If switching to story submenu, count time to leave.

       if self.next_transition != VALID_STATES['QUIT']:
          if self.count < 120:
             self.count += 1
             self.next_transition = VALID_STATES['STAY']
          else:
             self.count = 0
             self.next_transition = VALID_STATES['IN_GAME']
       return self.next_transition

    def render(self, canvas):
       # Draw the appropiate submenu.

       canvas.fill(self.background_color)
       pygame.draw.rect(canvas, (0, 255, 255), self.rectangle)
