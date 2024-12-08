from pico2d import *
from pico2d import clear_canvas, update_canvas, get_events, load_image

import game_framework

win_image = None  # 승리 화면 이미지

def init():
    """승리 모드에 진입"""
    global win_image
    open_canvas()
    win_image = load_image('./Art/Menu/win.png')  # 승리 화면 이미지 로드

def update():
    pass

def draw():
    clear_canvas()
    win_image.draw_to_origin(0, 0, 800, 600)
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            exit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:  # ESC 키로 게임 종료
                exit()
            elif event.key == SDLK_SPACE:  # M 키로 메인 화면으로 이동
                import start_mode
                game_framework.change_mode(start_mode)

def finish():
    global win_image
    del win_image


