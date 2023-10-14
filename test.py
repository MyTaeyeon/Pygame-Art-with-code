import pygame
import sys
import math

# Khởi tạo Pygame
pygame.init()

# Kích thước màn hình
screen = pygame.display.set_mode((400, 400))

# Tạo một Surface
image = pygame.Surface((100, 100))
pygame.draw.rect(image, (255, 0, 0), (0, 0, 90, 100))  # Vẽ hình vuông đỏ

# Xoay Surface với một góc (độ)
angle = 30
rotated_image = pygame.transform.rotate(image, angle)
print(rotated_image.get_height(), rotated_image.get_width())
# Vị trí để vẽ
x, y = 150, 150

# Hiển thị hình ảnh đã xoay lên màn hình
screen.blit(rotated_image, (x, y))
# screen.blit(image, (150, 150))

# Vòng lặp chính
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()

# Đóng cửa sổ Pygame
pygame.quit()
sys.exit()
