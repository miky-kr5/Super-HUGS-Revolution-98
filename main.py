#! /usr/bin/env python
###########################################
# Created on 1-7-2013. Miguel Angel Astor #
###########################################
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
      screen  = pygame.display.set_mode((800, 600),
                                        pygame.FULLSCREEN | pygame.HWSURFACE)
      pygame.display.set_caption("Super HUGS Revolution 98")
   pygame.mouse.set_visible(False)

   # Create the game object and start the main game loop.
   game = Game(screen)
   game.game_loop()

   # Cleanly terminate PyGame.
   pygame.quit()
   
# Required by pgs4a.
if __name__ =="__main__":
    main()
