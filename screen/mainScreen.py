from pico2d import *
import screen.background
import game_framework
import screen.intro
game_start = None
game_logo = None
running = True
mscreen_start_time = 0.0
background =None
class main_screen:
    def __init__(self):
        #self.game_start = load_image('game_start.png')
        self.game_start = load_image(os.path.join('asset/screen','main_icon.png'))
        self.game_logo = load_image(os.path.join('asset/screen','game_logo.png', ))
    def draw(self):
        #화면 중앙에 200x100크기로 그림
       # self.game_start.draw(1400//2, 600//2, 200, 100)
        self.game_start.clip_draw(0,380,291,190, 1400//2, 600//2+100, 200, 100)
        self.game_start.clip_draw(0, 190, 291, 190, 1400 // 2, 600 // 2, 200, 100)
        self.game_start.clip_draw(0, 0, 291, 190, 1400 // 2, 600 // 2-100, 200, 100)
        self.game_logo.draw(1400//2, 600, 1155, 200)

def init():
    global game_start,game_logo, running, mscreen_start_time, background
    background = screen.background.Background()
    game_start = load_image(os.path.join('asset/screen','main_icon.png'))
    game_logo = load_image(os.path.join('asset/screen','game_logo.png', ))
    running = True
    mscreen_start_time = get_time()
def finish():
    global game_start,game_logo
    del game_start
    del game_logo
def update():
    # 핸들이벤트로 상태변경
    result = handle_events()
    if result == 'start':
        game_framework.change_mode(screen.intro)
    elif result == 'continue':
        #세이브 로드 추가 예정
        pass
    elif result == 'exit':
        game_framework.quit()
    elif result is None:
        pass

def draw():
    clear_canvas()
    background.draw()
    game_logo.draw(1400//2, 600, 1155, 200)
    game_start.clip_draw(0,380,291,190, 1400//2, 600//2+100, 200, 100)
    game_start.clip_draw(0, 190, 291, 190, 1400 // 2, 600 // 2, 200, 100)
    game_start.clip_draw(0, 0, 291, 190, 1400 // 2, 600 // 2-100, 200, 100)
    update_canvas()
def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_MOUSEBUTTONDOWN:
            x, y = event.x, 800 - 1 - event.y
            #시작 버튼 영역
            if 540 <= x <= 840 and 360 <= y <= 450:
                return 'start'
            # 컨티뉴 버튼 영역
            elif 540 <= x <= 840 and 250 <= y <= 330:
                #세이브 로드 추가 예정
                return 'continue'
            # 종료 버튼 영역
            elif 540 <= x <= 840 and 150 <= y <= 230:
                return 'exit'
    return None

def pause():
    pass
def resume():
    pass
