from pico2d import *

import game_framework
import game_world



player = None
def init():
    from player.character import Character
    global player
    for layer in game_world.world_persistent:
        for o in layer:
            if isinstance(o, Character):  # 예시) Character 클래스에 player_flag=True 넣어두면 탐색 가능
                player = o
    pass

def finish():
    pass

def update():
    handle_events()
    pass

def draw():

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


def pause():
    pass
def resume():
    pass
