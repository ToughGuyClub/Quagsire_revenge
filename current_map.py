from pico2d import *

class CurrentMap:
    def __init__(self):
        self.current_map = 0
    def change_map(self, new_map):
        self.current_map = new_map
    def get_current_map(self):
        return self.current_map
