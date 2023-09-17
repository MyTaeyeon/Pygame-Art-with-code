import pygame
import math
import random
import sys
import utilities as u
import noise
# import lib.utilities as u
# import lib.noise as noise
import threading

pygame.init()

def drawTree(**p):
	if p['depth'] < p['maxdepth']:

		if p['height'] <1:return

		dep = p['depth']
		p['width'] *= p['dwidth'](dep)


		x0 = p['x']+math.cos(p['angle'])*p['trunk']
		y0 = p['y']-math.sin(p['angle'])*p['trunk']
		u.line(p['surf'],p['color'],[p['x'],p['y']],[x0,y0],p['width'])


		p['width'] *= p['dwidth'](dep)
		a1 = p['angle']-p['opening']*p['dopening'](dep)
		a2 = p['angle']+p['opening']*p['dopening'](dep)

		h1 = p['height'] * p['dheight'](dep)
		x1 = x0+math.cos(a1)*h1
		y1 = y0-math.sin(a1)*h1

		h2 = p['height'] * p['dheight'](dep)
		x2 = x0+math.cos(a2)*h2
		y2 = y0-math.sin(a2)*h2

		u.line(p['surf'],p['color'],[x0,y0],[x1,y1],p['width'])
		u.line(p['surf'],p['color'],[x0,y0],[x2,y2],p['width'])


		p['trunk'] *= p['dtrunk'](dep)

		p['depth'] += .5
		p['x'],p['y'],p['height'],p['angle'] = x1,y1,h1,a1-p['dangle'](dep)

		drawTree(**p)


		p['depth'] += .5
		p['x'],p['y'],p['height'],p['angle'] = x2,y2,h2,a2+p['dangle'](dep)
		drawTree(**p)
	else:
		return

def tree1(surf,x,y,shade=0):    
	drawTree(surf = surf,
			 x = x,
			 y = y,
			 angle = math.pi/2,
			 dangle = lambda dep: -(random.random()-0.5)*math.pi/3,

			 trunk = 50,
			 dtrunk = lambda dep: 0.8*random.random(),

			 width = 8,
			 dwidth = lambda dep: random.random()*0.2+0.8,

			 height = 50,
			 dheight = lambda dep: random.random()*0.6+0.4,

			 opening = math.pi/6,
			 dopening = lambda dep: random.random()*0.5+0.8,

			 color = (100+shade,100+shade,100+shade),
			 depth = 0,
			 maxdepth = 10
			)

def tree2(surf,x,y,shade=0):
	drawTree(surf = surf,
			 x = x,
			 y = y,
			 angle = math.pi/2,
			 dangle = lambda dep: 0,

			 trunk = 20,
			 dtrunk = lambda dep: 0.9,

			 width = 10,
			 dwidth = lambda dep: random.random()*0.35+0.7,

			 height = 100,
			 dheight = lambda dep: 0.6,

			 opening = math.pi/3,
			 dopening = lambda dep: ((dep*2)%2)*(0.8+random.random()*0.4),

			 color = (100+shade,100+shade,100+shade),
			 depth = 0,
			 maxdepth = 12
			)

def tree3(surf,x,y,shade=0):
	drawTree(surf = surf,
			 x = x,
			 y = y,
			 angle = math.pi/2,
			 dangle = lambda dep: -(random.random()-0.5)*math.pi/3,

			 trunk = 0,
			 dtrunk = lambda dep: 0.8*random.random(),

			 width = 6,
			 dwidth = lambda dep: random.random()*0.2+0.8,

			 height = 100,
			 dheight = lambda dep: random.random()*0.7+0.2,

			 opening = math.pi/3,
			 dopening = lambda dep: random.random()*2-1,

			 color = (100+shade,100+shade,100+shade),
			 depth = 0,
			 maxdepth = 10
			)



