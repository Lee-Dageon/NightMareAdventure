import math
import pygame

# 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zoom and Camera Follow")

# 색상 정의
WHITE = (255, 255, 255)

# FPS 설정
clock = pygame.time.Clock()
FPS = 60

# 배경 이미지 로드
background = pygame.image.load("./assets/gamebackground.png").convert()
background = pygame.transform.scale(background, (1600, 1200))  # 배경은 플레이어 이동에 맞게 더 크게 설정

# Player 클래스
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Player, self).__init__()
        # 플레이어 이미지 불러오기
        self.image = pygame.image.load('./Art/Character/Player Secondary Attack frame 1.png').convert_alpha()
        self.original_image = self.image  # 회전 시 원본 보존
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5  # 플레이어 이동 속도

    def update_direction(self, mouse_pos):
        # 마우스와의 각도 계산 및 이미지 회전
        dx = mouse_pos[0] - WIDTH // 2  # 화면 중앙 기준
        dy = mouse_pos[1] - HEIGHT // 2
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

# 카메라 클래스
class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        # 카메라 위치를 적용하여 객체의 렌더링 위치 조정
        return entity.rect.move(-self.camera.topleft[0], -self.camera.topleft[1])

    def update(self, target):
        # 플레이어를 중심으로 카메라 위치 업데이트
        x = target.rect.centerx - WIDTH // 2
        y = target.rect.centery - HEIGHT // 2

        # 카메라가 맵 경계를 벗어나지 않도록 제한
        x = max(0, min(x, self.width - WIDTH))
        y = max(0, min(y, self.height - HEIGHT))

        self.camera = pygame.Rect(x, y, WIDTH, HEIGHT)

# Player 객체 생성
player = Player(800, 600)  # 맵 중앙에서 시작
camera = Camera(1600, 1200)  # 배경 크기에 맞춰 설정

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

    # 플레이어 이동 및 방향 업데이트
    player.move(keys)
    player.update_direction(mouse_pos)

    # 카메라 업데이트
    camera.update(player)

    # 배경 및 플레이어 그리기
    screen.fill(WHITE)
    screen.blit(background, (-camera.camera.x, -camera.camera.y))  # 카메라 위치에 맞춰 배경 이동
    screen.blit(player.image, camera.apply(player))  # 카메라 적용된 플레이어 위치

    # 화면 업데이트
    pygame.display.flip()

    # FPS 유지
    clock.tick(FPS)

pygame.quit()
