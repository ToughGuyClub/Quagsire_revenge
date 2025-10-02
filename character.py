from pico2d import *


width, height =  1400, 800
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
        self.frame_interval = 0.3
        # 위치
        self.x = x
        self.y = y
        self.scale=150   #크기

        # 이동 방향
        self.dirX = 0
        self.dirY = 0
        # 멈춘 방향 (캐릭터가 마지막으로 바라본 방향)
        self.stopdirX = 0
        self.stopdirY = -1  # 기본값: 아래쪽

        # 레벨
        self.level = 1
        self.exp = 0



        # 스프라이트 이미지
        self.image_walking = load_image('Walk-Anim.png')
        self.image_idle = load_image('Idle-Anim.png')
        self.frame = 0

    def draw(self):
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

    def update_frame(self, dt=0.05):
        self.frame_timer += dt
        if self.frame_timer >= self.frame_interval:
            if self.dirX == 0 and self.dirY == 0:
                self.frame = (self.frame + 1) % 7
            else:
                self.frame = (self.frame + 1) % 4
            self.frame_timer = 0
    def move(self):
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