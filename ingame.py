###########################################
# Created on 1-7-2013. Miguel Angel Astor #
###########################################
import math

import pygame
try:
   import android
except ImportError:
   android = None

import player
import background
import imloader
import actor
from state import BaseState, VALID_STATES

class InGameState(BaseState):
    def __init__(self):
       BaseState.__init__(self)

       self.background_color = (125, 158, 192)

       self.next_transition = VALID_STATES['STAY']
       self.cursor_x = 0
       self.cursor_y = 0
       self.user_click = False

       self.bckg_x = 0
       self.bckg_y = 0

       play_img = imloader.cached_image_loader.get_image_to_screen_percent('gfx/Player/player_idle_front.png')
       self.player = actor.BaseActor(0, play_img, "Player", False)

       # Create a surface for the background.
       bg_w = int(float(pygame.display.Info().current_w * 1280) / 1024.0)
       bg_h = int(float(pygame.display.Info().current_h * 1024) / 768.0)
       self.background = pygame.Surface((bg_w, bg_h))

       # Center the player.
       self.player.set_position([bg_w // 2, bg_h // 2])

       # Create the floor.
       floor = background.TiledBackground(bg_w, bg_h, 'gfx/piso.png')

       # Create the walls for the top and the bottom (the same for both).
       bg_h = int((80.0 * float(pygame.display.Info().current_h)) / 768.0)
       walls_top = background.TiledBackground(bg_w, bg_h, 'gfx/Pared.png')
       bg_y = 1024 - int((80.0 * float(pygame.display.Info().current_h)) / 768.0)

       # Create the left walls.
       bg_h = int(float(pygame.display.Info().current_h * 1024) / 768.0)
       walls_left = background.TiledBackground(-1, bg_h, 'gfx/Pared2.png')
       _y = int((80.0 * float(pygame.display.Info().current_h)) / 768.0)
       walls_left.set_position((0, _y))

       # Create the right walls.
       walls_right = background.TiledBackground(-1, bg_h, 'gfx/Pared3.png')
       _x = 1280 - int((40.0 * float(pygame.display.Info().current_w)) / 1024.0)
       walls_right.set_position((_x, _y))

       # Build the background image.
       floor.draw(self.background)
       walls_top.set_position((0, 0))
       walls_top.draw(self.background)
       walls_left.draw(self.background)
       walls_right.draw(self.background)
       walls_top.set_position((0, bg_y))
       walls_top.draw(self.background)

       # Center the view on the player
       p_pos = self.player.get_position()
       (dist_x, dist_y) = (math.fabs(self.screen_center[0] - p_pos[0]), math.fabs(self.screen_center[0] - p_pos[0]))
       self.bckg_x -= dist_x
       self.bckg_y -= dist_y

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

          # Reset the view.
          self.bckg_x = 0
          self.bckg_y = 0
          # Get the manhattan distance between the screen center and the player.
          p_pos = self.player.get_position()
          (dist_x, dist_y) = (math.fabs(self.screen_center[0] - p_pos[0]), math.fabs(self.screen_center[0] - p_pos[0]))
          # Center the view on the player.
          self.bckg_x -= dist_x
          self.bckg_y -= dist_y
          
          # Make sure the background is always inside the screen.
          if self.bckg_y > 0:
             self.bckg_y = 0
          if self.bckg_x > 0:
             self.bckg_x = 0
          if self.bckg_y + self.background.get_height() < pygame.display.Info().current_h:
             self.bckg_y += pygame.display.Info().current_h - (self.bckg_y + self.background.get_height())
          if self.bckg_x + self.background.get_width() < pygame.display.Info().current_w:
             self.bckg_x += pygame.display.Info().current_w - (self.bckg_x + self.background.get_width())

          #if self.user_click:
          #   self.next_transition = VALID_STATES['SCORE']
          #   self.user_click = False

       return self.next_transition

    def render(self, canvas):
       canvas.fill(self.background_color)
       
       # Blit everything to the bacground.
       self.player.draw(self.background)
       
       canvas.blit(self.background, (self.bckg_x, self.bckg_y))
