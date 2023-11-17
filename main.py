import pygame
import lib.utilities as u
import lib.tree as tree
import lib.noise as noise
import lib.creature as creature
import random
import math
import threading
import sys 
import lib.daynnightloop as filter
import lib.pattern as pattern
import lib.font as font

pygame.init()
clock = pygame.time.Clock()

# setting up variables ============================================================================
size = width, height = 1280, 320
buff = 200
screen = pygame.display.set_mode([width/2,height+50])
screen.fill((240, 240, 240))
pygame.display.set_caption("")

COLOR_KEY = [255,0,255]

# terrain =========================================================================================
treeDensity = 32
landDensity = 32

allloads = 2 * width/treeDensity
loaded = 0

Ls = [None]*4
Lrs = [None]*4

terrain = [0]*4

lspds = [0.2,0.4,0.6,1.2]
totalMade = [0]*4

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

land = [0]*int(width/landDensity+2)
landloc = 0
landni = 0
for landni in range(len(land)):
	land[landni]=makeLand(landni,maxheight=20+terrain[3]*120)

def onlandY(ox):
	if 0 <= ox / landDensity < len(land) - 1:
		return height - min(land[math.ceil(ox / landDensity)], land[math.floor(ox / landDensity)])
	else:
		return 320
	
locs = [0,0,0,0]
locrs = [width,width,width,width]

# set icon ========================================================================================
scheme = [(70,69,63),(225,225,210)]
icon = pygame.Surface([512,512])
icon.set_colorkey(COLOR_KEY)

def Icon():
	global icon, scheme
	icon.fill(scheme[1])
	pygame.draw.rect(icon,scheme[0],[0,0,512,512],50)
	pygame.draw.circle(icon, (255, 255, 255), (256, 256), 100)
	pygame.display.set_icon(icon)

Icon()

# background ======================================================================================
def makeBGLayer(n):
	global loaded, allloads, terrain, lspds, totalMade
	print("Making Background...")
	l = pygame.Surface([width+buff*2,height])
	l.fill(COLOR_KEY)
	l.set_colorkey(COLOR_KEY)

	if terrain[n] == 0:
		treesum = width/(len(Ls)*treeDensity)
		for i in range(0,int(treesum)):
			thetree = [ random.choice([tree.tree2]),
						random.choice([tree.tree1,tree.tree1,tree.tree2]),
						random.choice([tree.tree1,tree.tree4,tree.tree3]),
						random.choice([tree.tree1,tree.tree4,tree.tree3]) ][n]
			thetree(l,random.random()*width+buff,height,(120-n*30)+random.randrange(-10,10))
			loaded += 1
	elif terrain[n] == 1:

		treesum = (width/(len(Ls)*treeDensity))
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

	return l

# camera ==========================================================================================
canvas = pygame.Surface([width/2,height])
scroll = 0
SPEED = 0.3
T = 0

# animal ==========================================================================================
birds = []
deers = []
cranes = []
fireflies = []

