# Miguel Angel Astor Romero. Created on 7-1-2013. #
###################################################
import pygame

try:
   import android
except ImportError:
   android = None

from state import VALID_STATES
from intro import IntroState
from menu import MenuState
from ingame import InGameState
from score import ScoreState
from notvalidstate import NotValidState
from constants import DEBUG

# The Game class implements the state machine of the game and
# runs the main game loop.
class Game:
    def __init__(self, screen):
        """ Sets the rendering canvas and the intial state. """
        self.canvas = screen
        self.current_state = VALID_STATES['INTRO']
        self.done = False
        self.clock = pygame.time.Clock()
        
        # Initialize the different game states.
        intro = IntroState()
        menu = MenuState()
        in_game = InGameState()
        score = ScoreState()
        not_valid = NotValidState()
        
        # Create a states list.
        self.state_vector = [intro, menu, in_game, score, not_valid]

    def get_state(self):
       """ Returns the current state of the game. """
       if self.current_state == VALID_STATES['INTRO']:
          return "INTRO"
       elif self.current_state == VALID_STATES['MENU']:
          return "MENU"
       elif self.current_state == VALID_STATES['IN_GAME']:
          return "IN_GAME"
       elif self.current_state == VALID_STATES['SCORE']:
          return "SCORE"
       elif self.current_state == VALID_STATES['QUIT']:
          return "QUIT"
       else:
          return "NOT_VALID"

    def game_loop(self):
        """ The main game loop. """
        while not self.done:
           # Get user input first.
           self.state_vector[self.current_state].input()
           # Then update the game state.
           transition = self.state_vector[self.current_state].update()
           # Check if a state transition is required.
           if transition != VALID_STATES['STAY']:
              if transition == VALID_STATES['INTRO']:
                 self.current_state = VALID_STATES['INTRO']
              elif transition == VALID_STATES['MENU']:
                 self.current_state = VALID_STATES['MENU']
              elif transition == VALID_STATES['IN_GAME']:
                 self.current_state = VALID_STATES['IN_GAME']
              elif transition == VALID_STATES['SCORE']:
                 self.current_state = VALID_STATES['SCORE']
              elif transition == VALID_STATES['QUIT']:
                 self.done = True
                 self.current_state = VALID_STATES['QUIT']
              else:
                 self.current_state = VALID_STATES['NOT_VALID']
              if DEBUG:
                 print self.get_state()
           # If the game is not over, render the current state.
           if not self.done:
              self.state_vector[self.current_state].render(self.canvas)
              pygame.display.update()
              self.clock.tick(60)

