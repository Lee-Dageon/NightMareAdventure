import game_world
from pico2d import *

# 포션 사운드 전역 변수
potion_sound = None


class Potion:
    def __init__(self, x, y, camera):
        global potion_sound
        self.image = load_image('./Art/Items/Health Potion.png')  # 1행 2열 스프라이트 이미지 경로
        self.x, self.y = x, y
        self.frame = 0  # 현재 프레임 (0 또는 1)
        self.frame_time = 0  # 프레임 갱신 시간 계산
        self.frame_interval = 0.5  # 프레임 전환 간격 (초)
        self.tag = "potion"  # 충돌 태그
        self.camera = camera  # 카메라 참조 추가

        # 크기 조정
        self.width = 120  # 출력할 폭
        self.height = 120  # 출력할 높이

        # 포션 사운드 로드 (처음 초기화 시)
        if potion_sound is None:
            potion_sound = load_wav('./assets/sound/potion.wav')
            potion_sound.set_volume(64)  # 볼륨 설정

    def update(self):
        """프레임 애니메이션 업데이트"""
        self.frame_time += 0.016  # 60 FPS 기준
        if self.frame_time >= self.frame_interval:
            self.frame_time = 0
            self.frame = (self.frame + 1) % 2  # 0과 1 사이에서 반복

    def draw(self):
        """현재 프레임을 기준으로 포션 그리기 (카메라 보정 포함)"""
        sprite_width = self.image.w // 2  # 스프라이트 폭
        sprite_height = self.image.h  # 스프라이트 높이

        # 카메라 보정 좌표
        screen_x = self.x - self.camera.x
        screen_y = self.y - self.camera.y

        self.image.clip_draw(
            self.frame * sprite_width, 0,  # 현재 프레임에 따른 위치
            sprite_width, sprite_height,
            screen_x, screen_y,  # 카메라 보정된 위치
            self.width, self.height  # 크기 조정
        )

    def get_bb(self):
        """충돌 박스 반환 (카메라 보정 포함)"""
        size = self.width // 2
        return self.x - size, self.y - size, self.x + size, self.y + size

    def handle_collision(self, group, other):
        """충돌 처리"""
        if group == "player:potion":
            other.heal(5)  # 플레이어 체력을 5 회복
            print("[DEBUG] Potion consumed! Player HP increased.")
            game_world.remove_object(self)  # 포션 제거

            # 포션 획득 사운드 재생
            if potion_sound:
                potion_sound.play()
