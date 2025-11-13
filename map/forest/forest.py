from pico2d import *

import game_world
width, height =  1400, 800
from enemy.Enemy import create_enemy

class FOREST01:
    def __init__(self,player):
        self.tile = load_image(os.path.join('asset/map/forest', 'tile1-1.png'))
        self.background = load_image(os.path.join('asset/map/forest', 'bg1-1.png'))

        # 적 배치
        create_enemy('ruinmaniac', 710, 380, player)
        create_enemy('ruinmaniac', 660, 280, player)
        create_enemy('ruinmaniac', 710, 180, player)
        create_enemy('ranger', 910, 380, player)
    def update(self):
        pass

    def draw(self):

        self.background.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림

        self.tile.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림
class FOREST02:
    def __init__(self,player):
        self.tile = load_image(os.path.join('asset/map/forest', 'tile1-2.png'))
        self.background = load_image(os.path.join('asset/map/forest', 'bg1-2.png'))

        # 적 배치

        create_enemy('ruinmaniac', 760, 300, player)
        create_enemy('ruinmaniac', 810, 200, player)
        create_enemy('ranger', 610, 480, player)
        create_enemy('ranger', 630, 380, player)
    def update(self):
        pass

    def draw(self):

        self.background.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림

        self.tile.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림

class FOREST03:
    def __init__(self,player):
        self.tile = load_image(os.path.join('asset/map/forest', 'tile1-3.png'))
        self.background = load_image(os.path.join('asset/map/forest', 'bg1-3.png'))

        create_enemy('ruinmaniac', 840, 360, player)
        create_enemy('ruinmaniac', 540, 240, player)
        create_enemy('ruinmaniac', 710, 120, player)
        create_enemy('ranger', 810, 330, player)
        create_enemy('ranger', 580, 280, player)
        create_enemy('ranger', 740, 180, player)

    def update(self):
        pass

    def draw(self):

        self.background.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림

        self.tile.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림