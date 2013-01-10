############################################
# Created on 1-10-2013. Miguel Angel Astor #
############################################
import math
import random

import pygame

class Particle(pygame.sprite.Sprite):
    def __init__(self, lifespan, scale, texture, gravity = [0.0, 9.8], position = [0,0], initial_vel = [100.0, 100.0], frame_rate = 60.0):
        pygame.sprite.Sprite.__init__(self)

        self.age = 0
        self.lifespan = lifespan
        self.gravity = [gravity[0] * (1.0 / frame_rate), gravity[1] * (1.0 / frame_rate)]
        self.position = position
        self.velocity = [initial_vel[0] * (1.0 / frame_rate), initial_vel[1] * (1.0 / frame_rate)] # Pixels per frame.
        self.size = (int(float(texture.get_width()) * scale), int(float(texture.get_height()) * scale))
        self.alive = True
        self.frame_rate = frame_rate

        self.then = pygame.time.get_ticks()

        self.image = pygame.transform.smoothscale(texture, self.size)
        self.rect = self.image.get_rect()
        
        self.rect.center = (self.position[0], self.position[1])

    def is_alive(self):
        return self.alive

    def kill(self):
        self.alive = False

    def set_gravity(self, gravity):
        self.gravity = list(gravity)
    
    def update(self):
        if self.age >= self.lifespan:
            self.alive = False
            return None

        now = pygame.time.get_ticks()
        delta_t = now - self.then

        self.position[0] += (self.velocity[0] * delta_t) * (self.frame_rate / 1000)
        self.position[1] += (self.velocity[1] * delta_t) * (self.frame_rate / 1000)

        self.position[0] += (self.gravity[0] * delta_t) * (self.frame_rate / 1000)
        self.position[1] += (self.gravity[1] * delta_t) * (self.frame_rate / 1000)

        self.rect.center = (self.position[0], self.position[1])

        self.age += 1
        

    def draw(self, canvas):
        canvas.blit(self.image, self.rect)
        

class ParticleSystem:
    def __init__(self, id, name, texture_filename, lifespan = 100, max_particles = 1000, parts_per_second = 25, angle = 0):
        self.id = id
        self.name = name
        self.lifespan = lifespan
        self.max_particles = max_particles
        self.ppms = float(parts_per_second) / 1000.0 # Particles per milisecond.
        self.mspp = float(1000.0 / parts_per_second) # Miliseconds per particle.
        self.angle = angle
        self.working = False
        self.particles = set()
        self.texture = pygame.image.load(texture_filename)
        self.miliseconds_left = 1000
        self.part_creation_accum = 0.0
        self.then = pygame.time.get_ticks()

        self.gravity = [0.0, 9.8]
        self.position = [pygame.display.Info().current_w / 2, pygame.display.Info().current_h / 2]
        self.initial_velocity = [float(random.randrange(-10, 10)), float(random.randrange(-10, 10))] # Pixels per second.
        self.frame_rate = 60.0

        random.seed(None)

    def is_working(self):
        return self.working

    def start(self):
        self.working = True

    def stop(self):
        self.working = False

    def update(self):
        # Calculate the time delta.
        now = pygame.time.get_ticks()
        delta_t = now - self.then

        # Eliminate dead particles.
        remove_set = set()
        for particle in self.particles:
            if not particle.is_alive():
                remove_set.add(particle)
        self.particles.difference_update(remove_set)
        
        if self.working:            
            # Create new particles if possible.
            if len(self.particles) < self.max_particles:
                max_parts = self.max_particles - len(self.particles)
                self.part_creation_accum += (self.ppms * delta_t)
                parts_needed = int(self.part_creation_accum // 1) 
                if parts_needed >= 1:
                    for i in range(parts_needed):
                        particle = Particle(
                            self.lifespan,
                            random.random(),
                            self.texture,
                            self.gravity,
                            self.position,
                            self.initial_velocity,
                            self.frame_rate)
                        self.particles.add(particle)
                    self.part_creation_accum = 0.0

        # Update every particle.
        for particle in self.particles:
            particle.update()
        
        # Restart the time counter.
        if self.miliseconds_left >= 0:
            self.miliseconds_left = 1000
        self.then = now

    def draw(self, canvas):
        for particle in self.particles:
            particle.draw(canvas)
