import sys, os, time, random, struct
import pygame
from pygame.locals import *

import input
import net

sys.path.append('../proto')
import message_pb2

import random as _random

timestart = time.time()
timenow = lambda : int(int((time.time() - timestart) * 1000) & 0x7fffffff)


ctimebase = 0
ctimesvr = 0

ctimenow = lambda : ctimesvr + (timenow() - ctimebase)

# 0-无, 1-上, 2-右上, 3-右, 4-右下, 5-下, 6-左下, 7-左, 8-左上
direction = ( (0, 0), (0, -1), (1, -1), (1, 0), (1, 1), 
			(0, 1), (-1, 1), (-1, 0), (-1, -1) )

middle = lambda begin, n, end: max(begin, min(n, end))

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))

aircraft1 = pygame.image.load("asset/aircraft1.png")
aircraft2 = pygame.image.load("asset/aircraft2.png")
star1     = pygame.image.load("asset/s1.png")
star2     = pygame.image.load("asset/s2.png")

FRAME_DELAY = 20


# draw some star
MAX_STAR = 64
stars = []

random = lambda n: _random.randint(0, n)

for i in range(MAX_STAR):
	stars.append([random(width), -100 + random(width)])

# background
def update_star():
	limit = MAX_STAR / 3
	
	for i in range(len(stars)):
		star = stars[i]
		star[1] += (i < limit) and 0.25 or 0.1
		s = (i < limit) and star1 or star2

		if star[1] >= height:
			star[0], star[1] = random(width), (-200 + random(150))

		screen.blit(s, (star[0], star[1]))

#----------------------------------------------------------------------
# aircraft class
#----------------------------------------------------------------------
class aircraft(object):
	def __init__(self, id=0):
		self.x = 0
		self.y = 0
		self.d = 0
		self.v = 0
		self.id = 0
	
	def draw_craft(self):
		screen.blit(aircraft1, (self.x, self.y))

	def craft_move(self, step):
		x, y, d, v = self.x, self.y, self.d, self.v
		for i in range(step):
			x += v * direction[d][0]
			y += v * direction[d][1]

			x = middle(0, x, width)
			y = middle(0, y, height)
			
			self.x, self.y = x, y

	def initpos(self):
		self.x = 320 - 40 * 4 + self.id + 40
		self.y = 350
		self.v = 8
		self.d = 0
		
		return 0

class cclient(object):
	def __init__(self):
		self.client = net.netconn()
		self.timebase = timenow()
		self.state = 0
		self.frame = 0
		self.frameslap = 0
		self.current = 0
		self.crafts = [aircraft(i) for i in range(8)]
		self.craft  = self.crafts[0]
		self.input_state = input.none_state

		self.snapshot = message_pb2.Snapshot()

	def __current(self):
		return timenow() - self.timebase

	def startup(self, ip='127.0.0.1', port=8000):
		# connect to the server
		self.client.connect(ip, port)
		self.craft.initpos()
	
	def handleInput(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit(0)
			elif event.type == pygame.KEYDOWN:
				self.keydown(event)
			elif event.type == pygame.KEYUP:
				self.keyup(event)

	def keydown(self, event):
		self.craft.d, self.input_state = self.input_state.keydown(event.key)


	def keyup(self, event):
		self.craft.d, self.input_state = self.input_state.keyup(event.key)
	
	def logic(self):
		current = self.__current()
		while current >= self.frameslap:
			self.frame += 1
			self.frameslap += FRAME_DELAY
			self.ontimer()

	def ontimer(self):
		current = self.__current()
		frame = self.frame

		self.craft.craft_move(1)

		# 测试, 上报数据
		if frame %60 == 0:
			snapshot = self.snapshot
			snapshot.x = self.craft.x
			snapshot.y = self.craft.y
			snapshot.d = self.craft.d
			snapshot.v = self.craft.v
	
			msg = snapshot.SerializeToString()
			self.client.send(msg)

	def render(self):
		update_star()
		self.craft.draw_craft()

	def process(self):
		# net process
		self.client.process()

		# input process
		self.handleInput()

		# run logic
		self.logic()
	
		# render frame
		self.render()
		
	

def game_main():
	client = cclient()
	client.startup()

	while 1 :
		time.sleep(0.001)

		screen.fill(0)
	
		client.process()

		pygame.display.flip()

if __name__ == '__main__':
	game_main()
