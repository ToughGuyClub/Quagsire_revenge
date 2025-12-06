from pico2d import *


class Background:
    def __init__(self):
        self.image = load_image(os.path.join('asset/screen','background.png'))
        # 사운드
        import sound
        self.intro_bgm = load_music('asset/screen/intro.mp3')
        self.intro_bgm.set_volume(sound.get_sound_volume())
        self.intro_bgm.repeat_play()
    def draw(self):
        width, height = 1400, 800
        self.image.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림