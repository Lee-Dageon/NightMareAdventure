from pico2d import *
import random
import math

class Monster:
    def __init__(self, x, y, player, camera):
        self.image = load_image('./Art/Enemies/Basic_Enemy.png')
        self.x, self.y = x, y
        self.speed = random.uniform(0.5, 1.0)
        self.player = player  # 플레이어 객체 참조
        self.camera = camera  # 카메라 객체 참조
        self.tag = "m"  # 태그 추가

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

    def draw(self):
        # 카메라 위치를 보정하여 몬스터 그리기
        camera_x, camera_y = self.camera.x, self.camera.y
        self.image.rotate_draw(self.angle, self.x - camera_x, self.y - camera_y)

        # 충돌 박스도 카메라 보정 후 그리기
        left, bottom, right, top = self.get_bb()
        draw_rectangle(left - camera_x, bottom - camera_y, right - camera_x, top - camera_y)

    def get_bb(self):
        # 충돌 박스 반환 (몬스터 크기 기준)
        width, height = 32, 32
        return self.x - width // 2, self.y - height // 2, self.x + width // 2, self.y + height // 2

    def handle_collision(self, group, other):
        pass
