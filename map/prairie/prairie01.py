from pico2d import *

import game_world
width, height =  1400, 800


class PRAIRIE01:
    def __init__(self):
        self.image = load_image(os.path.join('asset/map/town', 'town_tile.png'))

    def update(self):
        pass

    def draw(self):
        self.image.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림