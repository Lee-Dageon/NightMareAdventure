from pico2d import *
import math

import game_world
import base_stage

class Idle:
    @staticmethod
    def enter(player):
        pass
      #  print("Entering Idle state")

    @staticmethod
    def exit(player):
        pass
      #  print("Exiting Idle state")

    @staticmethod
    def update(player):
        # 이동 입력이 있으면 Move 상태로 전환
        if player.key_states.get(SDLK_w) or player.key_states.get(SDLK_s) or player.key_states.get(SDLK_a) or player.key_states.get(SDLK_d):
            player.change_state(Move)


class Move:
    @staticmethod
    def enter(player):
        pass
      #  print("Entering Move state")

    @staticmethod
    def exit(player):
        pass
       # print("Exiting Move state")

    @staticmethod
    def update(player):
        # 이동 로직
        if player.key_states.get(SDLK_w, False):
            player.y += player.speed
        if player.key_states.get(SDLK_s, False):
            player.y -= player.speed
        if player.key_states.get(SDLK_a, False):
            player.x -= player.speed
        if player.key_states.get(SDLK_d, False):
            player.x += player.speed

        # 맵 경계 제한
        player.x = max(0, min(player.x, 1600))
        player.y = max(0, min(player.y, 1200))

        # 이동 입력이 없으면 Idle 상태로 전환
        if not (player.key_states.get(SDLK_w) or player.key_states.get(SDLK_s) or player.key_states.get(SDLK_a) or player.key_states.get(SDLK_d)):
            player.change_state(Idle)


class Player:
    def __init__(self, x, y, camera):
        self.image = load_image('./Art/Character/main_player.png')
        self.x, self.y = x, y
        self.speed = 8
        self.angle = 0  # 플레이어의 회전 각도
        self.state = Idle  # 초기 상태는 Idle
        self.state.enter(self)

        self.key_states = {}  # 키 입력 상태를 저장
        self.camera = camera  # 카메라 객체를 참조

        # 애니메이션 속성 초기화
        self.frame = 0  # 현재 프레임
        self.frame_time = 0  # 프레임 갱신을 위한 시간 계산
        self.scale = 1.5  # 캐릭터 크기를 조정하는 배율

        # 체력 관련 속성
        self.max_hp = 100  # 최대 체력
        self.hp = self.max_hp  # 현재 체력

    def take_damage(self, amount):
        """체력을 감소시키는 메서드"""
        self.hp = max(0, self.hp - amount)  # 최소 0으로 제한

    def heal(self, amount):
        """체력을 회복시키는 메서드"""
        self.hp = min(self.max_hp, self.hp + amount)  # 최대 체력으로 제한

    def change_state(self, new_state):
        """상태 전환 메서드"""
        self.state.exit(self)
        self.state = new_state
        self.state.enter(self)

    def update(self):
        """현재 상태에 따라 업데이트 실행"""
        self.state.update(self)
        # 마우스 위치에 따라 플레이어의 회전 각도 계산
        mouse_x, mouse_y = self.camera.mouse_x, self.camera.mouse_y
        dx = mouse_x + self.camera.x - self.x
        dy = mouse_y + self.camera.y - self.y
        self.angle = math.atan2(dy, dx)

        # 프레임 애니메이션 업데이트
        self.frame_time += 1
        if self.frame_time >= 5:  # 5틱마다 프레임 변경 (애니메이션 속도 조정 가능)
            self.frame = (self.frame + 1) % 3
            self.frame_time = 0



    def draw(self):
        # 플레이어 이미지를 카메라 보정 좌표에 따라 회전하며 그리기
        camera_x, camera_y = self.camera.x, self.camera.y

        # 각도에 따라 행 계산
        degree = math.degrees(self.angle)
        if -45 <= degree < 45:
            row = 2  # 오른쪽
        elif 45 <= degree < 135:
            row = 3  # 위쪽
        elif 135 <= degree or degree < -135:
            row = 1  # 왼쪽
        elif -135 <= degree < -45:
            row = 0  # 아래쪽

        # 스프라이트 크기 및 위치 계산
        sprite_width = self.image.w // 3
        sprite_height = self.image.h // 4

        # 확대된 크기
        scaled_width = sprite_width * self.scale
        scaled_height = sprite_height * self.scale

        # 그리기
        self.image.clip_draw(
            self.frame * sprite_width, (3 - row) * sprite_height,
            sprite_width, sprite_height,
            self.x - camera_x, self.y - camera_y,
            scaled_width, scaled_height  # 키운 크기로 출력
        )

        # 충돌 박스도 카메라 보정 후 그리기
        left, bottom, right, top = self.get_bb()
        draw_rectangle(left - camera_x, bottom - camera_y, right - camera_x, top - camera_y)

    def get_bb(self):
        # 충돌 박스 반환 (플레이어 크기 기준)
        width, height = 32, 32
        return self.x - width // 2, self.y - height // 2, self.x + width // 2, self.y + height // 2

    def handle_collision(self, group, other):
        if group == "player:monster":
            self.hp -= 0.03
            print("Player collided with a Monster!")
            # 몬스터 충돌 처리 로직 추가

        if group == "player:bomb":
           # print("Player collided with a Bomb!")
            base_stage.bomb_count += 1  # 폭탄 개수 증가
