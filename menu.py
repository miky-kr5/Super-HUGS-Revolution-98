# -*- coding: latin-1 -*-
###########################################
# Created on 1-7-2013. Miguel Angel Astor #
###########################################
import pygame
try:
   import android
except ImportError:
   android = None

import database
import player
from constants import DEBUG
from imloader import cached_image_loader
from actor import BaseActor
from state import BaseState, VALID_STATES

MENUS = {'MAIN':0, 'SCORE':1, 'INTRO':2}

class MenuState(BaseState):
    def __init__(self):
       BaseState.__init__(self)

       self.next_transition = VALID_STATES['STAY']
       self.current_menu = MENUS['MAIN']
       self.story_time = 0
       self.story_timeout = 7000 # 7 seconds.
       self.then = 0
       
       self.cursor_x = 0
       self.cursor_y = 0
       
       self.background_color = (125, 158, 192)

       # Load main menu buttons.
       image = cached_image_loader.get_image_to_screen_percent('gfx/logo.png')
       self.logo = BaseActor(0, image, "SHR98 logo", False, True, False)
       self.logo.set_position([pygame.display.Info().current_w // 2, (image.get_height() // 2) + 20])

       image2 = cached_image_loader.get_image_to_screen_percent('gfx/boton_socre.png')
       self.scr_button = BaseActor(1, image2, "Score Button", False, True, False)
       self.scr_button.set_position([pygame.display.Info().current_w // 2,
                                     self.logo.get_position()[1] + (image.get_height()) + 20])

       image = cached_image_loader.get_image_to_screen_percent('gfx/boton_new.png')
       self.new_button = BaseActor(2, image, "New button", False, True, False)
       self.new_button.set_position([pygame.display.Info().current_w // 2 - 10 -image2.get_width(),
                                     self.scr_button.get_position()[1]])

       image = cached_image_loader.get_image_to_screen_percent('gfx/boton_salir.png')
       self.quit_button = BaseActor(3, image, "Quit button", False, True, False)
       self.quit_button.set_position([pygame.display.Info().current_w // 2 + 10 +image2.get_width(),
                                     self.scr_button.get_position()[1]])

       # Load score menu buttons.
       image = cached_image_loader.get_image_to_screen_percent('gfx/MenosMalos.png')
       self.scoreboard = BaseActor(4, image, "Scoreboard", False, True, False)
       self.scoreboard.set_position([(image.get_width() // 2) + 20, pygame.display.Info().current_h // 2])

       image2 = cached_image_loader.get_image_to_screen_percent('gfx/boton_back.png')
       self.back_button = BaseActor(5, image2, "Back button", False, True, False)
       self.back_button.set_position([self.scoreboard.get_position()[0] + image.get_width() - (image.get_width() // 10),
                                      pygame.display.Info().current_h // 2])
       
       font_size = 42
       screen_prop = (float(font_size) / 768.0)
       screen_fract = (float(pygame.display.Info().current_h) * screen_prop) / 768.0
       scale_factor = screen_fract / screen_prop
       self.font = pygame.font.Font('font/ProfaisalEliteRiqa/Profaisal-EliteRiqaV1.0.ttf', int(font_size * scale_factor))

       # Score labels.
       self.score_1 = None
       self.score_2 = None
       self.score_3 = None
       self.score_4 = None
       self.score_5 = None

       # Story labels.
       font_size = 22
       screen_prop = (float(font_size) / 768.0)
       screen_fract = (float(pygame.display.Info().current_h) * screen_prop) / 768.0
       scale_factor = screen_fract / screen_prop
       font_small = pygame.font.Font('font/ProfaisalEliteRiqa/Profaisal-EliteRiqaV1.0.ttf', int(font_size * scale_factor))

       self.story_1 = font_small.render("Este es Moncho, nuestro heroe...", True, (0, 0, 0))
       self.story_2 = font_small.render("Moncho ama a toda la gente, gente como esta...", True, (0, 0, 0))
       self.story_3 = font_small.render("Ama tanto a la gente que solo quiere abrazarlos...", True, (0, 0, 0))
       self.story_5 = font_small.render("Aunque, tal vez Moncho no ame a TODA la gente...", True, (0, 0, 0))

       font_size = 35
       screen_prop = (float(font_size) / 768.0)
       screen_fract = (float(pygame.display.Info().current_h) * screen_prop) / 768.0
       scale_factor = screen_fract / screen_prop
       font_big = pygame.font.Font('font/ProfaisalEliteRiqa/Profaisal-EliteRiqaV1.0.ttf', int(font_size * scale_factor))

       self.story_4 = font_big.render("¡¡¡ABRAZARLOS HASTA QUE EXPLOTEN!!!", True, (255, 0, 0))
       
       self.interrogation = font_big.render("?", True, (0, 0, 0))

       self.player_label_1 = cached_image_loader.get_image_to_screen_percent('gfx/Player/player_idle_front.png')
       self.player_label_2 = cached_image_loader.get_image_to_screen_percent('gfx/Player/player_idle_front_HUG.png')

       self.he_huggable_1 = cached_image_loader.get_image_to_screen_percent('gfx/HeHuggable/Idle_front.png')
       self.he_huggable_2 = cached_image_loader.get_image_to_screen_percent('gfx/HeHuggable/Walking_front_1_scared.png')

       self.she_huggable_1 = cached_image_loader.get_image_to_screen_percent('gfx/SheHuggable/Idle_front.png')
       self.she_huggable_2 = cached_image_loader.get_image_to_screen_percent('gfx/SheHuggable/Walking_front_2_scared.png')

       self.explosion = cached_image_loader.get_image_to_screen_percent('gfx/Explosion2.png')
       self.mystery_guy = cached_image_loader.get_image_to_screen_percent('gfx/ForeverAlone/Idle_Front_face_hidden.png')
       
       self.score_text_x = int(float(image.get_width()) * 0.183) + self.scoreboard.rect.left   # image holds the scoreboard graphic.
       self.score_text_1_y = int(float(image.get_height()) * 0.300) + self.scoreboard.rect.top
       self.score_text_inc = int(float(image.get_height()) * 0.112)

       self.story_1_x = int((float(pygame.display.Info().current_w) * 177.0 ) / 1024.0)
       self.story_1_y = int((float(pygame.display.Info().current_h) * 109.0 ) / 768.0)
       self.story_2_x = int((float(pygame.display.Info().current_w) * 211.0 ) / 1024.0)
       self.story_2_y = int((float(pygame.display.Info().current_h) * 223.0 ) / 768.0)
       self.story_3_x = int((float(pygame.display.Info().current_w) * 240.0 ) / 1024.0)
       self.story_3_y = int((float(pygame.display.Info().current_h) * 346.0 ) / 768.0)
       self.story_4_x = int((float(pygame.display.Info().current_w) * 38.0 ) / 1024.0)
       self.story_4_y = int((float(pygame.display.Info().current_h) * 517.0 ) / 768.0)
       self.story_5_x = int((float(pygame.display.Info().current_w) * 244.0 ) / 1024.0)
       self.story_5_y = int((float(pygame.display.Info().current_h) * 710.0 ) / 768.0)
       self.interr_x = int((float(pygame.display.Info().current_w) * 173.0 ) / 1024.0)
       self.interr_y = int((float(pygame.display.Info().current_h) * 650.0 ) / 768.0)

       self.moncho_1_x = int((float(pygame.display.Info().current_w) * 49.0 ) / 1024.0)
       self.moncho_1_y = int((float(pygame.display.Info().current_h) * 49.0 ) / 768.0)
       self.moncho_2_x = int((float(pygame.display.Info().current_w) * 98.0 ) / 1024.0)
       self.moncho_2_y = int((float(pygame.display.Info().current_h) * 293.0 ) / 768.0)
       self.hug_male_1_x = int((float(pygame.display.Info().current_w) * 834.0 ) / 1024.0)
       self.hug_male_1_y = int((float(pygame.display.Info().current_h) * 193.0 ) / 768.0)
       self.hug_male_2_x = int((float(pygame.display.Info().current_w) * 702.0 ) / 1024.0)
       self.hug_male_2_y = int((float(pygame.display.Info().current_h) * 495.0 ) / 768.0)
       self.hug_female_1_x = int((float(pygame.display.Info().current_w) * 738.0 ) / 1024.0)
       self.hug_female_1_y = int((float(pygame.display.Info().current_h) * 184.0 ) / 768.0)
       self.hug_female_2_x = int((float(pygame.display.Info().current_w) * 797.0 ) / 1024.0)
       self.hug_female_2_y = int((float(pygame.display.Info().current_h) * 457.0 ) / 768.0)
       self.explosion_x = int((float(pygame.display.Info().current_w) * 705.0 ) / 1024.0)
       self.explosion_y = int((float(pygame.display.Info().current_h) * 428.0 ) / 768.0)
       self.mystery_x = int((float(pygame.display.Info().current_w) * 117.0 ) / 1024.0)
       self.mystery_y = int((float(pygame.display.Info().current_h) * 706.0 ) / 768.0)

       self.user_click = False

    def reload_scores(self):
       # Reload the scores from the database.
       database.cursor.execute('SELECT * FROM score ORDER BY _id')
       rows = database.cursor.fetchall()
       rows = sorted(rows, key = lambda row: row[2], reverse = True)
       i = 1
       for row in rows:
          if i == 1:
             self.score_1 = self.font.render("1) " + row[1] + " . . . . . . . . . " + str(max(row[2], 0)), True, (0, 0, 0))
          elif i == 2:
             self.score_2 = self.font.render("2) " + row[1] + " . . . . . . . . . " + str(max(row[2], 0)), True, (0, 0, 0))
          elif i == 3:
             self.score_3 = self.font.render("3) " + row[1] + " . . . . . . . . . " + str(max(row[2], 0)), True, (0, 0, 0))
          elif i == 4:
             self.score_4 = self.font.render("4) " + row[1] + " . . . . . . . . . " + str(max(row[2], 0)), True, (0, 0, 0))
          else:
             self.score_5 = self.font.render("5) " + row[1] + " . . . . . . . . . " + str(max(row[2], 0)), True, (0, 0, 0))
          i += 1

    def input(self):
       for event in pygame.event.get():
          if android is not None:
             if android.check_pause():
                android.wait_for_resume()

          if event.type == pygame.KEYDOWN:
             if event.key == pygame.K_ESCAPE:
                self.next_transition = VALID_STATES['QUIT']
             if self.current_menu == MENUS['INTRO']:
                self.user_click = True
          if event.type == pygame.QUIT:
             self.next_transition = VALID_STATES['QUIT']

          # Catch the position of a mouse click (or tap).
          if event.type == pygame.MOUSEBUTTONDOWN:
             (self.cursor_x, self.cursor_y) = event.pos
             if self.current_menu == MENUS['INTRO']:
                self.user_click = True

    def update(self):
       if android is None:
          pygame.mouse.set_visible(True)

       player.PLAYERS[1].reset_score()

       if self.next_transition != VALID_STATES['QUIT']:
          if self.next_transition != VALID_STATES['STAY']:
             # Set next_transition to STAY if the game gets to this state from ScoreState.
             self.next_transition = VALID_STATES['STAY']
             # Reset the scores label to force a database reload.
             self.score_1 = None
             self.score_2 = None
             self.score_3 = None
             self.score_4 = None
             self.score_5 = None

          if self.current_menu == MENUS['MAIN']:
             # Check for mouse (tap) collisions with the main menu buttons.
             if self.quit_button.rect.collidepoint(self.cursor_x, self.cursor_y):
                # Collision with the quit button.
                self.next_transition = VALID_STATES['QUIT']
             elif self.scr_button.rect.collidepoint(self.cursor_x, self.cursor_y):
                # Collision with the high scores button.
                self.current_menu = MENUS['SCORE']
                self.reload_scores()
             elif self.new_button.rect.collidepoint(self.cursor_x, self.cursor_y):
                # Collision with the new game button.
                self.current_menu = MENUS['INTRO']
                self.then = pygame.time.get_ticks()

          elif self.current_menu == MENUS['SCORE']:
             # Check for mouse (tap) collisions with the high scores menu buttons.
             if self.back_button.rect.collidepoint(self.cursor_x, self.cursor_y):
                # Collision with the go back button.
                self.current_menu = MENUS['MAIN']

          elif self.current_menu == MENUS['INTRO']:
             # Wait for a timeout before going to the game.
             now = pygame.time.get_ticks()
             delta_t = now - self.then
             self.story_time += delta_t
             if self.user_click:
                # If the user taps or presses a key before the timeout, go to the game.
                self.user_click = False
                self.story_time = 0
                self.current_menu = MENUS['SCORE']
                self.next_transition = VALID_STATES['IN_GAME']
             elif self.story_time >= self.story_timeout:
                # After the timeout, reset the time counter and go to the game.
                self.story_time = 0
                self.current_menu = MENUS['SCORE']
                self.next_transition = VALID_STATES['IN_GAME']
             else:
                # Keep tracking time.
                self.then = now

       # Reset the mouse pointer.
       self.cursor_x = 0
       self.cursor_y = 0

       return self.next_transition

    def render(self, canvas):
       canvas.fill(self.background_color)
       
       if self.current_menu == MENUS['MAIN']:
          self.logo.draw(canvas)
          self.scr_button.draw(canvas)
          self.new_button.draw(canvas)
          self.quit_button.draw(canvas)

       elif self.current_menu == MENUS['SCORE']:
          self.scoreboard.draw(canvas)
          self.back_button.draw(canvas)
          
          if self.score_1 is None:
             self.reload_scores()

          rect = self.score_1.get_rect()
          rect.top = self.score_text_1_y
          rect.left = self.score_text_x
          canvas.blit(self.score_1, rect)

          rect = self.score_2.get_rect()
          rect.top = self.score_text_1_y + self.score_text_inc
          rect.left = self.score_text_x
          canvas.blit(self.score_2, rect)
 
          rect = self.score_3.get_rect()
          rect.top = self.score_text_1_y + (2 * self.score_text_inc)
          rect.left = self.score_text_x
          canvas.blit(self.score_3, rect)
          
          rect = self.score_4.get_rect()
          rect.top = self.score_text_1_y + (3 * self.score_text_inc)
          rect.left = self.score_text_x
          canvas.blit(self.score_4, rect)
 
          rect = self.score_5.get_rect()
          rect.top = self.score_text_1_y + (4 * self.score_text_inc)
          rect.left = self.score_text_x
          canvas.blit(self.score_5, rect)

       elif self.current_menu == MENUS['INTRO']:
          rect = self.story_1.get_rect()
          rect.top = self.story_1_y
          rect.left = self.story_1_x
          canvas.blit(self.story_1, rect)

          rect = self.story_2.get_rect()
          rect.top = self.story_2_y
          rect.left = self.story_2_x
          canvas.blit(self.story_2, rect)

          rect = self.story_3.get_rect()
          rect.top = self.story_3_y
          rect.left = self.story_3_x
          canvas.blit(self.story_3, rect)

          rect = self.story_4.get_rect()
          rect.top = self.story_4_y
          rect.left = self.story_4_x
          canvas.blit(self.story_4, rect)

          rect = self.story_5.get_rect()
          rect.top = self.story_5_y
          rect.left = self.story_5_x
          canvas.blit(self.story_5, rect)
          
          rect = self.player_label_1.get_rect()
          rect.top = self.moncho_1_y
          rect.left = self.moncho_1_x
          canvas.blit(self.player_label_1, rect)

          rect = self.player_label_2.get_rect()
          rect.top = self.moncho_2_y
          rect.left = self.moncho_2_x
          canvas.blit(self.player_label_2, rect)

          rect = self.she_huggable_1.get_rect()
          rect.top = self.hug_female_1_y
          rect.left = self.hug_female_1_x
          canvas.blit(self.she_huggable_1, rect)

          rect = self.he_huggable_1.get_rect()
          rect.top = self.hug_male_1_y
          rect.left = self.hug_male_1_x
          canvas.blit(self.he_huggable_1, rect)

          rect = self.explosion.get_rect()
          rect.top = self.explosion_y
          rect.left = self.explosion_x
          canvas.blit(self.explosion, rect)

          rect = self.she_huggable_2.get_rect()
          rect.top = self.hug_female_2_y
          rect.left = self.hug_female_2_x
          canvas.blit(self.she_huggable_2, rect)

          rect = self.he_huggable_2.get_rect()
          rect.top = self.hug_male_2_y
          rect.left = self.hug_male_2_x
          canvas.blit(self.he_huggable_2, rect)

          rect = self.mystery_guy.get_rect()
          rect.top = self.mystery_y
          rect.left = self.mystery_x
          canvas.blit(self.mystery_guy, rect)

          rect = self.interrogation.get_rect()
          rect.top = self.interr_y
          rect.left = self.interr_x
          canvas.blit(self.interrogation, rect)
