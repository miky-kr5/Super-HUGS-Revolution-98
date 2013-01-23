###########################################
# Created on 1-7-2013. Miguel Angel Astor #
###########################################
import math
import copy
import random

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

       random.seed(None)

       self.background_color = (125, 158, 192)

       self.next_transition = VALID_STATES['SCORE']
       self.cursor_x = 0
       self.cursor_y = 0
       self.user_click = False
       self.cancel = False

       self.time_left = 160
       self.then = pygame.time.get_ticks()
       self.wave = 0
       self.done = False
       self.max_npc = 15
       self.create_huggable = False
       self.change_angle = False

       self.bckg_x = 0
       self.bckg_y = 0

       self.explosions = set()
       self.npcs = set()

       play_img = imloader.cached_image_loader.get_image_to_screen_percent('gfx/Player/player_idle_front.png')
       self.player = actor.OmnidirectionalActor(0, play_img, "Player", True)
       self.player.set_fps(5)
       self.player.set_angle(math_utils.PI / 2.0)
       self.player.set_velocity([0, 0])

       self.spawners = set()
       for i in range(8):
          spawner = actor.BaseActor(40 + i + 1, None, "Spawner " + str(i))
          self.spawners.add(spawner)

       # Add idle frames to the player:
       play_img = imloader.cached_image_loader.get_image_to_screen_percent('gfx/Player/player_idle_side.png')
       self.player.add_idle_frame(play_img)
       play_img = imloader.cached_image_loader.get_image_to_screen_percent('gfx/Player/player_idle_front.png')
       self.player.add_idle_frame(play_img)
       play_img = imloader.cached_image_loader.get_image_to_screen_percent('gfx/Player/player_idle_side2.png')
       self.player.add_idle_frame(play_img)
       play_img = imloader.cached_image_loader.get_image_to_screen_percent('gfx/Player/player_idle_back.png')
       self.player.add_idle_frame(play_img)

       # Add moving frames to the player.
       play_img = imloader.cached_image_loader.get_image_to_screen_percent('gfx/Player/player_walk_side_HUG_1.png')
       self.player.add_moving_frame(play_img)
       play_img = imloader.cached_image_loader.get_image_to_screen_percent('gfx/Player/player_walk_side_HUG_2.png')
       self.player.add_moving_frame(play_img)
       play_img = imloader.cached_image_loader.get_image_to_screen_percent('gfx/Player/player_walk_HUG_front_1.png')
       self.player.add_moving_frame(play_img)
       play_img = imloader.cached_image_loader.get_image_to_screen_percent('gfx/Player/player_walk_HUG_front_2.png')
       self.player.add_moving_frame(play_img)
       play_img = imloader.cached_image_loader.get_image_to_screen_percent('gfx/Player/player_walk_side_HUG_1_flipped.png')
       self.player.add_moving_frame(play_img)
       play_img = imloader.cached_image_loader.get_image_to_screen_percent('gfx/Player/player_walk_side_HUG_2_flipped.png')
       self.player.add_moving_frame(play_img)
       play_img = imloader.cached_image_loader.get_image_to_screen_percent('gfx/Player/player_walk_back_HUG_1.png')
       self.player.add_moving_frame(play_img)
       play_img = imloader.cached_image_loader.get_image_to_screen_percent('gfx/Player/player_walk_back_HUG_2.png')
       self.player.add_moving_frame(play_img)

       # Create a surface for the background.
       bg_w = int(float(pygame.display.Info().current_w * 1315) / 1024.0)
       bg_h = int(float(pygame.display.Info().current_h * 1280) / 768.0)
       self.background = pygame.Surface((bg_w, bg_h))
       self.game_area = pygame.Surface((bg_w, bg_h))

       # Center the player.
       self.player.set_position([bg_w // 2, bg_h // 2])
       self.constraints = [int((95.0 * float(pygame.display.Info().current_w)) / 1024.0),
                           bg_w - int((95.0 * float(pygame.display.Info().current_w)) / 1024.0),
                           int((155.0 * float(pygame.display.Info().current_h)) / 768.0),
                           bg_h - int((155.0 * float(pygame.display.Info().current_h)) / 768.0)]

       # Place the spawners in position.
       positions = [(137, 181), (660, 181), (1190, 181), (1190, 662), (1190, 1155), (660, 1155), (137, 1155), (137, 662)]
       i = 0
       for spawner in self.spawners:
          spawner.set_position([(positions[i][0] * bg_w) / 1315, (positions[i][1] * bg_h) / 1280])
          i += 1
       
       # Create the floor.
       floor = background.TiledBackground(bg_w, bg_h, 'gfx/piso.png')

       # Create the walls for the top and the bottom (the same for both).
       bg_h = int((80.0 * float(pygame.display.Info().current_h)) / 768.0)
       walls_top = background.TiledBackground(bg_w, bg_h, 'gfx/Pared.png')
       bg_y = self.background.get_height() - int((80.0 * float(pygame.display.Info().current_h)) / 768.0)

       # Create the left walls.
       bg_h = int(float(pygame.display.Info().current_h * 1280) / 768.0)
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

       self.font = pygame.font.Font('font/ProfaisalEliteRiqa/Profaisal-EliteRiqaV1.0.ttf', 22)

       self.score_text = self.font.render("Puntos:   " + str(1000), True, (0, 0, 0))
       self.time_text = self.font.render("Tiempo:   " + str(190), True, (0, 0, 0))
       self.wave_text = self.font.render("Oleada:   " + str(999), True, (0, 0, 0))

       text_w = max(self.font.size("Puntos:   " + str(1000))[0], 
                    max(self.font.size("Tiempo:   " + str(190))[0], self.font.size("Oleada: " + str(999))[0])) + 10
       self.text_h = (3 * self.font.size("Puntos:   " + str(1000))[1]) + 20
       self.text_box = pygame.Surface((text_w, self.text_h))
       self.text_h = self.font.size("Puntos:   " + str(1000))[1]
       self.text_box.set_alpha(128 + 64 + 32)

       self.reticule = imloader.cached_image_loader.get_image_to_screen_percent('gfx/reticula.png')
       self.ret_rect = self.reticule.get_rect()
       self.ret_rect.center = self.screen_center

       self.scare_dist = (250 * pygame.display.Info().current_h) / 768

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

    def create_explosion(self, position):
       # Create a explosion object.
       expl_img = imloader.cached_image_loader.get_image_to_screen_percent('gfx/Explosion1.png')
       explosion = actor.BaseActor(1, expl_img, "Eplosion", True, True, False)
       explosion.set_fps(6)
       explosion.set_position(position)
       explosion.set_looping(False)

       # Add all it's frames.
       expl_img = imloader.cached_image_loader.get_image_to_screen_percent('gfx/Explosion2.png')
       explosion.add_frame(expl_img)
       expl_img = imloader.cached_image_loader.get_image_to_screen_percent('gfx/Explosion3.png')
       explosion.add_frame(expl_img)
       expl_img = imloader.cached_image_loader.get_image_to_screen_percent('gfx/Explosion4.png')
       explosion.add_frame(expl_img)
       expl_img = imloader.cached_image_loader.get_image_to_screen_percent('gfx/Explosion5.png')
       explosion.add_frame(expl_img)
       expl_img = imloader.cached_image_loader.get_image_to_screen_percent('gfx/Explosion6.png')
       explosion.add_frame(expl_img)
       expl_img = imloader.cached_image_loader.get_image_to_screen_percent('gfx/Explosion6.png')
       explosion.add_frame(expl_img)

       # Append it to the explosions set.
       self.explosions.add(explosion)

    def create_new_huggable(self, position):
       play_img = imloader.cached_image_loader.get_image_to_screen_percent('gfx/Player/player_idle_front.png')
       huggable = actor.OmnidirectionalActor(0, play_img, "Random Huggable", True)
       huggable.set_fps(5)
       huggable.set_angle(math_utils.ang_2_radians(float(random.randrange(-180, 180, 1))))
       huggable.set_velocity([0, 0])
       huggable.set_acceleration_fraction(0.35)
       huggable.set_position(position)
       huggable.set_constraints(self.constraints)
       huggable.set_rotate_on_constraint(True)
       huggable.move()

       gender = random.choice([0, 1])
       if gender == 0:
          # Create a male huggable.
          image = imloader.cached_image_loader.get_image_to_screen_percent('gfx/HeHuggable/Idle_side.png')
          huggable.add_idle_frame(image)
          image = imloader.cached_image_loader.get_image_to_screen_percent('gfx/HeHuggable/Idle_front.png')
          huggable.add_idle_frame(image)
          image = imloader.cached_image_loader.get_image_to_screen_percent('gfx/HeHuggable/Idle_side_flipped.png')
          huggable.add_idle_frame(image)
          image = imloader.cached_image_loader.get_image_to_screen_percent('gfx/HeHuggable/Idle_back.png')
          huggable.add_idle_frame(image)

          # Add moving frames.
          image = imloader.cached_image_loader.get_image_to_screen_percent('gfx/HeHuggable/Walking_side_1.png')
          huggable.add_moving_frame(image)
          image = imloader.cached_image_loader.get_image_to_screen_percent('gfx/HeHuggable/Walking_side_2.png')
          huggable.add_moving_frame(image)
          image = imloader.cached_image_loader.get_image_to_screen_percent('gfx/HeHuggable/Walking_front_1.png')
          huggable.add_moving_frame(image)
          image = imloader.cached_image_loader.get_image_to_screen_percent('gfx/HeHuggable/Walking_front_2.png')
          huggable.add_moving_frame(image)
          image = imloader.cached_image_loader.get_image_to_screen_percent('gfx/HeHuggable/Walking_side_1_flipped.png')
          huggable.add_moving_frame(image)
          image = imloader.cached_image_loader.get_image_to_screen_percent('gfx/HeHuggable/Walking_side_2_flipped.png')
          huggable.add_moving_frame(image)
          image = imloader.cached_image_loader.get_image_to_screen_percent('gfx/HeHuggable/Walking_back_1.png')
          huggable.add_moving_frame(image)
          image = imloader.cached_image_loader.get_image_to_screen_percent('gfx/HeHuggable/Walking_back_2.png')
          huggable.add_moving_frame(image)

          huggable.toggle_scared()
          # Add scared frames.
          image = imloader.cached_image_loader.get_image_to_screen_percent('gfx/HeHuggable/Walking_side_1_scared.png')
          huggable.add_moving_frame(image)
          image = imloader.cached_image_loader.get_image_to_screen_percent('gfx/HeHuggable/Walking_side_2_scared.png')
          huggable.add_moving_frame(image)
          image = imloader.cached_image_loader.get_image_to_screen_percent('gfx/HeHuggable/Walking_front_1_scared.png')
          huggable.add_moving_frame(image)
          image = imloader.cached_image_loader.get_image_to_screen_percent('gfx/HeHuggable/Walking_front_2_scared.png')
          huggable.add_moving_frame(image)
          image = imloader.cached_image_loader.get_image_to_screen_percent('gfx/HeHuggable/Walking_side_1_scared_flipped.png')
          huggable.add_moving_frame(image)
          image = imloader.cached_image_loader.get_image_to_screen_percent('gfx/HeHuggable/Walking_side_2_scared_flipped.png')
          huggable.add_moving_frame(image)
          image = imloader.cached_image_loader.get_image_to_screen_percent('gfx/HeHuggable/Walking_back_1.png')
          huggable.add_moving_frame(image)
          image = imloader.cached_image_loader.get_image_to_screen_percent('gfx/HeHuggable/Walking_back_2.png')
          huggable.add_moving_frame(image)

          huggable.toggle_scared()

       else:
          # Create a female huggable.
          image = imloader.cached_image_loader.get_image_to_screen_percent('gfx/SheHuggable/Idle_side.png')
          huggable.add_idle_frame(image)
          image = imloader.cached_image_loader.get_image_to_screen_percent('gfx/SheHuggable/Idle_front.png')
          huggable.add_idle_frame(image)
          image = imloader.cached_image_loader.get_image_to_screen_percent('gfx/SheHuggable/Idle_side_flipped.png')
          huggable.add_idle_frame(image)
          image = imloader.cached_image_loader.get_image_to_screen_percent('gfx/SheHuggable/Idle_back.png')
          huggable.add_idle_frame(image)

          # Add moving frames.
          image = imloader.cached_image_loader.get_image_to_screen_percent('gfx/SheHuggable/Walking_side_1.png')
          huggable.add_moving_frame(image)
          image = imloader.cached_image_loader.get_image_to_screen_percent('gfx/SheHuggable/Walking_side_2.png')
          huggable.add_moving_frame(image)
          image = imloader.cached_image_loader.get_image_to_screen_percent('gfx/SheHuggable/Walking_front_1.png')
          huggable.add_moving_frame(image)
          image = imloader.cached_image_loader.get_image_to_screen_percent('gfx/SheHuggable/Walking_front_2.png')
          huggable.add_moving_frame(image)
          image = imloader.cached_image_loader.get_image_to_screen_percent('gfx/SheHuggable/Walking_side_1_flipped.png')
          huggable.add_moving_frame(image)
          image = imloader.cached_image_loader.get_image_to_screen_percent('gfx/SheHuggable/Walking_side_2_flipped.png')
          huggable.add_moving_frame(image)
          image = imloader.cached_image_loader.get_image_to_screen_percent('gfx/SheHuggable/Walking_back_1.png')
          huggable.add_moving_frame(image)
          image = imloader.cached_image_loader.get_image_to_screen_percent('gfx/SheHuggable/Walking_back_2.png')
          huggable.add_moving_frame(image)
          
          huggable.toggle_scared()
          # Add scared frames.
          image = imloader.cached_image_loader.get_image_to_screen_percent('gfx/SheHuggable/Walking_side_1_scared.png')
          huggable.add_moving_frame(image)
          image = imloader.cached_image_loader.get_image_to_screen_percent('gfx/SheHuggable/Walking_side_2_scared.png')
          huggable.add_moving_frame(image)
          image = imloader.cached_image_loader.get_image_to_screen_percent('gfx/SheHuggable/Walking_front_1_scared.png')
          huggable.add_moving_frame(image)
          image = imloader.cached_image_loader.get_image_to_screen_percent('gfx/SheHuggable/Walking_front_2_scared.png')
          huggable.add_moving_frame(image)
          image = imloader.cached_image_loader.get_image_to_screen_percent('gfx/SheHuggable/Walking_side_1_scared_flipped.png')
          huggable.add_moving_frame(image)
          image = imloader.cached_image_loader.get_image_to_screen_percent('gfx/SheHuggable/Walking_side_2_scared_flipped.png')
          huggable.add_moving_frame(image)
          image = imloader.cached_image_loader.get_image_to_screen_percent('gfx/SheHuggable/Walking_back_1.png')
          huggable.add_moving_frame(image)
          image = imloader.cached_image_loader.get_image_to_screen_percent('gfx/SheHuggable/Walking_back_2.png')
          huggable.add_moving_frame(image)
          
          huggable.toggle_scared()

       self.npcs.add(huggable)
          
    def input(self):
       for event in pygame.event.get():
          if android:
             if android.check_pause():
                android.wait_for_resume()

          if event.type == pygame.KEYDOWN:
             if event.key == pygame.K_ESCAPE:
                self.cancel = True
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

          if event.type == pygame.USEREVENT + 1:
             self.create_huggable = True

          if event.type == pygame.USEREVENT + 2:
             self.change_angle = True

    def update(self):
       if self.next_transition != VALID_STATES['QUIT']:
          if self.next_transition != VALID_STATES['STAY']:
             self.next_transition = VALID_STATES['STAY']
             self.player.reset_then()
             self.then = pygame.time.get_ticks()
             # Start the huggable creation timer.
             pygame.time.set_timer(pygame.USEREVENT + 1, 1000)
             # Start the huggable angle change event.
             pygame.time.set_timer(pygame.USEREVENT + 2, 2000)

          if self.cancel and self.time_left > 0:
             # If the player pressed escape, force a timeout.
             self.time_left = 0

          now = pygame.time.get_ticks()
          delta_t = now - self.then
          if delta_t >= 1000:
             self.time_left -= delta_t // 1000
             self.then = now

          if self.time_left <= 0 and player.PLAYERS[1].is_alive():
             player.PLAYERS[1].kill()
             self.done = True
             self.create_explosion(self.player.get_position())

          if not self.done:
             if self.cursor_x != self.screen_center[0] or self.cursor_y != self.screen_center[1]:
                vec_2 = (float(self.cursor_x) - float(self.screen_center[0]), float(self.cursor_y) - float(self.screen_center[1]))
                vec_2 = math_utils.normalize_vector_2D(vec_2)
                self.player.set_angle(math_utils.angle_vectors_2D(self.vec_1, vec_2))

             self.player.update()
             self.recenter_view()

             # Create new huggables.
             if self.create_huggable:
                for spawner in self.spawners:
                   if len(self.npcs) >= self.max_npc:
                      # If we reached the maximum number of npcs, cancel the timer and ignore the rest of the spawners.
                      pygame.time.set_timer(pygame.USEREVENT + 1, 0)
                      break
                   else:
                      chance = random.randrange(100)
                      if chance < 20:
                         self.create_new_huggable(spawner.get_position())
                         self.create_explosion(spawner.get_position())
                self.create_huggable = False

             if self.change_angle:
                for npc in self.npcs:
                   npc.set_angle(math_utils.ang_2_radians(float(random.randrange(-180, 180, 1))))
                self.change_angle = False

             removal = set()
             for npc in self.npcs:
                # Check if the npc must run away from the player.
                if math_utils.distance_2D(self.player.get_position(), npc.get_position()) < self.scare_dist:
                   if not npc.is_scared():
                      npc.toggle_scared()
                   
                      npc.set_velocity([0, 0])

                   # Move in the opposite direction of the player.
                   n_pos = npc.get_position()
                   p_pos = self.player.get_position()
                   vec_2 = (float(n_pos[0] - p_pos[0]), float(n_pos[1] - p_pos[1]))
                   vec_2 = math_utils.normalize_vector_2D(vec_2)
                   npc.set_angle(math_utils.angle_vectors_2D(self.vec_1, vec_2))
                else:
                   if npc.is_scared():
                      npc.toggle_scared()

                npc.update()

                # Detect collisions with the player.
                if self.player.is_moving() and npc.test_collision_with_actor(self.player):
                   npc.make_invisible()
                   self.create_explosion(npc.get_position())
                   player.PLAYERS[1].inc_score_by_one()

                # If the npc exploded this turn, remove it.
                if not npc.is_visible():
                   removal.add(npc)

             if len(removal) > 0 and len(self.npcs) >= self.max_npc:
                # If npcs dissapeared this cycle restart the timer.
                pygame.time.set_timer(pygame.USEREVENT + 1, 1000)

             self.npcs.difference_update(removal)
             
             if player.PLAYERS[1].get_score() > 0 and player.PLAYERS[1].get_score() % 25 == 0:
                self.wave += 1
                player.PLAYERS[1].inc_score_by_one()

          elif self.time_left < -3:
             # Reset everything.
             self.time_left = 190
             self.wave = 0
             self.user_click = False
             self.done = False

             # Reset the player.
             self.player.set_angle(90)
             self.player.set_velocity([0, 0])
             self.player.stop()
             bg_w = int(float(pygame.display.Info().current_w * 1280) / 1024.0)
             bg_h = int(float(pygame.display.Info().current_h * 1024) / 768.0)
             self.player.set_position([bg_w // 2, bg_h // 2])

             # TODO: Destroy all NPC's.
             self.explosions.clear()
             self.npcs.clear()

             player.PLAYERS[1].revive()
             if not self.cancel:
                # Register scores only if the game ended cleanly.
                self.next_transition = VALID_STATES['SCORE']
             else:
                self.next_transition = VALID_STATES['MENU']

             # Stop the huggable creation timer.
             pygame.time.set_timer(pygame.USEREVENT + 1, 0)
             pygame.time.set_timer(pygame.USEREVENT + 2, 0)

             self.cancel = False

       # Remove finished explosions
       removal = set()
       for explosion in self.explosions:
          if explosion.get_current_frame() == 6:
             removal.add(explosion)
       self.explosions.difference_update(removal)

       self.score_text = self.font.render("Puntos:   " + str(player.PLAYERS[1].get_score()), True, (0, 0, 0))
       if self.time_left > 30:
          self.time_text = self.font.render("Tiempo:   " + str(self.time_left), True, (0, 0, 0))
       else:
          self.time_text = self.font.render("Tiempo:   " + str(max(self.time_left, 0)), True, (255, 0, 0))
       self.wave_text = self.font.render("Oleada:   " + str(self.wave), True, (0, 0, 0))

       self.cursor_x = self.screen_center[0]
       self.cursor_y = self.screen_center[1]

       return self.next_transition

    def render(self, canvas):
       #canvas.fill(self.background_color)
       self.game_area.blit(self.background, (0, 0))

       # Blit everything to the bacground.
       # Sort npcs by Y coordinate and draw.
       # The idea is to draw npcs near the bottom edge of the screen last.
       #npc_list = list(self.npcs)
       #if player.PLAYERS[1].is_alive():
       #   npc_list.append(self.player)
       #sorted(npc_list, key = lambda npc: npc.get_position()[1])
       #for npc in npc_list:
       #   npc.draw(self.game_area)
       for npc in self.npcs:
          npc.draw(self.game_area)

       if player.PLAYERS[1].is_alive():
          self.player.draw(self.game_area)

       # Same idea here.
       #expl_list = list(self.explosions)
       #sorted(expl_list, key = lambda explosion: explosion.get_position()[1])
       #for explosion in expl_list:
       #   explosion.draw(self.game_area)
       for explosion in self.explosions:
          explosion.draw(self.game_area)

       self.text_box.fill((128, 128, 128))
       self.text_box.blit(self.score_text, (5, 5))
       self.text_box.blit(self.time_text, (5, 10 + self.text_h))
       self.text_box.blit(self.wave_text, (5, 15 + (2 * self.text_h)))

       canvas.blit(self.game_area, (self.bckg_x, self.bckg_y))
       canvas.blit(self.text_box, (5, 5))
       canvas.blit(self.reticule, self.ret_rect)
