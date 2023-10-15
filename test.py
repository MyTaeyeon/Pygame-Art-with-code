import pygame

# Khởi tạo Pygame
pygame.init()

# Cài đặt màn hình
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Hình Vuông Nằm Chéo")

# Màu sắc
white = (255, 255, 255)
black = (0, 0, 0)

# Tọa độ các đỉnh của hình vuông
x1, y1 = 300, 300
x2, y2 = 500, 300
x3, y3 = 500, 500
x4, y4 = 300, 500

# Vòng lặp chính
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Xóa màn hình
    screen.fill(white)

    # Vẽ hình vuông nằm chéo
    pygame.draw.line(screen, black, (x1, y1), (x2, y2), 2)
    pygame.draw.line(screen, black, (x2, y2), (x3, y3), 2)
    pygame.draw.line(screen, black, (x3, y3), (x4, y4), 2)
    pygame.draw.line(screen, black, (x4, y4), (x1, y1), 2)

    pygame.display.flip()

# Kết thúc
