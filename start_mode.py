from pico2d import *
from pico2d import clear_canvas, update_canvas, get_events, load_image, load_music

import enter_stage1
import game_framework

start_image = None  # 시작 화면 이미지
start_music = None  # 시작 화면 음악


def init():
    """시작 모드에 진입"""
    global start_image, start_music
    start_image = load_image('./assets/game_start.png')  # 시작 화면 이미지 로드

    # 음악 로드 및 재생
    start_music = load_music('./assets/Music/start_mode.mp3')  # 음악 파일 로드
    start_music.set_volume(64)  # 볼륨 조절 (0 ~ 128)
    start_music.repeat_play()  # 반복 재생


def update():
    pass


def draw():
    global start_image
    if start_image:  # start_image가 None인지 확인
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
    global start_image, start_music
    # 음악 중지
    if start_music:
        start_music.stop()
        start_music = None
    # 이미지 삭제
    if start_image:
        del start_image
        start_image = None
    game_framework.quit()  # 게임 프레임워크 종료


def finish():
    global start_image, start_music
    # 음악 중지
    if start_music:
        start_music.stop()
        start_music = None
    # 이미지 삭제
    if start_image:
        del start_image
        start_image = None
