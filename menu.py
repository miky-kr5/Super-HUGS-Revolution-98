############################################
# Created on 1-7-2013. Miguel Angel Astor #
############################################
import pygame
try:
   import android
except ImportError:
   android = None

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
