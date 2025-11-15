from pico2d import *
from enemy.Enemy import create_enemy
import game_world
width, height =  1400, 800


class CEMETERY01:
    def __init__(self,player):
        self.tile = load_image(os.path.join('asset/map/cemetery', 'tile1-1.png'))
        self.background = load_image(os.path.join('asset/map/cemetery', 'bg1-1.png'))
        self.background2 = load_image(os.path.join('asset/map/cemetery', 'bg2.png'))

        # 적 배치
        create_enemy('ghost', 900, 200, player)

    def update(self):
        pass

    def draw(self):
        self.background2.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림
        self.background.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림
        self.tile.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림

class CEMETERY02:
    def __init__(self,player):
        self.tile = load_image(os.path.join('asset/map/cemetery', 'tile1-2.png'))
        self.background = load_image(os.path.join('asset/map/cemetery', 'bg1-2.png'))
        self.background2 = load_image(os.path.join('asset/map/cemetery', 'bg2.png'))


    def update(self):
        pass

    def draw(self):
        self.background2.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림
        self.background.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림
        self.tile.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림

class CEMETERY03:
    def __init__(self,player):
        self.tile = load_image(os.path.join('asset/map/cemetery', 'tile1-3.png'))
        self.background = load_image(os.path.join('asset/map/cemetery', 'bg1-3.png'))
        self.background2 = load_image(os.path.join('asset/map/cemetery', 'bg2.png'))

    def update(self):
        pass

    def draw(self):
        self.background2.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림
        self.background.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림

        self.tile.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림