import base_stage
import game_framework
import lose_mode_stage1
from lose_mode_stage1 import current_stage
from pico2d import load_music

stage1_music = None  # 스테이지 1 음악

def init():
    global stage1_music
    base_stage.init()

    # stage1 음악 로드 및 재생
    stage1_music = load_music("./assets/Music/stage_1.mp3")
    stage1_music.set_volume(50)  # 볼륨 설정 (0~128)
    stage1_music.repeat_play()  # 반복 재생

def update():
    base_stage.update()

def draw():
    base_stage.draw()

def finish():
    global stage1_music
    base_stage.finish()
    if stage1_music:
        stage1_music.stop()  # 모드 종료 시 음악 정지
        stage1_music = None  # 메모리 정리

def handle_events():
    base_stage.handle_events()
