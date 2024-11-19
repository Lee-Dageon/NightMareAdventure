# stage1_mode.py
from pico2d import *
import game_framework
import game_world
from player import Player
from monster import Monster
from bomb import Bomb
import random

# 초기화
WIDTH, HEIGHT = 800, 600
MAP_WIDTH, MAP_HEIGHT = 1600, 1200
click_position = None  # 마우스 클릭 위치
bomb_count = 0  # 플레이어가 수집한 폭탄의 수

# 스폰 관련 변수
spawn_timer = 0  # 마지막 몬스터 스폰 시점
spawn_interval = 5.0  # 몬스터 스폰 간격 (초)
spawn_count = 10  # 처음 스폰되는 몬스터 수

# 폭탄 생성 관련 변수
bomb_spawn_timer = 0  # 마지막 폭탄 생성 시점
bomb_spawn_interval = 3.0  # 폭탄 생성 간격 (초)

# 게임 객체 초기화
def init():
    global player, monsters, bombs, camera, background,range_image, bomb_count

    open_canvas(WIDTH, HEIGHT)

    # 배경 이미지 로드
    background = load_image('./assets/gamebackground.png')
    range_image = load_image("./Art/Mouse/Mouse InRange.png")  # "InRange.png" 로드
    # 카메라 생성
    camera = Camera(MAP_WIDTH, MAP_HEIGHT)

    # 게임 객체 생성
    player = Player(800, 600, camera)  # 초기 위치
    game_world.add_object(player, 1)  # 레이어 1에 추가
    monsters = []
    bombs = []

    # 초기 몬스터 스폰
    spawn_monsters(spawn_count, player, camera)

# 카메라 클래스 정의
class Camera:
    def __init__(self, width, height):
        self.x, self.y = 0, 0
        self.width = width
        self.height = height

    def update(self, target_x, target_y):
        self.x = max(0, min(target_x - WIDTH // 2, self.width - WIDTH))
        self.y = max(0, min(target_y - HEIGHT // 2, self.height - HEIGHT))

def spawn_monsters(count, player, camera):
    for _ in range(count):
        x = random.randint(0, MAP_WIDTH)
        y = random.randint(0, MAP_HEIGHT)
        monster = Monster(x, y, player, camera)
        game_world.add_object(monster, 1)  # 게임 월드에 추가
        game_world.add_collision_pair('player:monster', player, monster)

def spawn_bomb(camera):
    bomb = Bomb(camera)
    game_world.add_object(bomb, 1)  # Depth 1에 추가
    game_world.add_collision_pair('player:bomb', player, bomb)
    print(f"Bomb spawned at ({bomb.x}, {bomb.y})")


#충돌 박스 그리기
def draw_bounding_box(obj, camera_x, camera_y):
    left, bottom, right, top = obj.get_bb()
    draw_rectangle(left - camera_x, bottom - camera_y, right - camera_x, top - camera_y)

def handle_bomb_explosion(x, y):
    for obj in game_world.world[1]:
        if hasattr(obj, 'tag') and obj.tag == "m":  # 태그로 몬스터 구분
            distance = ((obj.x - x) ** 2 + (obj.y - y) ** 2) ** 0.5
            print(f"Distance to monster: {distance}")
            if distance <= 2000:
                print(f"Removing monster at ({obj.x}, {obj.y})")
                game_world.remove_object(obj)



def handle_events():
    global player, click_position, bomb_count
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            player.key_states[event.key] = True
        elif event.type == SDL_KEYUP:
            player.key_states[event.key] = False
        elif event.type == SDL_MOUSEMOTION:
            camera.mouse_x, camera.mouse_y = event.x, HEIGHT - event.y  # 카메라에 마우스 위치 저장
        elif event.type == SDL_MOUSEBUTTONDOWN:  # 마우스 클릭 이벤트
            x, y = event.x, HEIGHT - event.y  # 클릭 좌표 변환
            click_position = (x, y)  # 클릭 위치 저장

         # 폭탄을 사용할 수 있는 경우
            if bomb_count > 0:
                handle_bomb_explosion(x, y)  # 클릭 좌표에서 폭발 처리
                bomb_count -= 1  # 폭탄 사용

        elif event.type == SDL_MOUSEBUTTONUP:  # 마우스 버튼 떼기 이벤트
            click_position = None  # 클릭 위치 초기화

# 게임 업데이트 로직
def update():
    global spawn_timer, spawn_count, bomb_spawn_timer

    # 현재 시간 가져오기
    current_time = get_time()

    # 몬스터 스폰 타이머 확인 및 호출
    if current_time > spawn_timer + spawn_interval:
        spawn_timer = current_time  # 타이머 갱신
        spawn_monsters(spawn_count, player, camera)  # 현재 스폰 카운트만큼 몬스터 스폰
        spawn_count += 1  # 스폰 카운트 증가

    # 폭탄 생성 타이머 확인 및 호출
    if current_time > bomb_spawn_timer + bomb_spawn_interval:
        bomb_spawn_timer = current_time  # 폭탄 타이머 갱신
        spawn_bomb(camera)  # 폭탄 생성


    camera.update(player.x, player.y)

    # 모든 객체 업데이트
    game_world.update()

    # 충돌 처리
    game_world.handle_collisions()

    # 프레임 속도를 유지하기 위해 지연 추가
    delay(0.016)  # 약 60 FPS 유지


font = None  # 폰트 객체

def draw_bomb_count():
    """폭탄 개수를 실시간으로 화면에 출력"""
    global font
    if font is None:  # 폰트가 로드되지 않은 경우 로드
        font = load_font('consola.ttf', 30)
    font.draw(10,570, f"Bomb Count: {bomb_count}", (255, 0,0))  # 좌상단에 출력

# 화면 그리기
def draw():
    clear_canvas()



    # 배경 이미지 그리기
    background.draw_to_origin(-camera.x, -camera.y, MAP_WIDTH, MAP_HEIGHT)
    # 게임 월드의 모든 객체 렌더링
    game_world.render()

    # 폭탄 개수 그리기
    draw_bomb_count()



    # 마우스 클릭 이미지 그리기
    if click_position:
        x, y = click_position
        range_image.draw(x, y)


    update_canvas()

# 게임 종료
def finish():
    close_canvas()

# 게임 프레임워크가 사용하는 메소드 연결
def pause():
    pass

def resume():
    pass

# 키 입력 상태 추적
key_states = {SDLK_w: False, SDLK_s: False, SDLK_a: False, SDLK_d: False}

