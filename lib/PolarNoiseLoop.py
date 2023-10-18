'''
Polar Perlin Noise Loop - Daniel Shiffman
Based on:
    https://thecodingtrain.com/CodingChallenges/136-polar-perlin-noise-loops.html
    https://youtu.be/ZI1dmHv3MeM
    https://editor.p5js.org/codingtrain/sketches/sy1p1vnQn
Posted to Python by Nguyen Giang (GitHub: MyTaeyeon)
'''

import pygame
import math
from lib.noise import noise

pygame.init()
width, height = 400, 400
screen = pygame.display.set_mode((width, height))

phase = 0
zoff = 0

slider = pygame.Rect(10, height - 30, 200, 20)
slider_value = 5.0

def map_value(value, start1, stop1, start2, stop2):
    return (value - start1) / (stop1 - start1) * (stop2 - start2) + start2

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            if slider.collidepoint(event.pos):
                if pygame.mouse.get_pressed()[0]:
                    slider_value = max(0, min(10, (event.pos[0] - slider.left) / slider.width * 10))

    screen.fill((0, 0, 0))

    pygame.draw.rect(screen, (255, 255, 255), slider, 2)
    pygame.draw.rect(screen, (255, 255, 255), (slider.left + slider.width * slider_value / 10, slider.top, 2, 20))

    translate_x = width / 2
    translate_y = height / 2

    vertices = []

    for a in range(0, int(2 * math.pi / math.radians(5))):
        a = a * math.radians(5)
        xoff = math.cos(a + phase)
        yoff = math.sin(a + phase)
        xoff = map_value(xoff, -1, 1, 0, slider_value)
        yoff = map_value(yoff, -1, 1, 0, slider_value)
        r = map_value(noise(xoff, yoff,zoff), 0, 1, 100, 30)
        x = r * math.cos(a) + translate_x
        y = r * math.sin(a) + translate_y
        vertices.append((x, y))

    pygame.draw.polygon(screen, (255, 255, 255), vertices, 1)

    phase += 0.003
    zoff += 0.01

    pygame.display.flip()

pygame.quit()
