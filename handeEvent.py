from pico2d import *
from player.character import Character
from player.character import Bubble
from player.character import AttackManager
from current_map import *
width, height =  1400, 800
# 키 입력 상태를 저장할 리스트
pressed_keys = []

def handle_events(player,world,current_Map):
    global pressed_keys
    events = get_events()


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
        if event.type == SDL_MOUSEBUTTONDOWN:
            #기본공격 생성
            if(player.attack_manager.trigger_attack(get_time())):
                x, y = event.x, height - 1 - event.y
                bubble=Bubble(player.x,player.y,player.get_angle(x,y))
                player.motion_state = 'normal_attack'
                player.attack_anim_timer=1.5
                world.append(bubble)
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
            elif event.key in (SDLK_LEFT, SDLK_RIGHT, SDLK_UP, SDLK_DOWN):
                if event.key not in pressed_keys:   # 중복 방지
                    pressed_keys.append(event.key)

        elif event.type == SDL_KEYUP:
            if event.key in (SDLK_w, SDLK_a, SDLK_s, SDLK_d):
                if event.key in pressed_keys:
                    pass
    # 방향 업데이트 (리스트의 마지막 입력 기준)


    return True

