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
        create_enemy('biker', 700, 300, player)
        create_enemy('rocketman', 500, 200, player)
        create_enemy('rocketman', 300, 400, player)
        create_enemy('rocketgirl', 600, 300, player)
        create_enemy('rocketgirl', 800, 500, player)

        import sound
        self.bgm = load_music(os.path.join('asset/map/cemetery/cemetery_bgm.mid'))
        self.bgm.set_volume(sound.get_sound_volume())
        self.bgm.repeat_play()
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

        create_enemy('ghost', 900, 200, player)
        create_enemy('ghost', 700, 400, player)
        create_enemy('biker', 600, 300, player)
        create_enemy('rocketman', 400, 200, player)
        create_enemy('rocketgirl', 800, 500, player)
        create_enemy('rocketgirl', 500, 200, player)
        import sound
        self.bgm = load_music(os.path.join('asset/map/cemetery/cemetery_bgm.mid'))
        self.bgm.set_volume(sound.get_sound_volume())
        self.bgm.repeat_play()
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

        create_enemy('ghost', 800, 300, player)
        create_enemy('ghost', 600, 400, player)
        create_enemy('biker', 400, 200, player)
        create_enemy('biker', 700, 500, player)
        create_enemy('rocketman', 600, 300, player)
        create_enemy('rocketman', 500, 300, player)
        create_enemy('rocketgirl', 300, 200, player)
        import sound
        self.bgm = load_music(os.path.join('asset/map/cemetery/cemetery_bgm.mid'))
        self.bgm.set_volume(sound.get_sound_volume())
        self.bgm.repeat_play()
    def update(self):
        pass

    def draw(self):
        self.background2.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림
        self.background.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림

        self.tile.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림