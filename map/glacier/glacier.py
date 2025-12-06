from pico2d import *
from enemy.Enemy import create_enemy
import game_world
width, height =  1400, 800


class GLACIER01:
    def __init__(self,player):
        self.tile = load_image(os.path.join('asset/map/glacier', 'tile1-1.png'))

        # 적 배치

        create_enemy('swimmer', 50, 580, player)
        create_enemy('swimmer', 1250, 580, player)
        create_enemy('swimmer', 50, 100, player)
        create_enemy('swimmer', 1250, 100, player)
        import sound
        self.bgm = load_music(os.path.join('asset/map/glacier/glacier_bgm.mid'))
        self.bgm.set_volume(sound.get_sound_volume())
        self.bgm.repeat_play()
    def update(self):
        pass

    def draw(self):
        self.tile.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림

class GLACIER02:
    def __init__(self,player):
        self.tile = load_image(os.path.join('asset/map/glacier', 'tile1-2.png'))
        create_enemy('swimmer', 100, 530, player)
        create_enemy('swimmer', 1200, 530, player)
        create_enemy('swimmer', 100, 150, player)
        create_enemy('swimmer', 1200, 150, player)
        create_enemy('captin', 600, 530, player)
        create_enemy('captin', 600, 150, player)
        import sound
        self.bgm = load_music(os.path.join('asset/map/glacier/glacier_bgm.mid'))
        self.bgm.set_volume(sound.get_sound_volume())
        self.bgm.repeat_play()
    def update(self):
        pass

    def draw(self):
        self.tile.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림

class GLACIER03:
    def __init__(self,player):
        self.tile = load_image(os.path.join('asset/map/glacier', 'tile1-3.png'))
        create_enemy('swimmer', 600, 550, player)
        create_enemy('swimmer', 600, 120, player)
        create_enemy('captin', 660, 500, player)
        create_enemy('captin', 660, 170, player)
        create_enemy('captin', 720, 400, player)
        create_enemy('captin', 720, 270, player)
        import sound
        self.bgm = load_music(os.path.join('asset/map/glacier/glacier_bgm.mid'))
        self.bgm.set_volume(sound.get_sound_volume())
        self.bgm.repeat_play()
    def update(self):
        pass

    def draw(self):

        self.tile.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림