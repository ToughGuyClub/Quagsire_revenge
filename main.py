from pico2d import *


width, height =  1400, 800
open_canvas(width, height)

backgrounds = load_image('background.png')
backgrounds.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림
update_canvas()

delay(1)

close_canvas()