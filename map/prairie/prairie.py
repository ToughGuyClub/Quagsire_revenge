from pico2d import *
from enemy.Enemy import create_enemy
import game_world
width, height =  1400, 800


class PRAIRIE01:
    def __init__(self,player):
        self.tile = load_image(os.path.join('asset/map/prairie', 'tile1-1.png'))
        self.background = load_image(os.path.join('asset/map/prairie', 'bg1-1.png'))
        self.background2 = load_image(os.path.join('asset/map/prairie', 'bg2-1.png'))
        # 적 배치
        create_enemy('researcher',900,400,player)
        create_enemy('researcher', 800, 500, player)
        create_enemy('researcher', 500, 400, player)
       # create_enemy('doctor',1300,40,player)
        import sound
        self.bgm = load_music(os.path.join('asset/map/prairie/prairie_bgm.mid'))
        self.bgm.set_volume(sound.get_sound_volume())
        self.bgm.repeat_play()
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
        create_enemy('researcher', 500, 500, player)
        create_enemy('researcher', 650, 450, player)
        create_enemy('researcher', 500, 100, player)
        create_enemy('doctor',900,400,player)

        import sound
        self.bgm = load_music(os.path.join('asset/map/prairie/prairie_bgm.mid'))
        self.bgm.set_volume(sound.get_sound_volume())
        self.bgm.repeat_play()
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

        create_enemy('researcher', 510, 480, player)
        create_enemy('researcher', 510, 80, player)
        create_enemy('doctor', 800, 460, player)
        create_enemy('doctor', 850, 370, player)
        create_enemy('doctor', 800, 260, player)
        import sound
        self.bgm = load_music(os.path.join('asset/map/prairie/prairie_bgm.mid'))
        self.bgm.set_volume(sound.get_sound_volume())
        self.bgm.repeat_play()
    def update(self):
        pass

    def draw(self):

        self.background.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림
        self.background2.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림
        self.tile.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림