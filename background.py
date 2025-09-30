from pico2d import *


class Background:
    def __init__(self):
        self.image = load_image('background.png')

    def draw(self):
        width, height = 1400, 800
        self.image.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림