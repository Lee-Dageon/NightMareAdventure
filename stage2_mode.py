from pico2d import get_time
import base_stage
import game_framework
import lose_mode_stage2

def init():
    base_stage.init()  # Base 스테이지 초기화

def update():
    global key_spawned, key_collected, key_display_time
    base_stage.update()  # 기본 업데이트 로직 실행
    base_stage.spawn_key()  # Key 생성

def draw():
    base_stage.draw()  # 기본 그리기 로직 실행

def finish():
    base_stage.finish()  # 기본 종료 로직 실행

def handle_events():
    base_stage.handle_events()  # 기본 이벤트 처리 실행
