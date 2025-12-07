from pico2d import *

import game_framework
import game_world
import random
from screen.thunder_scene import Thunder,Step1_Thunder_Mode,reset_half_stack,get_half_stack,increase_half_stack
width, height =  1400, 800
thunder =None
step = 0
qf = None
Thunder_create_time=0.0
Thunder_list=[]
def next_step(s):
    global step
    step += s
def current_step():
    global step
    return step
def init():
    from player.character import Character
    global player
    global thunder
    global step
    step=0
    global qf
    global Thunder_create_time
    Thunder_create_time=0.0
    global Thunder_list
    Thunder_list.clear()
    for layer in game_world.world_persistent:
        for o in layer:
            if isinstance(o, Character):  # 예시) Character 클래스에 player_flag=True 넣어두면 탐색 가능
                player = o
                thunder = Thunder(player.x,player.y)
    qf = Step1_Thunder_Mode(player.type)
    reset_half_stack()

    pass

def finish():


    pass

def update():
    global Thunder_create_time
    global Thunder_list
    if step==0:
        thunder.update()
    elif step>=1:
        #누오
        qf.update()
    if step==2:

        Thunder_create_time+=game_framework.frame_time
        if Thunder_create_time>=0.1 and len(Thunder_list)<20:
            Thunder_create_time=0.0
            rx=random.randint(100,1300)
            ry=random.randint(250,600)
            Thunder_list.append(Thunder(rx,ry))
        for thunders in Thunder_list:
            thunders.update()
        if len(Thunder_list)>=20 and Thunder_create_time>=1.5:
            next_step(1)
    elif step==3:
        qf.update()
    elif step==4:
        increase_half_stack()
        if get_half_stack()>=60:
            #여기 있는 모든거 다 지우고 팝
            #리스트에서 모든 적 제거

            #game_world.clear_enemy()
            for e in game_world.enemy_list[:]:  # 리스트 복사본을 순회
                r = getattr(e, 'is_onix', None)

                if not r:  # 일반 적
                    game_world.remove_object(e)
                    game_world.enemy_list.remove(e)

                else:  # 보스(onix)
                    e.HP -= 100
                    if e.HP <= 0:
                        e.HP = 1

            Thunder_list.clear()
            game_framework.pop_mode()
    pass

def draw():

    clear_canvas()
    if step<4:
        game_world.render_for_thunder_mode()
    draw_rectangle(0, 0, width, height, 0, 0, 0, 128, True)
    if step==0:
        thunder.draw()
    elif step>=1:
        qf.draw()
    if step==2:
        for thunders in Thunder_list:
            thunders.draw()
    elif step==3:
        for thunders in Thunder_list:
            thunders.draw()
        qf.draw()
    elif step==4:
        draw_rectangle(0, 0, width, height, 0, 0, 0, 255, True)
        game_world.render_for_thunder_mode_half()


    update_canvas()
    pass

def handle_events():
    pass

def pause():
    pass
def resume():
    pass
