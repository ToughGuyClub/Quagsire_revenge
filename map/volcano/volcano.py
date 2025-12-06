from pico2d import *

import game_world
width, height =  1400, 800
from enemy.Enemy import create_enemy
from enemy.Charizard import Charizard
import game_framework
import map.volcano.volcano_dialogue
class VOLCANO:
    def __init__(self,player):
        self.tile = load_image(os.path.join('asset/map/volcano', 'tile1-1.png'))

        Charizard(player)
        from player.character import reset_pressed_keys
        reset_pressed_keys()
        game_framework.push_mode(map.volcano.volcano_dialogue)
        import sound
        self.bgm = load_music(os.path.join('asset/map/volcano/volcano_bgm.mp3'))
        self.bgm.set_volume(sound.get_sound_volume())
        self.bgm.repeat_play()
    def update(self):
        pass

    def draw(self):


        self.tile.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림
