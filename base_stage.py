from pico2d import *

import game_framework
import game_world
import lose_mode_stage2
from bomb_effect import BombEffect
from key import Key
from monster_removal_timer import MonsterRemovalTimer
from player import Player
from monster import Monster
from bomb import Bomb
import random
import lose_mode_stage1
from potion import Potion
from power_monster import PowerMonster

# 폭탄 사운드 로드
bomb_sound = None
potion_sound = None  # 포션 사운드 추가


# 초기화
WIDTH, HEIGHT = 800, 600
MAP_WIDTH, MAP_HEIGHT = 1600, 1200
click_position = None  # 마우스 클릭 위치
bomb_count = 0  # 플레이어가 수집한 폭탄의 수

key_collected = False  # Key 획득 여부

# 스폰 관련 변수
spawn_timer = 0  # 마지막 몬스터 스폰 시점
spawn_interval = 5.0  # 몬스터 스폰 간격 (초)
spawn_count = 0  # 처음 스폰되는 몬스터 수

# 폭탄 생성 관련 변수
bomb_spawn_timer = 0  # 마지막 폭탄 생성 시점
bomb_spawn_interval = 1.5  # 폭탄 생성 간격 (초)
special_bomb_timer = 0  # 마지막 특수 폭탄 생성 시점
potion_spawn_timer = 0
power_monster_spawn_timer = 0
stage_start_time = 0  # 스테이지 시작 시간을 저장하는 변수

def init():
    global player, monsters, bombs, camera, background, range_image, health_bar_image
    global bomb_count, spawn_timer, spawn_interval, spawn_count, current_time, key_display_time
    global bomb_spawn_timer, special_bomb_timer, monster_removal_timers, bomb_effects, key_collected, key_spawned, bomb_sound
    global stage_start_time

    # 스테이지 시작 시 Key 표시 시간 초기화
    key_display_time = 101  # 현재 시간 + 3분

    stage_start_time = get_time()  # 스테이지가 시작된 시점 기록

    # 폭탄 터지는 사운드 로드
    bomb_sound = load_wav('./assets/sound/bomb.wav')  # 폭탄 사운드
    bomb_sound.set_volume(128)  # 볼륨 조절 (0 ~ 128)

    # 포션 획득 사운드 로드
    potion_sound = load_wav('./assets/sound/potion.wav')  # 포션 사운드
    potion_sound.set_volume(128)  # 볼륨 조절 (0 ~ 128)

    # 현재 모드를 확인하여 배경 이미지 설정
    current_mode = game_framework.stack[-1].__name__
    if current_mode == "stage1_mode":
        background_path = './assets/gamebackground.png'
    elif current_mode == "stage2_mode":
        background_path = './assets/gamebackground_2.png'
    else:
        background_path = './assets/gamebackground.png'  # 기본 배경 이미지

    # 배경 이미지 로드
    background = load_image(background_path)
    print(f"[DEBUG] Background Loaded: {background_path}")
    range_image = load_image("./Art/Mouse/Mouse InRange.png")  # "InRange.png" 로드
    health_bar_image = load_image('./Art/HUD/Health bar Temp.png')  # Health bar 이미지 로드

    # 모든 게임 월드 객체 삭제 및 충돌 데이터 초기화
    game_world.clear()

    # 카메라 생성
    camera = Camera(MAP_WIDTH, MAP_HEIGHT)
    current_time = 0

    # 플레이어 생성 및 초기화
    player = Player(800, 600, camera)  # 초기 위치
    game_world.add_object(player, 1)  # 레이어 1에 추가

    # 몬스터 및 폭탄 관련 변수 초기화
    bomb_count = 0  # 초기 폭탄 개수
    spawn_timer = 0  # 마지막 몬스터 스폰 시점
    spawn_interval = 5.0  # 몬스터 스폰 간격
    spawn_count = 17  # 처음 스폰되는 몬스터 수
    bomb_spawn_timer = 0  # 마지막 폭탄 생성 시점
    special_bomb_timer = 0  # 특수 폭탄 생성 타이머


    # 폭발 효과 및 제거 타이머 초기화
    # 폭발 효과 및 제거 타이머 초기화
    monster_removal_timers = []
    bomb_effects = []

    # Key 관련 변수 초기화
    key_spawned = False  # Key가 생성되었는지 상태를 추적
    key_collected = False

    # 초기 몬스터 스폰
    spawn_monsters(spawn_count, player, camera)
    spawn_key()


# 카메라 클래스 정의
class Camera:
    def __init__(self, width, height):
        self.x, self.y = 0, 0
        self.width = width
        self.height = height

        self.mouse_x = 0  # 마우스 X 좌표 초기화
        self.mouse_y = 0  # 마우스 Y 좌표 초기화

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

def spawn_key():
    """Key를 3분 후에 생성."""
    global key_display_time, key_collected, key_spawned, current_time

    if not key_collected and not key_spawned and current_time >= key_display_time:
        # Key 생성
        x = random.randint(100, MAP_WIDTH - 100)  # Key 생성 위치
        y = random.randint(100, MAP_HEIGHT - 100)
        key_object = Key(x, y, camera)
        game_world.add_object(key_object, 1)  # Key를 게임 월드에 추가
        game_world.add_collision_pair('player:key', player, key_object)  # 충돌 처리
        print("Key spawned!")  # 디버깅용 메시지
        key_spawned = True;


