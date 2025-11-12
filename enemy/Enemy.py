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

def level_to_image(level):
    level_images = {
        1: 'level1ball.png',
        2: 'level2ball.png',
        3: 'level3ball.png'
    }
    return level_images.get(level, 'level1ball.png')
class Enemy:
    def __init__(self, image_path, x, y, type,player):
        self.image = load_image(os.path.join('asset/enemy', 'trainer_BURGLAR.png'))
        #타입=레벨 레벨별 이미지다름
        self.HP = type * 2
        self.ball_image = load_image(os.path.join('asset/enemy', level_to_image(type)))
        self.x = x
        self.y = y
        self.type = type
        self.speed = 2.0
        self.scale = 70
        self.dirX = 0
        self.dirY = 0
        self.frame = 0
        self.frame_time = 0.3
        self.is_enemy = True
        #플레이어 위치를 위한 참조
        self.target_player = player

        # 상태 클래스 생성
        self.IDLE = EnemyIdle(self)
        self.RUN = EnemyRun(self)
        self.ATTACK = EnemyAttack(self)

        # 상태머신 연결
        self.state_machine = EnemyStateMachine(
            self.IDLE,
            {
                self.IDLE: { self.detect_player: self.RUN },
                self.RUN: { self.lost_player: self.IDLE, self.in_attack_range: self.ATTACK },
                self.ATTACK: { self.lost_player: self.IDLE }
            }
        )

        game_world.add_object(self, 1)
        game_world.add_collision_pair('bubble:enemy', None, self)
        game_world.add_collision_pair('cannon:enemy', None, self)
        game_world.add_collision_pair('EQ:enemy', None, self)

    def detect_player(self, e):
        # 플레이어가 일정 거리 내에 들어왔는가
        player = e
        distance = math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)



        return distance < 400  # 감지 범위

    def in_attack_range(self, e):
        player = e
        distance = math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)
        return distance < 300  # 공격 사거리

    def lost_player(self, e):
        player = e
        distance = math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)
        return distance > 500  # 너무 멀어지면 잃음

    def update(self):
        # 상태 머신 업데이트 (플레이어 정보를 event로 넘김)
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

        # 플레이어랑 위치 계산해서 dirx, diry 설정
        dx =  self.target_player.x - self.x
        dy =  self.target_player.y - self.y
        if abs(dx) > abs(dy):  # 수평이 더 크면 좌
            self.dirX = 1 if dx > 0 else -1
            self.dirY = 0
        else:  # 수직이 더 크면 상하
            self.dirY = 1 if dy > 0 else -1
            self.dirX = 0
        self.state_machine.update(self.target_player)

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())
    def draw_half(self):
        enemy = self
        from screen.thunder_scene import get_half_stack
        step = get_half_stack()

        #상부 몸체
        if enemy.dirX == 0 and enemy.dirY == 0:
            enemy.image.clip_draw(0, 168, 32, 24, enemy.x + step, enemy.y + enemy.scale / 4, enemy.scale,
                                  enemy.scale / 2)
        elif enemy.dirX == -1:
            enemy.image.clip_draw(0, 120, 32, 24, enemy.x + step, enemy.y + enemy.scale / 4, enemy.scale,
                                  enemy.scale / 2)
        elif enemy.dirX == 1:
            enemy.image.clip_draw(0, 72, 32, 24, enemy.x + step, enemy.y + enemy.scale / 4, enemy.scale,
                                  enemy.scale / 2)
        elif enemy.dirY == 1:
            enemy.image.clip_draw(0, 24, 32, 24, enemy.x + step, enemy.y + enemy.scale / 4, enemy.scale, enemy.scale / 2)
        elif enemy.dirY == -1:
            enemy.image.clip_draw(0, 168, 32, 24, enemy.x + step, enemy.y + enemy.scale / 4, enemy.scale,
                                  enemy.scale / 2)

        #하부 몸체
        if enemy.dirX == 0 and enemy.dirY == 0:
            enemy.image.clip_draw(0, 144, 32, 24, enemy.x-step, enemy.y-enemy.scale/4, enemy.scale, enemy.scale/2)
        elif enemy.dirX == -1:
            enemy.image.clip_draw(0, 96, 32, 24, enemy.x-step, enemy.y-enemy.scale/4, enemy.scale, enemy.scale/2)
        elif enemy.dirX == 1:
            enemy.image.clip_draw(0, 48, 32, 24, enemy.x-step, enemy.y-enemy.scale/4, enemy.scale, enemy.scale/2)
        elif enemy.dirY == 1:
            enemy.image.clip_draw(0, 0, 32, 24, enemy.x-step, enemy.y-enemy.scale/4, enemy.scale, enemy.scale/2)
        elif enemy.dirY == -1:
            enemy.image.clip_draw(0, 144, 32, 24, enemy.x-step, enemy.y-enemy.scale/4, enemy.scale, enemy.scale/2)
    def get_bb(self):
        return self.x - self.scale/2 , self.y - self.scale/2 , self.x + self.scale/2 , self.y + self.scale/2
    def handle_collision(self, group, other):
        if group == 'bubble:enemy':
            self.HP -= 1*other.damage
        elif group == 'cannon:enemy':
            self.HP -= 1*other.damage
        elif group == 'EQ:enemy':
            self.HP -= 1*other.damage

        if self.HP <= 0:
            #사망 처리 전에 경험치 지급
            if hasattr(self.target_player, "gain_exp"):
                self.target_player.gain_exp(self.type * 20)  # type에 비례해서 EXP 보상
            game_world.remove_object(self)



