from pico2d import *

class Status:
    def __init__(self, player):
        self.current_selected_skill = [0, 0]  # [현재 선택된 슬롯, 현재 선택된 레벨]
        self.player = player

        # --- 화살표 이미지 로드 ---
        self.arrowR_image = load_image(os.path.join('asset/player/UI', 'arrow_right.png'))
        self.arrowL_image = load_image(os.path.join('asset/player/UI', 'arrow_left.png'))

        # --- 스킬 아이콘 정보 미리 로드 ---
        # Player_UI에서와 같은 구조로 맞춤
        self.skill_icons = {
            1: {
                1: (load_image(os.path.join('asset/player/skill', 'water_cannon.png')), (0, 0, 85, 120)),
                2: (load_image(os.path.join('asset/player/skill', 'water_beam.png')), (200, 200, 200, 200)),
                3: (load_image(os.path.join('asset/player/skill', 'hyper_beam.png')), (200, 200, 200, 200)),
            },
            2: {
                1: (load_image(os.path.join('asset/player/skill', 'water_sheild.png')), (100, 100, 100, 100)),
                2: (load_image(os.path.join('asset/player/skill', 'water_parrying.png')), (0, 0, 102, 75)),
                3: (load_image(os.path.join('asset/player/skill', 'water_heal.png')), (170, 0, 85, 90))
            },
            3: {
                1: (load_image(os.path.join('asset/player/skill', 'ice_spear.png')), (0, 0, 88, 16)),
                2: (load_image(os.path.join('asset/player/skill', 'earth_quake.png')), (0, 0, 60, 60)),
                3: (load_image(os.path.join('asset/player/skill', 'flash.png')), (0, 0, 256, 256)),
            },
            4: {
                1:(load_image(os.path.join('asset/player/skill', 'meteor.png')), (0, 0, 100, 100)),
                2:(load_image(os.path.join('asset/player/skill', 'thunder.png')), (0, 0, 104, 108))
            }
        }
        self.skill_icons_p = {
            1: {  # slot 2
                1: (load_image(os.path.join('asset/player/skill', 'water_cannon_p.png')), (0, 0, 85, 120)),
                2: (load_image(os.path.join('asset/player/skill', 'water_beam_p.png')), (200, 200, 200, 200)),
                3: (load_image(os.path.join('asset/player/skill', 'hyper_beam.png')), (200, 200, 200, 200)),
            },
            2: {  # slot 2
                1: (load_image(os.path.join('asset/player/skill', 'water_sheild_p.png')), (100, 100, 100, 100)),
                2: (load_image(os.path.join('asset/player/skill', 'water_parrying_p.png')), (0, 0, 102, 75)),
                3: (load_image(os.path.join('asset/player/skill', 'water_heal.png')), (170, 0, 85, 90))
            },
            3: {
                1: (load_image(os.path.join('asset/player/skill', 'ice_spear_p.png')), (0, 0, 88, 16)),
                2: (load_image(os.path.join('asset/player/skill', 'earth_quake.png')), (0, 0, 60, 60)),
                3: (load_image(os.path.join('asset/player/skill', 'flash.png')), (0, 0, 256, 256)),
            },
            4: {
                1: (load_image(os.path.join('asset/player/skill', 'meteor_p.png')), (0, 0, 100, 100)),
                2: (load_image(os.path.join('asset/player/skill', 'thunder.png')), (0, 0, 104, 108)),
            }
        }

        #캐릭터 선택창
        self.character_quag = load_image(os.path.join('asset/player/Quagsire', 'Normal.png'))
        self.character_clod = load_image(os.path.join('asset/player/Clodsire', 'Normal.png'))
        self.selected_character = self.player.type

        if not hasattr(self, 'font'):
            self.font = load_font('asset/screen/intro/introFont.ttf', 30)

        # --- UI 기본 설정 ---
        self.skill_size = 64
        self.spacing = 30
        self.start_x = 500
        self.start_y = 600

    # ==============================================
    # 메인 draw()
    # ==============================================
    def draw(self):
        # 배경 창
        draw_rectangle(190, 90, 1210, 710, 47, 248, 240, 255, True)
        draw_rectangle(200, 100, 1200, 700, 0, 0, 0, 255, True)
        self.draw_skill_icon()
        self.character_select_draw()
    # ==============================================
    # 스킬 아이콘 출력
    # ==============================================
    def draw_skill_icon(self):
        sm = self.player.skill_manager

        for slot in range(1, 5):
            x = self.start_x
            y = self.start_y - (self.skill_size + self.spacing) * (slot - 1)

            # 현재 슬롯의 스킬 레벨
            skill_level = sm.current_skills[slot - 1] if slot - 1 < len(sm.current_skills) else 0

            # 선택 표시 (현재 선택된 슬롯이라면)
            if slot - 1 == self.current_selected_skill[0]:
                draw_rectangle(
                    x - self.skill_size // 2 - 5, y - self.skill_size // 2 - 5,
                    x + self.skill_size // 2 + 5, y + self.skill_size // 2 + 5,
                    0, 144, 248, 255, True
                )

            # --- 아이콘 정보 가져오기 ---
            icon_info = self.skill_icons.get(slot, {}).get(skill_level, None)

            if self.player.type == 2:
                icon_info = self.skill_icons_p.get(slot, {}).get(skill_level, None)
            if icon_info:
                draw_rectangle(
                    x - self.skill_size // 2, y - self.skill_size // 2,
                    x + self.skill_size // 2, y + self.skill_size // 2,
                    255, 255, 255, 255, True)
                image, (sx, sy, sw, sh) = icon_info
                image.clip_draw(sx, sy, sw, sh, x, y, self.skill_size, self.skill_size)
            else:
                # 없으면 기본 사각형으로
                draw_rectangle(
                    x - self.skill_size // 2, y - self.skill_size // 2,
                    x + self.skill_size // 2, y + self.skill_size // 2,
                    255, 255, 255, 255, True
                )

            # 좌우 화살표 표시
            self.arrowL_image.draw(x - self.skill_size - 10, y)
            self.arrowR_image.draw(x + self.skill_size + 10, y)
    def character_select_draw(self):
        # 캐릭터 선택창 배경

        if self.selected_character == 1:
            draw_rectangle(840, 240, 960, 360, 0, 0, 255, 255, True)
        else:
            draw_rectangle(980, 240, 1120, 360, 0, 0, 255, 255, True)
        # 캐릭터 이미지 출력
        self.character_quag.draw(900, 300, 100, 100)
        self.character_clod.draw(1050, 300, 100, 100)

    # ==============================================
    # 업데이트 (입력, 상태변화용)
    # ==============================================
    def update(self):
        pass
