###########################################
# Created on 1-9-2013. Miguel Angel Astor #
###########################################
import math

import pygame

import math_utils
import game

ACTOR_STATES = { 'IDLE': 0, 'MOVING': 1 }

class BaseActor(pygame.sprite.Sprite):
    def __init__(self, id, image = None, name = "Default", animated = False, visible = True, solid = True):
        pygame.sprite.Sprite.__init__(self)
        
        self.id = id
        self.name = name
        self.animated = animated
        self.visible = visible
        self.solid = solid

        self.angle = 0.0
        self.position = [0, 0]
        self.velocity = [0, 0]
        self.acceleration = [0, 0]
        self.max_velocity = [0, 0]
        self.friction = 1.0

        self.image = image
        self.rect = self.image.get_rect()

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def is_animated(self):
        return self.animated

    def is_visible(self):
        return self.visible

    def is_solid(self):
        return self.solid

    def get_position(self):
        return self.position

    def set_position(self, new_pos):
        self.position = list(new_pos)

    def get_velocity(self):
        return self.velocity

    def set_velocity(self, new_vel):
        self.velocity = list(new_vel)

    def get_acceleration(self):
        return self.acceleration

    def set_acceleration(self, new_accel):
        self.acceleration = list(new_accel)

    def get_max_velocity(self):
        return self.max_velocity

    def set_max_velocity(self, max_vel):
        self.max_velocity = list(max_vel)

    def get_friction(self):
        return self.get_friction

    def set_friction(self, new_friction):
        self.friction = new_friction

    def draw(self, canvas):
        if self.image is not None:
            canvas.blit(self.image, self.rect)
        else:
            pygame.draw.rect(canvas, (255, 206, 99), self.rect)
        

class BulletActor(BaseActor):
    """ Actor class with fixed velocity bullet behavior. """
    def __init__(self, id, image, name = "Default", animated = False, visible = True, solid = True, frame_rate = 60.0):
        BaseActor.__init__(self, id, image, name, animated, visible, solid)
        self.then = pygame.time.get_ticks()
        self.now = pygame.time.get_ticks()
        self.frame_rate = frame_rate
        self.moving = False

    def is_moving(self):
        return self.moving

    def move(self):
        self.moving = True

    def stop(self):
        self.moving = False

    def update(self):
        # Calculate the time elapsed between the previous call to update and this one.
        self.now = pygame.time.get_ticks()
        delta_t = self.now - self.then
        if delta_t < 0:
            delta_t = 0 # Compensatefor overflow of self.now

        if game.DEBUG:
            print
            print "Bullet actor: " + self.name
            print "THEN: " + str(self.then) + " :: NOW: " + str(self.now) + " :: DELTA: " + str(delta_t)

        if self.moving:
            if game.DEBUG:
                print "NEW VEL X: " + str((self.velocity[0] * delta_t) * (self.frame_rate / 1000))
                print "NEW VEL Y: " + str((self.velocity[1] * delta_t) * (self.frame_rate / 1000))
            self.position[0] += (self.velocity[0] * delta_t) * (self.frame_rate / 1000)
            self.position[1] += (self.velocity[1] * delta_t) * (self.frame_rate / 1000)
        self.rect.center = (self.position[0], self.position[1])

        if game.DEBUG:
            print "NEW POSITION: " + str(self.position)

        # TODO: Update animation frame if any.

        self.then = self.now
        
