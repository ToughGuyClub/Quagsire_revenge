from pico2d import *
from current_map import *
from state_machine import StateMachine
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_a,SDLK_w,SDLK_s,SDLK_d,SDLK_1
from player.playerskill import PlayerSkills  # 추가

width, height =  1400, 800
global last_input
pressed_keys = set()
def right_down(e):
    return e[0]=='INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d
def left_down(e):
    return e[0]=='INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a
def right_up(e):
    return e[0]=='INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_d
def left_up(e):
    return e[0]=='INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_a
def up_down(e):
    return e[0]=='INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_w
def down_down(e):
    return e[0]=='INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s
def up_up(e):
    return e[0]=='INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_w
def down_up(e):
    return e[0]=='INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_s
def key_down(e):
    if e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN:
        key = e[1].key
        if key in (SDLK_w, SDLK_a, SDLK_s, SDLK_d):
            pressed_keys.add(key)
        return True
    return False
def key_up(e):
    if e[0] == 'INPUT' and e[1].type == SDL_KEYUP:
        key = e[1].key
        if key in (SDLK_w, SDLK_a, SDLK_s, SDLK_d):
            pressed_keys.discard(key)
        return True
    return False
def click_left_down(e):
    return e[0]=='INPUT' and e[1].type == SDL_MOUSEBUTTONDOWN and e[1].button ==1
def click_left_up(e):
    return e[0]=='INPUT' and e[1].type == SDL_MOUSEBUTTONUP and e[1].button ==1
def down_1(e):# 숫자 1이 눌렸을 때
    return e[0]=='INPUT' and e[1].type == SDL_KEYDOWN and e[1].key ==SDLK_1
class AttackManager:
    def __init__(self, cooldown_time):
        self.cooldown_time = cooldown_time  # 공격 쿨타임
        self.last_attack_time = 0  # 마지막으로 공격한 시간

    def can_attack(self, current_time):
        # 현재 공격 가능한지 확인
        return current_time - self.last_attack_time > self.cooldown_time

    def trigger_attack(self, current_time):
        # 공격 실행 및 시간 업데이트
        if self.can_attack(current_time):
            self.last_attack_time = current_time
            return True
        else:
            return False

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8
class Bubble:
    def __init__(self, x, y, degree):
        self.x = x
        self.y = y
        self.degree = degree
        self.speed = 10
        self.image = load_image(os.path.join('asset/player','bubble.png'))
        self.scale=32
        self.active=True

    def update(self):
        #각도를 기준으로 이동

        self.x += math.cos(self.degree) * self.speed
        self.y += math.sin(self.degree) * self.speed
        if self.x < 0 or self.x > width or self.y < 0 or self.y > height:
            self.active = False

    def draw(self):
        self.image.draw(self.x, self.y,self.scale,self.scale)

class Character:
    def __init__(self, x=100, y=100):
        self.max_HP = 100
        self.cur_HP = 100

        self.frame_timer = 0
        self.frame_interval = 0.2
        # 위치
        self.x = x
        self.y = y
        self.scale=150   #크기

        # 이동 방향
        self.dirX = 0
        self.dirY = 0
        # 현재 모션 상태
        self.motion_state = 'idle'
        self.attack_anim_timer = 0
        # 멈춘 방향 (캐릭터가 마지막으로 바라본 방향)
        self.stopdirX = 0
        self.stopdirY = -1  # 기본값: 아래쪽

        # 레벨
        self.level = 1
        self.exp = 0
        self.skill_points = 0
        self.attack_manager = AttackManager(1.5)  # 1.5초 쿨타임

        self.skills = PlayerSkills(self)

        self.IDLE = IDLE(self)
        self.RUN = RUN(self)
        self.ATTACK = ATTACK(self)
        self.state_machine = StateMachine(
            self.IDLE,  # <-시작상태 지정
            {
                self.IDLE: {
                    key_down: self.RUN,
                    click_left_down: self.ATTACK,

                },
                self.RUN: {
                    key_down: self.RUN,
                    key_up: self.RUN,
                    click_left_down: self.ATTACK

                },
                self.ATTACK: {
                    click_left_up: self.RUN,
                    key_down: self.RUN,
                    key_up: self.RUN,
                }
            }

        )
        # 스프라이트 이미지
        self.image_walking = load_image(os.path.join('asset/player', 'Walk-Anim.png'))
        self.image_idle = load_image(os.path.join('asset/player', 'Idle-Anim.png'))
        self.image_normal_attack = load_image(os.path.join('asset/player', 'Shoot-Anim.png'))
        self.frame = 0

    def draw(self):

        # 공격 애니메이션 우선
        if self.motion_state == 'normal_attack':
            self.ATTACK.draw()
            return

        # 눌린 이동키가 있으면 RUN, 없으면 IDLE 호출
        if pressed_keys:
            self.RUN.draw()
        else:
            self.IDLE.draw()
    def update(self, current_map,event=None):
        self.state_machine.update(current_map)

    def update_frame(self, dt=0.02):
        self.frame_timer += dt
        if self.frame_timer >= self.frame_interval:
            if self.motion_state == 'normal_attack':
                self.frame = (self.frame + 4) % 5  # 공격 애니메이션은 11프레임
            elif self.dirX == 0 and self.dirY == 0:
                self.frame = (self.frame + 1) % 7  # idle은 7프레임
            else:
                self.frame = (self.frame + 1) % 4  # 걷기는 4프레임
            self.frame_timer = 0

        if self.attack_anim_timer > 0.0:
            self.attack_anim_timer -= 0.1
            if self.attack_anim_timer <= 0.0:
                self.attack_anim_timer = 0.0
                self.motion_state = 'idle'
                self.frame=0


    def handle_event(self, event,current_map):
        self.state_machine.handle_state_event(('INPUT',event),current_map)
    def get_pos(self):
        return (self.x, self.y)

    def get_angle(self,mouse_x, mouse_y):
        dx = mouse_x - self.x
        dy = mouse_y - self.y
        angle = math.atan2(dy, dx)  # 라디안 반환
        return angle

