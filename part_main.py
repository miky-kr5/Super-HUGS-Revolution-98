import pygame 
from particle import ParticleSystem

def main():
    pygame.init()  
    pantalla=pygame.display.set_mode([600,400])
    salir=False
    reloj1=pygame.time.Clock()

    blanco=(255,255,255)

    ps = ParticleSystem(0, "Test", 'gfx/burbuja.png')
    ps.start()
    
    while not salir:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                salir=True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    salir = True

        ps.update()

        pantalla.fill(blanco)
        ps.draw(pantalla)
        pygame.display.update()

        reloj1.tick(60)
        
    pygame.quit()

main()
