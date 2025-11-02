from pico2d import *
import math

class Skill:
    def __init__(self, cooldown):
        self.cooldown = cooldown
        self.timer = 0.0

    def update(self, dt):
        if self.timer > 0:
            self.timer = max(0.0, self.timer - dt)

    def can_use(self):
        return self.timer == 0.0

    def use(self, user, *args, **kwargs):
        if not self.can_use():
            return False
        self.timer = self.cooldown
        return True
class PlayerSkills:
    def __init__(self, user):
        self.user = user
        self.skills = {
            "water_cannon": WaterCannonSkill(),
            # 다른 스킬 추가
        }

    def update(self, dt):
        for s in self.skills.values():
            s.update(dt)

    def use(self, name, *args, **kwargs):
        skill = self.skills.get(name)
        if not skill:
            print("no such skill:", name)
            return False
        return skill.use(self.user, *args, **kwargs)

    def draw(self):
        # 플레이어를 인자로 주어야 하는 스킬 드로우 호출
        for s in self.skills.values():
            if hasattr(s, 'draw'):
                s.draw(self.user)

class WaterCannonSkill(Skill):
    def __init__(self, cooldown=5.0, damage=10, radius=300, width=24, active_time=0.2, image_path=None):
        super().__init__(cooldown)
        self.damage = damage
        self.radius = radius
        self.width = width
        self.active_time = active_time
        self.active_timer = 0.0
        self.angle_rad = 0.0
        self.dir = (1.0, 0.0)
        self.image =  load_image(os.path.join('asset/player/skill','water_cannon.png'))

    def update(self, dt):
        super().update(dt)
        if self.active_timer > 0:
            self.active_timer = max(0.0, self.active_timer - dt)

    def use(self, user, enemies, mouse_pos=None):
        if not super().use(user):
            print("water_cannon on cooldown:", self.timer)
            return False

        mx, my = mouse_pos if mouse_pos is not None else (user.x + 1, user.y)
        dx = mx - user.x
        dy = my - user.y
        dist = math.hypot(dx, dy)
        if dist == 0:
            dirx, diry = 1.0, 0.0
            self.angle_rad = 0.0
        else:
            dirx, diry = dx / dist, dy / dist
            self.angle_rad = math.atan2(diry, dirx)

        self.dir = (dirx, diry)
        self.active_timer = self.active_time

        # 선형(1자) 판정: 적의 위치를 방향 벡터로 투영해서 범위 안에 있고, 수선거리(width/2) 이내면 히트
        r = self.radius
        half_w = self.width / 2.0
        for e in enemies:
            ex = e.x - user.x
            ey = e.y - user.y
            proj = ex * dirx + ey * diry
            if proj < 0 or proj > r:
                continue
            perp_sq = ex*ex + ey*ey - proj*proj
            if perp_sq <= half_w * half_w:
                if hasattr(e, 'take_damage'):
                    e.take_damage(self.damage)
       # print("water_cannon used")
        return True

    def draw(self, user):
        if self.active_timer <= 0:
            return

        # 이미지가 있을 때: 이미지 중심을 캐논의 중간 지점에 맞추고 회전하여 그림
        cx = user.x + self.dir[0] * (self.radius / 2.0)
        cy = user.y + self.dir[1] * (self.radius / 2.0)
        # pico2d의 회전 드로우 함수는 엔진 버전에 따라 다름(라디안/도). 보통 rotate_draw(rad, x, y) 형태를 사용.
        try:
            # angle = self.angle_rad (라디안)
            self.image.rotate_draw(self.angle_rad, cx, cy)
        except Exception:
            # rotate_draw가 없으면 기본 draw로 대체 (이미지를 회전하지 못함)
            self.image.draw(cx, cy)
        print("water_cannon used")

