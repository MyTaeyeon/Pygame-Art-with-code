import pygame
import math
from pygame.locals import *

# Pygame initialization
pygame.init()
width, height = 400, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Vẽ hình vuông nghiêng trong Pygame')

# Create a clock for controlling frame rate
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    screen.fill((0, 0, 0))

    # Điểm trung tâm của hình vuông
    center_x, center_y = width // 2, height // 2

    # Độ dài cạnh hình vuông
    side_length = 100

    # Góc quay (pi/3 radians tương ứng với 60 độ)
    angle = math.pi / 9

    # Tính toán các đỉnh của hình vuông
    vertices = []
    for i in range(4):
        x = center_x + side_length * math.cos(angle + i * math.pi / 2)
        y = center_y + side_length * math.sin(angle + i * math.pi / 2)
        vertices.append((x, y))

    # Vẽ hình vuông
    pygame.draw.polygon(screen, (255, 255, 255), vertices, 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
