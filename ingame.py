###########################################
# Created on 1-7-2013. Miguel Angel Astor #
###########################################
import math

import pygame
try:
   import android
except ImportError:
   android = None

import math_utils
import player
import background
import imloader
import actor
from state import BaseState, VALID_STATES

class InGameState(BaseState):
    def __init__(self):
       BaseState.__init__(self)

       self.background_color = (125, 158, 192)

       self.next_transition = VALID_STATES['SCORE']
       self.cursor_x = 0
       self.cursor_y = 0
       self.user_click = False

       self.time_left = 190
       self.then = pygame.time.get_ticks()
       self.wave = 0
       self.done = False

       self.bckg_x = 0
       self.bckg_y = 0

       play_img = imloader.cached_image_loader.get_image_to_screen_percent('gfx/Player/player_idle_front.png')
       self.player = actor.OmnidirectionalActor(0, play_img, "Player", False)
       self.player.set_angle(90)
       self.player.set_velocity([0, 0])

       # Create a surface for the background.
       bg_w = int(float(pygame.display.Info().current_w * 1280) / 1024.0)
       bg_h = int(float(pygame.display.Info().current_h * 1024) / 768.0)
       self.background = pygame.Surface((bg_w, bg_h))
       self.game_area = pygame.Surface((bg_w, bg_h))

       # Center the player.
       self.player.set_position([bg_w // 2, bg_h // 2])
       self.constraints = [int((95.0 * float(pygame.display.Info().current_w)) / 1024.0),
                           bg_w - int((95.0 * float(pygame.display.Info().current_w)) / 1024.0),
                           int((155.0 * float(pygame.display.Info().current_h)) / 768.0),
                           bg_h - int((155.0 * float(pygame.display.Info().current_h)) / 768.0)]

       # Create the floor.
       floor = background.TiledBackground(bg_w, bg_h, 'gfx/piso.png')

       # Create the walls for the top and the bottom (the same for both).
       bg_h = int((80.0 * float(pygame.display.Info().current_h)) / 768.0)
       walls_top = background.TiledBackground(bg_w, bg_h, 'gfx/Pared.png')
       bg_y = self.background.get_height() - int((80.0 * float(pygame.display.Info().current_h)) / 768.0)

       # Create the left walls.
       bg_h = int(float(pygame.display.Info().current_h * 1024) / 768.0)
       walls_left = background.TiledBackground(-1, bg_h, 'gfx/Pared2.png')
       _y = int((80.0 * float(pygame.display.Info().current_h)) / 768.0)
       walls_left.set_position((0, _y))

       # Create the right walls.
       walls_right = background.TiledBackground(-1, bg_h, 'gfx/Pared3.png')
       _x = self.background.get_width() - int((40.0 * float(pygame.display.Info().current_w)) / 1024.0)
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
       (dist_x, dist_y) = (math.fabs(self.screen_center[0] - p_pos[0]), math.fabs(self.screen_center[1] - p_pos[1]))
       self.bckg_x -= dist_x
       self.bckg_y -= dist_y
                      
       self.player.set_constraints(self.constraints)

       self.cursor_x = self.screen_center[0]
       self.cursor_y = self.screen_center[1]
       self.vec_1 = (float(pygame.display.Info().current_w) - float(self.screen_center[0]), 0.0)
       self.vec_1 = math_utils.normalize_vector_2D(self.vec_1)

       font_size = 22
       screen_prop = (float(font_size) / 768.0)
       screen_fract = (float(pygame.display.Info().current_h) * screen_prop) / 768.0
       scale_factor = screen_fract / screen_prop
       self.font = pygame.font.Font('font/ProfaisalEliteRiqa/Profaisal-EliteRiqaV1.0.ttf', int(font_size * scale_factor))

       self.score_text = self.font.render("Puntos:   " + str(1000), True, (0, 0, 0))
       self.time_text = self.font.render("Tiempo:   " + str(190), True, (0, 0, 0))
       self.wave_text = self.font.render("Oleada:   " + str(999), True, (0, 0, 0))

       text_w = max(self.font.size("Puntos:   " + str(1000))[0], 
                    max(self.font.size("Tiempo:   " + str(190))[0], self.font.size("Oleada: " + str(999))[0])) + 10
       self.text_h = (3 * self.font.size("Puntos:   " + str(1000))[1]) + 20
       self.text_box = pygame.Surface((text_w, self.text_h))
       self.text_h = self.font.size("Puntos:   " + str(1000))[1]
       self.text_box.set_alpha(128 + 64 + 32)

    def recenter_view(self):
       # Reset the view.
       self.bckg_x = 0
       self.bckg_y = 0
       # Get the manhattan distance between the screen center and the player.
       p_pos = self.player.get_position()
       (dist_x, dist_y) = (self.screen_center[0] - p_pos[0], self.screen_center[1] - p_pos[1])
       # Center the view on the player.
       self.bckg_x += dist_x
       self.bckg_y += dist_y
          
       # Make sure the background is always inside the screen.
       if self.bckg_y > 0:
          self.bckg_y = 0
       if self.bckg_x > 0:
          self.bckg_x = 0
       if self.bckg_y + self.background.get_height() < pygame.display.Info().current_h:
          self.bckg_y += pygame.display.Info().current_h - (self.bckg_y + self.background.get_height())
       if self.bckg_x + self.background.get_width() < pygame.display.Info().current_w:
          self.bckg_x += pygame.display.Info().current_w - (self.bckg_x + self.background.get_width())

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

          if event.type == pygame.MOUSEBUTTONDOWN:
             self.user_click = True
             self.player.move()

          if event.type == pygame.MOUSEBUTTONUP:
             self.user_click = False
             self.player.stop()

          if self.user_click:
             (self.cursor_x, self.cursor_y) = pygame.mouse.get_pos()

    def update(self):
       if self.next_transition != VALID_STATES['QUIT']:
          if self.next_transition != VALID_STATES['STAY']:
             self.next_transition = VALID_STATES['STAY']
             self.player.reset_then()
             self.then = pygame.time.get_ticks()

          self.done = not player.PLAYERS[1].is_alive()

          now = pygame.time.get_ticks()
          delta_t = now - self.then
          if delta_t >= 1000:
             self.time_left -= delta_t // 1000
             self.then = now
             if self.time_left <= 0:
                player.PLAYERS[1].kill()

          if not self.done:
             if self.cursor_x != self.screen_center[0] or self.cursor_y != self.screen_center[1]:
                #p_pos = self.player.get_position()
                #(dist_x, dist_y) = (self.screen_center[0] - p_pos[0], self.screen_center[1] - p_pos[1])
                #self.cursor_x += dist_x
                #self.cursor_y += dist_y
                #vec_2 = (float(self.cursor_x) - float(p_pos[0]), float(self.cursor_y) - float(p_pos[1]))
                vec_2 = (float(self.cursor_x) - float(self.screen_center[0]), float(self.cursor_y) - float(self.screen_center[1]))
                vec_2 = math_utils.normalize_vector_2D(vec_2)
                self.player.set_angle(math_utils.angle_vectors_2D(self.vec_1, vec_2))

                self.player.update()

                self.score_text = self.font.render("Puntos:   " + str(player.PLAYERS[1].get_score()), True, (0, 0, 0))
                if self.time_left > 30:
                   self.time_text = self.font.render("Tiempo:   " + str(self.time_left), True, (0, 0, 0))
                else:
                   self.time_text = self.font.render("Tiempo:   " + str(max(self.time_left, 0)), True, (255, 0, 0))
                self.wave_text = self.font.render("Oleada:   " + str(self.wave), True, (0, 0, 0))

             self.recenter_view()

          elif self.time_left < -3:
             self.time_left = 190
             self.wave = 0
             self.player.set_angle(90)
             self.player.set_velocity([0, 0])
             self.user_click = False
             self.done = False
             self.player.stop()
             bg_w = int(float(pygame.display.Info().current_w * 1280) / 1024.0)
             bg_h = int(float(pygame.display.Info().current_h * 1024) / 768.0)
             self.player.set_position([bg_w // 2, bg_h // 2])
             player.PLAYERS[1].revive()
             self.next_transition = VALID_STATES['SCORE']

       self.cursor_x = self.screen_center[0]
       self.cursor_y = self.screen_center[1]

       return self.next_transition

    def render(self, canvas):
       #canvas.fill(self.background_color)
       self.game_area.blit(self.background, (0, 0))
       
       # Blit everything to the bacground.
       if player.PLAYERS[1].is_alive():
          self.player.draw(self.game_area)

       self.text_box.fill((128, 128, 128))
       self.text_box.blit(self.score_text, (5, 5))
       self.text_box.blit(self.time_text, (5, 10 + self.text_h))
       self.text_box.blit(self.wave_text, (5, 15 + (2 * self.text_h)))

       canvas.blit(self.game_area, (self.bckg_x, self.bckg_y))
       canvas.blit(self.text_box, (5, 5))
