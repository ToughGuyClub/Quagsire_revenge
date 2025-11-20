from pico2d import *

import game_framework
import game_world
from player.status import Status


player = None
status = None
def init():
    from player.character import Character
    global player
    global status
    for layer in game_world.world_persistent:
        for o in layer:
            if isinstance(o, Character):  # 예시) Character 클래스에 player_flag=True 넣어두면 탐색 가능
                player = o
                if status is None:
                    status = Status(player)
                    pass
                #game_world.add_object(status, 2,True)


    pass

def finish():
    #스테이터스 찾아서 삭제
    #game_world.remove_object(status)
    pass

def update():
    handle_events()
    pass

def draw():
    clear_canvas()
    game_world.render()
    status.draw()
    #기본 스텟창이 될 사각형 그리기

    update_canvas()
    pass

def handle_events():
    from player.character import Character
    events=get_events()
    for event in events:
        if event.type==SDL_QUIT:
            game_framework.quit()
        elif event.type==SDL_KEYDOWN:
            if event.key==SDLK_ESCAPE:
                game_framework.pop_mode()
            '''
            elif event.key==SDLK_1:
                if player.skill_points>0:
                    player.skill_manager.current_skills[0]+=1
                    player.skill_points-=1
            elif event.key==SDLK_2:
                if player.skill_points>0:
                    player.skill_manager.current_skills[1]+=1
                    player.skill_points-=1
            elif event.key==SDLK_3:
                if player.skill_points>0:
                    player.skill_manager.current_skills[2]+=1
                    player.skill_points-=1
            elif event.key==SDLK_4:
                if player.skill_points>0:
                    player.skill_manager.current_skills[3]+=1
                    player.skill_points-=1
            '''
            if event.key == SDLK_DOWN:
                if status.current_selected_skill[0] <3:
                    status.current_selected_skill[0] +=1
                    cur_slot = status.current_selected_skill[0]
                    status.current_selected_skill[1] = player.skill_manager.current_skills[cur_slot] - 1
            elif event.key == SDLK_UP:
                if status.current_selected_skill[0] >0:
                    status.current_selected_skill[0] -=1
                    cur_slot = status.current_selected_skill[0]
                    status.current_selected_skill[1] = player.skill_manager.current_skills[cur_slot] - 1
            elif event.key == SDLK_RIGHT:
                slot = status.current_selected_skill[0]
                if status.current_selected_skill[1] < 2 and player.skill_manager.current_skills[slot]<player.skill_manager.current_unlock_skills[slot]:
                    status.current_selected_skill[1] += 1
                    player.skill_manager.current_skills[slot] = status.current_selected_skill[1] + 1

            elif event.key == SDLK_LEFT:
                slot = status.current_selected_skill[0]
                if status.current_selected_skill[1] > 0:
                    status.current_selected_skill[1] -= 1
                    player.skill_manager.current_skills[slot] = status.current_selected_skill[1] + 1



def pause():
    pass
def resume():
    pass
