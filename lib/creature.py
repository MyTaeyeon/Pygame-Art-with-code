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

class Bird:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.yo = 0
        self.s = 2
        self.t = 0
        self.aspd = 0.05
        self.color = (150,150,150)
        self.animations = [[]]
        self.dir = 1
        self.spd = 0.5
        self.timers = []
        self.health = 100
        self.skel=[ [ -60, 5, 1],
                    [  30, 5, 2],#1
                    [   0, 0, 2],
                    [ 190,10, 2],
                    [ -10, 8, 3],
                    [ 150, 8, 2],#5
                    [ -60,10, 5],
                    [  50,10, 6],
                    [ 150, 8, 2],
                    [ -60,10, 8],
                    [  50,10, 9],#10
                    [-140, 8, 2],
                    [ -30, 3,11],
                    [  50, 5,12],
                    [ -30, 3,11],
                    [  50, 5,14] #15
                    ]
        self.ssk = copy.deepcopy(self.skel)
        self.aspd = 0.1

        self.t = random.random()*math.pi*2

        self.w1 = [-5,-5]
        self.w2 = [-3,-20]
        self.w3 = [-8,-30]
        self.t2 = 0
        self.v = [0,0]
        self.on = 0

    def __str__(self):
        return self.skel

    def super(self):
        return super(type(self),self)

    def calcCoord(self,n):
        if n == self.skel[n][2]:
            return [0,0,0]
        else:
            trl = self.skel[n]
            pc = self.calcCoord(trl[2])
            tc = [0,0,0]

            tc[0] = pc[0] + trl[1]*math.cos(math.radians(trl[0]+pc[2]))
            tc[1] = pc[1] - trl[1]*math.sin(math.radians(trl[0]+pc[2]))
            tc[2] = pc[2] + trl[0]
            return tc
    def to(self,r,l,n,spd=3):
        self.skel[r][l] += (n-self.skel[r][l])/float(spd)

    def animate(self):
        for a in self.animations[0]:
            if a[0][0] == "trans":
                if a[0][1] == "x":
                    self.x+=(a[1][0]-self.x)/float(a[1][1])
                    #self.dir = (a[1][0]-self.x>0)*2-1
                    self.walk()
                if a[0][1] == "xt":
                    self.x+=(a[1][0]-self.x)/float(a[1][1])

                elif a[0][1] == "y":
                    self.y+=(a[1][0]-self.y)/float(a[1][1])
            else:
                self.skel[a[0][0]][a[0][1]]+=(a[1][0]-self.skel[a[0][0]][a[0][1]])/float(a[1][1])
            a[1][1]-=1
            if a[1][1]<=0:
                a.remove(a[1])
            if len(a) <= 1:
                self.animations[0].remove(a)
            if len(self.animations[0]) == 0:
                self.animations.pop(0)
            if len(self.animations)==0:
                self.animations.append([])

        for ti in self.timers:
            ti[0] -= 1
            if ti[0] == 0:
                ti[1](*ti[2])
                self.timers.remove(ti)



    def addanim(self,skn,rol,dest,t):
        na = [[skn,rol],[dest,t]]
        for a in self.animations[-1]:
            if a[0][0]==na[0][0] and a[0][1]==na[0][1]:
                a.append(na[1])
                return
        self.animations[-1].append(na)

    def animback(self,t,exceptions=[]):
        for i in range(0,len(self.skel)):
            if i not in exceptions:
                self.addanim(i,0,self.ssk[i][0],t)
                self.addanim(i,1,self.ssk[i][1],t)

    def poly(self,surf,*args):
        u.polygon(surf,self.color,list(map(lambda l: [self.x+l[0]*self.s*self.dir,self.y+self.yo+l[1]*self.s], args)))
    def circle(self,surf,pos,radius):
        u.circle(surf,self.color,[self.x+pos[0]*self.s*self.dir,self.y+self.yo+pos[1]*self.s],radius*self.s)
    def line(self,surf,start_pos,end_pos,width=1):
        u.line(surf,self.color,[self.x+start_pos[0]*self.s*self.dir,self.y+self.yo+start_pos[1]*self.s],
                                [self.x+  end_pos[0]*self.s*self.dir,self.y+self.yo+  end_pos[1]*self.s],width*self.s)
    
    def wingCoordToRL(self,n,w,lw=[0,0],lr=0,slr=0):
        self.skel[n][0] = -(180-(-math.degrees(math.atan2(w[1]-lw[1],w[0]-lw[0]))-slr+180-lr))
        self.skel[n][1] = math.sqrt((w[0]-lw[0])**2+(w[1]-lw[1])**2)

    def fly(self):
        s = self
        s.t += 1

        s.w1[1] = -1+u.trapwave(s.t*s.aspd)*3
        s.w2[1] = -2+u.trapwave(s.t*s.aspd)*8
        s.w3[1] = -1+u.trapwave(s.t*s.aspd+math.pi*0.2)*12

        s.w2[0] = -3+math.sin(s.t*s.aspd-math.pi*0.5)*2
        s.w3[0] = -12+math.sin(s.t*s.aspd-math.pi*0.5)*3


        s.wingCoordToRL(5,s.w1)
        s.wingCoordToRL(6,s.w2,s.w1,s.skel[5][0])
        s.wingCoordToRL(7,s.w3,s.w2,s.skel[6][0],s.skel[5][0])

        s.wingCoordToRL(8,s.w1)
        s.wingCoordToRL(9,s.w2,s.w1,s.skel[5][0])
        s.wingCoordToRL(10,s.w3,s.w2,s.skel[6][0],s.skel[5][0])


        s.to(4,0,-0+math.sin(s.t*s.aspd+math.pi)*10)
        s.to(1,0,10+math.sin(s.t*s.aspd)*10)

        s.to(12,0,-30)
        s.to(14,0,-30)
        s.to(1,1,3)


        s.to(13,0,50+math.sin(s.t*s.aspd)*10 + 10*noise.noise(s.t*s.aspd*0.01,1)-5)
        s.to(15,0,50+math.sin(s.t*s.aspd)*10 + 10*noise.noise(s.t*s.aspd*0.01,2)-5)

        s.x += s.v[0]*s.dir
        s.y += 0.5*s.v[1]+0.5*s.v[1]*(0.5*(math.sin(s.t*s.aspd)+1))
    
    def simpFly(self):
        s = self
        s.t += 1

        s.w1[1] = -1+u.trapwave(s.t*s.aspd)*3
        s.w2[1] = -2+u.trapwave(s.t*s.aspd)*8
        s.w3[1] = -1+u.trapwave(s.t*s.aspd+math.pi*0.2)*12

        s.w2[0] = -3+math.sin(s.t*s.aspd-math.pi*0.5)*2
        s.w3[0] = -12+math.sin(s.t*s.aspd-math.pi*0.5)*3

        s.wingCoordToRL(5,s.w1)
        s.wingCoordToRL(6,s.w2,s.w1,s.skel[5][0])
        s.wingCoordToRL(7,s.w3,s.w2,s.skel[6][0],s.skel[5][0])

        s.to(4,0,-0+math.sin(s.t*s.aspd+math.pi)*10)
        s.to(1,0,10+math.sin(s.t*s.aspd)*10)

        s.to(1,1,3)

        s.x += s.v[0]*s.dir
        s.y += 0.5*s.v[1]+0.5*s.v[1]*(0.5*(math.sin(s.t*s.aspd)+1))

    def fall(self):
        s = self
        s.v[0] = s.arrow.v[0]
        s.v[1] = s.arrow.v[1]
        s.x += s.v[0]
        s.y += s.v[1]

    def rest(self):

        s = self
        #s.t = -1 #math.pi
        s.t2 += 1
        s.to(5,0,20+180*2*((s.skel[5][0]>0)-0.5),10)
        s.to(6,0,-20+180*2*((s.skel[6][0]>0)-0.5),10)
        s.to(7,0,20-180*2*((s.skel[10][0]<0)-0.5),10)

        s.to(8,0,20+180*2*((s.skel[8][0]>0)-0.5),10)
        s.to(9,0,-20+180*2*((s.skel[9][0]>0)-0.5),10)
        s.to(10,0,20-180*2*((s.skel[10][0]<0)-0.5),10)

        s.to(12,0,30,10)
        s.to(14,0,30,10)
        s.to(13,0,100,10)
        s.to(15,0,100,10)

        noi = max(min((noise.noise(s.t2*s.aspd*0.5)-0.3)*50,1),-1)
        s.to(1,0,-10+noi*20,5)
        s.to(1,1,5-noi*2,5)
        s.to(4,0,-10+noi*10,5)

        s.x += s.v[0]*s.dir
        s.y += s.v[1]
        if s.y>=0:
            s.v[1] = 0
            s.v[0] = 0
            s.y = 0
        else:
            s.v[1] += 0.2*s.s
        if random.random() < 0.02 and s.v[1] == 0:
            s.v[1]=-1*s.s
            r = random.choice([1,1])
            s.v[0]+=0.5*r*s.s
            #s.dir = r

    def draw(self,surf):
        cd = []
        for i in range(len(self.skel)):
            cd.append(self.calcCoord(i)[:2])
        s = self
        s.poly(surf,cd[3],cd[2],cd[5],
                    [cd[5][0]-5,cd[5][1]])
        s.poly(surf,cd[5],cd[6],
                    [cd[6][0]-8,cd[6][1]],
                    [cd[5][0]-5,cd[5][1]])
        s.poly(surf,cd[6],[cd[6][0]-8,cd[6][1]],cd[7])
        s.poly(surf,cd[2],cd[5],cd[6])


        s.poly(surf,cd[3],cd[2],cd[8],
                    [cd[8][0]-5,cd[8][1]])
        s.poly(surf,cd[8],cd[9],
                    [cd[9][0]-8,cd[9][1]],
                    [cd[8][0]-5,cd[8][1]])
        s.poly(surf,cd[9],[cd[9][0]-8,cd[9][1]],cd[10])
        s.poly(surf,cd[2],cd[8],cd[9])

        s.poly(surf,cd[2],[(cd[2][0]+cd[3][0])/2,(cd[2][1]+cd[3][1])/2-2],cd[3],cd[11],[cd[11][0]+5,cd[11][1]])
        s.poly(surf,[(cd[3][0]+cd[4][0])/2,(cd[3][1]+cd[4][1])/2],cd[3],cd[11])
        s.poly(surf,cd[0],cd[1],cd[2])
        s.poly(surf,cd[11],[(cd[0][0]+cd[1][0])/2,(cd[0][1]+cd[1][1])/2],cd[1],cd[2])

        s.line(surf,cd[11],cd[12],3)
        s.line(surf,cd[11],cd[14],3)

        s.line(surf,cd[3],cd[4],2)

        s.line(surf,cd[12],cd[13])
        s.line(surf,cd[14],cd[15])
        
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