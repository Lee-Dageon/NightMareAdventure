from pico2d import *
import game_world
import random
import math

class PowerMonster:
    def __init__(self, x, y, player, camera):
        self.image = load_image('./Art/Enemies/power_monster.png')  # 강력한 몬스터 이미지 경로
        self.x, self.y = x, y
        self.width, self.height = 80, 80  # 몬스터 크기
        self.hp = 10  # 강력한 몬스터는 일반 몬스터보다 높은 체력을 가짐
        self.speed = 100  # 초당 이동 속도
        self.player = player  # 플레이어 객체 참조
        self.camera = camera  # 카메라 참조
        self.angle = 0  # 플레이어를 추적하는 각도
        self.frame = 0  # 애니메이션 프레임
        self.frame_timer = 0  # 프레임 전환 타이머
        self.tag = "M"  # 태그 추가
        self.type = "gray"

        # 사운드 로드
        self.bomb_sound = load_wav('./assets/sound/bomb.wav')  # 폭탄 사운드 파일 경로
        self.bomb_sound.set_volume(64)  # 볼륨 설정 (0 ~ 128)

    def update(self):
        """플레이어를 추적하는 로직"""
        dx, dy = self.player.x - self.x, self.player.y - self.y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance > 0:
            self.x += (dx / distance) * self.speed * 0.016  # 60FPS 기준 약 0.016초 타임스텝
            self.y += (dy / distance) * self.speed * 0.016
            self.angle = math.atan2(dy, dx)  # 플레이어를 향한 각도 계산

        # 애니메이션 프레임 업데이트
        self.frame_timer += 0.016
        if self.frame_timer >= 0.2:  # 0.2초마다 프레임 전환
            self.frame_timer = 0
            self.frame = (self.frame + 1) % 3  # 0, 1, 2 사이를 반복

        # 디버깅 메시지: 현재 위치와 HP 출력
      #  print(f"[DEBUG] PowerMonster Position: ({self.x:.2f}, {self.y:.2f}), HP: {self.hp}")

    def draw(self):
        """강력한 몬스터를 카메라 보정 후 화면에 그리기"""
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
        scale = 4  # 크기를 1.5배로 확대

        # 확대된 크기 계산
        scaled_width = int(sprite_width * scale)
        scaled_height = int(sprite_height * scale)

        # 스프라이트 그리기
        self.image.clip_draw(
            self.frame * sprite_width, (3 - row) * sprite_height,
            sprite_width, sprite_height,
            int(self.x - camera_x),  # 중심 좌표 맞춤
            int(self.y - camera_y),
            scaled_width, scaled_height
        )

    def get_bb(self):
        """충돌 박스 반환"""
        return self.x - self.width // 2, self.y - self.height // 1.7, self.x + self.width // 2, self.y + self.height // 1.7

    def handle_collision(self, group, other):
        """충돌 처리"""
        if group == "player:power_monster":
            self.player.hp -= 0.08  # 강력한 몬스터와 충돌 시 플레이어 HP 감소량 증가
          #  print("[DEBUG] Player hit by PowerMonster! HP reduced.")