def spawn_bomb(camera, is_special=False):
    bomb = Bomb(camera, is_special=is_special)
    game_world.add_object(bomb, 1)  # 게임 월드에 폭탄 추가
    game_world.add_collision_pair('player:bomb', player, bomb)
   # print(f"{'Special ' if is_special else ''}Bomb spawned at ({bomb.x}, {bomb.y})")

def spawn_potion(camera):
    x = random.randint(100, MAP_WIDTH-100)
    y = random.randint(100, MAP_HEIGHT-100)
    potion = Potion(x, y, camera)
    game_world.add_object(potion, 1)  # 레이어 1에 포션 추가
    game_world.add_collision_pair('player:potion', player, potion)

def spawn_power_monster(player, camera):
    """Power Monster 생성"""
    x = random.randint(100, MAP_WIDTH-100)
    y = random.randint(100, MAP_HEIGHT-100)
    power_monster = PowerMonster(x, y, player, camera)
    game_world.add_object(power_monster, 1)  # 레이어 1에 추가
    game_world.add_collision_pair('player:power_monster', player, power_monster)  # 플레이어와 충돌 처리
    game_world.add_collision_pair('bomb:power_monster', None, power_monster)  # 폭탄과 충돌 처리
  #  print("[DEBUG] Power Monster spawned!")



#충돌 박스 그리기
def draw_bounding_box(obj, camera_x, camera_y):
    left, bottom, right, top = obj.get_bb()
    draw_rectangle(left - camera_x, bottom - camera_y, right - camera_x, top - camera_y)


# 몬스터 제거 타이머 리스트
monster_removal_timers = []
# 폭발 효과 리스트
bomb_effects = []

def handle_bomb_explosion(x, y):
    global bomb_effects, bomb_sound

    world_x = x + camera.x
    world_y = y + camera.y

    for obj in game_world.world[1]:
        if hasattr(obj, 'tag') and obj.tag in ["m", "M"]:  # 일반 몬스터와 파워 몬스터 모두 처리
            distance = ((obj.x - world_x) ** 2 + (obj.y - world_y) ** 2) ** 0.5
            delay = distance * 0.002  # 거리 비례 딜레이
            if distance <= 300:  # 폭발 반경 내에 있는 경우
                if hasattr(obj, 'hp'):  # 파워 몬스터의 경우
                    obj.hp -= 1
                  #  print(f"[DEBUG] Power Monster HP: {obj.hp}")
                    if obj.hp <= 0:  # 파워 몬스터가 죽을 때
                        bomb_effects.append(BombEffect(obj.x, obj.y, camera, effect_type="gray", delay=delay))  # gray 효과
                        monster_removal_timers.append(MonsterRemovalTimer(obj, delay))  # 제거 타이머 추가
                      #  print("[DEBUG] Power Monster Killed!")
                else:  # 일반 몬스터의 경우
                    if obj.type == "green":
                        bomb_effects.append(BombEffect(obj.x, obj.y, camera, effect_type="green", delay=delay))
                    elif obj.type == "red":
                        bomb_effects.append(BombEffect(obj.x, obj.y, camera, effect_type="red", delay=delay))
                    monster_removal_timers.append(MonsterRemovalTimer(obj, delay))  # 제거 타이머 추가
                  #  print("[DEBUG] Monster Killed!")




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
    global spawn_timer, spawn_count, bomb_spawn_timer, \
        special_bomb_timer, bomb_effects, spawn_interval, potion_spawn_timer, power_monster_spawn_timer, current_time

    current_time = get_time() - stage_start_time  # 스테이지 기준 경과 시간

    # 몬스터 스폰 타이머 확인 및 호출
    if current_time > spawn_timer + spawn_interval:
        spawn_timer = current_time  # 타이머 갱신
        spawn_monsters(spawn_count, player, camera)  # 현재 스폰 카운트만큼 몬스터 스폰
        spawn_count += 1  # 스폰 카운트 증가

        # 현재 모드를 확인하여 스폰 속도 조정
        current_mode = game_framework.stack[-1].__name__
        if current_mode == "stage2_mode":
            spawn_interval = min(7.0, spawn_interval + 1)  # stage2에서는 스폰 간격을 느리게 조정
        else:
            spawn_interval = min(9.0, spawn_interval + 1)  # stage1에서는 스폰 간격을 느리게 조정

    # Power Monster 스폰 타이머 확인 및 호출
    current_mode = game_framework.stack[-1].__name__
    if current_mode == 'stage2_mode' and current_time > power_monster_spawn_timer + 10.0:
        power_monster_spawn_timer = current_time
        spawn_power_monster(player, camera)


    # 폭탄 생성 타이머 확인 및 호출
    if current_time > bomb_spawn_timer + bomb_spawn_interval:
        bomb_spawn_timer = current_time  # 폭탄 타이머 갱신
        spawn_bomb(camera)  # 폭탄 생성

    # 특수 폭탄 생성
    if game_framework.stack[-1].__name__ == "stage2_mode":
        # stage2에서는 5초마다 생성
        if current_time > special_bomb_timer + 7.0:
            special_bomb_timer = current_time
            spawn_bomb(camera, is_special=True)
    else:
        # 기본 스테이지에서는 20초마다 생성
        if current_time > special_bomb_timer + 20.0:
            special_bomb_timer = current_time
            spawn_bomb(camera, is_special=True)

    # 폭발 효과 업데이트 및 제거
    elapsed_time = 0.016  # 60FPS 기준 프레임 간 시간
    for effect in bomb_effects[:]:
        effect.update(elapsed_time)
        if effect.finished:  # 애니메이션이 끝난 효과 제거
            bomb_effects.remove(effect)

    # 몬스터 제거 타이머 업데이트 및 제거
    for timer in monster_removal_timers[:]:
        if timer.update(0.016):  # 매 프레임 0.016초씩 추가
            monster_removal_timers.remove(timer)
            if bomb_sound:
                bomb_sound.play()


    # 포션 생성
    if current_time > potion_spawn_timer + (8.0 if game_framework.stack[-1].__name__ == 'stage2_mode' else 15.0):
        potion_spawn_timer = current_time
        spawn_potion(camera)

    if player.hp <= 0:
            # 현재 게임 모드에 따라 다음 모드로 전환
            if game_framework.stack[-1].__name__ == 'stage1_mode':
                game_framework.change_mode(lose_mode_stage1)
              #  print(f"Current mode: {game_framework.stack[-1].__name__}")  # 디버깅 메시지

            elif game_framework.stack[-1].__name__ == 'stage2_mode':
                import win_mode  # Import win_mode 모드
                game_framework.change_mode(lose_mode_stage2)


    camera.update(player.x, player.y)

    # 모든 객체 업데이트
    game_world.update()

    # 충돌 처리
    game_world.handle_collisions()

    spawn_key()

    # 프레임 속도를 유지하기 위해 지연 추가
    delay(0.016)  # 약 60 FPS 유지


