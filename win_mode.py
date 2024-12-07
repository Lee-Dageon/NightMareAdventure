from pico2d import *

import game_framework

win_image = None  # 승리 화면 이미지

def enter():
    """승리 모드에 진입"""
    global win_image
    win_image = load_image('./Art/Menu/win.png')  # 승리 화면 이미지 로드

def update():
    pass

def draw():
    clear_canvas()
    win_image.draw(400, 300)  # 승리 화면을 중앙에 출력
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            exit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:  # ESC 키로 게임 종료
                exit()
            elif event.key == SDLK_m:  # M 키로 메인 화면으로 이동
                import main_mode
                game_framework.change_mode(main_mode)

def exit():
    global win_image
    del win_image
