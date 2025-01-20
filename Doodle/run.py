import pygame
import random
import sys

# 初始化 Pygame
pygame.init()

# 視窗設置
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Doodle Jump")

# 顏色定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# 時間設置
clock = pygame.time.Clock()
FPS = 60

# 角色設置
player = pygame.Rect(WIDTH // 2, HEIGHT - 50, 30, 30)
player_velocity = 0
gravity = 0.5
jump_strength = -10  # 最大跳躍距離約為 50 像素
max_jump_distance = 50

# 平台設置
# 第一個平台固定在較低位置
platforms = [pygame.Rect(WIDTH // 2 - 30, HEIGHT - 50, 60, 10)]  # 第一個平台位置

# 隨機生成其他平台，控制每個平台的垂直間距不超過跳躍範圍
y_position = HEIGHT - 100
while len(platforms) < 15:  # 初始化 15 個平台
    x_position = random.randint(0, WIDTH - 60)
    y_position -= random.randint(20, max_jump_distance)
    platforms.append(pygame.Rect(x_position, y_position, 60, 10))

# 分數
score = 0

# 遊戲主循環
running = True
while running:
    screen.fill(WHITE)
    
    # 事件處理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # 玩家移動
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= 5
    if keys[pygame.K_RIGHT]:
        player.x += 5

    # 左右穿越螢幕邏輯
    if player.x > WIDTH:  # 如果角色超出右邊界
        player.x = 0
    elif player.x < 0:  # 如果角色超出左邊界
        player.x = WIDTH
    
    # 重力與跳躍
    player_velocity += gravity
    player.y += player_velocity
    
    # 平台碰撞檢測
    for platform in platforms:
        if player.colliderect(platform) and player_velocity > 0:
            player_velocity = jump_strength
    
    # 平台與玩家移動
    if player.y < HEIGHT // 2:  # 當角色達到螢幕中間，平台向下移動
        player.y = HEIGHT // 2
        for platform in platforms:
            platform.y += abs(player_velocity)
    
    # 移除超出螢幕的舊平台
    platforms = [platform for platform in platforms if platform.y <= HEIGHT]
    
    # 確保平台數量至少為 15
    while len(platforms) < 15:
        x_position = random.randint(0, WIDTH - 60)
        y_position = platforms[-1].y - random.randint(20, max_jump_distance)
        platforms.append(pygame.Rect(x_position, y_position, 60, 10))
        score += 1  # 每生成一個新平台增加分數
    
    # 繪製玩家與平台
    pygame.draw.rect(screen, GREEN, player)
    for platform in platforms:
        pygame.draw.rect(screen, BLACK, platform)
    
    # 遊戲結束邏輯
    if player.y > HEIGHT:
        print(f"Game Over! Final Score: {score}")
        running = False
    
    # 更新畫面
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
