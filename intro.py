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
import particle
import imloader
from constants import DEBUG

class IntroState(BaseState):
   def __init__(self):
      BaseState.__init__(self)

      self.count = 0
      self.next_transition = VALID_STATES['STAY']

      self.screen_vertical_half = pygame.display.Info().current_h / 3

      image = imloader.cached_image_loader.get_image_to_screen_percent('gfx/burbuja.png')
      image2 = imloader.cached_image_loader.get_image_to_screen_percent('gfx/submarino1.png')
      image4 = imloader.cached_image_loader.get_image_to_screen_percent('gfx/submarino2.png')
      image3 = imloader.cached_image_loader.get_image_to_screen_percent('gfx/oneoop.png')

      self.sine_movement = actor.BulletActor(0, image, "SineMovement", False, True, False)
      self.sine_movement.set_position([-(image2.get_width() / 2 + 10), pygame.display.Info().current_h / 4])
      # The next line calculates the horizontal velocity of sine_movement.
      # We want it to cover the width of the screen plus the width of the submarine sprite
      # in 20 seconds. We divide by 60 to obtain the speed in pixels per frame.
      x_velocity = (float(pygame.display.Info().current_w + image2.get_width()) / 26.0) / 60.0 
      self.sine_movement.set_velocity([x_velocity, 0])
      self.sine_movement.move()
      self.w_extra = int((305.0 * pygame.display.Info().current_w) / 1024.0)

      self.submarine = actor.BaseActor(1, image2, "Submarine", True, True, False)
      self.submarine.set_image_point_xy(int(float(image2.get_width()) * 0.195), int(float(image2.get_height()) * 0.835))
      self.submarine.set_fps(10)
      self.submarine.add_frame(image4)

      self.particle_system = particle.ParticleSystem(0, "Bubbles", 'gfx/burbuja.png', 1000, 1000, 3, -130.0)
      self.particle_system.set_friction(1.0)
      self.particle_system.set_gravity([0.0, -60.0])
      self.particle_system.set_max_velocity(5.0)
      self.particle_system.start()

      self.oneoop_logo = actor.BaseActor(2, image3, "1-Oop logo", False, True, False)
      self.oneoop_logo.set_position([10 + (image3.get_width() / 2),
                                     pygame.display.Info().current_h - 10 - (image3.get_height() / 2)])

      screen_prop = (25.0 / 768.0)
      screen_fract = (float(pygame.display.Info().current_h) * screen_prop) / 768.0
      scale_factor = screen_fract / screen_prop

      font = pygame.font.Font('font/PressStart2P/PressStart2P.ttf', int(25.0 * scale_factor))
      text_surf = font.render("1-OOP Presenta", True, (0, 0, 0))
      self.text = actor.BaseActor(2, text_surf, "Text", False, True, False)
      self.text.set_position([self.oneoop_logo.get_position()[0] + image3.get_width() + (text_surf.get_width() // 2) + 10,
                                     pygame.display.Info().current_h - 10 - (image3.get_height() / 2)])
      
      if game.DEBUG:
         print "Velocity: " + str(self.sine_movement.get_velocity())
         print "Position: " + str(self.sine_movement.get_position())
         print self.sine_movement.is_moving()

   def input(self):
      for event in pygame.event.get():
         if android is not None:
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
      self.submarine.set_position([sm_position[0], 
                                   self.screen_vertical_half + math.sin(0.05 * float(0.5 * sm_position[0])) * 42.0])
      self.particle_system.set_position(self.submarine.get_image_point(0))
      self.particle_system.update()

      if game.DEBUG:
         print
         print "OBJECT: " + self.sine_movement.get_name()
         print "Velocity: " + str(self.sine_movement.get_velocity())
         print "Position: " + str(self.sine_movement.get_position())
         print self.sine_movement.is_moving()

      if self.next_transition != VALID_STATES['QUIT']:
         sm_position = self.sine_movement.get_position()
         if sm_position[0] > pygame.display.Info().current_w + self.w_extra:
            self.next_transition = VALID_STATES['MENU']

      return self.next_transition
          
   def render(self, canvas):
      canvas.fill(self.background_color)
      self.oneoop_logo.draw(canvas)
      self.text.draw(canvas)
      self.submarine.draw(canvas)
      self.particle_system.draw(canvas)
