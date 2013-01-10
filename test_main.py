#! /usr/bin/env python
############################################
# Created on 1-10-2013. Miguel Angel Astor #
############################################
import pygame 
from particle import ParticleSystem

def main():
    pygame.init()  
    pantalla = pygame.display.set_mode([600,400])
    done = False
    clock = pygame.time.Clock()

    white = (255,255,255)

    ps = ParticleSystem(0, "Test", 'gfx/burbuja.png')
    ps.start()
    
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True

        ps.update()

        screen.fill(white)
        ps.draw(screen)
        pygame.display.update()

        clock.tick(60)
        
    pygame.quit()

if __name__ =="__main__":
    main()
