from pico2d import get_time
import base_stage
import game_framework
import lose_mode_stage2

def init():
    base_stage.init()  # Base 스테이지 초기화

# stage2_mode 업데이트에서 Power Monster 스폰
def update():
    base_stage.update()


def draw():
    base_stage.draw()  # 기본 그리기 로직 실행

def finish():
    base_stage.finish()  # 기본 종료 로직 실행

def handle_events():
    base_stage.handle_events()  # 기본 이벤트 처리 실행
