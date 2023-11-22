import pygame
import math
import copy
import random
import lib.noise as noise
import lib.utilities as u
import lib.tree as tree

class Animal(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.yo = 0
        self.s = 2
        self.t = 0
        self.aspd = 0.05
        self.skel = []
        self.color = (150, 150, 150)
        self.animations = [[]]
        self.dir = 1
        self.spd = 0.5
        self.timers = []
        self.health = 100
        
    def __str__(self):
        return self.skel
        
    def super(self):
        return super(type(self), self)
        
    def calcCoord(self,n):
        if n == self.skel[n][2]:
            return [0, 0, 0]
        else:
            trl = self.skel[n]
            pc = self.calcCoord(trl[2])
            tc = [0, 0, 0]
            
            tc[0] = pc[0] + trl[1] * math.cos(math.radians(trl[0] + pc[2]))
            tc[1] = pc[1] - trl[1]* math.sin(math.radians(trl[0] + pc[2]))
            tc[2] = pc[2] + trl[0]
            return tc
    def to(self,r,l,n,spd=3):
        self.skel[r][l] += (n-self.skel[r][l]) / float(spd)
        
    def animate(self):
        for a in self.animations[0]:
            if a[0][0] == "trans":
                if a[0][1] == "x":
                    self.x += (a[1][0] - self.x) / float(a[1][1])
                    self.walk()
			
                if a[0][1] == "xt":
                    self.x += (a[1][0] - self.x) / float(a[1][1])
                elif a[0][1] == "y":
                    self.y += (a[1][0] - self.y) / float(a[1][1])
            else:
                self.skel[a[0][0]][a[0][1]] += (a[1][0] - self.skel[a[0][0]][a[0][1]]) / float(a[1][1])
            a[1][1] -= 1
            if a[1][1] <= 0:
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
            if a[0][0] == na[0][0] and a[0][1] == na[0][1]:
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

    def drawSkel(self,surf):
        for i in range(0,len(self.skel)):
            c = self.calcCoord(i)
            pc = self.calcCoord(self.skel[i][2])
            self.line(surf, [c[0], c[1]], [pc[0], pc[1]], 1)
				
class Horse(Animal):
	def __init__(self,x,y):
		
		super(Horse,self).__init__(x,y)
		self.phase = "playing"
		self.skel=[ [-90,10, 1],		
					[ 30,20, 2],#1
					[  0, 0, 2],
					[190,10, 2],
					[-20,10, 3],
					[ 50,10, 4],#5
					[ 30,15, 5],
					[-70,10, 2],
					[-10,12, 7],
					[  0,12, 8],
					[-30,12, 7],#10
					[ 20,12,10],
					[ 70,10, 4],
					[ 70,10,12],
					[-90,10,13],
					[ 45,12,14],#15
					[ 85,10,12],
					[-90,10,16],
					[ 45,12,17],#18
				]
		self.ssk = copy.deepcopy(self.skel)

	def draw(self,surf):
		cd = []
		for i in range(len(self.skel)):
			cd.append(self.calcCoord(i)[:2])
			
		self.poly(surf, cd[2],
						[cd[7][0]+2,cd[7][1]+2],  [cd[3][0]+5,cd[3][1]+13],
						cd[12],   cd[4],   [cd[4][0]+4,cd[4][1]],   cd[3]
						)
		self.poly(surf, cd[2],   [cd[1][0]-3,cd[1][1]],
						[cd[1][0]+1,cd[1][1]-1],   [cd[1][0]+3,cd[1][1]],
						[cd[1][0]+2,cd[1][1]+1],   [cd[0][0]+1,cd[0][1]-1],
						[cd[0][0]-1,cd[0][1]+1],   [cd[1][0]-1,cd[1][1]+5],
						[(cd[2][0]+cd[1][0])/2,(cd[2][1]+cd[1][1])/2+8],
						[cd[7][0]+2,cd[7][1]+2],
						)			
		self.poly(surf, cd[2],  [cd[7][0]+2,cd[7][1]],  [cd[8][0]+2,cd[8][1]],
						[cd[9][0]+2,cd[9][1]],   [cd[9][0],cd[9][1]],
						cd[8],   [cd[7][0]-6,cd[7][1]]
						)		
		self.poly(surf, cd[2],  [cd[7][0]+2,cd[7][1]],  [cd[10][0]+2,cd[10][1]],
						[cd[11][0]+2,cd[11][1]],   [cd[11][0],cd[11][1]],
						cd[10],   [cd[7][0]-6,cd[7][1]]
						)	
		self.poly(surf, cd[3],cd[2],cd[13],cd[12],cd[4])	
		self.poly(surf, cd[3],cd[2],cd[16],cd[12],cd[4])
		
		self.poly(surf, cd[12],cd[13],
						[cd[14][0]+2,cd[14][1]],   [cd[15][0]+1,cd[15][1]],
						[cd[15][0]-1,cd[15][1]],   [cd[14][0],cd[14][1]],
						[(cd[12][0]+cd[14][0])/2+2,(cd[12][1]+cd[14][1])/2]
						)
		self.poly(surf, cd[12],cd[16],
						[cd[17][0]+2,cd[17][1]],   [cd[18][0]+1,cd[18][1]],
						[cd[18][0]-1,cd[18][1]],   [cd[17][0],cd[17][1]],
						[(cd[12][0]+cd[17][0])/2+2,(cd[12][1]+cd[17][1])/2]
						)
						
		self.poly(surf, [cd[4][0],cd[4][1]],cd[5],cd[6])					


	def walk(self):
		s = self
		s.t += 1
		
		s.to(1,0,30-math.cos(s.t*s.aspd*2)*5)
		s.to(0,0,-85+math.cos(s.t*s.aspd*2)*10)
		
		s.to(3,0,190+math.cos(s.t*s.aspd*2)*1)
		s.to(4,0,-20+math.cos(s.t*s.aspd*2)*2)
		
		s.to(6,0,30+math.cos(s.t*s.aspd*1.5)*10)
		
		s.to(7,1,9-math.cos(s.t*s.aspd*2)*1)
		
		s.to(8,0,-18+math.sin(s.t*s.aspd)*25)
		s.to(9,0,-20-math.cos(s.t*s.aspd)*20)
		
		s.to(10,0,-18+math.sin(s.t*s.aspd+math.pi)*25)
		s.to(11,0,-20-math.cos(s.t*s.aspd+math.pi)*20)
		
		s.to(12,1,7+math.cos(s.t*s.aspd*2)*1)
		
		s.to(13,0,75+math.cos(s.t*s.aspd)*15)
		s.to(14,0,-90+math.cos(s.t*s.aspd)*15)
		s.to(15,0,55+math.sin(s.t*s.aspd)*2)

		s.to(16,0,75+math.cos(s.t*s.aspd+math.pi)*15)
		s.to(17,0,-90+math.cos(s.t*s.aspd+math.pi)*20)
		s.to(18,0,55+math.sin(s.t*s.aspd+math.pi)*2)	

	def rest(self):
		s = self
		s.x -= 0.3
		s.t +=1
		for i in range(0,len(s.skel)):
			if i != 6 and i != 1:
				s.to(i,0,s.ssk[i][0]+noise.noise(i*0.05,s.t*0.05),5)
		s.to(6,0,30+math.cos(s.t*s.aspd*0.5)*10)
		
		noi = max(min((noise.noise(s.t*s.aspd*0.05)-0.4)*40,1),-1)
		s.to(1,0,-5+noi*50,5)
		s.to(0,0,-40-noi*40,5)

class Deer(Horse):
	def __init__(self,x,y,color=(140,140,140),s=1.1):
		super(Deer,self).__init__(x,y)
		self.skel[1][1] = 15
		self.skel[5][1] = 5
		self.skel[6][1] = 5
		self.ssk = copy.deepcopy(self.skel)
		self.s = s
		self.dir = -1
		self.horn = pygame.Surface([100*self.s,50*self.s])
		self.horn.fill([255,0,255])
		self.horn.set_colorkey([255,0,255])
		self.color = color
		
		self.spd = 0.6
		self.tx = 0
		
		tree.drawTree(surf = self.horn,
				 x = 50*self.s,
				 y = 50*self.s,
				 angle = math.pi*2/3,
				 dangle = lambda dep: 0,
				 
				 trunk = 0,
				 dtrunk = lambda dep: 0,
				 
				 width = 3*self.s*0.6,
				 dwidth = lambda dep: random.random()*0.1+0.9,
				 
				 height = 4*self.s*0.6,
				 dheight = lambda dep: 1.2*((dep*2)%2)+0.4,
				 
				 opening = math.pi/6,
				 dopening = lambda dep: 0.5+random.random()*0.5,
				 
				 color = self.color,
				 depth = 0,
				 maxdepth = 6
				)	
		if self.dir == -1:
			self.horn = pygame.transform.flip(self.horn,1,0)
		self.shorn = self.horn	

	def draw(self,surf):
		super(Deer,self).draw(surf)
		cd = []
		for i in range(len(self.skel)):
			cd.append(self.calcCoord(i)[:2])
		self.horn = self.shorn
		a = self.dir*(self.calcCoord(0)[2]+30)

		self.horn = pygame.transform.rotate(self.horn, a)	
		if self.dir == 1:
			hc = [cd[1][0]*self.s+self.x     - 50*self.s*math.cos(math.radians(90+a))-70*self.s*math.cos(math.radians(45-a)),
								 cd[1][1]*self.s+self.y+self.yo        - 68*self.s*math.sin(math.radians(45-a))]
		else:
			hc = [-cd[1][0]*self.s+self.x   - 50*self.s*math.cos(math.radians(a))-49*self.s*math.sin(math.radians(a)),
								 cd[1][1]*self.s+self.y+self.yo  - 50*self.s*math.sin(math.radians(a)) - 49*self.s*math.cos(math.radians(a))]

		surf.blit(self.horn,[hc[0],hc[1]])
		
class Bird(Animal):
	def __init__(self,x,y):
		super(Bird,self).__init__(x,y)
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

		self.arrow = None

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
		s.x += 0.3
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
	def simpDraw(self,surf):
		cd = []
		for i in range(len(self.skel)-3):
			cd.append(self.calcCoord(i)[:2])		
		s = self

		s.poly(surf,cd[3],cd[2],cd[5],
					[cd[5][0]-5,cd[5][1]])
		s.poly(surf,cd[5],cd[6],
					[cd[6][0]-8,cd[6][1]],
					[cd[5][0]-5,cd[5][1]])
		s.poly(surf,cd[6],[cd[6][0]-8,cd[6][1]],cd[7])
			
		s.poly(surf,cd[4],cd[11],cd[0],cd[1],cd[2],cd[3])
	
class Crane(Bird):
	def __init__(self,x,y):
		super(Crane,self).__init__(x,y)
		self.skel=[ [ -5, 8, 1],		
					[  30,10, 2],#1
					[   0, 0, 2],
					[ 190,10, 2],
					[ -10, 5, 3],
					[ 150, 8, 2],#5
					[ -60,10, 5],
					[  50,10, 6],
					[ 150, 8, 2],
					[ -60,10, 8],
					[  50,10, 9],#10
					[-140, 8, 2],
					[ -30, 3,11],
					[  50,10,12],
					[ -30, 3,11],
					[  50,10,14] #15
				  ]		
		self.t = random.random()*math.pi*2	
	def fly(self):
		
		s = self
		s.t += 1
		
		s.w1[1] = -1+u.trapwave(s.t*s.aspd)*3 
		s.w2[1] = -2+u.trapwave(s.t*s.aspd)*8 
		s.w3[1] = -1+u.trapwave(s.t*s.aspd+math.pi*0.2)*12
			
		s.w2[0] = -3+math.sin(s.t*s.aspd-math.pi*0.5)*2 
		s.w3[0] = -5+math.sin(s.t*s.aspd-math.pi*0.5)*3 
			
			
		s.wingCoordToRL(5,s.w1)
		s.wingCoordToRL(6,s.w2,s.w1,s.skel[5][0])
		s.wingCoordToRL(7,s.w3,s.w2,s.skel[6][0],s.skel[5][0])
		
		s.wingCoordToRL(8,s.w1)
		s.wingCoordToRL(9,s.w2,s.w1,s.skel[5][0])
		s.wingCoordToRL(10,s.w3,s.w2,s.skel[6][0],s.skel[5][0])			
			
			
		s.to(4,0,-0+math.sin(s.t*s.aspd+math.pi)*10) 
		s.to(1,0,-5+math.sin(s.t*s.aspd)*1)
		
		s.to(12,0,-40)
		s.to(14,0,-40)
		
		s.to(13,0,10+math.sin(s.t*s.aspd)*5 + 10*noise.noise(s.t*s.aspd*0.01,1)-5)
		s.to(15,0,10+math.sin(s.t*s.aspd)*5 + 10*noise.noise(s.t*s.aspd*0.01,2)-5)

		s.y += 0.2*self.s*math.sin(s.t*s.aspd+math.pi)
		
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
		
			
		s.poly(surf,cd[2],[(cd[2][0]+cd[3][0])/2,(cd[2][1]+cd[3][1])/2-2],cd[3],cd[11],[(cd[2][0]+cd[1][0])/2,(cd[2][1]+cd[1][1])/2])
		s.poly(surf,[(cd[3][0]+cd[4][0])/2,(cd[3][1]+cd[4][1])/2],cd[3],cd[11])
		s.poly(surf,cd[1],cd[2],[cd[2][0],cd[2][1]+2])
		s.poly(surf,cd[0],cd[1],[(cd[0][0]+cd[1][0])/2,(cd[0][1]+cd[1][1])/2-2])
			
		s.line(surf,cd[11],cd[12],1)
		s.line(surf,cd[11],cd[14],1)
		
		s.poly(surf,cd[3],cd[4],cd[11])
		
		s.line(surf,cd[12],cd[13],0.5)

class Firefly:
	def __init__(self, x, y) -> None:
		self.x = x
		self.y = y
		self.radius = random.randint(7, 12)
		self.light = pygame.Surface((2*self.radius, 2*self.radius), pygame.SRCALPHA)
		self.light.set_colorkey((255, 0, 255))
		self.alpha = 0
		self.spd = 0.5
		self.time = 0
		self.dir = [-1, -1]

	def fly(self):
		self.x += noise.noise(self.x, self.y)*0.5* math.sin(self.alpha)*self.dir[0]
		self.y += noise.noise(self.x, self.y)*0.5*math.cos(self.alpha)*self.dir[1]
		self.time += random.random()
		if (random.random() < 0.005):
			self.dir = [random.choice((-1, 1)), random.choice((-1, 1))]
	
	def draw(self, surface):
		u.circle(surface, (0, 255 - self.alpha*30, 0), (self.x, self.y), 1)
		self.light.fill((255, 0, 255))
		u.circle(self.light, (0, 255, 0), (self.radius, self.radius), self.radius)
		self.light.set_alpha(55*abs(math.sin(self.alpha)))
		self.alpha += 0.005
		surface.blit(self.light, (self.x-self.radius, self.y-self.radius))
