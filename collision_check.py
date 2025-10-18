from pico2d import *


def collision_player_object(player, emenies_ball,world):
    px, py = player.x, player.y

    for ball in emenies_ball[:]:  # 리스트 복사로 안전하게 순회
        bx, by = getattr(ball, 'x', 0), getattr(ball, 'y', 0)
        br = getattr(ball, 'scale', 0) / 2
        pr = getattr(player, 'scale', 0) / 2

        distance = math.hypot(px - bx, py - by)+70
        if distance < (pr + br):
            dmg = 5*ball.level  # 볼의 레벨에 비례한 데미지
            player.cur_HP = max(0, player.cur_HP - dmg)
            emenies_ball.remove(ball)
            world.remove(ball)
