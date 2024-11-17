import math
import pygame
import random

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
background = pygame.transform.scale(background, (1600, 1200))

# Mouse 클릭 시 표시할 이미지 로드
mouse_click_image = pygame.image.load("./Art/Mouse/Mouse OutRange.png").convert_alpha()
mouse_click_image = pygame.transform.scale(mouse_click_image, (50, 50))
mouse_click_rect = mouse_click_image.get_rect()
mouse_image_visible = False

# Player 클래스
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Player, self).__init__()
        self.image = pygame.image.load('./Art/Character/Player Secondary Attack frame 1.png').convert_alpha()
        self.attack_image = pygame.image.load("./Art/Character/Player Primary Attack.png").convert_alpha()
        self.original_image = self.image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 8

    def update_direction(self, mouse_pos):
        dx = mouse_pos[0] - WIDTH // 2
        dy = mouse_pos[1] - HEIGHT // 2
        angle = math.atan2(dy, dx)
        self.image = pygame.transform.rotate(self.original_image, -math.degrees(angle) - 90)
        self.rect = self.image.get_rect(center=self.rect.center)

    def move(self, keys):
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed

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


# 카메라 클래스
class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(-self.camera.topleft[0], -self.camera.topleft[1])

    def update(self, target):
        # 주인공을 따라가는 속도를 설정 (중앙에 고정되지 않도록 약간의 오프셋 추가)
        smooth_factor = 0.02  # 카메라 따라가는 부드러움 조정
        target_x = target.rect.centerx - WIDTH // 2
        target_y = target.rect.centery - HEIGHT // 2

        # 카메라가 주인공을 따라갈 때 점진적으로 이동
        x = self.camera.x + smooth_factor * (target_x - self.camera.x)
        y = self.camera.y + smooth_factor * (target_y - self.camera.y)

        # 카메라가 맵 경계를 벗어나지 않도록 제한
        x = max(0, min(x, self.width - WIDTH))
        y = max(0, min(y, self.height - HEIGHT))

        self.camera = pygame.Rect(x, y, WIDTH, HEIGHT)

# 몬스터 그룹 및 스폰 함수
monsters = pygame.sprite.Group()

def spawn_monsters(count):
    for _ in range(count):
        side = random.choice(["left", "right", "top", "bottom"])
        if side == "left":
            x, y = 0, random.randint(0, HEIGHT)
        elif side == "right":
            x, y = WIDTH, random.randint(0, HEIGHT)
        elif side == "top":
            x, y = random.randint(0, WIDTH), 0
        else:  # bottom
            x, y = random.randint(0, WIDTH), HEIGHT
        monster = Monster(x, y)
        monsters.add(monster)

# Player 객체 생성
player = Player(800, 600)
camera = Camera(1600, 1200)

# 초기 몬스터 생성 및 타이머 설정
spawn_monsters(15)  # 시작 시 몬스터 15마리 생성
monster_spawn_timer = pygame.USEREVENT + 1
pygame.time.set_timer(monster_spawn_timer, 1000)  # 1초마다 이벤트 발생

# 몬스터 증가 수 관리 변수
monster_spawn_count = 5  # 1초마다 스폰할 초기 몬스터 수

# 메인 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            mouse_click_rect.center = (mouse_pos[0] + camera.camera.x, mouse_pos[1] + camera.camera.y)
            mouse_image_visible = True
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_image_visible = False
        elif event.type == monster_spawn_timer:
            spawn_monsters(monster_spawn_count)  # 현재 카운트만큼 몬스터 스폰
            monster_spawn_count += 1  # 몬스터 스폰 수 증가

    keys = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()

    player.move(keys)
    player.update_direction(mouse_pos)
    camera.update(player)

    screen.fill(WHITE)
    screen.blit(background, (-camera.camera.x, -camera.camera.y))
    screen.blit(player.image, camera.apply(player))

    # 몬스터 업데이트 및 그리기
    monsters.update(player)
    monsters.draw(screen)

    # 마우스 클릭 이미지 표시
    if mouse_image_visible:
        screen.blit(mouse_click_image, (mouse_click_rect.x - camera.camera.x, mouse_click_rect.y - camera.camera.y))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
