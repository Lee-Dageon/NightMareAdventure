from pico2d import *
import math

import game_world
import stage1_mode

class Idle:
    @staticmethod
    def enter(player):
        print("Entering Idle state")

    @staticmethod
    def exit(player):
        print("Exiting Idle state")

    @staticmethod
    def update(player):
        # 이동 입력이 있으면 Move 상태로 전환
        if player.key_states.get(SDLK_w) or player.key_states.get(SDLK_s) or player.key_states.get(SDLK_a) or player.key_states.get(SDLK_d):
            player.change_state(Move)


class Move:
    @staticmethod
    def enter(player):
        print("Entering Move state")

    @staticmethod
    def exit(player):
        print("Exiting Move state")

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
        self.image = load_image('./Art/Character/Player Secondary Attack frame 1.png')
        self.x, self.y = x, y
        self.speed = 8
        self.angle = 0  # 플레이어의 회전 각도
        self.state = Idle  # 초기 상태는 Idle
        self.state.enter(self)

        self.key_states = {}  # 키 입력 상태를 저장
        self.camera = camera  # 카메라 객체를 참조

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


    def draw(self):
        # 플레이어 이미지를 카메라 보정 좌표에 따라 회전하며 그리기
        camera_x, camera_y = self.camera.x, self.camera.y
        self.image.rotate_draw(self.angle, self.x - self.camera.x, self.y - self.camera.y)

        # 충돌 박스도 카메라 보정 후 그리기
        left, bottom, right, top = self.get_bb()
        draw_rectangle(left - camera_x, bottom - camera_y, right - camera_x, top - camera_y)

    def get_bb(self):
        # 충돌 박스 반환 (플레이어 크기 기준)
        width, height = 32, 32
        return self.x - width // 2, self.y - height // 2, self.x + width // 2, self.y + height // 2

    def handle_collision(self, group, other):
        if group == "player:monster":
            print("Player collided with a Monster!")
            # 몬스터 충돌 처리 로직 추가

        if group == "player:bomb":
            print("Player collided with a Bomb!")
            stage1_mode.bomb_count += 1  # 폭탄 개수 증가
