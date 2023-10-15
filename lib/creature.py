from typing import Any
import pygame
import sys
import math
import copy
import random
import noise
import tree
import utilities as u 

pygame.init()
screen = pygame.display.set_mode([640, 320])
screen.fill((255, 255, 255))
class Arrow:
	def __init__(self,x,y, spd):
		self.color = (150,150,150)
		self.x = x
		self.y = y
		self.l = 40
		self.a = 0
		self.spd = spd
		self.v = [-self.spd,0]
		self.g = 0.04
		self.flicker  =  1
            
	def calcA(self):
		return math.degrees(math.atan2(self.v[1],self.v[0]))
		
	def calcV(self):
		return [self.spd*math.cos(math.radians(self.a)), -self.spd*math.sin(math.radians(self.a))]
		
		
	def calcHead(self):
		return self.x+self.l*math.cos(math.radians(self.a)), self.y+self.l*math.sin(math.radians(self.a))

	def calcFeather(self):
		return self.x+self.l*0.3*math.cos(math.radians(self.a)), self.y+self.l*0.3*math.sin(math.radians(self.a))
		
	def draw(self,surf):
		u.line(surf,[245,245,245],[self.x,self.y],self.calcFeather(), 4)
		u.line(surf,self.color,[self.x,self.y],self.calcHead(),random.randrange(0,2)*self.flicker+2)
		
	def fly(self):
		self.a = self.calcA()
		self.x += self.v[0]
		self.y += self.v[1]
		self.v[1] += self.g
            
class Player:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.ay = 0
        self.vx = 0
        self.vy = 0
        self.color = (140, 140, 140)
        self.background = (245, 245, 245)
        self.time = 0
        self.stuckinSky = False
    
    def draw(self, surface):
        u.polygon(surface, self.color, [[self.x, self.y], [self.x + 20, self.y], [self.x + 20, self.y - 20], [self.x, self.y - 20]])
        u.polygon(surface, self.background, [[self.x + 6, self.y - 14], [self.x + 7, self.y - 14], [self.x + 6, self.y - 13], [self.x +7, self.y - 13]])
        u.polygon(surface, self.background, [[self.x + 13, self.y - 14], [self.x + 14, self.y - 14], [self.x + 13, self.y - 13], [self.x + 14, self.y - 13]])
        u.polygon(surface, self.background, [[self.x + 6, self.y - 7], [self.x + 6, self.y - 6], [self.x + 14, self.y - 6], [self.x + 14, self.y - 7]])
    
    def update(self, onland):
        self.x += self.vx
        if self.ay == 0:
            self.y = onland
        else:
            self.stuckinSky = True
            self.time += 1
            self.y -= self.vy - int(self.ay * (2*self.time - 1) / 2)
            if self.y > onland:
                self.y = onland
                self.ay = 0
                self.stuckinSky = False

class simplePlayer:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.ay = 0
        self.vx = 0
        self.vy = 0
        self.color = (140, 140, 140)
        self.time = 0
        self.stuckinSky = False
    
    def draw(self, surface):
        u.circle(surface, self.color, [self.x, self.y], 10)
    
    def update(self, onland):
        self.x += self.vx
        if self.ay == 0:
            self.y = onland
        else:
            self.stuckinSky = True
            self.time += 1
            self.y -= self.vy - int(self.ay * (2*self.time - 1) / 2)
            if self.y > onland:
                self.y = onland
                self.ay = 0
                self.stuckinSky = False
        
if __name__ == "__main__":
    arrows = [Arrow(100, 100), Arrow(100, 150), Arrow(100, 200)]
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill((255, 255, 255))
        
        for x in arrows:
            x.draw(screen)
            x.fly()
        pygame.display.update()