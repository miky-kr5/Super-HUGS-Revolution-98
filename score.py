###########################################
# Created on 1-7-2013. Miguel Angel Astor #
###########################################
import string

import pygame
try:
   import android
except ImportError:
   android = None

import player
import database
from constants import DEBUG
from imloader import cached_image_loader
from actor import BaseActor
from state import BaseState, VALID_STATES

class ScoreState(BaseState):
    def __init__(self):
       BaseState.__init__(self)

       self.background_color = (125, 158, 192)
       self.next_transition = VALID_STATES['STAY']
       self.cursor_x = 0
       self.cursor_y = 0

       self.letter_index = 0 # Tells how many letters the user has clicked.
       self.player_init = [] # Holds the player initials.

       image = cached_image_loader.get_image_to_screen_percent('gfx/iniciales.png')
       self.banner = BaseActor(0, image, "Banner", False, True, False)
       self.banner.set_position([pygame.display.Info().current_w // 2, (image.get_height() // 2) + 20])

       image2 = cached_image_loader.get_image_to_screen_percent('gfx/Fuente/_.png')
       self.underscore_c = BaseActor(1, image2, "Underscore center", False, True, False)
       self.underscore_c.set_position([pygame.display.Info().current_w // 2,
                                       self.banner.get_position()[1] + image.get_height() + 25])
       self.underscore_l = BaseActor(2, image2, "Underscore left", False, True, False)
       self.underscore_l.set_position([self.underscore_c.get_position()[0] - image2.get_width(),
                                       self.underscore_c.get_position()[1]])
       self.underscore_r = BaseActor(3, image2, "Underscore right", False, True, False)
       self.underscore_r.set_position([self.underscore_c.get_position()[0] + image2.get_width(),
                                       self.underscore_c.get_position()[1]])

       image = cached_image_loader.get_image_to_screen_percent('gfx/del.png')
       self.del_button = BaseActor(4, image, "Delete button", False, True, False)
       self.del_button.set_position([self.underscore_c.get_position()[0] + (2 * image2.get_width()),
                                     self.underscore_c.get_position()[1]])

       image = cached_image_loader.get_image_to_screen_percent('gfx/listo.png')
       self.done_button = BaseActor(5, image, "Done button", False, False, False)
       self.done_button.set_position([self.underscore_c.get_position()[0] + (3 * image2.get_width()),
                                     self.underscore_c.get_position()[1]])

       self.letters = {}

       letter_list = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h',
                      'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm']
       q_x_position = int((float(pygame.display.Info().current_w) * 88.0 ) / 1024.0)
       q_y_position = int((float(pygame.display.Info().current_h) * 438.0 ) / 768.0)
       letter_sep = int((float(pygame.display.Info().current_w) * 10.0 ) / 1024.0)
       for l in letter_list:
          image = cached_image_loader.get_image_to_screen_percent('gfx/Fuente/' + l + '.png')
          letter_actor = BaseActor(89, image, string.upper(l), False, True, False)
          if l == 'a':
             q_x_position = int((float(pygame.display.Info().current_w) * 154.0 ) / 1024.0)
             q_y_position = int((float(pygame.display.Info().current_h) * 543.0 ) / 768.0)
          elif l == 'z':
             q_x_position = int((float(pygame.display.Info().current_w) * 199.0 ) / 1024.0)
             q_y_position = int((float(pygame.display.Info().current_h) * 649.0 ) / 768.0)
          letter_actor.set_position([q_x_position, q_y_position])
          self.letters[l] = letter_actor
          q_x_position += image.get_width() + letter_sep

       self.letter_y = int((float(pygame.display.Info().current_h) * 265.0 ) / 768.0)


    def input(self):
       for event in pygame.event.get():
          if android is not None:
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
       if self.next_transition != VALID_STATES['QUIT']:
          if self.next_transition != VALID_STATES['STAY']:
             # Set next_transition to STAY if the game gets to this state from GameState a second or third time, etc.
             self.next_transition = VALID_STATES['STAY']

          if self.letter_index < 3:
             # If not all initials are set, check taps on every letter.
             for key in self.letters.keys():
                if self.letters[key].test_collision_with_point((self.cursor_x, self.cursor_y)):
                   self.player_init.append(self.letters[key].get_name())
                   self.letter_index += 1

          if self.letter_index > 0 and self.del_button.test_collision_with_point((self.cursor_x, self.cursor_y)):
             # If the player clicked on the delete button and there are initials set,
             # remove the last one.
             self.player_init.pop()
             self.letter_index -= 1
          
          if self.letter_index == 3:
             # If all initials have been set, make the done button visible.
             self.done_button.make_visible()
          else:
             self.done_button.make_invisible()

          if self.done_button.is_visible() and self.done_button.test_collision_with_point((self.cursor_x, self.cursor_y)):
             # If the user clicked on the done button, insert the score in the database and go to the main menu.
             database.cursor.execute('SELECT * FROM score ORDER BY score ASC')
             row = database.cursor.fetchone()
             score = (str(self.player_init[0] + self.player_init[1] + self.player_init[2]),
                      player.PLAYERS[1].get_score(),
                      row[0])
             database.cursor.execute('UPDATE score SET player_name = ?, score = ? WHERE _id = ?', score)
             database.scores.commit()
             # Don't forget to reset the initials list.
             self.player_init = []
             self.letter_index = 0
             self.next_transition = VALID_STATES['MENU']

       # Reset the mouse pointer.
       self.cursor_x = 0
       self.cursor_y = 0

       return self.next_transition

    def render(self, canvas):
       canvas.fill(self.background_color)

       self.banner.draw(canvas)
       if self.letter_index < 1:
          self.underscore_l.draw(canvas)
       if self.letter_index < 2:
          self.underscore_c.draw(canvas)
       if self.letter_index < 3:
          self.underscore_r.draw(canvas)

       self.del_button.draw(canvas)
       if self.done_button.is_visible():
          self.done_button.draw(canvas)

       for key in self.letters.keys():
          self.letters[key].draw(canvas)

       for i in range(self.letter_index):
          initial = self.letters[string.lower(self.player_init[i])].image
          position = None
          if i == 0:
             position = (self.underscore_l.rect.left, self.letter_y - (initial.get_height() // 2))
          elif i == 1:
             position = (self.underscore_c.rect.left, self.letter_y - (initial.get_height() // 2))
          else:
             position = (self.underscore_r.rect.left, self.letter_y - (initial.get_height() // 2))
          canvas.blit(initial, position)