class EnemyIdle:
    def __init__(self, enemy): self.enemy = enemy
    def enter(self,player): self.enemy.dirX = self.enemy.dirY = 0
    def exit(self,player): pass
    def do(self,player):
        # 가끔 랜덤 움직임
        if random.random() < 0.02:
            self.enemy.x += random.choice([-1, 0, 1]) * self.enemy.speed
            self.enemy.y += random.choice([-1, 0, 1]) * self.enemy.speed
    def draw(self):
        enemy = self.enemy
        if enemy.dirX == 0 and enemy.dirY == 0:
            enemy.image.clip_draw(0, 144, 32, 48, enemy.x, enemy.y, enemy.scale, enemy.scale)
        elif enemy.dirX == -1:
            enemy.image.clip_draw(0, 96, 32, 48, enemy.x, enemy.y, enemy.scale, enemy.scale)
        elif enemy.dirX == 1:
            enemy.image.clip_draw(0, 48, 32, 48, enemy.x, enemy.y, enemy.scale, enemy.scale)
        elif enemy.dirY == 1:
            enemy.image.clip_draw(0, 0, 32, 48, enemy.x, enemy.y, enemy.scale, enemy.scale)
        elif enemy.dirY == -1:
            enemy.image.clip_draw(0, 144, 32, 48, enemy.x, enemy.y, enemy.scale, enemy.scale)


class EnemyRun:
    def __init__(self, enemy): self.enemy = enemy
    def enter(self, player): pass
    def exit(self, player): pass
    def do(self, player):
        dx = player.x - self.enemy.x
        dy = player.y - self.enemy.y
        dist = math.sqrt(dx ** 2 + dy ** 2)
        if dist > 0:
            dx, dy = dx / dist, dy / dist
            self.enemy.x += dx * self.enemy.speed*game_framework.frame_time*self.enemy.speed*10.0
            self.enemy.y += dy * self.enemy.speed*game_framework.frame_time*self.enemy.speed*10.0
        if abs(dx) > abs(dy):  # 수평이 더 크면 좌우
            self.enemy.dirX = 1 if dx > 0 else -1
            self.enemy.dirY = 0
        else:  # 수직이 더 크면 상하
            self.enemy.dirY = 1 if dy > 0 else -1
            self.enemy.dirX = 0
    def draw(self):
        enemy = self.enemy
        if enemy.dirX == -1:
            enemy.image.clip_draw(int(enemy.frame) * 32, 96, 32, 48, enemy.x, enemy.y, enemy.scale, enemy.scale)
        elif enemy.dirX == 1:
            enemy.image.clip_draw(int(enemy.frame) * 32, 48, 32, 48, enemy.x, enemy.y, enemy.scale, enemy.scale)
        elif enemy.dirY == 1:
            enemy.image.clip_draw(int(enemy.frame) * 32, 0, 32, 48, enemy.x, enemy.y, enemy.scale, enemy.scale)
        elif enemy.dirY == -1:
            enemy.image.clip_draw(int(enemy.frame) * 32, 144, 32, 48, enemy.x, enemy.y, enemy.scale, enemy.scale)


class EnemyAttack:
    def __init__(self, enemy):
        self.enemy = enemy
        self.cooldown = 1.0
        self.timer = 0
    def enter(self,player): self.timer = 0
    def exit(self,player): pass
    def do(self,player):
        self.timer += game_framework.frame_time
        if self.timer >= self.cooldown:
            self.timer = 0
            # 플레이어를 향한 실제 방향 계산
            dx = player.x - self.enemy.x
            dy = player.y - self.enemy.y
            dist = math.sqrt(dx ** 2 + dy ** 2)
            if dist != 0:
                dirX = dx / dist
                dirY = dy / dist
            else:
                dirX, dirY = 0, 0

            # 그 방향으로 몬스터볼 생성
            ball = AttackBall(
                self.enemy.ball_image,
                self.enemy.x,
                self.enemy.y,
                dirX,
                dirY,
                self.enemy.type,
                speed=10,
            )
            game_world.add_object(ball, 2)
            game_world.add_collision_pair('player:enemy', None, ball)
            game_world.add_collision_pair('EQ:enemy', None, ball)
    def draw(self):
        enemy = self.enemy
        if enemy.dirX == -1:
            enemy.image.clip_draw(int(enemy.frame)* 32, 96, 32, 48, enemy.x, enemy.y, enemy.scale, enemy.scale)
        elif enemy.dirX == 1:
            enemy.image.clip_draw(int(enemy.frame) * 32, 48, 32, 48, enemy.x, enemy.y, enemy.scale, enemy.scale)
        elif enemy.dirY == 1:
            enemy.image.clip_draw(int(enemy.frame)* 32, 0, 32, 48, enemy.x, enemy.y, enemy.scale, enemy.scale)
        elif enemy.dirY == -1:
            enemy.image.clip_draw(int(enemy.frame)* 32, 144, 32, 48, enemy.x, enemy.y, enemy.scale, enemy.scale)

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
        self.frame_time = 0.2
    def update(self):
        self.x += self.dirX * self.speed*game_framework.frame_time* self.speed*5.0
        self.y += self.dirY * self.speed*game_framework.frame_time* self.speed*5.0
        if self.frame_time <= 0:
            self.frame_time = 0.2
            self.frame = (self.frame + 1) % 8
        self.frame_time -= 0.05
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


