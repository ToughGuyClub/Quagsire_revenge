from pico2d import *
import game_framework
width, height =  1400, 800
FRAMES_PER_ACTION =1.0
TIME_PER_ACTION = 0.1
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
class Thunder:
    image=None
    def __init__(self,x,y):
        if Thunder.image ==None:
            Thunder.image=load_image(os.path.join('asset/player/skill', 'thunder.png'))
        self.frame = 0.0
        self.x = x
        self.y = y
        self.stack=0
    def update(self):
        from play_modes.Thunder_mode import next_step, current_step
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        if current_step()==0:
            if int(self.frame) ==7:

                if current_step()==0:
                    next_step(1)
        elif current_step()>=2:
            if int(self.frame) ==7:
                self.stack+=1



    def draw(self):
        if self.stack<4:
            self.image.clip_draw(int(self.frame) * 100, 0, 100, 100, self.x, self.y, 200, 200)

class Step1_Thunder_Mode:
    def __init__(self):
        self.image = load_image(os.path.join('asset/player/Quagsire', 'Sleep.png'))

        self.x = -300
        self.y = 400
        self.size = 500

        self.top_rectY=800
        self.bottom_rectY=0
    def update(self):
        from play_modes.Thunder_mode import next_step, current_step
        if self.x <self.size/2:
            self.x+=500*game_framework.frame_time
        if current_step()<=2:
            if self.top_rectY>650:
                self.top_rectY -= 150*game_framework.frame_time
                self.bottom_rectY += 150*game_framework.frame_time

            if self.x >=self.size/2 and self.top_rectY<=650:

                if current_step()==1:
                    delay(0.5)
                    next_step(1)
        elif current_step()==3:
            if self.top_rectY<800:
                self.top_rectY += 150*game_framework.frame_time
                self.bottom_rectY -= 150*game_framework.frame_time
            if self.top_rectY>=800:

                next_step(1)
    def draw(self):
        draw_rectangle(0, self.top_rectY, 1400, 800,0,0,0,255,True)
        draw_rectangle(0, 0, 1400, self.bottom_rectY,0,0,0,255,True)
        from play_modes.Thunder_mode import current_step
        if current_step()==1:
            self.image.draw(self.x, self.y, self.size, self.size)

#반갈죽효과를 위한거 그냥 여기 넣음
half_stack=0
def reset_half_stack():
    global half_stack
    half_stack=0
def get_half_stack():
    global half_stack
    return half_stack
def increase_half_stack():
    global half_stack
    half_stack+=50*game_framework.frame_time