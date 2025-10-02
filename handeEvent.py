from pico2d import *
from character import Character
from character import Bubble

width, height =  1400, 800
# 키 입력 상태를 저장할 리스트
pressed_keys = []

def handle_events(player,world):
    global pressed_keys
    events = get_events()


    for event in events:

        if event.type == SDL_QUIT:
            return False
        if event.type == SDL_MOUSEBUTTONDOWN:
            #기본공격 생성
            x, y = event.x, height - 1 - event.y
            bubble=Bubble(player.x,player.y,player.get_angle(x,y))
            world.append(bubble)

        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                return False
            elif event.key in (SDLK_LEFT, SDLK_RIGHT, SDLK_UP, SDLK_DOWN):
                if event.key not in pressed_keys:   # 중복 방지
                    pressed_keys.append(event.key)

        elif event.type == SDL_KEYUP:
            if event.key in pressed_keys:
                pressed_keys.remove(event.key)

    # 방향 업데이트 (리스트의 마지막 입력 기준)
    if player is not None:
        if pressed_keys:
            last_key = pressed_keys[-1]
            if last_key == SDLK_LEFT:
                player.dirX, player.dirY = -1, 0
                player.stopdirX, player.stopdirY = -1, 0
            elif last_key == SDLK_RIGHT:
                player.dirX, player.dirY = 1, 0
                player.stopdirX, player.stopdirY = 1, 0
            elif last_key == SDLK_UP:
                player.dirX, player.dirY = 0, 1
                player.stopdirX, player.stopdirY = 0, 1
            elif last_key == SDLK_DOWN:
                player.dirX, player.dirY = 0, -1
                player.stopdirX, player.stopdirY = 0, -1
        else:
            player.dirX, player.dirY = 0, 0  # 아무 키도 안 눌렸으면 멈춤

    return True

