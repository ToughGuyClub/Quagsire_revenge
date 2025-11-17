from pico2d import *

from current_map import *
from play_modes import Status_mode
import game_world
width, height =  1400, 800
# 키 입력 상태를 저장할 리스트

x=0
y=0
last_mouse_x=0
last_mouse_y=0
def handle_events(player=None,world=None,current_Map=None):
    global pressed_keys
    global last_mouse_x, last_mouse_y
    if player is None and world is None and current_Map is None:
        return True
    events = get_events()
    global x, y

    for event in events:

        if event.type == SDL_QUIT:
            return False
        player.handle_event(event,current_Map)
        if current_Map.get_current_map()==0:
            if event.type == SDL_MOUSEBUTTONDOWN:
                x, y = event.x, height - 1 - event.y
                #시작 버튼 영역
                if 540 <= x <= 840 and 360 <= y <= 450:
                    current_Map.change_map(1)
                    return True
                # 컨티뉴 버튼 영역
                elif 540 <= x <= 840 and 250 <= y <= 330:
                    #세이브 로드 추가 예정

                    return True
                # 종료 버튼 영역
                elif 540 <= x <= 840 and 150 <= y <= 230:
                    close_canvas()
                    return False
                else:
                    return True
        if current_Map.get_current_map()==1:
            if event.type == SDL_MOUSEBUTTONDOWN:
                return 'next'
        if event.type == SDL_MOUSEMOTION:
            x, y = event.x, height - 1 - event.y

            last_mouse_x = x
            last_mouse_y = y
        if event.type == SDL_MOUSEBUTTONDOWN:

            x, y = event.x, height - 1 - event.y

            last_mouse_x = x
            last_mouse_y = y
            #기본공격 생성
            if(player.attack_manager.trigger_attack(get_time())):

                #bubble=Bubble(player.x,player.y,player.get_angle(x,y))
                player.motion_state = 'normal_attack'
                player.attack_anim_timer=0.3
                #world.append(bubble)
                #game_world.add_object(bubble, 2)
                #game_world.add_collision_pair('bubble:enemy', bubble, None)
                # 각도에 따라 방향 갱신
                angle = player.get_angle(x, y)
                dx = math.cos(angle)
                dy = math.sin(angle)

                player.stopdirX = int(round(dx))
                player.stopdirY = int(round(dy))
                player.frame = 0

        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                return False

            elif event.key == SDLK_t:
                from player.character import reset_pressed_keys
                reset_pressed_keys()
                game_framework.push_mode(Status_mode)
                pass
                #스텟창 띄울 예정
            elif event.key ==SDLK_SPACE:
                if player.dash_cooldown<=0:
                    player.dash_duration=0.1



        elif event.type == SDL_KEYUP:
            pass
        if current_Map.get_current_map() == 2:
            if event.type==SDL_KEYDOWN:
                if event.key==SDLK_f:
                    return 'Snorlax_npc'

    # 방향 업데이트 (리스트의 마지막 입력 기준)


    return True

def get_mouse_pos():
    return last_mouse_x, last_mouse_y