def tree4(surf,x,y,shade=0):
	drawTree(surf = surf,
			 x = x,
			 y = y,
			 angle = math.pi/2,
			 dangle = lambda dep: (-math.pi/6)+((random.random()-0.5)*(dep))*2,

			 trunk = 50,
			 dtrunk = lambda dep: 0.8*random.random(),

			 width = 8,
			 dwidth = lambda dep: random.random()*0.2+0.8,

			 height = 50,
			 dheight = lambda dep: random.random()*0.5+0.5,

			 opening = math.pi/5,
			 dopening = lambda dep: 0.8 + random.random()*0.5*dep*2,

			 color = (100+shade,100+shade,100+shade),
			 depth = 0,
			 maxdepth = 10
			)

pygame.init()

# setting up variables
size = width, height = 1280, 320
buff = 200
screen = pygame.display.set_mode([width/2,height+50])#,pygame.FULLSCREEN )
screen.fill((255, 255, 255))
pygame.display.set_caption("")

treeDensity = 32
landDensity = 32

allloads = width/treeDensity
loaded = 0

Ls = [None]*4
Lrs = [None]*4

gamestart = False

COLOR_KEY = [255,0,255]

terrain = [0]*4

lspds = [0.1,0.2,0.5,1]
totalMade = [0]*4

scheme = [(70,69,63),(225,225,210)]

def makeBGLayer(n):
	global loaded, allloads, terrain, lspds, totalMade
	print("Making Background...")
	l = pygame.Surface([width+buff*2,height])
	l.fill(COLOR_KEY)
	l.set_colorkey(COLOR_KEY)

	if terrain[n] == 0:
		treesum = width/(0.0+len(Ls)*treeDensity)
		for i in range(0,int(treesum)):
			thetree = [ random.choice([tree2]),
						random.choice([tree1,tree1,tree2]),
						random.choice([tree1,tree4,tree3]),
						random.choice([tree1,tree4,tree3]) ][n]
			thetree(l,random.random()*width+buff,height,(120-n*30)+random.randrange(-10,10))
			loaded += 1
	elif terrain[n] == 1:

		treesum = (width/(0.0+len(Ls)*treeDensity))
		for i in range(0,int(math.ceil(treesum/2.0))):
			thetree = [ random.choice([tree1,tree3]),
						random.choice([tree1,tree3]),
						random.choice([tree1,tree3]),
						random.choice([tree1,tree3]) ][n]
			thetree(l,random.random()*width+buff,height,(120-n*30)+random.randrange(-10,10))
			loaded += 2
		if n != 3:
			poly = []
			poly.append([0,height])
			for i in range(buff,width+buff,landDensity):
				poly.append([i,height-makeLand(i*0.05,n*0.5,500-n*90)])
			poly[1][1] = (poly[1][1]-height)/2.0+height
			poly[-1][1] = (poly[-1][1]-height)/2.0+height
			poly.append([width+buff*2,height])
			pygame.draw.polygon(l,(210-n*20,210-n*20,210-n*20),poly)

	totalMade[n] += 1
	if totalMade[n]%int(lspds[n]*10) == 0:
		terrain[n] = (terrain[n]+1) % 2


	print(str(loaded)+"/"+str(allloads))
	return l


def mt(LN, *args):
	global Ls, Lrs, loaded, allloads
	allloads = len(args)*(width/(len(Ls)*treeDensity))
	loaded = 0
	if LN == 1:
		for a in args:
			Ls[a] = makeBGLayer(a)
	elif LN == 2:
		for a in args:
			Lrs[a] = makeBGLayer(a)

def makeLand(n,m=0,maxheight = 20):
	return max(noise.noise(n*0.1,m*0.5)*maxheight,2)-2

thread1 = threading.Thread(target=mt, args=(2,  3, 2, 1, 0))
thread1.start()
thread1.join()

while loaded<allloads:
    pass

scroll = 0

while (True):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

	screen.fill((255, 255, 255))

	screen.blit(Lrs[0], (scroll, 0))
	screen.blit(Lrs[1], (scroll, 0))
	screen.blit(Lrs[2], (scroll, 0))
	screen.blit(Lrs[3], (scroll, 0))

	if pygame.key.get_pressed()[pygame.K_RIGHT]:
		scroll -= 1
	if pygame.key.get_pressed()[pygame.K_LEFT]:
		scroll += 1
	pygame.display.update()
		