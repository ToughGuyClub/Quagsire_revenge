from pico2d import *
from character import Character
from handeEvent import handle_events
width, height =  1400, 800
frame_character=0
open_canvas(width, height)

backgrounds = load_image('background.png')

player = Character(200, 200)
while True:
    clear_canvas()
    backgrounds.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림
    player.draw()

    update_canvas()
    delay(0.05)
    handle_events(player)
    Character.update_frame(player);
    Character.move(player);

close_canvas()