def makeBirds(n):
	global birds
	for i in range(0,n):
		b = creature.Bird(random.randrange(width//2+30,width//2+60),150)
		b.s = 0.5
		b.aspd = 0.3
		b.yo = height
		b.color = (140,140,140)
		b.dir = random.choice([1,-1])
		birds.append(b)

def birdCtrl():
	global birds, arrows, pctrl
	for b in birds:
		if random.random()<0.05 or random.random()<0.0002 and b.on == 0:
			b.on = 1
			ra = math.pi/20.0+random.random()*math.pi/6.0*2.1
			rl = random.choice([3,4,5])
			b.v=[rl*math.cos(ra)/4,-rl*math.sin(ra)/4]
		if b.on == 1:
			b.simpFly()

			if abs(320 - b.x) > 160:
				b.v[1] = min((b.v[1]+0.05) /4,0.1)
			if b.y >= 2:
				b.on = 0

		else:
			b.rest()
			if 0 < b.x < width/2:
				b.yo=height-3-onlandY(b.x)

		if b.x<0 or b.x>width or b.yo<0:
			birds.remove(b)

def makeDeers(n):
	global deers
	for i in range(0,n):
		r = random.randrange(-5,5)
		deer = creature.Deer(width/2+landDensity+50+r*10,0,color = (160+r,160+r,160+r))
		deer.yo = height
		deer.s = 1.1
		deer.aspd = 0.05
		deers.append(deer)

def makeCranes(n):
	global cranes
	for j in range(0,n):
		r = random.randrange(-5,5)
		crane = creature.Crane(width/2+landDensity+random.randrange(0,200),0)
		crane.color = (180+r,180+r,180+r)
		crane.yo = height-150-120*random.random()
		crane.s = 0.5+random.random()*0.2
		crane.aspd = 0.05
		crane.dir = -1
		crane.t = (j/5.0)*200
		cranes.append(crane)

def deersCtrl():
	for d in deers:
		d.yo = -30+onlandY(max(min(d.x,width/2),0))
		if noise.noise(T*0.001,deers.index(d))<0.5:
			d.x -= d.spd
			d.walk()
		else:
			d.rest()
		if d.x<-150:
			deers.remove(d)

def craneCtrl():
	global cranes
	for c in cranes:
		c.x -= 2*c.s
		c.fly()
		if c.x<-100:
			cranes.remove(c)

def makeFireflies(n):
	global fireflies
	for _ in range(n):
		fireflies.append(creature.Firefly(random.randrange(30,width//2+30), random.randint(30, 270)))

def fireflyCtrl():
	for a in fireflies:
		a.fly()
		a.x -= SPEED
		if a.y > height:
			a.dir[1] *= -1
		if a.time > 350 or a.x < -50:
			fireflies.remove(a)

# Game is running =================================================================================

def play():
	global scroll, T, birds, deers, screen, Lrs, locrs, Ls, locs, SPEED, canvas, terrain, landloc, landni, landDensity
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
					
		screen.fill((255, 255, 255))
		canvas.fill([240,240,240])
		
		for i in range(4):
			if Ls[i] is not None:
				canvas.blit(Ls[i],[locs[i]+scroll*lspds[i]-buff,0])

			if locs[i]+scroll*lspds[i] < -width-buff:
				locs[i] += width*2
				# Ls[i] = makeBGLayer(i)
				t1 = threading.Thread(target=mt, args=(1, i))
				t1.start()

			if Lrs[i] is not None:
				canvas.blit(Lrs[i],[locrs[i]+scroll*lspds[i]-buff,0])

			if locrs[i]+scroll*lspds[i] < -width-buff:
				locrs[i] += width*2
				# Lrs[i] = makeBGLayer(i)
				t2 = threading.Thread(target=mt, args=(2, i))
				t2.start()

		for d in deers:
			d.draw(canvas)
		for b in birds:
			b.draw(canvas)
		for c in cranes:
			c.draw(canvas)

		u.polygon(canvas,(130,130,130),[[0,height]]+[[landloc+i*landDensity,height-land[i]] for i in range(0,len(land))]+[[width/2,height]]) 

		landloc -= SPEED
		scroll -= SPEED

		if landloc < -landDensity:
			landni += 1
			land.append(makeLand(landni,maxheight=land[-1] + 20))
			landloc += landDensity
			land.pop(0)

		birdCtrl()
		deersCtrl()
		craneCtrl()
		fireflyCtrl()

		screen.blit(canvas,[0,0])

		# reflect
		reflection = canvas
		pygame.draw.rect(screen,(180,180,180),[0,height,width/2,50])
		for i in range(0,2*(screen.get_height()-height),2):
			screen.blit(reflection,[(math.sin(i*0.5))*i*0.5+(noise.noise(pygame.time.get_ticks()*0.001,i*0.2)-0.5)*20,height+i-1],(0,height-i,width/2,1))

		T += 1
		array = [pygame.surfarray.pixels_red(screen),pygame.surfarray.pixels_green(screen),pygame.surfarray.pixels_blue(screen)]
		filter.filter(array,T)
		del(array) 

		for f in fireflies:
			f.draw(screen)

			if f.y + f.radius > height - 50:
				for p in range(max(0, int(f.y - f.radius - height + 50)), int(f.y + f.radius - height + 50 + 1), 3):
					u.line(screen, (118, 171, 144), (f.x - f.radius - (math.sin(p*0.5))*p*0.5 + noise.noise(pygame.time.get_ticks()*0.001, p*0.2) + 3, height + 50 - p), (f.x + f.radius + (math.sin(p*0.5))*p*0.5 - noise.noise(pygame.time.get_ticks()*0.001, p*0.2) - 3, height + 50 - p))

		color = screen.get_at((0, 0))

		if color.r > 140:
			if random.random()<0.0002:
				makeBirds(random.randrange(6,10))
			if random.random() < 0.0002 and terrain[3] == 0:
				makeDeers(1)
			if random.random() < 0.0002 and terrain[3] == 1:
				makeCranes(5)
		elif color.r <= 120:
			if random.random() < 0.03:
				makeFireflies(1)

		pygame.display.update()	

thread2 = threading.Thread(target=mt, args=(1,  3, 2, 1, 0))
thread2.start()
thread1 = threading.Thread(target=mt, args=(2,  3, 2, 1, 0))
thread1.start()

vine = pattern.Vine(0,160)
screen.fill([240,240,240])
for _ in range(10000):
	vine.grow(screen)
	pygame.draw.rect(screen,(240,240,240),[0,170,100,20])
	u.text(screen,10,height/2+15,f"Loading... {'{:.1f}'.format(loaded / allloads / 2 * 100)}%",(180,180,180))
	u.line(screen,(180,180,180),[0,height/2],[(float(loaded)/allloads)*width/2,height/2],1)

	pen = font.GFont(20, 2)
	pen.drawStr(screen,"by MyTaeyeon",350,280, size=0.5)
	pygame.display.flip()
thread2.join()
thread1.join()

while loaded<allloads:
	pass

play()