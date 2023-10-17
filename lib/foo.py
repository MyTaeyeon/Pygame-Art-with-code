# implement code here
import pygame
import utilities as u
import tree 
import noise 
import creature 
import random
import math
import threading
import sys
import daynnightloop as filter

pygame.init()

clock = pygame.time.Clock()

# setting up variables
size = width, height = 1280, 320
buff = 200
screen = pygame.display.set_mode([width/2,height+50])
# screen = pygame.display.set_mode([width/2,height+50], pygame.FULLSCREEN)
screen.fill((255, 255, 255))
pygame.display.set_caption("")

treeDensity = 32
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

lspds = [0.2,0.4,0.6,1.2]
totalMade = [0]*4

birds = []

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


	# print(str(loaded)+"/"+str(allloads))
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
	if 0 < ox / landDensity < len(land) - 1:
		return height - min(land[math.ceil(ox / landDensity)], land[math.floor(ox / landDensity)])
	else:
		return 320

player = creature.Player(0, height - land[0])

def makeBirds(n):
	global birds
	for i in range(0,n):
		b = creature.Bird(random.randrange(width//2+30,width//2+60),0)
		b.s = 0.5
		b.aspd = 0.3
		b.yo = height
		b.color = (140,140,140)
		b.dir = random.choice([1,-1])
		birds.append(b)

def birdCtrl():
	global birds, arrows
	for b in birds:
		if b.health > 0:
			if ((abs(player.x - b.x) < 320 and random.random()<0.05) or random.random()<0.0002) and b.on == 0:
				b.on = 1
				ra = math.pi/20.0+random.random()*math.pi/6.0*2.1
				rl = random.choice([3,4,5])
				b.v=[rl*math.cos(ra),-rl*math.sin(ra)]
			if b.on == 1:
				b.simpFly()

				if abs(player.x - b.x) > 160 and random.random()<1:
					b.v[1] = min(b.v[1]+0.05,0.4)
				if b.y >= 2:
					b.on = 0

			else:
				b.rest()
				if 0 < b.x < width/2:
					b.yo=onlandY(b.x) - 3

			if b.x<0 or b.x>width or b.yo<0:
				birds.remove(b)
		else:
			b.fall()

locs = [0,0,0,0]
locrs = [width,width,width,width]

t1 = t2 = None

T = 0
r = 0
gifts = [creature.goStraight(random.randint(100, width // 2 - 50), random.randint(-30, -10), [random.randint(-6, 6), random.randint(3, 6)]) for i in range(7)]
shape = [None] * len(gifts)
cnt = [0] * len(gifts)
phase = 0
zoff = 0
while (True):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

	clock.tick(45)
 
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
	
	for j in range(len(gifts)):
		if cnt[j] == 0:
			if gifts[j].update(onlandY(gifts[j].x)) =='boom':
				cnt[j] = 21
				gifts[j] = [creature.splinter(gifts[j].x + random.randint(-6, 6), gifts[j].y + random.randint(0, 6), 
								[random.randint(-6, 6), random.randint(-3, -1)], 
								150, random.randint(3, 5), random.randint(15, 20)) for i in range(20)]
			else:
				if r==0 and u.dist(gifts[j].x, gifts[j].y, player.x, player.y) < 30:
					cnt = 21
					gifts[j] = [creature.splinter(gifts[j].x + random.randint(-6, 6), gifts[j].y + random.randint(0, 6), 
								[random.randint(-6, 6), random.randint(-3, -1)], 
								150, random.randint(3, 5), random.randint(15, 20)) for i in range(20)]
					r = 1
				else:	
					# draw gift!!!				
					vertices = []

					for a in range(0, int(2 * math.pi / math.radians(5))):
						a = a * math.radians(5)
						xoff = math.cos(a + phase) 
						yoff = math.sin(a + phase) 
						xoff = u.map_value(xoff, -1, 1, 0, 4.0)
						yoff = u.map_value(yoff, -1, 1, 0, 4.0)
						r = u.map_value(noise.noise(xoff, yoff,zoff), 0, 1, 15, 5)
						x = r * math.cos(a) + gifts[j].x
						y = r * math.sin(a) + gifts[j].y
						vertices.append((x, y))
					
					u.polygon(canvas, (110, 110, 110), vertices)
					
					phase += 0.003
					zoff += 0.01

		elif cnt[j] > 1:
			for i in range(len(gifts[j])):
				if gifts[j][i] == None:
					continue
				if gifts[j][i].update() == 'boom':
					gifts[j][i] = None
					cnt[j] -= 1
				else:
					gifts[j][i].draw(canvas)
		else:
			cnt[j] = 0
			gifts[j] = creature.goStraight(random.randint(100, width // 2 - 50), random.randint(-30, -10), [random.randint(-6, 6), random.randint(3, 6)])
		
	u.polygon(canvas,(130,130,130),[[0,height]]+[[landloc+i*landDensity,height-land[i]] for i in range(0,len(land))]+[[width/2,height]]) 
	player.update(onlandY(player.x))
	player.vx = 0
	player.draw(canvas)
	usercontrol = pygame.key.get_pressed()

	if usercontrol[pygame.K_RIGHT]:
		if player.x >= 10 * landDensity:
			player.x = 10 * landDensity
			landloc -= SPEED
			scroll -= SPEED
		else:
			player.vx = SPEED
	if usercontrol[pygame.K_LEFT]:
		player.vx = -SPEED
		if player.x < 10:
			player.x = 10
	if usercontrol[pygame.K_SPACE] and player.status == 'onland':
		player.status = 'insky'
		player.time = 0
		player.vy = SPEED * 4.5
		player.ay = SPEED / 3

	# for b in birds:
	# 	b.draw(canvas)

	if landloc < -landDensity:
		landni += 1
		land.append(makeLand(landni,maxheight=land[-1] + 20))
		landloc += landDensity
		land.pop(0)

	

	# if T % 1000 == 0:
	# 	makeBirds(20)
	# birdCtrl()

	screen.blit(canvas,[0,0])
     
	# reflect
	reflection = canvas#pygame.transform.flip(canvas,False,True)
	pygame.draw.rect(screen,(180,180,180),[0,height,width/2,50])
	for i in range(0,2*(screen.get_height()-height),2):
		screen.blit(reflection,[(math.sin(i*0.5))*i*0.5+(noise.noise(pygame.time.get_ticks()*0.001,i*0.2)-0.5)*20,height+i-1],(0,height-i,width/2,1))

	T += 1
	array = [pygame.surfarray.pixels_red(screen),pygame.surfarray.pixels_green(screen),pygame.surfarray.pixels_blue(screen)]
	filter.filter(array,T)
	del(array)

	pygame.display.update()	
 