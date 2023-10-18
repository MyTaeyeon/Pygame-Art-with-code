import pygame
import math
import random

# Pygame initialization
pygame.init()
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Chuyển đổi từ p5.js sang Pygame')

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

# Create a clock for controlling frame rate
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(black)
    center_x, center_y = width // 2, height // 2

    points = []

    for a in range(0, int(2 * math.pi / 0.01)):
        a = a * 0.01
        r = random.randint(8, 20)
        x = r * math.cos(a) + center_x
        y = r * math.sin(a) + center_y
        points.append((x, y))

    pygame.draw.lines(screen, white, False, points, 1)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
