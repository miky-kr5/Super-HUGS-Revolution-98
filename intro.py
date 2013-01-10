###########################################
# Created on 1-7-2013. Miguel Angel Astor #
###########################################
import pygame

try:
   import android
except ImportError:
   android = None

from state import BaseState, VALID_STATES
from actor import BulletActor
import game

class IntroState(BaseState):
   def __init__(self):
      self.count = 0
      screen_center = self.get_screen_center()
      self.rectangle = pygame.Rect(screen_center[0] - 50, screen_center[1] - 50, 100, 100)
      self.next_transition = VALID_STATES['STAY']
      self.background_color = (139, 210, 228)

      image = pygame.image.load('gfx/burbuja.png')
      self.sine_movement = BulletActor(0, image, "SineMovement", False, True, False)
      self.sine_movement.set_position([-20, pygame.display.Info().current_h / 2])
      # The next line calculates the horizontal velocity of sine_movement.
      # We want it to cover the width of the screen in 20 seconds. We divide
      # by 60 to obtain the speed in pixels per frame.
      x_velocity = (float(pygame.display.Info().current_w) / 20.0) / 60.0 
      self.sine_movement.set_velocity([0.5, 0])
      self.sine_movement.move()
      
      if game.DEBUG:
         print "Velocity: " + str(self.sine_movement.get_velocity())
         print "Position: " + str(self.sine_movement.get_position())
         print self.sine_movement.is_moving()

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
      self.sine_movement.update()
      if game.DEBUG:
         print
         print "NEXT UPDATE"
         print "Velocity: " + str(self.sine_movement.get_velocity())
         print "Position: " + str(self.sine_movement.get_position())
         print self.sine_movement.is_moving()
      if self.next_transition != VALID_STATES['QUIT']:
         sm_position = self.sine_movement.get_position()
         if sm_position[0] >  pygame.display.Info().current_w + 30:
            self.next_transition = VALID_STATES['MENU']
         else:
            self.next_transition = VALID_STATES['STAY']
      return self.next_transition
          
   def render(self, canvas):
      canvas.fill(self.background_color)
      canvas.blit(self.sine_movement.image, self.sine_movement.rect)
