from pico2d import *

import handleEvent
from current_map import *
from state_machine import StateMachine
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_a,SDLK_w,SDLK_s,SDLK_d,SDLK_1,SDLK_2,SDLK_3,SDLK_4,SDLK_t
from player.playerskill import PlayerSkillManager
from player.playerskill import HekirekiIssen
from player.status import Status
import current_map
import game_framework
import game_world
width, height =  1400, 800
global last_input
pressed_keys = set()
def reset_pressed_keys():
    pressed_keys.clear()
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
def down_2(e):# 숫자 2이 눌렸을 때
    return e[0]=='INPUT' and e[1].type == SDL_KEYDOWN and e[1].key ==SDLK_2
def down_3(e):# 숫자 3이 눌렸을 때
    return e[0]=='INPUT' and e[1].type == SDL_KEYDOWN and e[1].key ==SDLK_3
def down_4(e):# 숫자 4이 눌렸을 때
    return e[0]=='INPUT' and e[1].type == SDL_KEYDOWN and e[1].key ==SDLK_4
def down_t(e):# 숫자 T가 눌렸을 때
    return e[0]=='INPUT' and e[1].type == SDL_KEYDOWN and e[1].key ==SDLK_t
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

TIME_PER_ACTION = 0.2
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

TIME_PER_SPEED = 1


class Bubble:
    def __init__(self, x, y, degree):
        self.x = x
        self.y = y
        self.degree = degree
        self.speed = 50
        self.image = load_image(os.path.join('asset/player','bubble.png'))
        self.scale=32
        self.active=True
        self.damage=5
    def update(self):
        #각도를 기준으로 이동

        self.x += math.cos(self.degree) * self.speed*game_framework.frame_time*10
        self.y += math.sin(self.degree) * self.speed*game_framework.frame_time*10
        if self.x < 0 or self.x > width or self.y < 0 or self.y > height:
            game_world.remove_object(self)

    def draw(self):
        self.image.draw(self.x, self.y,self.scale,self.scale)
        draw_rectangle(*self.get_bb())
    def get_bb(self):
        return self.x - 16, self.y - 16, self.x + 16, self.y + 16

    def handle_collision(self, group, other):
        if group == 'bubble:enemy':
            game_world.remove_object(self)

