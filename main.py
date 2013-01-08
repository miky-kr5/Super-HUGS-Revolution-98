# Miguel Angel Astor Romero. Created on 7-1-2012. #
###################################################
import pygame

try:
   import android
except ImportError:
   android = None

from game import Game

def main():
   """ Initializes PyGame and pgs4a and starts the game loop. """
   # Variables.
   screen = None

   # Init PyGame.
   pygame.init()
   
   if android:
      # Init pgs4a and map Android's back button to PyGame's escape key.
      android.init()
      android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)
      # Get the device's screen size and request a surface of that size.
      screen_size = (pygame.display.Info().current_w,
                     pygame.display.Info().current_h)
      screen = pygame.display.set_mode(screen_size)
   else:
      # If not on Android, default to a 800x600 pixels screen.
      screen  = pygame.display.set_mode((800, 600))
      pygame.display.set_caption("Super HUGS Revolution 98")

   # Create the main game object.
   game = Game(screen)
   
   # Start the game.
   print game.get_state()
   game.game_loop()

   # Cleanly terminate PyGame.
   pygame.quit()
   
# Required by pgs4a.
if __name__ =="__main__":
    main()
