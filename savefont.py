from pico2d import *
import game_world
import game_framework
class save_font:
    def __init__(self,player):
        self.font = load_font('asset/screen/intro/introFont.ttf', 30)
        self.player=player
        self.x=player.x-50
        self.y=player.y+50
        self.time=3.0
        game_world.add_object(self,3)
    def update(self):
        self.x=self.player.x
        self.y=self.player.y+50
        self.time-=game_framework.frame_time
        if self.time<=0:
            game_world.remove_object(self)
    def draw(self):
        self.font.draw(self.x,self.y,'Save', (255, 255, 255))

class skillUnlock_font:
    def __init__(self,player):
        self.font = load_font('asset/screen/intro/introFont.ttf', 30)
        self.player=player
        self.x=player.x
        self.y=player.y+50
        self.time=3.0
        game_world.add_object(self,3)
    def update(self):
        self.x=self.player.x-100
        self.y=self.player.y+70
        self.time-=game_framework.frame_time
        if self.time<=0:
            game_world.remove_object(self)
    def draw(self):
        self.font.draw(self.x,self.y,'new skill unlock', (255, 255, 255))