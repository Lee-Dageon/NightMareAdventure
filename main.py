import math
import pygame

# 초기화
pygame.init()

# 화면 설정
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Player Movement with WASD and Mouse Direction")

# 색상 정의
WHITE = (255, 255, 255)

# FPS 설정
clock = pygame.time.Clock()
FPS = 60

# Player 클래스
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Player, self).__init__()
        # 이미지 불러오기 (PNG 파일)
        self.image = pygame.image.load('./Art/Character/Player Idle.png').convert_alpha()
        self.original_image = self.image  # 회전 시 원본 보존
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 3  # 플레이어 이동 속도

    def update_direction(self, mouse_pos):
        # 마우스와의 각도 계산 및 이미지 회전
        dx = mouse_pos[0] - self.rect.centerx
        dy = mouse_pos[1] - self.rect.centery
        angle = math.atan2(dy, dx)
        self.image = pygame.transform.rotate(self.original_image, -math.degrees(angle) - 90)
        self.rect = self.image.get_rect(center=self.rect.center)

    def move(self, keys):
        # WASD 키에 따라 이동
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed

# Player 객체 생성
player = Player(400, 300)

# 메인 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 키 입력 상태 가져오기
    keys = pygame.key.get_pressed()

    # 마우스 위치 가져오기
    mouse_pos = pygame.mouse.get_pos()

    # 배경 화면 채우기
    screen.fill(WHITE)

    # Player 이동 및 방향 업데이트
    player.move(keys)
    player.update_direction(mouse_pos)
    screen.blit(player.image, player.rect)

    # 화면 업데이트
    pygame.display.flip()

    # FPS 유지
    clock.tick(FPS)

pygame.quit()
