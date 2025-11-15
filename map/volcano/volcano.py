from pico2d import *

import game_world
width, height =  1400, 800
from enemy.Enemy import create_enemy

class VOLCANO:
    def __init__(self,player):
        self.tile = load_image(os.path.join('asset/map/volcano', 'tile1-1.png'))




    def update(self):
        pass

    def draw(self):


        self.tile.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림
