# implement code here
import pygame
import lib.utilities as u
import lib.tree as tree
import lib.noise as noise
import lib.creature as creature
import random
import math
import threading
import sys

pygame.init()

clock = pygame.time.Clock()

# setting up variables
size = width, height = 1280, 320
buff = 200
screen = pygame.display.set_mode([width/2,height+50])#,pygame.FULLSCREEN )
screen.fill((255, 255, 255))
pygame.display.set_caption("")

treeDensity = 64
landDensity = 32

allloads = 2 * width/treeDensity
loaded = 0

Ls = [None]*4
Lrs = [None]*4

gamestart = False

COLOR_KEY = [255,0,255]

terrain = [0]*4
landcreated = pygame.Surface([2 * width + buff*2, height])
landcreated.fill(COLOR_KEY)
landcreated.set_colorkey(COLOR_KEY)

lspds = [0.1,0.2,0.5,1]
totalMade = [0]*4

def makeBGLayer(n):
	global loaded, allloads, terrain, lspds, totalMade
	print("Making Background...")
	l = pygame.Surface([2 * width+buff*2,height])
	l.fill(COLOR_KEY)
	l.set_colorkey(COLOR_KEY)

	if terrain[n] == 0:
		treesum = 2 * width/(0.0+len(Ls)*treeDensity)
		for i in range(0,int(treesum)):
			thetree = [ random.choice([tree.tree2]),
						random.choice([tree.tree1,tree.tree1,tree.tree2]),
						random.choice([tree.tree1,tree.tree4,tree.tree3]),
						random.choice([tree.tree1,tree.tree4,tree.tree3]) ][n]
			thetree(l,random.random()*width+buff,height,(120-n*30)+random.randrange(-10,10))
			loaded += 1
	elif terrain[n] == 1:

		treesum = 2 * (width/(0.0+len(Ls)*treeDensity))
		for i in range(0,int(math.ceil(treesum/2.0))):
			thetree = [ random.choice([tree.tree1,tree.tree3]),
						random.choice([tree.tree1,tree.tree3]),
						random.choice([tree.tree1,tree.tree3]),
						random.choice([tree.tree1,tree.tree3]) ][n]
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


	# print(str(loaded)+"/"+str(allloads))
	return l

def mt(LN, *args):
	global Ls, Lrs, loaded, allloads
	allloads = len(args)*(2 * width/(len(Ls)*treeDensity))
	loaded = 0
	if LN == 1:
		for a in args:
			Ls[a] = makeBGLayer(a)
	elif LN == 2:
		for a in args:
			Lrs[a] = makeBGLayer(a)

def makeLand(n,m=0,maxheight = 20):
	return max(noise.noise(n*0.1,m*0.5)*maxheight,2)-2

land = [0]*int(width/landDensity+2)
landloc = 0
landni = 0
for landni in range(len(land)):
	land[landni]=makeLand(landni,maxheight=20+terrain[3]*120)

mt(1, 3, 2 , 1, 0)

thread1 = threading.Thread(target=mt, args=(2,  3, 2, 1, 0))
thread1.start()
thread1.join()

while loaded<allloads:
    pass

scroll = 0
canvas = pygame.Surface([width/2,height])
x = 0
SPEED = 3

def onlandY(ox):
	return height - land[math.ceil(ox // landDensity)] - 10

player = creature.simplePlayer(10, height - land[0] - 10)

locs = [0,0,0,0]
locrs = [width,width,width,width]

t1 = t2 = None

while (True):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

	clock.tick(60)

	screen.fill((255, 255, 255))
	canvas.fill([240,240,240])
	
	for i in range(4):
		if Ls[i] is not None:
			canvas.blit(Ls[i],[locs[i]+scroll*lspds[i]-buff,0])

		if locs[i]+scroll*lspds[i] < -width-buff:
			locs[i] += width*2
			t1 = threading.Thread(target=mt, args=(1, i))
			t1.start()

		if Lrs[i] is not None:
			canvas.blit(Lrs[i],[locrs[i]+scroll*lspds[i]-buff,0])

		if locrs[i]+scroll*lspds[i] < -width-buff:
			locrs[i] += width*2
			t2 = threading.Thread(target=mt, args=(2, i))
			t2.start()
	if t1 != None:
		t1.join()
		t1 = None
	if t2 != None:
		t2.join()
		t2 = None
		
	u.polygon(canvas,(130,130,130),[[0,height]]+[[landloc+i*landDensity,height-land[i]] for i in range(0,len(land))]+[[width/2,height]]) 
	player.update(onlandY(player.x))
	player.draw(canvas)

	if landloc < -landDensity:
		landni += 1
		land.append(makeLand(landni,maxheight=land[-1] + 20))
		landloc += landDensity
		land.pop(0)

	usercontrol = pygame.key.get_pressed()

	if usercontrol[pygame.K_RIGHT]:
		if player.x >= 15 * landDensity:
			player.x = 15 * landDensity
			landloc -= SPEED
			scroll -= SPEED
		else:
			player.x += SPEED
	if usercontrol[pygame.K_LEFT]:
		player.x -= SPEED
		if player.x < 10:
			player.x = 10
	if usercontrol[pygame.K_UP]:
		if player.jumping == False and player.falling == False:
			player.jumpy = player.y - 60
			player.jumping = True

	screen.blit(canvas,[0,0])
	pygame.display.update()	
	