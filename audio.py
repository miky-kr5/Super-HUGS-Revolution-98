############################################
# Created on 1-23-2013. Miguel Angel Astor #
############################################
import pygame

try:
    import pygame.mixer as mixer
except ImportError:
    import android.mixer as mixer

class CachedAudioManager:
    def __init__(self):
        self.cache = {}

    def load_sound(self, path):
        if path not in self.cache:
            self.cache[path] = mixer.Sound(path)

    def play_sound(self, path):
        if path not in self.cache:
            self.load_sound(path)
        self.cache[path].play()

cached_audio_manager = CachedAudioManager()
