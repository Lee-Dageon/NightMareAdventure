from pico2d import *
import random
import math

class Monster:
    def __init__(self, x, y, player, camera):
        self.type = random.choice(["red", "green"])  # 몬스터 타입 선택
        if self.type == "red":
            self.image = load_image('./Art/Enemies/red_enemy.png')
        else:
            self.image = load_image('./Art/Enemies/green_enemy.png')
        self.x, self.y = x, y
        self.speed = random.uniform(0.5, 1.0)
        self.player = player  # 플레이어 객체 참조
        self.camera = camera  # 카메라 객체 참조
        self.tag = "m"  # 태그 추가

        # 애니메이션 속성
        self.frame = 0  # 현재 프레임
        self.frame_time = 0  # 프레임 갱신 타이밍


    def update(self):
        # 플레이어 위치를 따라 이동
        dx = self.player.x - self.x
        dy = self.player.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > 0:
            self.x += (self.speed * dx / distance)
            self.y += (self.speed * dy / distance)

        # 플레이어를 바라보는 각도 계산
        self.angle = math.atan2(dy, dx)

        # 프레임 애니메이션 업데이트
        self.frame_time += 1
        if self.frame_time >= 5:  # 5틱마다 프레임 변경
            self.frame = (self.frame + 1) % 3  # 3열 기준 (0, 1, 2)
            self.frame_time = 0

    def draw(self):

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

        # 카메라 위치를 보정하여 몬스터 그리기
        camera_x, camera_y = self.camera.x, self.camera.y

        # 스프라이트 크기 계산
        sprite_width = self.image.w // 3  # 3열
        sprite_height = self.image.h // 4  # 4행
        scale = 1.5  # 크기를 1.5배로 확대

        # 확대된 크기 계산
        scaled_width = int(sprite_width * scale)
        scaled_height = int(sprite_height * scale)

        # 스프라이트 그리기
        self.image.clip_draw_to_origin(
            self.frame * sprite_width, (3 - row) * sprite_height,
            sprite_width, sprite_height,
            int(self.x - camera_x - scaled_width // 2),  # 중심 좌표 맞춤
            int(self.y - camera_y - scaled_height // 2),
            scaled_width, scaled_height
        )

        # 충돌 박스도 카메라 보정 후 그리기
        left, bottom, right, top = self.get_bb()
        draw_rectangle(left - camera_x, bottom - camera_y, right - camera_x, top - camera_y)

    def get_bb(self):
        # 충돌 박스 반환 (몬스터 크기 기준)
        width, height = 32, 32
        return self.x - width // 2, self.y - height // 2, self.x + width // 2, self.y + height // 2

    def handle_collision(self, group, other):
        pass
