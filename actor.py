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

        self.fps = 60
        self.frames = []
        self.time_per_frame = int(1000.0 / float(self.fps))
        self.current_frame = 0
        self.anim_then = pygame.time.get_ticks()
        self.stopped = False
        self.loop = True

        self.angle = 0.0
        self.position = [0, 0]
        self.velocity = [0, 0]
        self.acceleration = [0, 0]
        self.max_velocity = [0, 0]
        self.friction = 1.0

        self.color = (255, 206, 99)

        if image is not None:
            self.image = image.copy()
            self.frames.append(self.image)
            self.rect = self.image.get_rect()
        else:
            self.image = None
            self.rect = pygame.rect.Rect(0, 0, 42, 42)

        self.image_points = []

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def is_animated(self):
        return self.animated

    def is_visible(self):
        return self.visible

    def set_visible(self, visible):
        self.visible = visible

    def toggle_visible(self):
        self.visible = not self.visible

    def make_visible(self):
        self.visible = True

    def make_invisible(self):
        self.visible = False

    def is_solid(self):
        return self.solid

    def get_color(self):
        return self.color

    def set_color_tuple(self, color):
        self.color = color

    def set_color_rgb(self, red, green, blue):
        self.color = (red, green, blue)

    def get_position(self):
        return list(self.position)

    def set_position(self, new_pos):
        self.position = list(new_pos)
        self.rect.center = (self.position[0], self.position[1])

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

    def is_looping(self):
        return self.loop

    def set_looping(self, loop):
        self.loop = loop

    def get_fps(self):
        return self.fps
    
    def set_fps(self, fps):
        self.fps = fps
        self.time_per_frame = int(1000.0 / float(self.fps))

    def get_current_frame(self):
        return self.current_frame

    def resume_animation(self):
        self.stopped = False

    def stop_animation(self):
        self.stopped = True

    def add_frame(self, frame):
        self.frames.append(frame.copy())

    def change_frame(self, frame_index, frame):
        if frame_index < 0 or frame_index >= len(self.frames):
            pass
        else:
            self.frames[frame_index] = frame.copy()

    def remove_frame(self, frame_index):
        if frame_index < 1 or frame_index >= len(self.frames):
            # The first frame (frame 0) cannot be removed.
            pass
        else:
            self.frames.pop(im_point)
            if self.current_frame >= len(self.frames):
                self.current_frame = len(self.frames) - 1

    def get_image_point(self, point):
        if point < 0 or point > len(self.image_points):
            return (0, 0)
        else:
            im_point = [self.image_points[point][0] + self.rect.left, self.image_points[point][1] + self.rect.top]
            return im_point

    def set_image_point_xy(self, point_x, point_y):
        self.image_points.append((point_x, point_y))

    def remove_image_point(self, im_point):
        if im_point < 0 or im_point >= len(self.image_points):
            pass
        else:
            self.image_points.pop(im_point)

    def clear_image_points(self):
        del self.image_points[:]

    def test_collision_with_point(self, point):
        return self.rect.collidepoint(point[0], point[1])

    def draw(self, canvas):
        if self.image is not None:
            if not self.animated:
                canvas.blit(self.image, self.rect)
            else:
                anim_now = pygame.time.get_ticks()
                delta_t = anim_now - self.anim_then
                if not self.stopped and delta_t >= self.time_per_frame:
                    if self.current_frame == len(self.frames) and not self.loop:
                        pass
                    else:
                        self.current_frame = (self.current_frame + (delta_t // self.time_per_frame)) % len(self.frames)
                    self.anim_then = anim_now
                frame = self.frames[self.current_frame]
                frame_rect = frame.get_rect()
                frame_rect.center = (self.position[0], self.position[1])
                canvas.blit(frame, frame_rect)
        else:
            pygame.draw.rect(canvas, self.color, self.rect)
        

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
            delta_t = 0 # Compensate for overflow of self.now

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

        self.then = self.now

class OmnidirectionalActor(BaseActor):
    def __init__(self, id, image, name = "Default", animated = False, visible = True, solid = True, frame_rate = 60.0):
        BaseActor.__init__(self, id, image, name, animated, visible, solid)

        self.angle = 0.0
        self.then = pygame.time.get_ticks()
        self.frame_rate = frame_rate
        self.moving = False

        self.friction = 0.90

        self.constraint_min_x = 0
        self.constraint_min_y = 0
        self.constraint_max_x = 1024
        self.constraint_max_y = 768
        
        self.acc_fract_x = ((0.6 * float(pygame.display.Info().current_w)) / 1024.0)
        self.acc_fract_y = ((0.6 * float(pygame.display.Info().current_h)) / 768.0)

        self.idle_frames = []
        self.moving_frames = []
        self.scared_frames = []
        self.current_frame = 0

    def is_moving(self):
        return self.moving

    def move(self):
        self.moving = True

    def stop(self):
        self.moving = False

    def get_angle(self):
        return self.angle

    def set_angle(self, angle):
        self.angle = float(angle)

    def set_constraints(self, constraints):
        self.constraint_min_x = constraints[0]
        self.constraint_min_y = constraints[2]
        self.constraint_max_x = constraints[1]
        self.constraint_max_y = constraints[3]

    def reset_then(self):
        self.then = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        delta_t = now - self.then
        if delta_t < 0:
            delta_t = 0 # Compensate for overflow of now
            
        if self.moving:
            direction = math_utils.angle_to_vector(self.angle)

            self.velocity[0] += direction[0] * self.acc_fract_x
            self.velocity[1] += direction[1] * self.acc_fract_y

        self.position[0] += (self.velocity[0] * delta_t) * (self.frame_rate / 1000)
        self.position[1] += (self.velocity[1] * delta_t) * (self.frame_rate / 1000)

        if self.position[0] < self.constraint_min_x:
            self.position[0] = self.constraint_min_x
        if self.position[0] > self.constraint_max_x:
            self.position[0] = self.constraint_max_x
        if self.position[1] < self.constraint_min_y:
            self.position[1] = self.constraint_min_y
        if self.position[1] > self.constraint_max_y:
            self.position[1] = self.constraint_max_y
            
        self.velocity[0] *= self.friction
        self.velocity[1] *= self.friction

        self.rect.center = (self.position[0], self.position[1])

        self.then = now

    def add_idle_frame(self, frame):
        self.idle_frames.append(frame.copy())

    def change_idle_frame(self, frame_index, frame):
        if frame_index < 0 or frame_index >= len(self.idle_frames):
            pass
        else:
            self.idle_frames[frame_index] = frame.copy()

    def remove_idle_frame(self, frame_index):
        if frame_index < 1 or frame_index >= len(self.idle_frames):
            # The first frame (frame 0) cannot be removed.
            pass
        else:
            self.idle_frames.pop(im_point)
            if self.current_frame >= len(self.idle_frames):
                self.current_frame = len(self.idle_frames) - 1

    def add_moving_frame(self, frame):
        self.moving_frames.append(frame.copy())

    def change_moving_frame(self, frame_index, frame):
        if frame_index < 0 or frame_index >= len(self.moving_frames):
            pass
        else:
            self.moving_frames[frame_index] = frame.copy()

    def remove_moving_frame(self, frame_index):
        if frame_index < 1 or frame_index >= len(self.moving_frames):
            # The first frame (frame 0) cannot be removed.
            pass
        else:
            self.moving_frames.pop(im_point)
            if self.current_frame >= len(self.moving_frames):
                self.current_frame = len(self.moving_frames) - 1

    def toggle_scared(self):
        aux = self.moving_frames
        self.moving_frames = self.scared_frames
        self.scared_frames = aux

    def draw(self, canvas):
        if self.image is not None:
            if not self.animated:
                canvas.blit(self.image, self.rect)
            else:
                frame = None
                anim_now = pygame.time.get_ticks()
                delta_t = anim_now - self.anim_then
                if not self.stopped and delta_t >= self.time_per_frame:
                    self.current_frame = (self.current_frame + (delta_t // self.time_per_frame)) % 2
                    self.anim_then = anim_now
                if not self.moving:
                    if self.angle >= -(math_utils.PI / 4.0) and self.angle < math_utils.PI / 4.0:
                        # Between -45 and 45 degrees.
                        frame = self.idle_frames[0]
                    elif self.angle >= math_utils.PI / 4.0 and self.angle < 3.0 * (math_utils.PI / 4.0):
                        # Between 45 and 135 degrees.
                        frame = self.idle_frames[1]
                    elif self.angle >= 3.0 * (math_utils.PI / 4.0) and self.angle <= math_utils.PI:
                        # Between 135 and 180 degrees.
                        frame = self.idle_frames[2]
                    elif self.angle >= -3.0 * (math_utils.PI / 4.0) and self.angle < -(math_utils.PI / 4.0):
                        # Between -135 and -45 degrees.
                        frame = self.idle_frames[3]
                    else:
                        # Between -180 and -135 degrees.
                        frame = self.idle_frames[2]
                else:
                    if self.angle >= -(math_utils.PI / 4.0) and self.angle < math_utils.PI / 4.0:
                        # Between -45 and 45 degrees.
                        base_frame = 0
                    elif self.angle >= math_utils.PI / 4.0 and self.angle < 3.0 * (math_utils.PI / 4.0):
                        # Between 45 and 135 degrees.
                        base_frame = 2
                    elif self.angle >= 3.0 * (math_utils.PI / 4.0) and self.angle <= math_utils.PI:
                        # Between 135 and 180 degrees.
                        base_frame = 4
                    elif self.angle >= -3.0 * (math_utils.PI / 4.0) and self.angle < -(math_utils.PI / 4.0):
                        # Between -135 and -45 degrees.
                        base_frame = 6
                    else:
                        # Between -180 and -135 degrees.
                        base_frame = 4
                    frame = self.moving_frames[self.current_frame + base_frame]
                frame_rect = frame.get_rect()
                frame_rect.center = (self.position[0], self.position[1])
                canvas.blit(frame, frame_rect)
        else:
            pygame.draw.rect(canvas, self.color, self.rect)
