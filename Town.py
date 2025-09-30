from pico2d import *
import random
width, height =  1400, 800


class Tree:
    def __init__(self, x, y, treetype):
        self.x = x
        self.y = y
        self.treetype = treetype
        self.image = load_image('trees.png')
    def draw(self):
        self.image.clip_draw(0, 464 * self.treetype, 46, 46, self.x, self.y)


class Town:
    def __init__(self):
        self.image = load_image('town_tile.png')
        self.trees = load_image('trees.png')
    def draw(self):
        self.image.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림


