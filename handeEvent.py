from pico2d import *
from character import Character

def handle_events(player):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            return False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                return False
            elif event.key == SDLK_LEFT:
                player.dirX = -1
                player.stopdirX = -1
            elif event.key == SDLK_RIGHT:
                player.dirX = 1
                player.stopdirX = 1
            elif event.key == SDLK_UP:
                player.dirY = 1
                player.stopdirY = 1
            elif event.key == SDLK_DOWN:
                player.dirY = -1
                player.stopdirY = -1
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_LEFT or event.key == SDLK_RIGHT:

                player.stopdirX = player.dirX
                player.dirX = 0
                player.stopdirY = player.dirY
                player.dirY = 0
            elif event.key == SDLK_UP or event.key == SDLK_DOWN:
                player.stopdirX = player.dirX
                player.dirX = 0
                player.stopdirY = player.dirY
                player.dirY = 0

    return True