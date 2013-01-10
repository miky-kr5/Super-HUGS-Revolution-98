############################################
# Created on 1-10-2013. Miguel Angel Astor #
############################################
import math
import random

import pygame

import math_utils

class Particle(pygame.sprite.Sprite):
    def __init__(self, lifespan, scale, texture, gravity = [0.0, 9.8], position = [0,0], initial_vel = [100.0, 100.0], friction = 1.0, frame_rate = 60.0):
        pygame.sprite.Sprite.__init__(self)

        self.age = 0
        self.lifespan = lifespan
        self.gravity = [gravity[0] / frame_rate, gravity[1] / frame_rate]
        self.position = position
        self.velocity = [float(initial_vel[0]) / frame_rate, float(initial_vel[1]) / frame_rate] # Pixels per frame.
        self.friction = friction
        self.size = (int(float(texture.get_width()) * scale), int(float(texture.get_height()) * scale))
        self.alive = True
        self.frame_rate = frame_rate

        self.then = pygame.time.get_ticks()

        self.image = pygame.transform.smoothscale(texture, self.size)
        self.rect = self.image.get_rect()
        self.rect.center = (self.position[0], self.position[1])

        self.screen_w = pygame.display.Info().current_w
        self.screen_h = pygame.display.Info().current_h

    def is_alive(self):
        return self.alive

    def kill(self):
        self.alive = False

    def set_gravity(self, gravity):
        self.gravity = list(gravity)
    
    def update(self):
        if self.alive:
            if self.age >= self.lifespan:
                self.alive = False
                return None

            now = pygame.time.get_ticks()
            delta_t = now - self.then
            
            self.position[0] += (self.velocity[0] * delta_t) * (self.frame_rate / 1000.0)
            self.position[1] += (self.velocity[1] * delta_t) * (self.frame_rate / 1000.0)

            self.velocity[0] *= self.friction
            self.velocity[1] *= self.friction

            self.position[0] += (self.gravity[0] * delta_t) * (self.frame_rate / 1000.0)
            self.position[1] += (self.gravity[1] * delta_t) * (self.frame_rate / 1000.0)
        
            self.rect.center = (self.position[0], self.position[1])

            self.age += 1  
            self.then = now

            if self.rect.center[0] < 0 - self.rect.width or self.rect.center[0] > self.screen_w + self.rect.width:
                self.kill()
                return None
            if self.rect.center[1] < 0 - self.rect.height or self.rect.center[1] > self.screen_h + self.rect.height:
                self.kill()
                return None

    def draw(self, canvas):
        if self.alive:
            canvas.blit(self.image, self.rect)
        

class ParticleSystem:
    def __init__(self, id, name, texture_filename, lifespan = 1000, max_particles = 1000, parts_per_second = 25, angle = 0):
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
        self.part_creation_accum = 0.0
        self.then = pygame.time.get_ticks()

        self.gravity = [0.0, 9.8]
        self.position = [pygame.display.Info().current_w / 2, pygame.display.Info().current_h / 2]
        self.initial_velocity_max = 50 # Pixels per second.
        self.friction = 0.99
        self.frame_rate = 60.0

        self.rectangle = pygame.Rect(0, 0, 25, 25)
        self.rectangle.center = (self.position[0], self.position[1])

        random.seed(None)

    def is_working(self):
        return self.working

    def start(self):
        self.working = True

    def stop(self):
        self.working = False

    def set_position(self, position):
        self.position = list(position)

    def set_gravity(self, gravity):
        self.gravity = list(gravity)

    def set_max_velocity(self, max_vel):
        self.initial_velocity_max = max_vel

    def set_angle(self, angle):
        self.angle = angle

    def set_friction(self, friction):
        self.friction = friction

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
                        velocity = [float(random.randrange(-self.initial_velocity_max, self.initial_velocity_max)),
                                    float(random.randrange(-self.initial_velocity_max, self.initial_velocity_max))]
                        particle = Particle(
                            int(self.lifespan),
                            max(min(random.random(), 1.0), 0.2),
                            self.texture,
                            list(self.gravity),
                            list(self.position),
                            velocity,
                            self.friction,
                            int(self.frame_rate))
                        self.particles.add(particle)
                    self.part_creation_accum = 0.0

        # Update every particle.
        for particle in self.particles:
            particle.update()
        
        # Restart the time counter.
        self.then = now

    def draw(self, canvas):
        for particle in self.particles:
            particle.draw(canvas)
