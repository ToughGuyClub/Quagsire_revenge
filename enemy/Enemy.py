from pico2d import *
import math
import random

import game_world
from enemy.enemy_state_machine import EnemyStateMachine
import os
import game_framework
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

TIME_PER_SPEED = 1
def create_enemy(enemy_type, x, y, player):
    if enemy_type == "researcher":
        return Researcher(x, y,1,player)
    elif enemy_type == "doctor":
        return Doctor(x, y,2,player)
    elif enemy_type == "ruinmaniac":
        return Ruinmaniac(x,y,3,player)
    elif enemy_type == "ranger":
        return Ranger(x, y,4,player)
    elif enemy_type == "swimmer":
        return Swimmer(x, y,5,player)
    elif enemy_type == "captin":
        return Captin(x, y,6,player)

def level_to_image(level):
    level_images = {
        1: 'level1ball.png',
        2: 'level2ball.png',
        3: 'level3ball.png',
        4: 'level4ball.png',
        5: 'level5ball.png',
        6: 'level6ball.png',
    }
    return level_images.get(level, 'level1ball.png')
class Enemy:
    def __init__(self, x, y, type, player, file_name, frame_w=32, frame_h=48, scale=70):
        # --- 이미지 관련 ---
        self.image = load_image(os.path.join('asset/enemy', file_name))
        self.frame_w = frame_w
        self.frame_h = frame_h
        self.scale = scale

        # --- 스탯 관련 ---
        self.HP = type * 10
        self.ball_image = load_image(os.path.join('asset/enemy', level_to_image(type)))
        self.type = type
        self.speed = 2.0
        self.is_enemy = True

        # --- 위치 관련 ---
        self.x = x
        self.y = y
        self.dirX = 0
        self.dirY = 0
        self.frame = 0
        self.frame_time = 0.3

        #--- 상태이상 ---
        self.flashed = False
        self.flash_timer = 0.0

        # --- 플레이어 참조 ---
        self.target_player = player

        # --- 상태머신 초기화 ---
        self.IDLE = EnemyIdle(self)
        self.RUN = EnemyRun(self)
        self.ATTACK = EnemyAttack(self)
        self.state_machine = EnemyStateMachine(
            self.IDLE,
            {
                self.IDLE: {self.detect_player: self.RUN},
                self.RUN: {self.lost_player: self.IDLE, self.in_attack_range: self.ATTACK},
                self.ATTACK: {self.lost_player: self.IDLE}
            }
        )

        # --- 게임 월드 등록 ---
        game_world.add_object(self, 1)
        game_world.add_collision_pair('bubble:enemy', None, self)
        game_world.add_collision_pair('cannon:enemy', None, self)
        game_world.add_collision_pair('EQ:enemy', None, self)

    # ------------------------------
    # 감지 / 공격 / 잃음 범위 관련
    # ------------------------------
    def detect_player(self, e):
        player = e
        distance = math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)
        return distance < 400

    def in_attack_range(self, e):
        player = e
        distance = math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)
        return distance < 300

    def lost_player(self, e):
        player = e
        distance = math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)
        return distance > 500

    # ------------------------------
    # 업데이트 및 드로우
    # ------------------------------
    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

        dx = self.target_player.x - self.x
        dy = self.target_player.y - self.y
        if abs(dx) > abs(dy):
            self.dirX = 1 if dx > 0 else -1
            self.dirY = 0
        else:
            self.dirY = 1 if dy > 0 else -1
            self.dirX = 0

        self.state_machine.update(self.target_player)

    def attack_action(self, player):
        """기본 공격: 몬스터볼 한 발"""
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.sqrt(dx ** 2 + dy ** 2)
        if dist != 0:
            dirX = dx / dist
            dirY = dy / dist
        else:
            dirX, dirY = 0, 0

        ball = AttackBall(
            self.ball_image,
            self.x,
            self.y,
            dirX,
            dirY,
            self.type,
            speed=10,
        )
        game_world.add_object(ball, 2)
        game_world.add_collision_pair('player:enemy', None, ball)
        game_world.add_collision_pair('EQ:enemy', None, ball)
    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    # ------------------------------
    # 상/하 분리 드로우 (thunder_scene용)
    # ------------------------------
    def draw_half(self):
        from screen.thunder_scene import get_half_stack
        step = get_half_stack()

        enemy = self

        # 상부 몸체
        if enemy.dirX == 0 and enemy.dirY == 0:
            enemy.image.clip_draw(0, 3*enemy.frame_h+(enemy.frame_h//2), enemy.frame_w, enemy.frame_h//2, enemy.x + step, enemy.y + enemy.scale / 4, enemy.scale,
                                  enemy.scale / 2)
        elif enemy.dirX == -1:
            enemy.image.clip_draw(0, 2*enemy.frame_h+(enemy.frame_h//2), enemy.frame_w, enemy.frame_h//2, enemy.x + step, enemy.y + enemy.scale / 4, enemy.scale,
                                  enemy.scale / 2)
        elif enemy.dirX == 1:
            enemy.image.clip_draw(0, enemy.frame_h+(enemy.frame_h//2), enemy.frame_w, enemy.frame_h//2, enemy.x + step, enemy.y + enemy.scale / 4, enemy.scale,
                                  enemy.scale / 2)
        elif enemy.dirY == 1:
            enemy.image.clip_draw(0, enemy.frame_h//2, enemy.frame_w, enemy.frame_h//2, enemy.x + step, enemy.y + enemy.scale / 4, enemy.scale,
                                  enemy.scale / 2)
        elif enemy.dirY == -1:
            enemy.image.clip_draw(0, 3*enemy.frame_h+(enemy.frame_h//2), enemy.frame_w, enemy.frame_h//2, enemy.x + step, enemy.y + enemy.scale / 4, enemy.scale,
                                  enemy.scale / 2)

        # 하부 몸체
        if enemy.dirX == 0 and enemy.dirY == 0:
            enemy.image.clip_draw(0, 3*enemy.frame_h, enemy.frame_w, enemy.frame_h//2, enemy.x - step, enemy.y - enemy.scale / 4, enemy.scale,
                                  enemy.scale / 2)
        elif enemy.dirX == -1:
            enemy.image.clip_draw(0, 2*enemy.frame_h, enemy.frame_w, enemy.frame_h//2, enemy.x - step, enemy.y - enemy.scale / 4, enemy.scale,
                                  enemy.scale / 2)
        elif enemy.dirX == 1:
            enemy.image.clip_draw(0, enemy.frame_h, enemy.frame_w, enemy.frame_h//2, enemy.x - step, enemy.y - enemy.scale / 4, enemy.scale,
                                  enemy.scale / 2)
        elif enemy.dirY == 1:
            enemy.image.clip_draw(0, 0, enemy.frame_w, enemy.frame_h//2, enemy.x - step, enemy.y - enemy.scale / 4, enemy.scale, enemy.scale / 2)
        elif enemy.dirY == -1:
            enemy.image.clip_draw(0, 3*enemy.frame_h, enemy.frame_w, enemy.frame_h//2, enemy.x - step, enemy.y - enemy.scale / 4, enemy.scale,
                                  enemy.scale / 2)
    # ------------------------------
    # 충돌 / 피격 처리
    # ------------------------------
    def get_bb(self):
        return self.x - self.scale / 2, self.y - self.scale / 2, self.x + self.scale / 2, self.y + self.scale / 2

    def handle_collision(self, group, other):
        if group in ('bubble:enemy', 'cannon:enemy', 'EQ:enemy'):
            self.HP -= 1 * other.damage

        if self.HP <= 0:
            if hasattr(self.target_player, "gain_exp"):
                self.target_player.gain_exp(self.type * 20)
            game_world.remove_object(self)

class EnemyIdle:
    def __init__(self, enemy):
        self.enemy = enemy

    def enter(self, player):
        self.enemy.dirX = self.enemy.dirY = 0

    def exit(self, player):
        pass

    def do(self, player):
        # 가끔 랜덤하게 살짝 움직임
        if random.random() < 0.02:
            self.enemy.x += random.choice([-1, 0, 1]) * self.enemy.speed
            self.enemy.y += random.choice([-1, 0, 1]) * self.enemy.speed

    def draw(self):
        e = self.enemy
        fw, fh = e.frame_w, e.frame_h
        sx = 0

        if e.dirX == 0 and e.dirY == 0:
            sy = fh * 3
        elif e.dirX == -1:
            sy = fh * 2
        elif e.dirX == 1:
            sy = fh
        elif e.dirY == 1:
            sy = 0
        elif e.dirY == -1:
            sy = fh * 3
        else:
            sy = fh * 3

        e.image.clip_draw(sx, sy, fw, fh, e.x, e.y, e.scale, e.scale)
class EnemyRun:
    def __init__(self, enemy):
        self.enemy = enemy

    def enter(self, player):
        pass

    def exit(self, player):
        pass

    def do(self, player):
        if self.enemy.flashed:
            self.enemy.flash_timer += game_framework.frame_time
            if self.enemy.flash_timer >= 2.0:
                self.enemy.flashed = False
                self.enemy.flash_timer = 0.0
            return
        e = self.enemy
        dx = player.x - e.x
        dy = player.y - e.y
        dist = math.sqrt(dx ** 2 + dy ** 2)
        if dist > 0:
            dx, dy = dx / dist, dy / dist
            e.x += dx * e.speed * game_framework.frame_time * e.speed * 10.0
            e.y += dy * e.speed * game_framework.frame_time * e.speed * 10.0

        # 방향 업데이트
        if abs(dx) > abs(dy):
            e.dirX = 1 if dx > 0 else -1
            e.dirY = 0
        else:
            e.dirY = 1 if dy > 0 else -1
            e.dirX = 0

    def draw(self):
        e = self.enemy
        fw, fh = e.frame_w, e.frame_h
        fx = int(e.frame) * fw

        if e.dirX == -1:
            fy = fh * 2
        elif e.dirX == 1:
            fy = fh
        elif e.dirY == 1:
            fy = 0
        elif e.dirY == -1:
            fy = fh * 3
        else:
            fy = fh * 3

        e.image.clip_draw(fx, fy, fw, fh, e.x, e.y, e.scale, e.scale)
class EnemyAttack:
    def __init__(self, enemy):
        self.enemy = enemy
        self.cooldown = 1.0
        self.timer = 0

    def enter(self, player):
        self.timer = 0

    def exit(self, player):
        pass

    def do(self, player):
        if self.enemy.flashed:
            self.enemy.flash_timer += game_framework.frame_time
            if self.enemy.flash_timer >= 2.0:
                self.enemy.flashed = False
                self.enemy.flash_timer = 0.0
            return
        self.timer += game_framework.frame_time
        if self.timer >= self.cooldown:
            self.timer = 0
            #  공격 행위는 Enemy 객체에 위임
            self.enemy.attack_action(player)

    def draw(self):
        e = self.enemy
        fw, fh = e.frame_w, e.frame_h
        fx = int(e.frame) * fw

        if e.dirX == -1:
            fy = fh * 2
        elif e.dirX == 1:
            fy = fh
        elif e.dirY == 1:
            fy = 0
        elif e.dirY == -1:
            fy = fh * 3
        else:
            fy = fh * 3

        e.image.clip_draw(fx, fy, fw, fh, e.x, e.y, e.scale, e.scale)

class AttackBall:
    def __init__(self, image, x, y, dirX, dirY,level ,speed=10 ):
        self.image = image
        self.x = x
        self.y = y
        self.dirX = dirX
        self.dirY = dirY
        self.speed = speed
        self.scale = 32
        self. frame = 0
        self.level = level
        self.frame_time = 0.1
    def update(self):
        self.x += self.dirX * self.speed*game_framework.frame_time* self.speed*5.0
        self.y += self.dirY * self.speed*game_framework.frame_time* self.speed*5.0
        if self.frame_time <= 0:
            self.frame_time = 0.1
            self.frame = (self.frame + 1) % 8
        self.frame_time -= game_framework.frame_time
        #경계처리
        if self.x < 0 or self.x > 1600 or self.y < 0 or self.y > 900:
            game_world.remove_object(self)

    def draw(self):
        self.image.clip_draw(self.frame * 32, 0, 32, 64, self.x, self.y, 32, 64)
        draw_rectangle(*self.get_bb())
    def get_bb(self):
        return self.x - self.scale/2 , self.y - self.scale/2 , self.x + self.scale/2 , self.y + self.scale/2
    def handle_collision(self, group, other):
        if group == 'player:enemy':
            game_world.remove_object(self)
        elif group == 'EQ:enemy':
            game_world.remove_object(self)


class Researcher(Enemy):
    def __init__(self, x, y, type,player):
        super().__init__(x, y, type,player,'trainer_SCIENTIST.png')
class Doctor(Enemy):
    def __init__(self, x, y, type,player):
        super().__init__(x, y, type,player,'trainer_BURGLAR.png')

        self.attack_count = 0
    def attack_action(self, player):
        self.attack_count += 1
        if self.attack_count % 4 == 0:
            # 폭탄 발사
            dx = player.x - self.x
            dy = player.y - self.y
            dist = math.sqrt(dx ** 2 + dy ** 2)
            if dist != 0:
                dirX, dirY = dx / dist, dy / dist
            else:
                dirX, dirY = 0, 0
            bomb = BombAttack(self.x, self.y, dirX, dirY)
            game_world.add_object(bomb, 2)
            game_world.add_collision_pair('player:enemy', None, bomb)
            game_world.add_collision_pair('EQ:enemy', None, bomb)
        else:
            super().attack_action(player)
class Ruinmaniac(Enemy):
    def __init__(self, x, y, type,player):
        super().__init__(x, y, type,player,'trainer_RUINMANIAC.png')
class Ranger(Enemy):
    def __init__(self, x, y, type,player):
        super().__init__(x, y, type,player,'trainer_POKEMONRANGER_F.png')

    def attack_action(self, player):
        #거미줄 발사
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.sqrt(dx ** 2 + dy ** 2)
        if dist != 0:
            dirX, dirY = dx / dist, dy / dist
        else:
            dirX, dirY = 0, 0
        slow = SLOWATTACK(self.x, self.y, dirX, dirY)
        game_world.add_object(slow, 2)
        game_world.add_collision_pair('player:enemy', None, slow)
        game_world.add_collision_pair('EQ:enemy', None, slow)
class Swimmer(Enemy):
    def __init__(self, x, y, type, player):
        super().__init__(x, y, type, player, 'trainer_SWIMMER_M.png')
        self.swimming_image = load_image(os.path.join('asset/enemy', 'trainer_SWIMMER2_M.png'))
        self.swimming_mode = False
        self.swim_timer = 0.0
        self.degree = 0.0
        self.attack_count = 0
        self.hit_timer = 0.0
    def attack_action(self, player):

        # 이미 수영중이면 공격 불가
        if self.swimming_mode:
            return

        # 공격 카운트 증가
        self.attack_count += 1

        # 4번째마다 수영 모드 시작
        if self.attack_count % 4 == 0:
            self.swimming_mode = True
            self.swim_timer = 3.0

            dx = player.x - self.x
            dy = player.y - self.y
            self.degree = math.atan2(dy, dx)
            #충돌박스에 추가
            game_world.add_collision_pair('player:enemy', None, self)
        else:
            # 기본 공격 수행
            super().attack_action(player)

    def update(self):
        if not self.swimming_mode:
            super().update()
            return

        # 수영중 이동
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

        self.x += math.cos(self.degree) * self.speed*20.0 * game_framework.frame_time * self.speed * 10.0
        self.y += math.sin(self.degree) * self.speed*20.0 * game_framework.frame_time * self.speed * 10.0
        if self.hit_timer <= 1.0:
            self.hit_timer += game_framework.frame_time

            # 왼쪽/오른쪽 벽
        if self.x < 0:
            self.x = 0
            self.degree = math.pi - self.degree  # 반사

        elif self.x > 1600:
            self.x = 1600
            self.degree = math.pi - self.degree

            # 위/아래 벽
        if self.y < 0:
            self.y = 0
            self.degree = -self.degree

        elif self.y >850:
            self.y = 850
            self.degree = -self.degree
        # 방향 갱신 (draw에서 방향을 쓰기 때문에)
        if abs(math.cos(self.degree)) > abs(math.sin(self.degree)):
            self.dirX = 1 if math.cos(self.degree) > 0 else -1
            self.dirY = 0
        else:
            self.dirY = 1 if math.sin(self.degree) > 0 else -1
            self.dirX = 0

        self.swim_timer -= game_framework.frame_time
        if self.swim_timer <= 0:
            self.swimming_mode = False
            # 충돌박스 제거


    def draw(self):
        if not self.swimming_mode:
            super().draw()
            return

        fw, fh = self.frame_w, self.frame_h
        fx = int(self.frame) * fw

        if self.dirX == -1:
            fy = fh * 2
        elif self.dirX == 1:
            fy = fh
        elif self.dirY == 1:
            fy = 0
        elif self.dirY == -1:
            fy = fh * 3
        else:
            fy = fh * 3

        self.swimming_image.clip_draw(fx, fy, fw, fh, self.x, self.y, self.scale, self.scale)
    def handle_collision(self, group, other):
        if group in ('bubble:enemy', 'cannon:enemy', 'EQ:enemy'):
            self.HP -= 1 * other.damage
        if self.HP <= 0:
            if hasattr(self.target_player, "gain_exp"):
                self.target_player.gain_exp(self.type * 20)
            game_world.remove_object(self)
        if group == 'player:enemy' and self.swimming_mode:
            if self.hit_timer >= 1.0:
                self.hit_timer = 0.0

class Captin(Enemy):
    def __init__(self, x, y, type,player):
        super().__init__(x, y, type,player,'trainer_SAILOR.png')
class BombAttack:
    def __init__(self, x, y, dirX, dirY ):
        self.image = load_image(os.path.join('asset/enemy', 'doctor_skill.png'))
        self.x = x
        self.y = y
        self.dirX = dirX
        self.dirY = dirY
        self.speed = 15
        self.scale = 64
        self.frame = 0.0



    def update(self):
        self.x += self.dirX * self.speed*game_framework.frame_time* self.speed*5.0
        self.y += self.dirY * self.speed*game_framework.frame_time* self.speed*5.0

        #경계처리
        if self.x < 0 or self.x > 1600 or self.y < 0 or self.y > 900:
            game_world.remove_object(self)

    def draw(self):
        self.image.clip_draw(int(self.frame), 576, 192,192 , self.x, self.y, 64, 64)
        draw_rectangle(*self.get_bb())
    def get_bb(self):
        return self.x - self.scale/2 , self.y - self.scale/2 , self.x + self.scale/2 , self.y + self.scale/2
    def handle_collision(self, group, other):
        if group == 'player:enemy':
            game_world.remove_object(self)
        elif group == 'EQ:enemy':
            game_world.remove_object(self)
class SLOWATTACK:
    def __init__(self, x, y, dirX, dirY ):
        self.image = load_image(os.path.join('asset/enemy', 'ranger_skill.png'))
        self.x = x
        self.y = y
        self.dirX = dirX
        self.dirY = dirY
        self.speed = 8
        self.scale = 64
        self.frame = 0.0



    def update(self):
        self.x += self.dirX * self.speed*game_framework.frame_time* self.speed*5.0
        self.y += self.dirY * self.speed*game_framework.frame_time* self.speed*5.0

        #경계처리
        if self.x < 0 or self.x > 1600 or self.y < 0 or self.y > 900:
            game_world.remove_object(self)

    def draw(self):
        self.image.clip_draw(int(self.frame), 0, 200,200 , self.x, self.y, self.scale*2,  self.scale*2)
        draw_rectangle(*self.get_bb())
    def get_bb(self):
        return self.x - self.scale/2 , self.y - self.scale/2 , self.x + self.scale/2 , self.y + self.scale/2
    def handle_collision(self, group, other):
        if group == 'player:enemy':
            other.slow_effect_timer=3.0

            game_world.remove_object(self)
        elif group == 'EQ:enemy':
            game_world.remove_object(self)
