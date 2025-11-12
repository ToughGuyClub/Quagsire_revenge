from pico2d import *
import enemy.Enemy
import game_world
width, height =  1400, 800


class GLACIER01:
    def __init__(self,player):
        self.tile = load_image(os.path.join('asset/map/glacier', 'tile1-1.png'))

        # 적 배치


    def update(self):
        pass

    def draw(self):
        self.tile.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림

class GLACIER02:
    def __init__(self,player):
        self.tile = load_image(os.path.join('asset/map/glacier', 'tile1-2.png'))

    def update(self):
        pass

    def draw(self):
        self.tile.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림

class GLACIER03:
    def __init__(self,player):
        self.tile = load_image(os.path.join('asset/map/glacier', 'tile1-3.png'))

    def update(self):
        pass

    def draw(self):

        self.tile.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림