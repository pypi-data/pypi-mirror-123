import sys
import random
from itertools import cycle 

import pygame
from pygame.locals import* 


import os.path
from os import path
import json
import tkinter
import tkinter.messagebox as msgbox


class FlappyBird:
	def __init__(self): 

		self.isRobot = True
		self.isRender = True
		self.isOpenHitmaskFile = False
		self.isLearning = False


		self.FPS			= 30
		self.SCREENWIDTH 	= 288
		self.SCREENHEIGHT 	= 512
		self.PIPEGAPSIZE 	= 100 
		self.BASEY			= self.SCREENHEIGHT * 0.79	
		self.IMAGES, self.SOUNDS, self.HITMASKS = {}, {}, {}	

		self.IM_WIDTH = 0
		self.IM_HEIGTH = 1

		self.PIPE = [52, 320]
		self.PLAYER = [34, 24]
		self.BASE = [336, 112]
		self.BACKGROUND = [288, 512]
		self.MESSAGE 	= [184, 267]


	def initMainData(self):

		assets_path = path.join(path.dirname(__file__), 'assets')
		sprites_path = path.join(assets_path, 'sprites')
		audio_path = path.join(assets_path, 'audio')

		self.PLAYERS_LIST = (
			(
				path.join(sprites_path, 'redbird-upflap.png'),
				path.join(sprites_path, 'redbird-midflap.png'), 
				path.join(sprites_path, 'redbird-downflap.png'),
			),
			(
				path.join(sprites_path, 'bluebird-upflap.png'),
				path.join(sprites_path, 'bluebird-midflap.png'), 
				path.join(sprites_path, 'bluebird-downflap.png'),
			),
			(
				path.join(sprites_path, 'yellowbird-upflap.png'),
				path.join(sprites_path, 'yellowbird-midflap.png'), 
				path.join(sprites_path, 'yellowbird-downflap.png'),
			),
		)

		self.BACKGROUNDS_LIST = (
			path.join(sprites_path, 'background-day.png'),
			path.join(sprites_path, 'background-night.png'),
		)

		self.PIPES_LIST = (
			path.join(sprites_path, 'pipe-green.png'),
			path.join(sprites_path, 'pipe-red.png'),
		)

		global SCREEN, FPSCLOCK
		pygame.init()
		FPSCLOCK = pygame.time.Clock()
		SCREEN = pygame.display.set_mode((self.SCREENWIDTH, self.SCREENHEIGHT))
		pygame.display.set_caption('Flayppy Bird')
		icon = pygame.image.load(path.join(assets_path, 'flappy.ico'))
		pygame.display.set_icon(icon)

		self.IMAGES['numbers'] = (
	        pygame.image.load(path.join(sprites_path, '0.png')).convert_alpha(),
	        pygame.image.load(path.join(sprites_path, '1.png')).convert_alpha(),
	        pygame.image.load(path.join(sprites_path, '2.png')).convert_alpha(),
	        pygame.image.load(path.join(sprites_path, '3.png')).convert_alpha(),
	        pygame.image.load(path.join(sprites_path, '4.png')).convert_alpha(),
	        pygame.image.load(path.join(sprites_path, '5.png')).convert_alpha(),
	        pygame.image.load(path.join(sprites_path, '6.png')).convert_alpha(),
	        pygame.image.load(path.join(sprites_path, '7.png')).convert_alpha(),
	        pygame.image.load(path.join(sprites_path, '8.png')).convert_alpha(),
	        pygame.image.load(path.join(sprites_path, '9.png')).convert_alpha(),
	    )

		self.IMAGES['gameover'] = pygame.image.load(path.join(sprites_path, 'gameover.png')).convert_alpha()
		self.IMAGES['message'] = pygame.image.load(path.join(sprites_path, 'message.png')).convert_alpha()
		self.IMAGES['base'] = pygame.image.load(path.join(sprites_path, 'base.png')).convert_alpha()

		if 'win' in sys.platform: 
			soundExt = '.wav'
		else:
			soundExt = '.ogg'
		self.SOUNDS['die']    = pygame.mixer.Sound(path.join(audio_path, 'die') + soundExt)
		self.SOUNDS['hit']    = pygame.mixer.Sound(path.join(audio_path, 'hit') + soundExt)
		self.SOUNDS['point']  = pygame.mixer.Sound(path.join(audio_path, 'point') + soundExt)
		self.SOUNDS['swoosh'] = pygame.mixer.Sound(path.join(audio_path, 'swoosh') + soundExt)
		self.SOUNDS['wing']   = pygame.mixer.Sound(path.join(audio_path, 'wing') + soundExt)

		return True


	def main(self):
		randBg = random.randint(0, len(self.BACKGROUNDS_LIST) - 1)
		self.IMAGES['background'] = pygame.image.load(self.BACKGROUNDS_LIST[randBg]).convert()

		randPlayer = random.randint(0, len(self.PLAYERS_LIST) - 1)
		self.IMAGES['player'] = (
			pygame.image.load(self.PLAYERS_LIST[randPlayer][0]).convert_alpha(),
			pygame.image.load(self.PLAYERS_LIST[randPlayer][1]).convert_alpha(),
			pygame.image.load(self.PLAYERS_LIST[randPlayer][2]).convert_alpha(),
		)

		pipeIndex = random.randint(0, len(self.PIPES_LIST) - 1)
		self.IMAGES['pipe'] = (
			pygame.transform.rotate(
				pygame.image.load(self.PIPES_LIST[pipeIndex]).convert_alpha(), 180),
			pygame.image.load(self.PIPES_LIST[pipeIndex]).convert_alpha(),
		)

		self.HITMASKS['pipe'] = (
			self.getHitmask(self.IMAGES['pipe'][0]),
			self.getHitmask(self.IMAGES['pipe'][1]),
		)


		self.HITMASKS['player'] = (
			self.getHitmask(self.IMAGES['player'][0]),
			self.getHitmask(self.IMAGES['player'][1]),
			self.getHitmask(self.IMAGES['player'][2]),
		)


	def showWelcomeAnimation(self):
		playerIndex = 0
		playerIndexGen = cycle([0, 1, 2, 1])

		loopIter = 0

		playerx = int(self.SCREENWIDTH * 0.2)
		playery = int((self.SCREENHEIGHT - self.PLAYER[self.IM_HEIGTH]) / 2)
		
		messagex = int((self.SCREENWIDTH - self.MESSAGE[self.IM_WIDTH]) / 2)
		messagey = int(self.SCREENWIDTH * 0.12)

		basex = 0
		baseShift = self.BASE[self.IM_WIDTH] - self.BACKGROUND[self.IM_WIDTH]

		playerShmVals = {'val': 0, 'dir':1}
		if self.isRobot:
			return { 
					'playery': playery + playerShmVals['val'],
					'basex': basex,
					'playerIndexGen': playerIndexGen,
				}
		
		while True:
			
			for event in pygame.event.get():	
				if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):  
					pygame.quit()
					sys.exit()
				if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
					self.SOUNDS['wing'].play()
					return { 
						'playery': playery + playerShmVals['val'],
						'basex': basex,
						'playerIndexGen': playerIndexGen,
					}

			if (loopIter + 1) % 5 == 0:
				playerIndex = next(playerIndexGen) 
			loopIter = (loopIter + 1) % 30	


			basex = -((-basex + 4) % baseShift)	

			self.playerShm(playerShmVals)

			SCREEN.blit(self.IMAGES['background'], (0,0))
			SCREEN.blit(self.IMAGES['player'][playerIndex], (playerx, playery + playerShmVals['val']))
			SCREEN.blit(self.IMAGES['message'], (messagex, messagey))
			SCREEN.blit(self.IMAGES['base'], (basex, self.BASEY))

			pygame.display.update()
			FPSCLOCK.tick(self.FPS)


	def initMainGameData(self, movementInfo):
		self.score = self.playerIndex = self.loopIter = 0
		self.playerIndexGen = movementInfo['playerIndexGen']
		self.playerx, self.playery = int(self.SCREENWIDTH * 0.2), movementInfo['playery']

		self.basex = movementInfo['basex']
		self.baseShift = self.BASE[self.IM_WIDTH] - self.BACKGROUND[self.IM_WIDTH]

		self.newPipe1 = self.getRandomPipe()
		self.newPipe2 = self.getRandomPipe()

		self.upperPipes = [
			{'x': self.SCREENWIDTH + 200, 'y': self.newPipe1[0]['y']},
			{'x': self.SCREENWIDTH + 200 + (self.SCREENWIDTH / 2), 'y': self.newPipe2[0]['y']},
		]
		self.lowerPipes = [
			{'x': self.SCREENWIDTH + 200, 'y': self.newPipe1[1]['y']},
			{'x': self.SCREENWIDTH + 200 + (self.SCREENWIDTH / 2), 'y': self.newPipe2[1]['y']},
		]

		self.pipeVelX 		= -4  	

		self.playerVelY 		= -9	
		self.playerMaxVelY 	= 10 	
		self.playerMinVelY 	= -8 	
		self.playerAccY		= 1  	
		self.playerRot 		= 45	
		self.playerVelRot	= 3  	
		self.playerRotThr	= 20  	
		self.playerFlapAcc	= -9	
		self.playerFlapped	= False	


	def mainGame(self, action=0):
	
		if -self.playerx + self.lowerPipes[0]['x'] > -30:
			myPipe = self.lowerPipes[0]
		else:
			myPipe = self.lowerPipes[1]

		if self.isRender:
			for event in pygame.event.get():
				if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
					pygame.quit()
					sys.exit()
				if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
					if self.playery > -2 * self.PLAYER[self.IM_HEIGTH]:
						self.playerVelY = self.playerFlapAcc
						self.playerFlapped = True
						self.SOUNDS['wing'].play()

		if self.isRobot:
			if action:
				if self.playery > -2 * self.PLAYER[self.IM_HEIGTH]:
						self.playerVelY = self.playerFlapAcc
						self.playerFlapped = True
						if self.isRender:
							self.SOUNDS['wing'].play()




		self.crashTest = self.checkCrash({'x': self.playerx, 'y': self.playery, 'index': self.playerIndex},
								self.upperPipes, self.lowerPipes)
		if self.crashTest[0]:

			return{
				'y': self.playery,
				'groundCrash': self.crashTest[1],
				'basex': self.basex,
				'upperPipes': self.upperPipes,
				'lowerPipes': self.lowerPipes,
				'score': self.score,
				'playerVelY': self.playerVelY,
				'playerRot': self.playerRot,
				'state': (-self.playerx + myPipe['x'], -self.playery + myPipe['y'], self.playerVelY)
			}
			

		playerMidPos = self.playerx + self.PLAYER[self.IM_WIDTH] / 2
		for pipe in self.upperPipes:
			pipeMidPos = pipe['x'] + self.PIPE[self.IM_WIDTH] / 2
			if pipeMidPos <= playerMidPos < pipeMidPos + 4:
				self.score += 1
				if self.isRender:
					self.SOUNDS['point'].play()


		if (self.loopIter + 1) % 3 == 0:
			self.playerIndex = next(playerIndexGen) 
		loopIter = (self.loopIter + 1) % 30	
		self.basex = -((-self.basex + 100) % self.baseShift)	

		if self.playerRot > -90:
			self.playerRot -= self.playerVelRot

		if self.playerVelY < self.playerMaxVelY and not self.playerFlapped:
			self.playerVelY += self.playerAccY
		if self.playerFlapped:
			self.playerFlapped = False
			self.playerRot = 45

		playerHeight = self.PLAYER[self.IM_HEIGTH]
		self.playery += min(self.playerVelY, self.BASEY - self.playery - playerHeight)

		for uPipe, lPipe in zip(self.upperPipes, self.lowerPipes):
			uPipe['x'] += self.pipeVelX
			lPipe['x'] += self.pipeVelX

		if len(self.upperPipes) > 0 and 0 < self.upperPipes[0]['x'] < 5:
			newPipe = self.getRandomPipe()
			self.upperPipes.append(newPipe[0])
			self.lowerPipes.append(newPipe[1])

		if len(self.upperPipes) > 0 and self.upperPipes[0]['x'] < -self.PIPE[self.IM_WIDTH]:
			self.upperPipes.pop(0)
			self.lowerPipes.pop(0)


		if self.isRobot and self.isRender==False:
			return{
				'state': (-self.playerx + myPipe['x'], -self.playery + myPipe['y'], self.playerVelY),
				'score': self.score
			}

		SCREEN.blit(self.IMAGES['background'], (0, 0))

		for uPipe, lPipe in zip(self.upperPipes, self.lowerPipes):
			SCREEN.blit(self.IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
			SCREEN.blit(self.IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

		SCREEN.blit(self.IMAGES['base'], (self.basex, self.BASEY))
		self.showScore(self.score)

		self.visibleRot = self.playerRotThr
		if self.playerRot <= self.playerRotThr:
			self.visibleRot = self.playerRot

		playerSurface = pygame.transform.rotate(self.IMAGES['player'][self.playerIndex], self.visibleRot)
		SCREEN.blit(playerSurface, (self.playerx, self.playery))

		pygame.display.update()
		FPSCLOCK.tick(self.FPS)

		if self.isRobot:
			return{
				'state': (-self.playerx + myPipe['x'], -self.playery + myPipe['y'], self.playerVelY),
				'score': self.score
			}


	def play(self):
		self.isRobot = False
		self.initMainData()
		while True:
			self.main()
			movementInfo = self.showWelcomeAnimation()
			self.initMainGameData(movementInfo)
			while True:
				crashInfo = self.mainGame()
				if self.is_terminal():
					break
			self.showGameOverScreen(crashInfo)


	def reset(self, isRender=True):
		self.isRobot = True
		self.isRender = isRender
		if isRender:
			if self.isLearning == False:
				self.isLearning = self.initMainData()
			self.main()
		else:
			if self.isOpenHitmaskFile == False:
				if os.path.exists('data/hitmasks_data.json') == True:
					with open('data/hitmasks_data.json', 'r') as input:
						self.HITMASKS = json.load(input)
					print('hitmasks_data.json was Opened')
					self.isOpenHitmaskFile = True
				else:
					self.creatHismasksFile()
		movementInfo = self.showWelcomeAnimation()
		self.initMainGameData(movementInfo)
		return (420, 240, 0)

	def step(self, action):
		crashInfo = self.mainGame(action)
		state = crashInfo['state']
		score = crashInfo['score']
		done = self.crashTest[0]
		return state, score, done

	def is_terminal(self):
		if self.crashTest[0]==True:
			return True
		else:
			return False


	def creatHismasksFile(self):
		os.environ["SDL_VIDEODRIVER"] = "dummy"
		
		pygame.init()
		SCREEN = pygame.display.set_mode((1, 1))

		assets_path = path.join(path.dirname(__file__), 'assets')
		sprites_path = path.join(assets_path, 'sprites')

		self.PLAYERS_LIST = (
				path.join(sprites_path, 'redbird-upflap.png'),
				path.join(sprites_path, 'redbird-midflap.png'), 
				path.join(sprites_path, 'redbird-downflap.png'),
			)

		self.PIPES_LIST = (
			path.join(sprites_path, 'pipe-green.png'),
		)

		self.IMAGES['player'] = (
			pygame.image.load(self.PLAYERS_LIST[0]).convert_alpha(),
			pygame.image.load(self.PLAYERS_LIST[1]).convert_alpha(),
			pygame.image.load(self.PLAYERS_LIST[2]).convert_alpha(),
		)

		self.IMAGES['pipe'] = (
			pygame.transform.rotate(
				pygame.image.load(self.PIPES_LIST[0]).convert_alpha(), 180),
			pygame.image.load(self.PIPES_LIST[0]).convert_alpha(),
		)

		self.HITMASKS['pipe'] = (
			self.getHitmask(self.IMAGES['pipe'][0]),
			self.getHitmask(self.IMAGES['pipe'][1]),
		)


		self.HITMASKS['player'] = (
			self.getHitmask(self.IMAGES['player'][0]),
			self.getHitmask(self.IMAGES['player'][1]),
			self.getHitmask(self.IMAGES['player'][2]),
		)
		pygame.quit()
		os.environ["SDL_VIDEODRIVER"] = 'windib'

		if os.path.exists('data') == False:
			dir_path = os.getcwd() + '/data'
			os.mkdir(dir_path)

		if os.path.exists('data/hitmasks_data.json') == False:
			with open('data/hitmasks_data.json', 'w') as output:
				json.dump(self.HITMASKS, output)
			print('hitmask_data.json was created successfully')


	def showGameOverScreen(self, crashInfo):
		score = crashInfo['score']
		playerx = self.SCREENWIDTH * 0.2
		playery = crashInfo['y']
		playerHeight = self.IMAGES['player'][0].get_height()
		playerVelY = crashInfo['playerVelY']
		playerAccY = 2  
		playerRot = crashInfo['playerRot']
		playerVelRot = 7

		basex = crashInfo['basex']

		upperPipes, lowerPipes = crashInfo['upperPipes'], crashInfo['lowerPipes']

		self.SOUNDS['hit'].play()
		if not crashInfo['groundCrash']:
			self.SOUNDS['die'].play()

		if self.isRobot:
			return

		while True:
			for event in pygame.event.get():
				if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
					pygame.quit()
					sys.exit()
				if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
					if playery + playerHeight >= self.BASEY - 1:
						return

			if playery + playerHeight < self.BASEY - 1:
				playery += min(playerVelY, self.BASEY - playery - playerHeight)

			if playerVelY < 15:
				playerVelY += playerAccY

			if not crashInfo['groundCrash']:
				if playerRot > -90:
					playerRot -= playerVelRot

			SCREEN.blit(self.IMAGES['background'], (0, 0))

			for uPipe, lPipe in zip(upperPipes, lowerPipes):
				SCREEN.blit(self.IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
				SCREEN.blit(self.IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

			SCREEN.blit(self.IMAGES['base'], (basex, self.BASEY))
			self.showScore(score)

			playerSurface = pygame.transform.rotate(self.IMAGES['player'][1], playerRot)
			SCREEN.blit(playerSurface, (playerx, playery))
			SCREEN.blit(self.IMAGES['gameover'], (50, 180))

			pygame.display.update()
			FPSCLOCK.tick(self.FPS)


	def showScore(self, score):
		scroeDigits = [int(x) for x in list(str(score))]
		totalWidth = 0
		for digit in scroeDigits:
			totalWidth += self.IMAGES['numbers'][digit].get_width()

		Xoffset = (self.SCREENWIDTH - totalWidth) / 2

		for digit in scroeDigits:
			SCREEN.blit(self.IMAGES['numbers'][digit], (Xoffset, self.SCREENHEIGHT * 0.1))
			Xoffset += self.IMAGES['numbers'][digit].get_width()


	def checkCrash(self, player, upperPipes, lowerPipes):
		pi = player['index']
		player['w'] = self.PLAYER[self.IM_WIDTH]
		player['h'] = self.PLAYER[self.IM_HEIGTH]

		if player['y'] + player['h'] >= self.BASEY - 1:
			return[True, True]
		else:
			playerRect = pygame.Rect(player['x'], player['y'], player['w'], player['h'])
			pipeW = self.PIPE[self.IM_WIDTH]
			pipeH = self.PIPE[self.IM_HEIGTH]

			for uPipe, lPipe in zip(upperPipes, lowerPipes):
				uPipeRect = pygame.Rect(uPipe['x'], uPipe['y'], pipeW, pipeH)
				lPipeRect = pygame.Rect(lPipe['x'], lPipe['y'], pipeW, pipeH)

				pHitMask = self.HITMASKS['player'][pi]
				uHitmask = self.HITMASKS['pipe'][0]
				lHitmask = self.HITMASKS['pipe'][1]

				uCollide = self.pixelCollision(playerRect, uPipeRect, pHitMask, uHitmask)
				lCollide = self.pixelCollision(playerRect, lPipeRect, pHitMask, lHitmask)

				if uCollide or lCollide:
					return[True, False]

		return [False, False]


	def pixelCollision(self, rect1, rect2, hitmask1, hitmask2):
		rect = rect1.clip(rect2)

		if rect.width == 0 or rect.height == 0:
			return False

		x1, y1 = rect.x - rect1.x, rect.y - rect1.y
		x2, y2 = rect.x - rect2.x, rect.y - rect2.y

		for x in range(rect.width):
			for y in range(rect.height):
				if hitmask1[x1+x][y1+y] and hitmask2[x2+x][y2+y]:
					return True
		return False


	def getRandomPipe(self):
		gapY = random.randrange(0, int(self.BASEY * 0.6 - self.PIPEGAPSIZE))
		gapY += int(self.BASEY * 0.2)
		pipeHeight = self.PIPE[self.IM_HEIGTH]
		pipeX = self.SCREENWIDTH + 10

		return [
			{'x': pipeX, 'y': gapY - pipeHeight},
			{'x': pipeX, 'y': gapY + self.PIPEGAPSIZE}, 
		]


	def playerShm(self, playerShm):
		if abs(playerShm['val']) == 8:
			playerShm['dir'] *= -1

		if playerShm['dir'] == 1:
			playerShm['val'] += 1
		else:
			playerShm['val'] -= 1


	def getHitmask(self, image):
		mask = []
		for x in range(image.get_width()):
			mask.append([])
			for y in range(image.get_height()):
				mask[x].append(bool(image.get_at((x,y))[3]))
		return mask