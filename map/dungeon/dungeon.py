from pico2d import *
import enemy.Enemy
import game_world
width, height =  1400, 800


class DUNGEON01:
    def __init__(self,player):
        self.tile = load_image(os.path.join('asset/map/dungeon', 'tile1-1.png'))
        self.background = load_image(os.path.join('asset/map/dungeon', 'bg1-1.png'))
        self.background2 = load_image(os.path.join('asset/map/dungeon', 'bg2-1.png'))
        self.background3 = load_image(os.path.join('asset/map/dungeon', 'bg3.png'))
        # 적 배치


    def update(self):
        pass

    def draw(self):
        self.background2.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림
        self.background.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림
        self.background3.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림
        self.tile.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림

class DUNGEON02:
    def __init__(self,player):
        self.tile = load_image(os.path.join('asset/map/dungeon', 'tile1-2.png'))
        self.background = load_image(os.path.join('asset/map/dungeon', 'bg1-2.png'))
        self.background2 = load_image(os.path.join('asset/map/dungeon', 'bg2-2.png'))
        self.background3 = load_image(os.path.join('asset/map/dungeon', 'bg3.png'))

    def update(self):
        pass

    def draw(self):
        self.background2.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림
        self.background.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림
        self.background3.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림
        self.tile.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림

class DUNGEON03:
    def __init__(self,player):
        self.tile = load_image(os.path.join('asset/map/dungeon', 'tile1-3.png'))
        self.background = load_image(os.path.join('asset/map/dungeon', 'bg1-3.png'))
        self.background2 = load_image(os.path.join('asset/map/dungeon', 'bg2-3.png'))
        self.background3 = load_image(os.path.join('asset/map/dungeon', 'bg3.png'))
    def update(self):
        pass

    def draw(self):
        self.background2.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림
        self.background.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림
        self.background3.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림
        self.tile.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림