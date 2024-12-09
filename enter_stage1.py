from pico2d import *
import game_framework
from pico2d import clear_canvas, update_canvas, get_events, load_image, load_music, get_time
import stage1_mode

timer = 0  # 경과 시간을 저장할 변수
delay_time = 3  # 3초 후에 stage1_mode로 진입
background_image = None  # 배경 이미지
background_music = None  # 배경 음악

def init():
    global background_image, background_music, timer

    # 배경 이미지 로드
    background_image = load_image('./assets/enter_stage1.png')  # Stage 1 전환 화면

    # 음악 로드 및 재생
    background_music = load_music('./assets/Music/enter_stage_1.ogg')  # 음악 파일 로드
    background_music.set_volume(128)  # 볼륨 설정 (0 ~ 128)
    background_music.repeat_play()  # 음악 반복 재생

    timer = get_time()  # 시작 시간을 초기화

def update():
    global timer
    current_time = get_time()  # 현재 시간 가져오기
    if current_time - timer >= delay_time:  # 3초가 경과하면
        stop_music()  # 음악 정지
        game_framework.change_mode(stage1_mode)  # stage1_mode로 진입

def draw():
    clear_canvas()
    background_image.draw_to_origin(0, 0, 800, 600)  # 배경 이미지 그리기
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            quit_game()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:  # ESC 키로 게임 종료
            quit_game()

def stop_music():
    """배경 음악 정지"""
    global background_music
    if background_music:
        background_music.stop()


def quit_game():
    game_framework.quit()  # 게임 프레임워크 종료


def finish():
    """모드 종료"""
    global background_image, background_music
    stop_music()  # 음악 정지
    if background_image:
        del background_image
