###########################################
# Created on 1-9-2013. Miguel Angel Astor #
###########################################

class Animation:
    """ This class represents an animated sprite. No sprite information is
        stored in this class, only sprite indexes. """
    def __init__(self, name):
        """ Initializes an empty animation. """
        self.fps = 0
        self.name = name
        self.looping = False
        self.current_frame = 0
        self.frames = []

    def __str__(self):
        """ Returns a string representation of this animation. """
        return "Animation :: Name: " + self.name + " :: FPS: " + str(self.fps) +
               " :: Looping : " + str(self.looping) + " :: Current frame: " +
               str(self.current_frame)

    def add_frame(self, frame):
        """ Adds a frame to this animation. Frames should be added in order. """
        self.frames.append(frame)

    def get_next_frame(self):
        """ Returns the current frame of the animation. Moves the current frame
            count by one. """
        if(self.looping):
            self.current_frame = (self.current_frame + 1) % len(self.frames)
        elif (self.current_frame == len(self.frames) - 1):
            pass
        return self.frames[self.current_frame]

    def get_current_frame(self):
        """ Returns the current frame of the animation. """
        return self.current_frame

    def set_current_frame(self, frame):
        """ Changes the current frame of the animation. """
        # The frame is wrapped modulo the number of frames to ensure it is valid.
        self.current_frame = frame % len(self.frames)

    def get_looping(self):
        """ Returns wether this animation should loop or not. """
        return self.looping

    def set_looping(self, looping):
        self.looping = looping

    def get_frames_per_second(self):
        return self.fps

    def set_frames_per_second(self, fps):
        self.fps = fps
