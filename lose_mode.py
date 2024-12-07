from pico2d import *
import game_framework
from pico2d import clear_canvas, update_canvas, get_events, load_image, get_time
import stage1_mode  # 필요한 경우 import
import stage2_mode  # 필요한 경우 import


def init(stage="stage1"):
    global image
    global current_stage

    open_canvas()

    current_stage = stage  # 현재 스테이지를 저장

    # 스테이지에 따라 로드할 이미지 선택
    if current_stage == "stage1":
        image_path = './Art/Menu/lose.png'  # stage1 전용 이미지
    elif current_stage == "stage2":
        image_path = './Art/Menu/lose.png'  # stage2 전용 이미지
    else:
        image_path = './Art/Menu/lose.png'  # 기본 이미지 (예외 처리)

    image = load_image(image_path)
    print(f"Lose Mode Initialized for {current_stage}")

def update():
    pass  # 필요한 업데이트 로직을 여기에 추가

def draw():
    clear_canvas()
    image.draw_to_origin(0, 0, 800, 600)
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_r:  # R키로 재시작
            # 현재 스테이지에 따라 해당 스테이지로 돌아감
            if current_stage == "stage1":
                game_framework.change_mode(stage1_mode)
            elif current_stage == "stage2":
                game_framework.change_mode(stage2_mode)

def finish():
    global image
    del image
    print(f"Lose Mode Finished for {current_stage}")
