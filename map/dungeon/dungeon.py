from pico2d import *
from enemy.Enemy import create_enemy
import game_world
width, height =  1400, 800


class DUNGEON01:
    def __init__(self,player):
        self.tile = load_image(os.path.join('asset/map/dungeon', 'tile1-1.png'))
        self.background = load_image(os.path.join('asset/map/dungeon', 'bg1-1.png'))
        self.background2 = load_image(os.path.join('asset/map/dungeon', 'bg2-1.png'))
        self.background3 = load_image(os.path.join('asset/map/dungeon', 'bg3.png'))
        # 적 배치

        create_enemy('rocker', 900, 200, player)
        create_enemy('rocker', 320, 200, player)
        #create_enemy('rival', 610, 480, player)
        create_enemy('rival', 120, 380, player)

        import sound
        self.bgm = load_music(os.path.join('asset/map/dungeon/dungeon_bgm.mid'))
        self.bgm.set_volume(sound.get_sound_volume())
        self.bgm.repeat_play()
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

        create_enemy('boldore', 760, 300, player)
        create_enemy('rocker', 440, 200, player)
        create_enemy('rocker', 810, 200, player)
        create_enemy('rival', 520, 380, player)
        create_enemy('rival', 600, 480, player)


        import sound
        self.bgm = load_music(os.path.join('asset/map/dungeon/dungeon_bgm.mid'))
        self.bgm.set_volume(sound.get_sound_volume())
        self.bgm.repeat_play()
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

        create_enemy('boldore', 840, 360, player)
        create_enemy('boldore', 540, 240, player)
        create_enemy('rocker', 710, 120, player)
        create_enemy('rival', 810, 330, player)
        create_enemy('rival', 580, 280, player)
        create_enemy('rival', 740, 180, player)

        import sound
        self.bgm = load_music(os.path.join('asset/map/dungeon/dungeon_bgm.mid'))
        self.bgm.set_volume(sound.get_sound_volume())
        self.bgm.repeat_play()

    def update(self):
        pass

    def draw(self):
        self.background2.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림
        self.background.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림
        self.background3.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림
        self.tile.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림