font = None  # 폰트 객체

def draw_bomb_count():
    """폭탄 개수를 실시간으로 화면에 출력"""
    global font
    if font is None:  # 폰트가 로드되지 않은 경우 로드
        font = load_font('consola.ttf', 30)
    font.draw(10,570, f"Bomb Count: {bomb_count}", (255, 0,0))  # 좌상단에 출력


def draw_current_time():
    """100에서 감소하는 시간을 실시간으로 화면에 출력"""
    global font, current_time
    if font is None:  # 폰트가 로드되지 않은 경우 로드
        font = load_font('consola.ttf', 30)

    # 100에서 감소한 시간 계산
    remaining_time = max(0, 101 - current_time)

    font.draw(580, 570, f"Time: {remaining_time:.2f} s", (255, 255, 0))  # 좌상단에 초 단위로 출력


# 화면 그리기
def draw():
    clear_canvas()

    # 배경 이미지 그리기
    background.draw_to_origin(-camera.x, -camera.y, MAP_WIDTH, MAP_HEIGHT)

    # 게임 월드의 모든 객체 렌더링
    game_world.render()

    # 폭탄 개수 그리기
    draw_bomb_count()

    draw_current_time()

    # Health Bar 이미지 그리기
    health_bar_image.draw(130, 530)  # 적절한 위치에 출력 (좌표 조정 가능)

    # Health Bar 내부에 체력 비례한 크기로 이미지 출력
    max_bar_width = 200  # Health Bar의 최대 길이
    current_hp_width = max_bar_width * (player.hp / 105)  # 현재 HP에 비례한 길이 계산
    left = 50  # Health Bar 왼쪽 X 좌표
    bottom = 520  # Health Bar 아래쪽 Y 좌표
    bar_center_x = left + current_hp_width / 2  # Health Bar 중심 X 좌표
    bar_height = 20  # Health Bar 높이

    # 체력 게이지 이미지 로드 (health_bar_rectangle.png)
    health_fill_image = load_image('./Art/HUD/Health Bar rectangle.png')

    # 현재 HP에 맞춰 크기 조정 후 출력
    health_fill_image.draw(bar_center_x, bottom + bar_height / 2, current_hp_width, bar_height)


    # 폭발 효과 그리기
    for effect in bomb_effects:
        effect.draw()


    # 마우스 클릭 이미지 그리기
    if click_position:
        x, y = click_position
        range_image.draw(x, y)


    update_canvas()

# 게임 종료
def finish():
    global font
    if font is not None:
        del font  # 폰트 객체 해제
        font = None
    game_world.clear()  # 모든 게임 객체 정리

# 게임 프레임워크가 사용하는 메소드 연결
def pause():
    pass

def resume():
    pass

# 키 입력 상태 추적
key_states = {SDLK_w: False, SDLK_s: False, SDLK_a: False, SDLK_d: False}

