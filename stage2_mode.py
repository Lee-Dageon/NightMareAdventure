from pico2d import get_time
import base_stage
import game_framework
import lose_mode_stage2

def init():
    global key_collected, key_display_time, key_spawned

    base_stage.init()  # Base 스테이지 초기화
    key_collected = False  # Key 초기화 상태를 설정
    key_spawned = False

    # 스테이지 시작 시점의 시간에서 3분 후를 Key 생성 시점으로 설정
    key_display_time = get_time() + 200  # 현재 시간 + 180초

def update():
    global key_spawned, key_collected, key_display_time

    base_stage.update()  # 기본 업데이트 로직 실행

    # Key 생성 조건 확인
    if not key_spawned and not key_collected and get_time() >= key_display_time:
        base_stage.spawn_key()  # Key 생성
        key_spawned = True  # Key가 생성되었음을 표시
        print("Key spawned!")  # 디버깅 메시지 출력


def draw():
    base_stage.draw()  # 기본 그리기 로직 실행

def finish():
    base_stage.finish()  # 기본 종료 로직 실행

def handle_events():
    base_stage.handle_events()  # 기본 이벤트 처리 실행
