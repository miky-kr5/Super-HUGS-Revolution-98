############################################
# Created on 1-12-2013. Miguel Angel Astor #
############################################
import pygame

class CachedImageLoader:
    def __init__(self):
        self.image_cache = {}

    def load_image(self, path):
        if path in self.image_cache:
            return self.image_cache[path]
        else:
            image = pygame.image.load(path)
            self.image_cache[path] = image
            return image

    def get_image_to_screen_percent(self, path):
        if path in self.image_cache:
            return self.image_cache[path]
        else:
            image = self.load_image(path)
        
            screen_prop = (float(image.get_height()) / 768.0)
            screen_fract = (float(pygame.display.Info().current_h) * screen_prop) / 768.0
            scale_factor = screen_fract / screen_prop

            size = (int(image.get_width() * scale_factor), int(image.get_height() * scale_factor))
            ret_image = pygame.transform.smoothscale(image, size)
            
            self.image_cache[path] = ret_image
            return ret_image

cached_image_loader = CachedImageLoader()
