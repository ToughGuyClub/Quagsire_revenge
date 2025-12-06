from pico2d import *
import game_world
import game_framework
class POTION:
    def __init__(self,player):
        self.image_1= load_image(os.path.join('asset/player', 'POTION.png'))
        self.image_2= load_image(os.path.join('asset/player', 'SUPERPOTION.png'))
        self.image_3= load_image(os.path.join('asset/player', 'HYPERPOTION.png'))
        self.player=player
        self.type=0
        self.cooldown=0.0
        game_world.add_object(self,1,True)
    def use_potion(self):
        if self.cooldown>0.0:
            return
        else:
            if self.type == 1:
                self.player.cur_HP = min(self.player.max_HP, self.player.cur_HP + self.player.max_HP // 4)
            elif self.type == 2:
                self.player.cur_HP = min(self.player.max_HP, self.player.cur_HP +self.player.max_HP // 2)
            elif self.type == 3:
                self.player.cur_HP = min(self.player.max_HP, self.player.cur_HP + self.player.max_HP)
            self.cooldown=5.0
    def update(self):
        self.cooldown-=game_framework.frame_time
        pass
    def draw(self):
        pass
