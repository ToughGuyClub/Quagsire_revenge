

from pico2d import *


class Player_UI:
    def __init__(self,player):
        self.HP_bar_img = load_image(os.path.join('asset/player','hp_bar.png'))
        self.player = player
    def draw(self ):
        self.draw_health_bar(self.player)
        pass
    def draw_health_bar(self,player):
        bar_width = 400
        bar_height = 20
        bar_color = 2
        #체력비율에 따라 색깔 바꿈 50%이상 초록 50%미만 노랑 20%미만 빨강
        health_ratio = player.cur_HP / player.max_HP
        if health_ratio > 0.5: bar_color = 2
        elif health_ratio > 0.2: bar_color = 1
        else: bar_color = 0
        self.HP_bar_img.clip_draw(0, bar_color * 6, 96, 6, 250, 750, bar_width * health_ratio, bar_height)
    def update(self):
        pass
