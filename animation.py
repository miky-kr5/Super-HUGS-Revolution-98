###########################################
# Created on 1-9-2013. Miguel Angel Astor #
###########################################

class Animation:
    """ This class represents an animated sprite. """
    def __init__(self, name = "Default", num_frames = 1, frame_start_offset = 0):
        """ Initializes an empty animation. """
        self.fps = 0
        self.name = name
        self.looping = False
        self.frame_start = frame_start_offset
        self.num_frames = num_frames
        self.current_frame = 0

    def __str__(self):
        """ Returns a string representation of this animation. """
        return "Animation :: Name: " + self.name + " :: FPS: " + str(self.fps) +
               " :: Looping : " + str(self.looping) + " :: Current frame: " +
               str(self.current_frame)

    def get_current_frame(self):
        """ Returns the current frame of the animation. """
        return self.current_frame

    def get_looping(self):
        return self.looping

    def set_looping(self, looping):
        self.looping = looping

    def get_frames_per_second(self):
        return self.fps

    def set_frames_per_second(self, fps):
        self.fps = fps

    def generate_animation(self):
        """ Generator function that returns the next frame of the animation. """
        while True:
            for frame in range(self.frame_start, self.frame_start + self.num_frames):
                self.current_frame = frame - self.frame_start
                yield frame