class Character:
    def __init__(self,cm, x=100, y=100):
        #필요한 정보
        self.current_map = cm
        self.max_HP = 100
        self.cur_HP = 100

        self.frame_timer = 0
        self.frame_interval = 0.2
        # 위치
        self.x = x
        self.y = y
        self.scale=100   #크기

        # 이동 방향
        self.dirX = 0
        self.dirY = 0
        self.speed = 30.0
        self.dash_speed=150.0
        self.dash_duration=0.0
        self.dash_cooldown=1.0

        # 현재 모션 상태
        self.motion_state = 'idle'
        self.attack_anim_timer = 0
        # 멈춘 방향 (캐릭터가 마지막으로 바라본 방향)
        self.stopdirX = 0
        self.stopdirY = -1  # 기본값: 아래쪽

        # 레벨
        self.level = 1
        self.max_exp = 100
        self.exp = 0
        self.skill_points = 0

        #적에게 맞았을 때 생기는 효과
        self.slow_effect_timer=0.0
        self.is_hit=False
        self.hit_effect_timer=0.0
        self.push_degree=0.0

        #공격 및 스킬
        self.attack_manager = AttackManager(1.5)  # 1.5초 쿨타임
        self.skill_manager=PlayerSkillManager(self)
        self.lock_move=False

        self.IDLE = IDLE(self)
        self.RUN = RUN(self)
        self.ATTACK = ATTACK(self)

        self.SKILL=SKILL(self)
        self.state_machine = StateMachine(
            self.IDLE,  # <-시작상태 지정
            {
                self.IDLE: {
                    down_1: self.SKILL,
                    down_2: self.SKILL,
                    down_3: self.SKILL,
                    down_4: self.SKILL,
                    key_down: self.RUN,
                    click_left_down: self.ATTACK,


                },
                self.RUN: {
                    down_1: self.SKILL,
                    down_2: self.SKILL,
                    down_3: self.SKILL,
                    down_4: self.SKILL,
                    key_down: self.RUN,
                    key_up: self.RUN,
                    click_left_down: self.ATTACK,


                },
                self.ATTACK: {
                    down_1: self.SKILL,
                    down_2: self.SKILL,
                    down_3: self.SKILL,
                    down_4: self.SKILL,
                    click_left_up: self.RUN,
                    key_down: self.RUN,
                    key_up: self.RUN,

                },
                self.SKILL:{
                    key_down: self.RUN,
                    key_up: self.RUN,
                    click_left_down: self.ATTACK,

                },

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
        draw_rectangle(*self.get_bb())
    def update(self):
        if self.is_hit:
            self.hit_effect_timer-=game_framework.frame_time
            if self.hit_effect_timer<=0.0:
                self.is_hit=False
            else:
                #넉백효과
                push_distance=100.0*game_framework.frame_time*10.0*self.hit_effect_timer
                self.x+=math.cos(self.push_degree)*push_distance
                self.y+=math.sin(self.push_degree)*push_distance
        else: self.state_machine.update(self.current_map)
        self.update_frame()
        self.skill_manager.update()
        #상태이상효과 타이머 감소하는거
        if self.slow_effect_timer>0.0:
            self.slow_effect_timer-=game_framework.frame_time
            if self.slow_effect_timer<0.0:
                self.slow_effect_timer=0.0
        #대쉬관련
        if self.dash_duration>0.0:
            self.dash_duration-=game_framework.frame_time
            if self.dash_duration<0.0:
                self.dash_duration=0.0
                self.dash_cooldown=1.0  #대쉬끝나면 쿨타임 시작
        if self.dash_cooldown>0.0:
            self.dash_cooldown-=game_framework.frame_time
            if self.dash_cooldown<0.0:
                self.dash_cooldown=0.0

    def update_frame(self):
        # 공격, 이동, 대기 상태별로 다르게 처리
        if self.motion_state == 'normal_attack':
            TIME_PER_ACTION = 0.4  # 공격 애니메이션 한 번 도는 데 걸리는 시간
            FRAMES_PER_ACTION = 5
        elif self.dirX == 0 and self.dirY == 0:
            TIME_PER_ACTION = 0.8  # idle은 느리게
            FRAMES_PER_ACTION = 7
        else:
            TIME_PER_ACTION = 0.5  # 걷기는 보통 속도
            FRAMES_PER_ACTION = 4

        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

        # 실제 프레임 시간 기반으로 프레임 계산
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

        # 공격 애니메이션 끝나면 idle로 복귀
        if self.attack_anim_timer > 0.0:
            self.attack_anim_timer -= game_framework.frame_time
            if self.attack_anim_timer <= 0.0:
                self.attack_anim_timer = 0.0
                self.motion_state = 'idle'
                self.frame = 0

    def handle_event(self, event,current_map):

        self.state_machine.handle_state_event(('INPUT',event),current_map)
    def get_pos(self):
        return (self.x, self.y)

    def get_angle(self,mouse_x, mouse_y):
        dx = mouse_x - self.x
        dy = mouse_y - self.y
        angle = math.atan2(dy, dx)  # 라디안 반환
        return angle
    def get_bb(self):
        return self.x - 25, self.y - 20, self.x + 25, self.y + 60

    def handle_collision(self, group, other):
        ishit=False
        if self.dash_duration>0.0:
            #대쉬중에는 피격무시
            return
        if group == 'player:enemy':
            if hasattr(other, 'swimming_mode'):
                # 예: 스위머가 수영 상태이고 hit_timer가 일정 이상이면 강타
                if getattr(other, 'hit_timer', 0) >= 0.2:
                    self.cur_HP -= other.damage
                    if self.cur_HP < 0:
                        self.cur_HP = 0
                    ishit=True
            elif hasattr(other, 'dashing'):
                # 예: 스위머가 수영 상태이고 hit_timer가 일정 이상이면 강타
                if getattr(other, 'hit_timer', 0) >= 0.2:
                    self.cur_HP -= other.damage
                    if self.cur_HP < 0:
                        self.cur_HP = 0
                ishit = True
                print(f'Player HP: {self.cur_HP}/{self.max_HP}')
            else:

                self.cur_HP -= other.damage
                if self.cur_HP < 0:
                    self.cur_HP = 0
                ishit = True

                print(f'Player HP: {self.cur_HP}/{self.max_HP}')
        if ishit:
            self.push_degree=math.atan2(self.y-other.y,self.x-other.x)
            self.hit_effect_timer=0.2
            self.is_hit=True
            HIT_EFFECT(self,other.damage)

    def gain_exp(self, amount):
        self.exp += amount
        print(f"EXP +{amount} ({self.exp}/{self.max_exp})")

        #  레벨업 체크
        while self.exp >= self.max_exp:
            self.exp -= self.max_exp
            self.level_up()
            self.hp_update()
    def hp_update(self):
        #레벨업시 최대체력으로회복및 최대체력1.1배증가
        self.max_HP = int(self.max_HP * 1.1)
        self.cur_HP = self.max_HP

    def level_up(self):
        self.level += 1
        #5레벨당 스킬포인트 지급
        if self.level % 5 == 0:
            self.skill_points += 1
            print(f" Skill Point +1 (Total: {self.skill_points})")
        self.max_exp = int(self.max_exp * 1.2)
        print(f" LEVEL UP! Lv.{self.level} | Next EXP: {self.max_exp}")
    def hit_check(self,e):
        return self.is_hit

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
            p.image_idle.clip_draw(int(p.frame) * 48, 0, 48, 56, p.x, p.y, p.scale, p.scale)
        elif p.stopdirX < 0 and p.stopdirY == 0:  # 좌
            p.image_idle.clip_draw(int(p.frame) * 48, 56, 48, 56, p.x, p.y, p.scale, p.scale)
        elif p.stopdirX < 0 and p.stopdirY > 0:  # 좌상
            p.image_idle.clip_draw(int(p.frame) * 48, 112, 48, 56, p.x, p.y, p.scale, p.scale)
        elif p.stopdirX == 0 and p.stopdirY > 0:  # 상
            p.image_idle.clip_draw(int(p.frame) * 48, 168, 48, 56, p.x, p.y, p.scale, p.scale)
        elif p.stopdirX > 0 and p.stopdirY > 0:  # 우상
            p.image_idle.clip_draw(int(p.frame) * 48, 224, 48, 56, p.x, p.y, p.scale, p.scale)
        elif p.stopdirX > 0 and p.stopdirY == 0:  # 우
            p.image_idle.clip_draw(int(p.frame) * 48, 280, 48, 56, p.x, p.y, p.scale, p.scale)
        elif p.stopdirX > 0 and p.stopdirY < 0:  # 우하
            p.image_idle.clip_draw(int(p.frame) * 48, 336, 48, 56, p.x, p.y, p.scale, p.scale)
        elif p.stopdirX == 0 and p.stopdirY < 0:  # 하
            p.image_idle.clip_draw(int(p.frame) * 48, 392, 48, 56, p.x, p.y, p.scale, p.scale)
        else:
            p.image_idle.clip_draw(int(p.frame) * 48, 0, 48, 56, p.x, p.y, p.scale, p.scale)  # 기본값


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
        if self.player.lock_move:
            return
        if self.player.is_hit:
            return
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
            self.player.state_machine.cur_state = self.player.IDLE
            #self.player.state_machine.handle_state_event(('AUTO', 'IDLE'), current_map)
            return

        # 정규화
        length = math.sqrt(dx ** 2 + dy ** 2)
        if length != 0:
            dx /= length
            dy /= length
            self.player.dirX, self.player.dirY = dx, dy
        if self.player.slow_effect_timer>0.0:
            #느려지는 효과 적용
            next_x = self.player.x + self.player.dirX * self.player.speed*0.5*game_framework.frame_time*10.0
            next_y = self.player.y + self.player.dirY * self.player.speed*0.5*game_framework.frame_time*10.0
        elif self.player.dash_duration>0.0:
            next_x = self.player.x + self.player.dirX * self.player.dash_speed*game_framework.frame_time*10.0
            next_y = self.player.y + self.player.dirY * self.player.dash_speed*game_framework.frame_time*10.0
        else:
            next_x = self.player.x + self.player.dirX * self.player.speed*game_framework.frame_time*10.0
            next_y = self.player.y + self.player.dirY * self.player.speed*game_framework.frame_time*10.0

        # 마을 경계처리
        if current_map.get_current_map() == 2:
        #if current_map.get_current_map == 2:
            if next_y >= 550 or next_y < 250:
                if next_x < 1040:
                    return
        #일반 경계처리

        self.player.x = next_x
        self.player.y =  next_y

        # 화면 경계 처리
        transition = None

        if next_x > 1400:
            transition = current_map.get_transition( "east")
        elif next_x < 0:
            transition = current_map.get_transition( "west")
        elif next_y > 800:
            transition = current_map.get_transition( "north")
        elif next_y < 0:
            transition = current_map.get_transition( "south")

        if transition:
            next_map_id, spawn_x, spawn_y = transition
            print(f" 맵 {current_map.get_current_map()} -> {next_map_id} 이동")
            current_map.change_map(next_map_id)
            self.player.x, self.player.y = spawn_x, spawn_y
            return




    def draw(self):
        p = self.player
        if p.dirX < 0 and p.dirY < 0:  # 좌하
            p.image_walking.clip_draw(int(p.frame) * 48, 0, 48, 40, p.x, p.y, p.scale, p.scale)
        elif p.dirX < 0 and p.dirY == 0:  # 좌
            p.image_walking.clip_draw(int(p.frame) * 48, 40, 48, 40, p.x, p.y, p.scale, p.scale)
        elif p.dirX < 0 and p.dirY > 0:  # 좌상
            p.image_walking.clip_draw(int(p.frame) * 48, 80, 48, 40, p.x, p.y, p.scale, p.scale)
        elif p.dirX == 0 and p.dirY > 0:  # 상
            p.image_walking.clip_draw(int(p.frame) * 48, 120, 48, 40, p.x, p.y, p.scale, p.scale)
        elif p.dirX > 0 and p.dirY > 0:  # 우상
            p.image_walking.clip_draw(int(p.frame) * 48, 160, 48, 40, p.x, p.y, p.scale, p.scale)
        elif p.dirX > 0 and p.dirY == 0:  # 우
            p.image_walking.clip_draw(int(p.frame)* 48, 200, 48, 40, p.x, p.y, p.scale, p.scale)
        elif p.dirX > 0 and p.dirY < 0:  # 우하
            p.image_walking.clip_draw(int(p.frame) * 48, 240, 48, 40, p.x, p.y, p.scale, p.scale)
        elif p.dirX == 0 and p.dirY < 0:  # 하
            p.image_walking.clip_draw(int(p.frame) * 48, 280, 48, 40, p.x, p.y, p.scale, p.scale)
        else:
            p.image_walking.clip_draw(int(p.frame) * 48, 0, 48, 40, p.x, p.y, p.scale, p.scale)


class ATTACK:

    def __init__(self, player):
        self.player = player
        self.dirX=player.dirX
        self.dirY=player.dirY
    def enter(self,e):
        if self.player.attack_manager.trigger_attack(get_time()):
            (x, y) = handleEvent.get_mouse_pos()
            print(f'Attack at mouse position: ({x}, {y})')
            bubble = Bubble(self.player.x, self.player.y, self.player.get_angle(x, y))
            game_world.add_object(bubble, 2)
            game_world.add_collision_pair('bubble:enemy', bubble, None)
            #버블방향에 맞게 플레이어 각도수정
            if x - self.player.x !=0 or y - self.player.y !=0:
                dx = x - self.player.x
                dy = y - self.player.y
                length = math.sqrt(dx ** 2 + dy ** 2)
                if length != 0:
                    dx /= length
                    dy /= length
                    self.dirX=self.player.dirX=self.player.stopdirX = int(round(dx))
                    self.dirY=self.player.dirY=self.player.stopdirY = int(round(dy))

            pass

    def exit(self,e):
        pass

    def do(self,e,current_map):

        pass

    def draw(self):
        p=self.player
        if p.stopdirX < 0 and p.stopdirY < 0:  # 좌하
            p.image_normal_attack.clip_draw(int(p.frame) * 48, 0, 48, 56, p.x, p.y, p.scale, p.scale)
        elif p.stopdirX < 0 and p.stopdirY == 0:  # 좌
            p.image_normal_attack.clip_draw(int(p.frame) * 48, 56, 48, 56, p.x, p.y, p.scale, p.scale)
        elif p.stopdirX < 0 and p.stopdirY > 0:  # 좌상
            p.image_normal_attack.clip_draw(int(p.frame) * 48, 112, 48, 56, p.x, p.y, p.scale, p.scale)
        elif p.stopdirX == 0 and p.stopdirY > 0:  # 상
            p.image_normal_attack.clip_draw(int(p.frame) * 48, 168, 48, 56, p.x, p.y, p.scale, p.scale)
        elif p.stopdirX > 0 and p.stopdirY > 0:  # 우상
            p.image_normal_attack.clip_draw(int(p.frame) * 48, 224, 48, 56, p.x, p.y, p.scale, p.scale)
        elif p.stopdirX > 0 and p.stopdirY == 0:  # 우
            p.image_normal_attack.clip_draw(int(p.frame) * 48, 280, 48, 56, p.x, p.y, p.scale, p.scale)
        elif p.stopdirX > 0 and p.stopdirY < 0:  # 우하
            p.image_normal_attack.clip_draw(int(p.frame) * 48, 336, 48, 56, p.x, p.y, p.scale, p.scale)
        elif p.stopdirX == 0 and p.stopdirY < 0:  # 하
            p.image_normal_attack.clip_draw(int(p.frame) * 48, 392, 48, 56, p.x, p.y, p.scale, p.scale)
        else:
            p.image_normal_attack.clip_draw(int(p.frame) * 48, 0, 48, 56, p.x, p.y, p.scale, p.scale)  # 기본값

    def draw(self):
        p = self.player
        if p.dirX < 0 and p.dirY < 0:  # 좌하
            p.image_walking.clip_draw(int(p.frame) * 48, 0, 48, 40, p.x, p.y, p.scale, p.scale)
        elif p.dirX < 0 and p.dirY == 0:  # 좌
            p.image_walking.clip_draw(int(p.frame) * 48, 40, 48, 40, p.x, p.y, p.scale, p.scale)
        elif p.dirX < 0 and p.dirY > 0:  # 좌상
            p.image_walking.clip_draw(int(p.frame) * 48, 80, 48, 40, p.x, p.y, p.scale, p.scale)
        elif p.dirX == 0 and p.dirY > 0:  # 상
            p.image_walking.clip_draw(int(p.frame) * 48, 120, 48, 40, p.x, p.y, p.scale, p.scale)
        elif p.dirX > 0 and p.dirY > 0:  # 우상
            p.image_walking.clip_draw(int(p.frame) * 48, 160, 48, 40, p.x, p.y, p.scale, p.scale)
        elif p.dirX > 0 and p.dirY == 0:  # 우
            p.image_walking.clip_draw(int(p.frame)* 48, 200, 48, 40, p.x, p.y, p.scale, p.scale)
        elif p.dirX > 0 and p.dirY < 0:  # 우하
            p.image_walking.clip_draw(int(p.frame) * 48, 240, 48, 40, p.x, p.y, p.scale, p.scale)
        elif p.dirX == 0 and p.dirY < 0:  # 하
            p.image_walking.clip_draw(int(p.frame) * 48, 280, 48, 40, p.x, p.y, p.scale, p.scale)
        else:
            p.image_walking.clip_draw(int(p.frame) * 48, 0, 48, 40, p.x, p.y, p.scale, p.scale)

#스킬도 상태로 구현하기위한 그런거
class SKILL:

    def __init__(self, player):
        self.player = player
        self.timer=0.0


    def enter(self,e):
        self.timer=0.0
        #입력된 이벤트에 따라 해당 스킬 생성
        if down_1(e):
            self.player.skill_manager.use_skill(1)
        elif down_2(e):
            self.player.skill_manager.use_skill(2)
        elif down_3(e):
            self.player.skill_manager.use_skill(3)
        elif down_4(e):
            self.player.skill_manager.use_skill(4)
        pass

    def exit(self,e):
        pass

    def do(self,e,current_map):
        self.player.skill_manager.update()
        if self.player.skill_manager.timer<0.0:
            #IDLE상태로
            self.player.skill_manager.timer=2.0

            self.player.state_machine.cur_state = self.player.RUN
            self.player.state_machine.handle_state_event(('AUTO', 'TO_IDLE'), current_map)



    def draw(self):
        if isinstance(self.player.skill_manager.cur_using_skill,HekirekiIssen):
            return
        else:
            self.player.IDLE.draw()
        pass

class HIT_EFFECT:
    def __init__(self, player,dmg):
        self.font = load_font('asset/screen/intro/introFont.ttf', 30)
        self.player = player
        self.timer=0.3  #맞는 효과 지속시간
        self.y=player.y
        self.dmg=dmg
        self.offset=player.scale/2
        game_world.add_object(self,3)

    def update(self):
        self.timer-=game_framework.frame_time
        self.offset+=50*game_framework.frame_time
        if self.timer<=0.0:
            game_world.remove_object(self)



    def draw(self):
        self.font.draw(self.player.x-self.player.scale//4, self.y + self.offset, f"{self.dmg}", (255, 0, 0))