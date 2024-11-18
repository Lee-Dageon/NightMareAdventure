import math
import random

import pygame

from main import background


class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Monster, self).__init__()
        self.original_image = pygame.image.load('./Art/Enemies/Basic_Enemy.png').convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (40, 40))  # 크기 조정
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = random.uniform(0.5, 0.8)  # 속도 조정

    def update(self, target):
        # 플레이어를 향한 방향 계산
        dx = target.rect.centerx - self.rect.centerx
        dy = target.rect.centery - self.rect.centery
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > 0:
            # 몬스터의 회전
            angle = math.degrees(math.atan2(-dy, dx))  # atan2의 결과를 각도로 변환
            self.image = pygame.transform.rotate(self.original_image, angle)
            self.rect = self.image.get_rect(center=self.rect.center)

            # 몬스터 이동
            self.rect.x += (self.speed * dx / distance)
            self.rect.y += (self.speed * dy / distance)





def spawn_monsters(count):
    map_width, map_height = background.get_width(), background.get_height()  # 전체 맵 크기 가져오기
    for _ in range(count):
        side = random.choice(["left", "right", "top", "bottom"])
        if side == "left":
            x, y = 0, random.randint(0, map_height)
        elif side == "right":
            x, y = map_width, random.randint(0, map_height)
        elif side == "top":
            x, y = random.randint(0, map_width), 0
        else:  # bottom
            x, y = random.randint(0, map_width), map_height
        monster = Monster(x, y)
        monsters.add(monster)
