from pico2d import *

import enter_stage1
import enter_stage2
import game_framework
from pico2d import clear_canvas, update_canvas, get_events, load_image, load_music, get_time

current_stage = None  # 현재 스테이지 상태를 저장
background_music = None  # 배경음악 객체

def init():
    global image, current_stage, background_music

    current_mode = "stage2_mode"

    # 모드에 따라 current_stage 설정
    if current_mode == "stage2_mode":
        current_stage = "stage2"
        image_path = './Art/Menu/lose.png'  # stage2 전용 이미지

    print(f"[DEBUG] current_stage set to {current_stage}")  # 디버깅 로그 추가

    # 이미지 로드
    image = load_image(image_path)

    # lose.mp3 음악 로드 및 재생
    background_music = load_music('./assets/Music/lose.mp3')
    background_music.set_volume(64)  # 볼륨 설정 (0 ~ 128)
    background_music.repeat_play()  # 반복 재생

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
            quit_game()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_SPACE:  # SPACE 키로 재시작
                # 현재 스테이지에 따라 해당 스테이지로 돌아감
                if current_stage == "stage2":
                    stop_music()  # 음악 정지
                    game_framework.change_mode(enter_stage2)
            elif event.key == SDLK_ESCAPE:
                quit_game()

def stop_music():
    """배경 음악 정지"""
    global background_music
    if background_music:
        background_music.stop()

def quit_game():
    """게임 종료"""
    global image, background_music
    stop_music()  # 음악 정지
    if image:
        del image
    close_canvas()  # 캔버스 닫기
    game_framework.quit()  # 게임 프레임워크 종료

def finish():
    global image, background_music
    stop_music()  # 음악 정지
    if image:
        del image
    print(f"Lose Mode Finished for {current_stage}")
