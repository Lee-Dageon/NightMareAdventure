from pico2d import *
import random

import game_world


class Bomb:
    def __init__(self, camera):
        self.image = load_image('./Art/Items/bomb.png')
        self.x = random.randint(100, 1600 - 100)  # 폭탄이 생성될 X 좌표
        self.y = random.randint(100, 1200 - 100)  # 폭탄이 생성될 Y 좌표
        self.camera = camera  # 카메라 객체를 참조

    def draw(self):
        # 카메라 보정을 적용하여 폭탄을 그리기
        camera_x, camera_y = self.camera.x, self.camera.y
        self.image.draw(self.x - camera_x, self.y - camera_y)

        # 충돌 박스도 카메라 보정 후 그리기
        left, bottom, right, top = self.get_bb()
        draw_rectangle(left - camera_x, bottom - camera_y, right - camera_x, top - camera_y)

    def get_bb(self):
        # 충돌 박스 반환 (폭탄 크기 기준)
        width, height = 40, 50
        return self.x - width // 2, self.y - height // 2, self.x + width // 2, self.y + height // 2

    def handle_collision(self, group, other):
        if group == "player:bomb":
            print("Bomb collided with Player!")
            game_world.remove_object(self)  # 폭탄 삭제

    def update(self):
        pass
