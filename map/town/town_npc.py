from pico2d import *
import game_framework
TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8
class Snorlax:
    def __init__(self):
        self.image_idle = load_image(os.path.join('asset/map/town','Idle-Anim.png'))
        self.x, self.y = 900, 550
        self.scale = 150
        self.frameX=0.0
        self.frameY=7
        self.dirX=0
        self.dirY=0
        self.state='idle'
    def draw(self):
        self.image_idle.clip_draw(int(self.frameX) * 32, self.frameY * 64, 32, 64, self.x, self.y, self.scale, self.scale+self.scale//2)
        pass
    def update(self):
        if self.state=='idle':
            FRAMES_PER_ACTION=6
        self.frameX = (self.frameX + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        pass