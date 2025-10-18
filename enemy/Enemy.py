from pico2d import *
import math
import random
from enemy.enemy_state_machine import EnemyStateMachine
import os
def level_to_image(level):
    level_images = {
        1: 'level1ball.png',
        2: 'level2ball.png',
        3: 'level3ball.png'
    }
    return level_images.get(level, 'level1ball.png')
class Enemy:
    def __init__(self, image_path, x, y, type):
        self.image = load_image(os.path.join('asset/enemy', 'trainer_BURGLAR.png'))
        #타입=레벨 레벨별 이미지다름
        self.ball_image = load_image(os.path.join('asset/enemy', level_to_image(type)))
        self.x = x
        self.y = y
        self.type = type
        self.speed = 2
        self.scale = 100
        self.dirX = 0
        self.dirY = 0
        self.frame = 0
        self.frame_time = 0.2

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

    def update(self, player, frame_time):
        # 상태 머신 업데이트 (플레이어 정보를 event로 넘김)
        self.frame_time -= frame_time
        if self.frame_time <= 0:
            self.frame_time = 0.2
            self.frame = (self.frame + 1) % 4
        # 플레이어랑 위치 계산해서 dirx, diry 설정
        dx = player.x - self.x
        dy = player.y - self.y
        if abs(dx) > abs(dy):  # 수평이 더 크면 좌
            self.dirX = 1 if dx > 0 else -1
            self.dirY = 0
        else:  # 수직이 더 크면 상하
            self.dirY = 1 if dy > 0 else -1
            self.dirX = 0
        result = self.state_machine.update(player)
        return result  # 공격 시 생성된 몬스터볼 반환
    def draw(self):
        self.state_machine.draw()




class EnemyIdle:
    def __init__(self, enemy): self.enemy = enemy
    def enter(self, player): self.enemy.dirX = self.enemy.dirY = 0
    def exit(self, player): pass
    def do(self, player):
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
            self.enemy.x += dx * self.enemy.speed
            self.enemy.y += dy * self.enemy.speed
        if abs(dx) > abs(dy):  # 수평이 더 크면 좌우
            self.enemy.dirX = 1 if dx > 0 else -1
            self.enemy.dirY = 0
        else:  # 수직이 더 크면 상하
            self.enemy.dirY = 1 if dy > 0 else -1
            self.enemy.dirX = 0
    def draw(self):
        enemy = self.enemy
        if enemy.dirX == -1:
            enemy.image.clip_draw(enemy.frame * 32, 96, 32, 48, enemy.x, enemy.y, enemy.scale, enemy.scale)
        elif enemy.dirX == 1:
            enemy.image.clip_draw(enemy.frame * 32, 48, 32, 48, enemy.x, enemy.y, enemy.scale, enemy.scale)
        elif enemy.dirY == 1:
            enemy.image.clip_draw(enemy.frame * 32, 0, 32, 48, enemy.x, enemy.y, enemy.scale, enemy.scale)
        elif enemy.dirY == -1:
            enemy.image.clip_draw(enemy.frame * 32, 144, 32, 48, enemy.x, enemy.y, enemy.scale, enemy.scale)


class EnemyAttack:
    def __init__(self, enemy):
        self.enemy = enemy
        self.cooldown = 2.0
        self.timer = 0
    def enter(self, player): self.timer = 0
    def exit(self, player): pass
    def do(self, player):
        self.timer += 0.05
        if self.timer >= self.cooldown:
            #몬스터볼 던지는거 추가
            self.timer = 0
            ball = AttackBall(self.enemy.ball_image, self.enemy.x, self.enemy.y, self.enemy.dirX, self.enemy.dirY,self.enemy.type, speed=10,)
            return ball
    def draw(self):
        enemy = self.enemy
        if enemy.dirX == -1:
            enemy.image.clip_draw(enemy.frame * 32, 96, 32, 48, enemy.x, enemy.y, enemy.scale, enemy.scale)
        elif enemy.dirX == 1:
            enemy.image.clip_draw(enemy.frame * 32, 48, 32, 48, enemy.x, enemy.y, enemy.scale, enemy.scale)
        elif enemy.dirY == 1:
            enemy.image.clip_draw(enemy.frame * 32, 0, 32, 48, enemy.x, enemy.y, enemy.scale, enemy.scale)
        elif enemy.dirY == -1:
            enemy.image.clip_draw(enemy.frame * 32, 144, 32, 48, enemy.x, enemy.y, enemy.scale, enemy.scale)

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
        self.x += self.dirX * self.speed
        self.y += self.dirY * self.speed
        if self.frame_time <= 0:
            self.frame_time = 0.1
            self.frame = (self.frame + 1) % 8
        self.frame_time -= 0.05

    def draw(self):
        self.image.clip_draw(self.frame * 32, 0, 32, 64, self.x, self.y, 32, 64)