from pico2d import get_time, load_music
import base_stage
import game_framework

# stage2 전용 배경음악 변수
stage2_music = None

def init():
    global stage2_music
    base_stage.init()  # Base 스테이지 초기화

    # 배경음악 로드 및 재생
    stage2_music = load_music('./assets/Music/stage_2.mp3')  # Stage 2
    stage2_music.set_volume(30)  # 볼륨 설정 (0~128)
    stage2_music.repeat_play()  # 반복 재생

def update():
    base_stage.update()


def draw():
    base_stage.draw()  # 기본 그리기 로직 실행

def finish():
    base_stage.finish()  # 기본 종료 로직 실행

def handle_events():
    base_stage.handle_events()  # 기본 이벤트 처리 실행
