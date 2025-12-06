from pico2d import *
import game_framework
TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8
class Snorlax:
    def __init__(self):
        self.image_idle = load_image(os.path.join('asset/map/town/Snorlax','Idle-Anim.png'))
        self.image_sleep = load_image(os.path.join('asset/map/town/Snorlax','Sleep-Anim.png'))
        self.x, self.y = 900, 550
        self.scale = 150
        self.frameX=0.0
        self.frameY=0
        self.dirX=0
        self.dirY=0
        self.state='sleep'
    def draw(self):
        if self.state=='sleep':
            self.image_sleep.clip_draw(int(self.frameX) * 40, self.frameY * 24, 40, 24, self.x, self.y, 40*4, 24*4)
        elif self.state=='idle':
            self.image_idle.clip_draw(int(self.frameX) * 32, self.frameY * 64, 32, 64, self.x, self.y, self.scale, self.scale+self.scale//2)

        pass
    def update(self):
        if self.state=='idle':
            FRAMES_PER_ACTION=6
        elif self.state=='sleep':
            FRAMES_PER_ACTION=2
        self.frameX = (self.frameX + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        pass
    def get_bb(self):
        return self.x - self.scale//2, self.y - (self.scale)//4, self.x + self.scale//2, self.y + (self.scale+self.scale//2)//2