from pico2d import *
from pico2d import clear_canvas, update_canvas, get_events, load_image, load_music
import game_framework

win_image = None  # 승리 화면 이미지
win_music = None  # 승리 음악

def init():
    """승리 모드에 진입"""
    global win_image, win_music
    open_canvas()
    win_image = load_image('./Art/Menu/win.png')  # 승리 화면 이미지 로드

    # MP3 음악 로드 및 재생
    win_music = load_music('./assets/Music/win.mp3')  # 음악 파일 경로
    win_music.set_volume(64)  # 볼륨 설정 (0 ~ 128)
    win_music.repeat_play()  # 음악 반복 재생

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
            quit_game()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:  # ESC 키로 게임 종료
                quit_game()
            elif event.key == SDLK_SPACE:  # SPACE 키로 메인 화면으로 이동
                import start_mode
                stop_music()  # 음악 정지
                game_framework.change_mode(start_mode)

def stop_music():
    """배경 음악 정지"""
    global win_music
    if win_music:
        win_music.stop()

def quit_game():
    """게임 종료"""
    global win_image, win_music
    stop_music()  # 음악 정지
    if win_image:
        del win_image
    close_canvas()  # 캔버스 닫기
    game_framework.quit()  # 게임 프레임워크 종료

def finish():
    global win_image, win_music
    stop_music()  # 음악 정지
    if win_image:
        del win_image
    close_canvas()
