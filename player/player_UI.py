from pico2d import *

class Player_UI:
    def __init__(self, player):
        # --- 기본 이미지 및 폰트 로드 ---
        self.HP_bar_img = load_image(os.path.join('asset/player', 'hp_bar.png'))
        self.font = load_font('asset/screen/intro/introFont.ttf', 30)

        self.player = player

        # --- 스킬 아이콘 정보 저장용 (slot: (image, (sx, sy, sw, sh))) ---
        self.skill_icons = {
            1: {  # slot 2
                1: (load_image(os.path.join('asset/player/skill', 'water_cannon.png')), (0, 0, 85, 120)),
                2: (load_image(os.path.join('asset/player/skill', 'water_beam.png')), (200, 200, 200, 200)),
                3: (load_image(os.path.join('asset/player/skill', 'hyper_beam.png')), (200, 200, 200, 200)),
            },
             2: {  # slot 2
                1: (load_image(os.path.join('asset/player/skill', 'water_sheild.png')), (100, 100, 100, 100)),
                2: (load_image(os.path.join('asset/player/skill', 'water_parrying.png')), (0, 0, 102, 75)),
                3: (load_image(os.path.join('asset/player/skill', 'water_heal.png')), (170, 0, 85, 90))
            },
            3: {
                1: (load_image(os.path.join('asset/player/skill', 'ice_spear.png')), (0, 0, 88, 16)),
                2: (load_image(os.path.join('asset/player/skill', 'earth_quake.png')), (0, 0, 60, 60)),
                3: (load_image(os.path.join('asset/player/skill', 'thunder.png')), (0, 0, 104, 108))
            },
            4: {
             }
        }   # 예: {1: (image, (0,0,64,64)), 2: (...), ...}

        # --- UI 좌표/크기 ---
        self.skill_size = 64
        self.skill_spacing = 10
        self.skill_start_x = 100
        self.skill_start_y = 100

    # ================================================
    # 외부에서 스킬 아이콘 정보 등록 (초기 1회 호출)
    # ================================================
    def set_skill_icon(self, slot: int, image, clip_rect):
        """
        slot : 1~4
        image : pico2d 이미지 객체
        clip_rect : (sx, sy, sw, sh)
        """
        self.skill_icons[slot] = (image, clip_rect)

    # ================================================
    # 메인 draw()
    # ================================================
    def draw(self):
        self.draw_health_bar(self.player)
        self.draw_skill_cooldown(self.player)

    # ================================================
    # 체력바
    # ================================================
    def draw_health_bar(self, player):
        bar_width = 400
        bar_height = 20
        health_ratio = player.cur_HP / player.max_HP

        if health_ratio > 0.5:
            bar_color = 2
        elif health_ratio > 0.2:
            bar_color = 1
        else:
            bar_color = 0

        self.HP_bar_img.clip_draw(
            0, bar_color * 6, 96, 6,
            100 + bar_width * health_ratio // 2, 750,
            bar_width * health_ratio, bar_height
        )

    # ================================================
    # 스킬 아이콘 + 쿨타임 UI
    # ================================================
    def draw_skill_cooldown(self, player):
        sm = player.skill_manager

        for slot in range(1, 5):
            x = self.skill_start_x + (self.skill_size + self.skill_spacing) * (slot - 1)
            y = self.skill_start_y

            # 현재 슬롯의 스킬 레벨
            skill_level = sm.current_skills[slot - 1] if slot - 1 < len(sm.current_skills) else 0
            if skill_level == 0:
                continue

            # 해당 슬롯, 해당 레벨의 아이콘 정보 가져오기
            icon_info = self.skill_icons.get(slot, {}).get(skill_level, None)

            if icon_info:
                draw_rectangle(
                    x - self.skill_size // 2, y - self.skill_size // 2,
                    x + self.skill_size // 2, y + self.skill_size // 2,
                    255, 255, 255, 255, True)
                image, (sx, sy, sw, sh) = icon_info
                image.clip_draw(sx, sy, sw, sh, x, y, self.skill_size, self.skill_size)
            else:
                draw_rectangle(
                    x - self.skill_size // 2, y - self.skill_size // 2,
                    x + self.skill_size // 2, y + self.skill_size // 2,
                    255, 255, 255, 255, True)

            # 쿨타임 표시
            cd = sm.cooldowns.get(slot, 0.0)
            if cd > 0:
                draw_rectangle(x - self.skill_size // 2, y - self.skill_size // 2,
                               x + self.skill_size // 2, y + self.skill_size // 2,
                               0, 0, 0, 128, True)
                self.font.draw(x - 20, y - 10, f"{cd:.1f}", (255, 0, 0))

    def update(self):
        pass