class IDLE:

    def __init__(self, player):
        self.player = player

    def enter(self,e):
        pass

    def exit(self,e):
        pass

    def do(self,e,current_map):
        pass

    def draw(self):
        p = self.player

        if p.stopdirX < 0 and p.stopdirY < 0:  # 좌하
            p.image_idle.clip_draw(p.frame * 48, 0, 48, 56, p.x, p.y, p.scale, p.scale)
        elif p.stopdirX < 0 and p.stopdirY == 0:  # 좌
            p.image_idle.clip_draw(p.frame * 48, 56, 48, 56, p.x, p.y, p.scale, p.scale)
        elif p.stopdirX < 0 and p.stopdirY > 0:  # 좌상
            p.image_idle.clip_draw(p.frame * 48, 112, 48, 56, p.x, p.y, p.scale, p.scale)
        elif p.stopdirX == 0 and p.stopdirY > 0:  # 상
            p.image_idle.clip_draw(p.frame * 48, 168, 48, 56, p.x, p.y, p.scale, p.scale)
        elif p.stopdirX > 0 and p.stopdirY > 0:  # 우상
            p.image_idle.clip_draw(p.frame * 48, 224, 48, 56, p.x, p.y, p.scale, p.scale)
        elif p.stopdirX > 0 and p.stopdirY == 0:  # 우
            p.image_idle.clip_draw(p.frame * 48, 280, 48, 56, p.x, p.y, p.scale, p.scale)
        elif p.stopdirX > 0 and p.stopdirY < 0:  # 우하
            p.image_idle.clip_draw(p.frame * 48, 336, 48, 56, p.x, p.y, p.scale, p.scale)
        elif p.stopdirX == 0 and p.stopdirY < 0:  # 하
            p.image_idle.clip_draw(p.frame * 48, 392, 48, 56, p.x, p.y, p.scale, p.scale)
        else:
            p.image_idle.clip_draw(p.frame * 48, 0, 48, 56, p.x, p.y, p.scale, p.scale)  # 기본값


