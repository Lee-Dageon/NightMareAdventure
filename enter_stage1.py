from pico2d import *
import game_framework
from pico2d import clear_canvas, update_canvas, get_events, load_image, get_time
import stage1_mode

timer = 0  # 경과 시간을 저장할 변수
delay_time = 3  # 5초 후에 stage1_mode로 진입
background_image = None  # 배경 이미지

def init():
    global background_image, timer
    open_canvas()  # 캔버스 열기
    background_image = load_image('./assets/enter_stage1.png')  # Stage 1 전환 화면
    timer = get_time()  # 시작 시간을 초기화

def update():
    global timer
    current_time = get_time()  # 현재 시간 가져오기
    if current_time - timer >= delay_time:  # 5초가 경과하면
        game_framework.change_mode(stage1_mode)  # stage1_mode로 진입

def draw():
    clear_canvas()
    background_image.draw_to_origin(0, 0, 800, 600)  # 배경 이미지 그리기
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:  # ESC 키로 게임 종료
            game_framework.quit()

def finish():
    global background_image
    del background_image
    close_canvas()
