from pico2d import *
from pico2d import clear_canvas, update_canvas, get_events, load_image

import enter_stage1
import game_framework
import stage1_mode  # 게임 시작 시 이동할 모드

start_image = None  # 시작 화면 이미지

def init():
    """시작 모드에 진입"""
    global start_image
    open_canvas()
    start_image = load_image('./assets/game_start.png')  # 시작 화면 이미지 로드

def update():
    pass

def draw():
    clear_canvas()
    start_image.draw_to_origin(0, 0, 800, 600)
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            exit_game()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_SPACE:  # 스페이스바로 게임 시작
                game_framework.change_mode(enter_stage1)
            elif event.key == SDLK_ESCAPE:  # ESC 키로 게임 종료
                exit_game()

def exit_game():
    global start_image
    if start_image:
        del start_image
    game_framework.quit()

def finish():
    pass
