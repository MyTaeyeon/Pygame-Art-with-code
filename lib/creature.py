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

class simplePlayer:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
    
    def draw(self, surface):
        u.circle(surface, (255, 0, 0), [self.x, self.y], 10)
 

class animal():
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        pass

if __name__ == "__main__":
    pass
