from pico2d import *

import enter_stage1
import game_framework
from pico2d import clear_canvas, update_canvas, get_events, load_image, get_time

current_stage = None  # 현재 스테이지 상태를 저장

def init():
    global image, current_stage

    open_canvas()

    current_mode = "stage1_mode"

    # 모드에 따라 current_stage 설정
    if current_mode == "stage1_mode":
        current_stage = "stage1"
        image_path = './Art/Menu/lose.png'  # stage1 전용 이미지

    print(f"[DEBUG] current_stage set to {current_stage}")  # 디버깅 로그 추가

    image = load_image(image_path)
    print(f"Lose Mode Initialized for {current_stage}")

def update():
    pass

def draw():
    clear_canvas()
    image.draw_to_origin(0, 0, 800, 600)
    update_canvas()

def handle_events():
    global current_stage

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:  # SPACE 키로 재시작
            # 현재 스테이지에 따라 해당 스테이지로 돌아감
            if current_stage == "stage1":
                game_framework.change_mode(enter_stage1)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()

def finish():
    global image
    del image
    print(f"Lose Mode Finished for {current_stage}")
