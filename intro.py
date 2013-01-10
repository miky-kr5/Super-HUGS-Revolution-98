###########################################
# Created on 1-7-2013. Miguel Angel Astor #
###########################################
import math

import pygame

try:
   import android
except ImportError:
   android = None

from state import BaseState, VALID_STATES
import actor
import game

class IntroState(BaseState):
   def __init__(self):
      BaseState.__init__(self)

      self.count = 0
      self.next_transition = VALID_STATES['STAY']

      self.screen_vertical_half = pygame.display.Info().current_h / 2

      image = pygame.image.load('gfx/burbuja.png')
      self.sine_movement = actor.BulletActor(0, image, "SineMovement", False, True, False)
      self.sine_movement.set_position([-300, pygame.display.Info().current_h / 2])
      # The next line calculates the horizontal velocity of sine_movement.
      # We want it to cover the width of the screen plus the width of the submarine sprite
      # in 20 seconds. We divide by 60 to obtain the speed in pixels per frame.
      x_velocity = (float(pygame.display.Info().current_w + 600) / 20.0) / 60.0 
      self.sine_movement.set_velocity([0.5, 0])
      self.sine_movement.move()

      image2 = pygame.image.load('gfx/submarino1.png')
      self.submarine = actor.BaseActor(1, image2, "Submarine", True, True, False)
      self.submarine.set_image_point_tuple((117, 284))
      # Instert second animation frame of the subamrine.

      # Create the particle system.
      
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
            else:
               self.next_transition = VALID_STATES['MENU']
         if event.type == pygame.QUIT:
            self.next_transition = VALID_STATES['QUIT']

         if event.type == pygame.MOUSEBUTTONDOWN:
            self.next_transition = VALID_STATES['MENU']

   def update(self):
      self.sine_movement.update()
      sm_position = self.sine_movement.get_position()
      self.submarine.set_position([sm_position[0], self.screen_vertical_half + math.sin(0.05 * float(sm_position[0])) * 42.0])

      if game.DEBUG:
         print
         print "OBJECT: " + self.sine_movement.get_name()
         print "Velocity: " + str(self.sine_movement.get_velocity())
         print "Position: " + str(self.sine_movement.get_position())
         print self.sine_movement.is_moving()

      if self.next_transition != VALID_STATES['QUIT']:
         sm_position = self.sine_movement.get_position()
         if sm_position[0] > pygame.display.Info().current_w + 300:
            self.next_transition = VALID_STATES['MENU']

      return self.next_transition
          
   def render(self, canvas):
      canvas.fill(self.background_color)
      self.submarine.draw(canvas)
