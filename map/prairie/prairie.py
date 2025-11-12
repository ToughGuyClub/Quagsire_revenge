from pico2d import *
import enemy.Enemy
import game_world
width, height =  1400, 800


class PRAIRIE01:
    def __init__(self,player):
        self.tile = load_image(os.path.join('asset/map/prairie', 'tile1-1.png'))
        self.background = load_image(os.path.join('asset/map/prairie', 'bg1-1.png'))
        self.background2 = load_image(os.path.join('asset/map/prairie', 'bg2-1.png'))
        # 적 배치
        e1 = enemy.Enemy.Enemy('trainer_BURGLAR.png', 900, 400, 1, player)
        e2 = enemy.Enemy.Enemy('trainer_BURGLAR.png', 1200, 300, 1, player)
        e3=enemy.Enemy.Enemy('trainer_BURGLAR.png', 900, 350, 1, player)

    def update(self):
        pass

    def draw(self):

        self.background.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림
        self.background2.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림
        self.tile.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림
class PRAIRIE02:
    def __init__(self,player):
        self.tile = load_image(os.path.join('asset/map/prairie', 'tile1-2.png'))
        self.background = load_image(os.path.join('asset/map/prairie', 'bg1-2.png'))
        self.background2 = load_image(os.path.join('asset/map/prairie', 'bg2-2.png'))
        # 적 배치
        e1 = enemy.Enemy.Enemy('trainer_BURGLAR.png', 900, 400, 1, player)
        e2 = enemy.Enemy.Enemy('trainer_BURGLAR.png', 1200, 300, 1, player)

    def update(self):
        pass

    def draw(self):

        self.background.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림
        self.background2.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림
        self.tile.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림

class PRAIRIE03:
    def __init__(self,player):
        self.tile = load_image(os.path.join('asset/map/prairie', 'tile1-3.png'))
        self.background = load_image(os.path.join('asset/map/prairie', 'bg1-3.png'))
        self.background2 = load_image(os.path.join('asset/map/prairie', 'bg2-3.png'))

    def update(self):
        pass

    def draw(self):

        self.background.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림
        self.background2.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림
        self.tile.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림