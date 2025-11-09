from pico2d import *

import game_world
width, height =  1400, 800


class PRAIRIE01:
    def __init__(self):
        self.tile = load_image(os.path.join('asset/map/prairie', 'tile1-1.png'))
        self.background = load_image(os.path.join('asset/map/prairie', 'bg1-1.png'))
        self.background2 = load_image(os.path.join('asset/map/prairie', 'bg2-2.png'))
    def update(self):
        pass

    def draw(self):

        self.background.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림
        self.background2.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림
        self.tile.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림
