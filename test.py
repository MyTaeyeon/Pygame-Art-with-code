import pygame

# Khởi tạo Pygame
pygame.init()

# Cài đặt màn hình
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

# Màu sắc
black = (0, 0, 0)

# Vòng lặp chính
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Xóa màn hình
    screen.fill(black)

    # Vẽ hình vuông nằm chéo

    pygame.display.flip()

# Kết thúc