class RUN:

    def __init__(self, player):
        self.player = player

    def enter(self,e):


            # 키를 뗄 때는 멈추도록
        global last_input
        last_input = e
        print(last_input)

    def exit(self,e):
        pass

    def do(self,e,current_map):

        dx, dy = 0, 0

        # 눌린 키 전부 반영
        if SDLK_d in pressed_keys:
            dx += 1
        if SDLK_a in pressed_keys:
            dx -= 1
        if SDLK_w in pressed_keys:
            dy += 1
        if SDLK_s in pressed_keys:
            dy -= 1

        # 눌린 키가 없으면 IDLE 상태로
        if not pressed_keys:
            self.player.stopdirX = self.player.dirX
            self.player.stopdirY = self.player.dirY
            self.player.state_machine.handle_state_event(('AUTO', 'TO_IDLE'), current_map)
            return

        # 정규화
        length = math.sqrt(dx ** 2 + dy ** 2)
        if length != 0:
            dx /= length
            dy /= length
            self.player.dirX, self.player.dirY = dx, dy
        next_x = self.player.x + self.player.dirX * 5
        next_y = self.player.y + self.player.dirY * 5

        # 마을 경계처리
        if current_map == 2:
            if next_y >= 550 or next_y < 250:
                if next_x < 1040:
                    return
        self.player.x += self.player.dirX * 5
        self.player.y += self.player.dirY * 5

        # 화면 경계 처리
        if self.player.x < 0:
            self.player.x = 0
        elif self.player.x > 1400:
            self.player.x = 1400

        if self.player.y < 0:
            self.player.y = 0
        elif self.player.y > 800:
            self.player.y = 800




    def draw(self):
        p = self.player
        if p.dirX < 0 and p.dirY < 0:  # 좌하
            p.image_walking.clip_draw(p.frame * 48, 0, 48, 40, p.x, p.y, p.scale, p.scale)
        elif p.dirX < 0 and p.dirY == 0:  # 좌
            p.image_walking.clip_draw(p.frame * 48, 40, 48, 40, p.x, p.y, p.scale, p.scale)
        elif p.dirX < 0 and p.dirY > 0:  # 좌상
            p.image_walking.clip_draw(p.frame * 48, 80, 48, 40, p.x, p.y, p.scale, p.scale)
        elif p.dirX == 0 and p.dirY > 0:  # 상
            p.image_walking.clip_draw(p.frame * 48, 120, 48, 40, p.x, p.y, p.scale, p.scale)
        elif p.dirX > 0 and p.dirY > 0:  # 우상
            p.image_walking.clip_draw(p.frame * 48, 160, 48, 40, p.x, p.y, p.scale, p.scale)
        elif p.dirX > 0 and p.dirY == 0:  # 우
            p.image_walking.clip_draw(p.frame * 48, 200, 48, 40, p.x, p.y, p.scale, p.scale)
        elif p.dirX > 0 and p.dirY < 0:  # 우하
            p.image_walking.clip_draw(p.frame * 48, 240, 48, 40, p.x, p.y, p.scale, p.scale)
        elif p.dirX == 0 and p.dirY < 0:  # 하
            p.image_walking.clip_draw(p.frame * 48, 280, 48, 40, p.x, p.y, p.scale, p.scale)
        else:
            p.image_walking.clip_draw(p.frame * 48, 0, 48, 40, p.x, p.y, p.scale, p.scale)


class ATTACK:

    def __init__(self, player):
        self.player = player

    def enter(self,e):
        pass

    def exit(self,e):
        pass

    def do(self,e,current_map):
        pass

    def draw(self):
        p=self.player
        if p.stopdirX < 0 and p.stopdirY < 0:  # 좌하
            p.image_normal_attack.clip_draw(p.frame * 48, 0, 48, 56, p.x, p.y, p.scale, p.scale)
        elif p.stopdirX < 0 and p.stopdirY == 0:  # 좌
            p.image_normal_attack.clip_draw(p.frame * 48, 56, 48, 56, p.x, p.y, p.scale, p.scale)
        elif p.stopdirX < 0 and p.stopdirY > 0:  # 좌상
            p.image_normal_attack.clip_draw(p.frame * 48, 112, 48, 56, p.x, p.y, p.scale, p.scale)
        elif p.stopdirX == 0 and p.stopdirY > 0:  # 상
            p.image_normal_attack.clip_draw(p.frame * 48, 168, 48, 56, p.x, p.y, p.scale, p.scale)
        elif p.stopdirX > 0 and p.stopdirY > 0:  # 우상
            p.image_normal_attack.clip_draw(p.frame * 48, 224, 48, 56, p.x, p.y, p.scale, p.scale)
        elif p.stopdirX > 0 and p.stopdirY == 0:  # 우
            p.image_normal_attack.clip_draw(p.frame * 48, 280, 48, 56, p.x, p.y, p.scale, p.scale)
        elif p.stopdirX > 0 and p.stopdirY < 0:  # 우하
            p.image_normal_attack.clip_draw(p.frame * 48, 336, 48, 56, p.x, p.y, p.scale, p.scale)
        elif p.stopdirX == 0 and p.stopdirY < 0:  # 하
            p.image_normal_attack.clip_draw(p.frame * 48, 392, 48, 56, p.x, p.y, p.scale, p.scale)
        else:
            p.image_normal_attack.clip_draw(p.frame * 48, 0, 48, 56, p.x, p.y, p.scale, p.scale)  # 기본값