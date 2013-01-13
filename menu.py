###########################################
# Created on 1-7-2013. Miguel Angel Astor #
###########################################
# Update score database:
# UPDATE score SET player_name = ?, score = ? WHERE _id IN (SELECT _id FROM score WHERE score IN (SELECT MIN(score) FROM score))
import pygame
try:
   import android
except ImportError:
   android = None

import database
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
       self.intro_time = 0
       self.intro_max_time = 5000 # Miliseconds.
       self.then = 0
       
       self.cursor_x = 0
       self.cursor_y = 0

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
       
       screen_prop = (42.0 / 768.0)
       screen_fract = (float(pygame.display.Info().current_h) * screen_prop) / 768.0
       scale_factor = screen_fract / screen_prop

       self.font = pygame.font.Font('font/ProfaisalEliteRiqa/Profaisal-EliteRiqaV1.0.ttf', int(42.0 * scale_factor))
       self.score_1 = None
       self.score_2 = None
       self.score_3 = None
       self.score_4 = None
       self.score_5 = None
       
       self.score_text_x = int(float(image.get_width()) * 0.183) + self.scoreboard.rect.left
       self.score_text_1_y = int(float(image.get_height()) * 0.300) + self.scoreboard.rect.top
       self.score_text_inc = int(float(image.get_height()) * 0.112)

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

          # Catch the position of a mouse click (or tap).
          if event.type == pygame.MOUSEBUTTONDOWN:
             (self.cursor_x, self.cursor_y) = event.pos

    def update(self):
       if android is None:
          pygame.mouse.set_visible(True)

       if self.next_transition != VALID_STATES['QUIT']:
          if self.current_menu == MENUS['MAIN']:
             if self.quit_button.rect.collidepoint(self.cursor_x, self.cursor_y):
                self.next_transition = VALID_STATES['QUIT']

             elif self.scr_button.rect.collidepoint(self.cursor_x, self.cursor_y):
                self.current_menu = MENUS['SCORE']
                # Reload the scores from the database.
                for row in database.scores.execute('SELECT * FROM score ORDER BY _id'):
                   if row[0] == 1:
                      self.score_1 = self.font.render("1) " + row[1] + " . . . . . . . . . " + str(max(row[2], 0)), True, (0, 0, 0))
                   elif row[0] == 2:
                      self.score_2 = self.font.render("2) " + row[1] + " . . . . . . . . . " + str(max(row[2], 0)), True, (0, 0, 0))
                   elif row[0] == 3:
                      self.score_3 = self.font.render("3) " + row[1] + " . . . . . . . . . " + str(max(row[2], 0)), True, (0, 0, 0))
                   elif row[0] == 4:
                      self.score_4 = self.font.render("4) " + row[1] + " . . . . . . . . . " + str(max(row[2], 0)), True, (0, 0, 0))
                   else:
                      self.score_5 = self.font.render("5) " + row[1] + " . . . . . . . . . " + str(max(row[2], 0)), True, (0, 0, 0))

             elif self.new_button.rect.collidepoint(self.cursor_x, self.cursor_y):
                self.current_menu = MENUS['INTRO']

          elif self.current_menu == MENUS['SCORE']:
             if self.back_button.rect.collidepoint(self.cursor_x, self.cursor_y):
                self.current_menu = MENUS['MAIN']

          elif self.current_menu == MENUS['INTRO']:
             pass

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

          if self.score_1 is not None:
             rect = self.score_1.get_rect()
             rect.top = self.score_text_1_y
             rect.left = self.score_text_x
             canvas.blit(self.score_1, rect)
          if self.score_2 is not None:
             rect = self.score_2.get_rect()
             rect.top = self.score_text_1_y + self.score_text_inc
             rect.left = self.score_text_x
             canvas.blit(self.score_2, rect)
          if self.score_3 is not None:
             rect = self.score_3.get_rect()
             rect.top = self.score_text_1_y + (2 * self.score_text_inc)
             rect.left = self.score_text_x
             canvas.blit(self.score_3, rect)
          if self.score_4 is not None:
             rect = self.score_4.get_rect()
             rect.top = self.score_text_1_y + (3 * self.score_text_inc)
             rect.left = self.score_text_x
             canvas.blit(self.score_4, rect)
          if self.score_5 is not None:
             rect = self.score_5.get_rect()
             rect.top = self.score_text_1_y + (4 * self.score_text_inc)
             rect.left = self.score_text_x
             canvas.blit(self.score_5, rect)
