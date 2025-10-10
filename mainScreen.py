from pico2d import *

class main_screen:
    def __init__(self):
        #self.game_start = load_image('game_start.png')
        self.game_start = load_image('main_icon.png')
        self.game_logo = load_image('game_logo.png', )
    def draw(self):
        #화면 중앙에 200x100크기로 그림
       # self.game_start.draw(1400//2, 600//2, 200, 100)
        self.game_start.clip_draw(0,380,291,190, 1400//2, 600//2+100, 200, 100)
        self.game_start.clip_draw(0, 190, 291, 190, 1400 // 2, 600 // 2, 200, 100)
        self.game_start.clip_draw(0, 0, 291, 190, 1400 // 2, 600 // 2-100, 200, 100)
        self.game_logo.draw(1400//2, 600, 1155, 200)

