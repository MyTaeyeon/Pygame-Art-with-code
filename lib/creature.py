import pygame
import sys
import math
import copy
import random
import noise
import tree
import utilities as u
# import lib.utilities as u
# import lib.noise as noise
# import lib.tree as tree

pygame.init()

# class simplePlayer:
#     def __init__(self, screen, x, y):
#         self.screen = screen
#         self.character_color = (255, 0, 0)  # Đỏ
#         self.character_radius = 10
#         self.character_x = x
#         self.character_y = y
#         self.move_speed = 5
#         self.jump_height = -10
#         self.jump_count = 2  # Số lần nhảy tối đa
#         self.gravity = 1

#     def draw(self):
#         pygame.draw.circle(self.screen, self.character_color, (self.character_x, self.character_y), self.character_radius)

#     def move_left(self):
#         self.character_x -= self.move_speed

#     def move_right(self):
#         self.character_x += self.move_speed

#     def jump(self):
#         if self.jump_count > 0:
#             self.character_y += self.jump_height
#             self.jump_count -= 1

#     def fall(self):
#         if self.character_y + self.character_radius * 2 < self.screen.get_height():
#             self.character_y += self.gravity
#         else:
#             self.jump_count = 2  # Reset số lần nhảy khi đạt mặt đất

class simplePlayer:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.color = (255, 0, 0)
        self.jumping = False
        self.falling = False
        self.jumpy = 0
    
    def draw(self, surface):
        u.circle(surface, self.color, [self.x, self.y], 10)
    
    def update(self, onland):
        if self.falling == True:
            if self.y < onland:
                self.y += 3
            else:
                self.y = onland
                self.falling = False
            return
        if self.jumping == True:
            if self.y > self.jumpy:
                self.y -= 5
            else:
                self.y = self.jumpy
                self.jumping = False
                self.falling = True
            return
        self.y = onland
        return
        

class animal():
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        pass

if __name__ == "__main__":
    pass
