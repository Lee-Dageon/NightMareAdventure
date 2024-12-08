from pico2d import load_image

import game_framework
import game_world
import stage2_mode
import win_mode


class Key:
    def __init__(self, x, y, camera):
        self.image = load_image('./Art/Items/key.png')  # Key 이미지 로드
        self.x, self.y = x, y
        self.width, self.height = 120, 120  # Key의 크기
        self.tag = "key"  # 충돌 태그

        self.camera = camera  # 카메라 참조
        self.frame = 0  # 현재 프레임
        self.frame_count = 0  # 프레임 전환 타이머

    def update(self):
        """프레임 애니메이션 업데이트"""
        self.frame_count += 1
        if self.frame_count >= 30:  # 약 0.5초마다 전환 (60FPS 기준)
            self.frame_count = 0
            self.frame = (self.frame + 1) % 2  # 2프레임 사이를 전환

    def draw(self):
        """현재 프레임을 기준으로 Key를 그리기 (카메라 보정 포함)"""
        sprite_width = self.image.w // 2  # 스프라이트 폭
        sprite_height = self.image.h     # 스프라이트 높이

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
        """충돌 박스 반환"""
        return self.x - self.width // 2, self.y - self.height // 2, self.x + self.width // 2, self.y + self.height // 2

    def handle_collision(self, group, other):
        """Key와 플레이어의 충돌 처리"""
        if group == "player:key":
            print("Key collected!")
            key_collected = True  # Key가 획득되었음을 표시
            key_spawned = False  # Key가 다시 생성될 수 있도록 초기화
            game_world.remove_object(self)  # Key 제거

            # 현재 게임 모드에 따라 다음 모드로 전환
            if game_framework.stack[-1].__name__ == 'stage1_mode':
                print("Moving to Stage 2")
                import enter_stage2  # Import stage2_mode 모드
                game_framework.change_mode(enter_stage2)
                print(f"Current mode: {game_framework.stack[-1].__name__}")  # 디버깅 메시지

            elif game_framework.stack[-1].__name__ == 'stage2_mode':
                print("Moving to Win Mode")
                import win_mode  # Import win_mode 모드
                game_framework.change_mode(win_mode)

