from pico2d import *
from current_map import *

width, height =  1400, 800


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


class Bubble:
    def __init__(self, x, y, degree):
        self.x = x
        self.y = y
        self.degree = degree
        self.speed = 10
        self.image = load_image('bubble.png')
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

        self.attack_manager = AttackManager(1.5)  # 1.5초 쿨타임

        # 스프라이트 이미지
        self.image_walking = load_image('Walk-Anim.png')
        self.image_idle = load_image('Idle-Anim.png')
        self.image_normal_attack = load_image('Shoot-Anim.png')
        self.frame = 0

    def draw(self):
        if(self.motion_state == 'idle'):
            # clip_draw(잘라낼 시작x, 시작y, w, h, 그릴x, 그릴y)
            if self.dirX == 0 and self.dirY == 0:
                # 마지막 멈춘 방향 사용
                if self.stopdirX < 0 and self.stopdirY < 0:  # 좌하
                    self.image_idle.clip_draw(self.frame * 48, 0, 48, 56, self.x, self.y,  self.scale,  self.scale)
                elif self.stopdirX < 0 and self.stopdirY == 0:  # 좌
                    self.image_idle.clip_draw(self.frame * 48, 56, 48, 56, self.x, self.y,  self.scale,  self.scale)
                elif self.stopdirX < 0 and self.stopdirY > 0:  # 좌상
                    self.image_idle.clip_draw(self.frame * 48, 112, 48, 56, self.x, self.y,  self.scale,  self.scale)
                elif self.stopdirX == 0 and self.stopdirY > 0:  # 상
                    self.image_idle.clip_draw(self.frame * 48, 168, 48, 56, self.x, self.y,  self.scale,  self.scale)
                elif self.stopdirX > 0 and self.stopdirY > 0:  # 우상
                    self.image_idle.clip_draw(self.frame * 48, 224, 48, 56, self.x, self.y,  self.scale,  self.scale)
                elif self.stopdirX > 0 and self.stopdirY == 0:  # 우
                    self.image_idle.clip_draw(self.frame * 48, 280, 48, 56, self.x, self.y,  self.scale,  self.scale)
                elif self.stopdirX > 0 and self.stopdirY < 0:  # 우하
                    self.image_idle.clip_draw(self.frame * 48, 336, 48, 56, self.x, self.y,  self.scale,  self.scale)
                elif self.stopdirX == 0 and self.stopdirY < 0:  # 하
                    self.image_idle.clip_draw(self.frame * 48, 392, 48, 56, self.x, self.y,  self.scale,  self.scale)
                else:
                    self.image_idle.clip_draw(self.frame * 48, 0, 48, 56, self.x, self.y,  self.scale,  self.scale)  # 기본값
            else:

                    #캐릭터 방향에 따라 다르게 그려야함 개망했노
                    if self.dirX < 0 and self.dirY < 0:  # 좌하
                        self.image_walking.clip_draw(self.frame * 48, 0, 48, 40, self.x, self.y,  self.scale,  self.scale)
                    elif self.dirX < 0 and self.dirY == 0:  # 좌
                        self.image_walking.clip_draw(self.frame * 48, 40, 48, 40, self.x, self.y,  self.scale,  self.scale)
                    elif self.dirX < 0 and self.dirY > 0:  # 좌상
                        self.image_walking.clip_draw(self.frame * 48, 80, 48, 40, self.x, self.y,  self.scale,  self.scale)
                    elif self.dirX == 0 and self.dirY > 0:  # 상
                        self.image_walking.clip_draw(self.frame * 48, 120, 48, 40, self.x, self.y,  self.scale,  self.scale)
                    elif self.dirX > 0 and self.dirY > 0:  # 우상
                        self.image_walking.clip_draw(self.frame * 48, 160, 48, 40, self.x, self.y,  self.scale,  self.scale)
                    elif self.dirX > 0 and self.dirY == 0:  # 우
                        self.image_walking.clip_draw(self.frame * 48, 200, 48, 40, self.x, self.y,  self.scale,  self.scale)
                    elif self.dirX > 0 and self.dirY < 0:  # 우하
                        self.image_walking.clip_draw(self.frame * 48, 240, 48, 40, self.x, self.y,  self.scale,  self.scale)
                    elif self.dirX == 0 and self.dirY < 0:  # 하
                        self.image_walking.clip_draw(self.frame * 48, 280, 48, 40, self.x, self.y,  self.scale,  self.scale)
                    else:
                        self.image_walking.clip_draw(self.frame * 48, 0, 48, 40, self.x, self.y,  self.scale,  self.scale)  # 기본값



        # 공격 애니메이션 방향별 출력 (스탑dir 기준)
        if self.motion_state == 'normal_attack':
            if self.stopdirX < 0 and self.stopdirY < 0:  # 좌하
                self.image_normal_attack.clip_draw(self.frame * 48, 0, 48, 56, self.x, self.y, self.scale, self.scale)
            elif self.stopdirX < 0 and self.stopdirY == 0:  # 좌
                self.image_normal_attack.clip_draw(self.frame * 48, 56, 48, 56, self.x, self.y, self.scale, self.scale)
            elif self.stopdirX < 0 and self.stopdirY > 0:  # 좌상
                self.image_normal_attack.clip_draw(self.frame * 48, 112, 48, 56, self.x, self.y, self.scale, self.scale)
            elif self.stopdirX == 0 and self.stopdirY > 0:  # 상
                self.image_normal_attack.clip_draw(self.frame * 48, 168, 48, 56, self.x, self.y, self.scale, self.scale)
            elif self.stopdirX > 0 and self.stopdirY > 0:  # 우상
                self.image_normal_attack.clip_draw(self.frame * 48, 224, 48, 56, self.x, self.y, self.scale, self.scale)
            elif self.stopdirX > 0 and self.stopdirY == 0:  # 우
                self.image_normal_attack.clip_draw(self.frame * 48, 280, 48, 56, self.x, self.y, self.scale, self.scale)
            elif self.stopdirX > 0 and self.stopdirY < 0:  # 우하
                self.image_normal_attack.clip_draw(self.frame * 48, 336, 48, 56, self.x, self.y, self.scale, self.scale)
            elif self.stopdirX == 0 and self.stopdirY < 0:  # 하
                self.image_normal_attack.clip_draw(self.frame * 48, 392, 48, 56, self.x, self.y, self.scale, self.scale)
            else:
                self.image_normal_attack.clip_draw(self.frame * 48, 0, 48, 56, self.x, self.y, self.scale,
                                                   self.scale)  # 기본값

    def update_frame(self, dt=0.05):
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

    def move(self,current_map):
        next_x = self.x + self.dirX * 5
        next_y = self.y + self.dirY * 5

        # 마을 경계처리
        if current_map.get_current_map() == 1:
            if next_y >= 550 or next_y < 250:
                if next_x < 1040:
                    return
        self.x += self.dirX * 5
        self.y += self.dirY * 5

        # 화면 경계 처리
        if self.x < 0:
            self.x = 0
        elif self.x > 1400:
            self.x = 1400

        if self.y < 0:
            self.y = 0
        elif self.y > 800:
            self.y = 800


    def get_pos(self):
        return (self.x, self.y)

    def get_angle(self,mouse_x, mouse_y):
        dx = mouse_x - self.x
        dy = mouse_y - self.y
        angle = math.atan2(dy, dx)  # 라디안 반환
        return angle