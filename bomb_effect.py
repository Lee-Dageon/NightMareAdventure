from pico2d import load_image

class BombEffect:
    def __init__(self, x, y, camera, effect_type="red", delay=0):
        # 폭발 효과 이미지 로드
        effect_images = {
            "green": './Art/Items/bomb_effect_green.png',
            "red": './Art/Items/bomb_effect.png',
            "gray": './Art/Items/bomb_effect_gray.png'
        }
        self.image = load_image(effect_images.get(effect_type, './Art/Items/bomb_effect.png'))

        self.x, self.y = x, y
        self.camera = camera
        self.frame = 0
        self.finished = False
        self.delay = delay  # 폭발 시작 딜레이
        self.frame_time = 0.0  # 현재 프레임 시간
        self.time_since_spawn = 0.0  # 생성 이후 경과 시간
        self.effect_type = effect_type  # 효과 타입 저장

    def update(self, elapsed_time):
        self.time_since_spawn += elapsed_time

        if self.time_since_spawn >= self.delay:  # 딜레이를 초과한 경우에만 애니메이션 실행
            self.frame_time += elapsed_time
            if self.frame_time >= 0.08:  # 0.08초마다 다음 프레임으로 변경
                self.frame += 1
                self.frame_time = 0.0

                if self.frame >= 7:  # 7프레임까지 출력되면 완료
                    self.finished = True

    def draw(self):
        if not self.finished and self.time_since_spawn >= self.delay:
            sprite_width = self.image.w // 7  # 7열이므로 너비를 7로 나눔
            sprite_height = self.image.h  # 1행이므로 전체 높이 사용

            # 크기 조정
            scale = 4.0 if self.effect_type == "gray" else 1.8
            draw_width = sprite_width * scale
            draw_height = sprite_height * scale

            # 카메라 보정을 적용하여 스프라이트 출력
            self.image.clip_draw(
                self.frame * sprite_width -25, 0, sprite_width, sprite_height,
                int(self.x - self.camera.x), int(self.y - self.camera.y),
                int(draw_width), int(draw_height)
            )
