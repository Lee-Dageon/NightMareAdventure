from pico2d import *
import random

import game_world
import stage1_mode


class Bomb:
    def __init__(self, camera, is_special=False):
        # 일반 폭탄과 특수 폭탄 이미지 선택
        if is_special:
            self.image = load_image('./Art/Items/special_bomb_character.png')
        else:
            self.image = load_image('./Art/Items/bomb_character.png')

        self.is_special = is_special  # 특수 폭탄 여부 플래그
        self.x = random.randint(100, 1600 - 100)  # 폭탄이 생성될 X 좌표
        self.y = random.randint(100, 1200 - 100)  # 폭탄이 생성될 Y 좌표
        self.camera = camera  # 카메라 객체를 참조

        # 애니메이션 속성 초기화
        self.frame = 0  # 현재 프레임
        self.frame_time = 0  # 프레임 갱신 시간 계산

    def draw(self):
        # 카메라 보정을 적용하여 폭탄을 그리기
        camera_x, camera_y = self.camera.x, self.camera.y

        # 스프라이트 크기와 위치 계산
        sprite_width = self.image.w // 2  # 2열이므로 너비를 2로 나눔
        sprite_height = self.image.h  # 1행이므로 전체 높이 사용

        # 스프라이트를 2배로 확대하여 그리기
        self.image.clip_draw(
            self.frame * sprite_width, 0, sprite_width, sprite_height,
            self.x - camera_x, self.y - camera_y,
            sprite_width * 2, sprite_height * 2  # 2배 크기로 출력
        )

        # 충돌 박스도 카메라 보정 후 그리기
        left, bottom, right, top = self.get_bb()
        draw_rectangle(left - camera_x, bottom - camera_y, right - camera_x, top - camera_y)

    def get_bb(self):
        # 충돌 박스 반환 (폭탄 크기 기준)
        width, height = 40, 50
        return self.x - width // 2, self.y - height // 2, self.x + width // 2, self.y + height // 2

    def handle_collision(self, group, other):
        if group == "player:bomb":
            print(f"{'Special ' if self.is_special else ''}Bomb collided with Player!")
            # 특수 폭탄은 추가 효과 적용
            if self.is_special:
                stage1_mode.bomb_count += 9  # 플레이어의 폭탄 개수를 10 증가

            game_world.remove_object(self)  # 폭탄 삭제

    def update(self):
        # 프레임 애니메이션 업데이트
        self.frame_time += 1
        if self.frame_time >= 10:  # 10틱마다 프레임 전환 (속도 조정 가능)
            self.frame = (self.frame + 1) % 2  # 2프레임(0, 1) 번갈아 출력
            self.frame_time = 0
