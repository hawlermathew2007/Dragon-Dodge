import pygame
import math
import random
import os

pygame.init()

screen_width = 1200
screen_height = 700

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Dragon Dodge")

# establish a highscore text doc to hold player highscore
if not os.path.exists("dragonhighscore.txt"):
	f = open("dragonhighscore.txt", "x")
	with open("dragonhighscore.txt", "w") as f:
		f.write("0")
	highscore = 0
else:
	with open("dragonhighscore.txt", "r") as f:
		highscore = int(f.read())

# Path
images_path = 'images'
sounds_path = 'sounds'

# del color
white = (255, 255, 255)
darkblue = (18, 25, 69)
graywhite = (245,245,245)

# text
text = pygame.font.SysFont("Impact", 30)
dPowerText = pygame.font.SysFont('Impact', 15)
remindText = pygame.font.SysFont("Arial", 20, 'bold')
powerText = pygame.font.SysFont("Arial", 50, 'bold')

# game text
dragonDodge = pygame.image.load(f'{images_path}/introduction.png')
gameOverText = pygame.image.load(f'{images_path}/gameover.png')
startText = pygame.image.load(f'{images_path}/start.png')
restartText = pygame.image.load(f'{images_path}/restart.png')

# dragon img
dragonImg = pygame.image.load(f'{images_path}/dragon-fly.png')
dragonFire = pygame.image.load(f'{images_path}/dragon-fire.png')
dragonPain = pygame.image.load(f'{images_path}/dragon-pain.png').convert()
dragonPain.set_colorkey(white)
dragonSleep = pygame.image.load(f'{images_path}/dragon-sleep.png')
dragonAwake = pygame.image.load(f'{images_path}/dragon-awake.png')
dragonDeath = pygame.image.load(f'{images_path}/dragon-death.png')

# dragon power
fireballP = pygame.image.load(f'{images_path}/fireball.png').convert()
firebreathP = pygame.image.load(f'{images_path}/firebreath.png').convert()
fireballP.set_colorkey(white)
firebreathP.set_colorkey(darkblue)

# dragon power button
fbrBt = pygame.image.load(f'{images_path}/fbrBtt.png')
fbaBt = pygame.image.load(f'{images_path}/fbaBtt.png')
fbrBtGray = pygame.image.load(f'{images_path}/fbrGray.png').convert()
fbrBtGray.set_colorkey(graywhite)
fbaBtGray = pygame.image.load(f'{images_path}/fbaGray.png').convert()
fbaBtGray.set_colorkey(graywhite)
# fbaBt.set_alpha(200)

# asteroid img
asteroidImg = pygame.image.load(f'{images_path}/asteroid.png').convert()
asteroidImg.set_colorkey(white)
asteroidImg = pygame.transform.rotate(asteroidImg, -45)

#explosion
explosion = pygame.image.load(f'{images_path}/explode.png').convert()
explosion.set_colorkey(white)

# heart and black heart
heart = pygame.image.load(f'{images_path}/heart.png')
blackheart = pygame.image.load(f'{images_path}/blackheart.png')

# img for wall
cobblestone = pygame.image.load(f'{images_path}/cobblestone.png')
wood = pygame.image.load(f'{images_path}/wood.png')

# background
bg = pygame.image.load(f'{images_path}/dragonBg.png').convert()
pygame.transform.scale(bg, (screen_width - (screen_width/3), screen_height))
bg_width = bg.get_width()


# shortcut for scale
def scale(img,width, height):
	return pygame.transform.scale(img, (width, height))

def lessRepetive(self, velocityOb, scorepoint):	# will use this to make less repetive
	pass

class Dragon(pygame.sprite.Sprite):
	def __init__(self, image, width, height, x, y):
		super().__init__()
		self.image = image
		self.width = width
		self.height = height
		self.rect = self.image.get_rect()
		self.mask = pygame.mask.from_surface(self.image)
		self.rect.center = [x, y]
		self.breathEffect = pygame.mixer.Sound(f'{sounds_path}/drbreath.wav')
		self.fireballEffect = pygame.mixer.Sound(f'{sounds_path}/drball.mp3')
		self.drBlinkTimes = 3
		self.powerWidth = 100 
		self.powerHeight = 100


	def breath(self):
		self.breathEffect.play()

		xp = self.rect.x + (self.width/2)
		yp = self.rect.y + (self.height/2)

		firebrP = DrShot(firebreathP, self.powerWidth+10, self.powerHeight-70, xp, yp, 0)
		dragonPower.add(firebrP)


	def fireball(self):
		self.fireballEffect.play()

		xp = self.rect.x + (self.width/2)
		yp = self.rect.y + (self.height/2)

		firebaP = DrShot(pygame.transform.rotate(fireballP, -135), self.powerWidth+60, self.powerHeight+60, xp, yp, 1)
		dragonPower.add(firebaP)


	def update(self):
		
		if not game_over and not startIntro:

			velocity = 2
			angle = 18

			# control dragon 
			if pygame.key.get_pressed()[pygame.K_UP]:
				self.rect.y -= velocity
				rotate = pygame.transform.rotate(dragonImg, angle)
				self.image = scale(rotate, self.width+angle, self.height+(angle*2))

			if pygame.key.get_pressed()[pygame.K_DOWN]:
				self.rect.y += velocity
				rotate = pygame.transform.rotate(dragonImg, -angle)
				self.image = scale(rotate, self.width+angle, self.height+(angle*2))

			if pygame.key.get_pressed()[pygame.K_RIGHT]:
				self.rect.x += velocity
				self.image = scale(dragonImg, self.width, self.height)

			if pygame.key.get_pressed()[pygame.K_LEFT]:
				self.rect.x -= 	velocity
				self.image = pygame.transform.flip(scale(dragonImg, self.width, self.height), True, False)

			# limit dragon space
			if self.rect.x < 0:
				self.rect.x = 0

			if self.rect.right > screen_width:
				self.rect.right = screen_width

			if self.rect.y < 0:
				self.rect.y = 0

			if self.rect.bottom > screen_height:
				self.rect.bottom = screen_height



class Asteroid(pygame.sprite.Sprite):
	def __init__(self, image, width, height, x, y):
		super().__init__()
		self.image = scale(image, width, height)
		self.width = width
		self.height = height
		self.rect = self.image.get_rect()
		self.mask = pygame.mask.from_surface(self.image)
		self.rect.center = [x, y]
		# for displaying explosion
		self.count = 0
		self.displayExplosion = False
		self.playExplodeSound = pygame.mixer.Sound(f'{sounds_path}/boom.mp3')
		# for displaying explosion and plus score when dodge successfully
		self.trigger = True
		self.triggerEx = True

	def update(self, dragonInfo):
		
		global game_over
		global score
		global deathHeart

		velocityAs = 1

		if not game_over:

			if score > 500:
				velocityAs = 1.5

			if score > 800:
				velocityAs = 2

			if score > 1000:
				velocityAs = 2.2

			self.rect.x -= velocityAs

			# destroy itself when reach limit => less heavy game
			if self.rect.x < -self.width:
				self.kill()

			# plus score when dodge successfully
			if self.rect.x < dragonInfo.rect.x - self.width and self.trigger:

				score += 10 			# prevent from plus too much cause by while loop

				self.trigger = False


			# when dragon and self collide it will -30 point 
			if self.mask.overlap(dragonInfo.mask, (dragonInfo.rect.x - self.rect.x, dragonInfo.rect.y - self.rect.y)) and self.triggerEx:
				score -= 30
				self.triggerEx = False	# prevent from minus too much cause by while loop
				self.displayExplosion = True	# display explosion for more longer
				# self.rect.x += 20 		# for more realistic
				self.playExplodeSound.play()

			# display explosion when dragon get hit
			if self.displayExplosion:
				self.count += 1 		# count till 80 => allow explosion effect last longer	
				dragonInfo.image = scale(dragonPain, dragon_width, dragon_height)
				self.image = scale(explosion, 100, 100)

			# when done displaying delete a life and let dragon img back to normal
			if self.count > 80 and self.displayExplosion:
				self.displayExplosion = False
				dragonInfo.image = scale(dragonImg,dragon_width, dragon_height)
				deathHeart += 1
				self.kill()



class Wall(pygame.sprite.Sprite):
	def __init__(self, img, width, height, x, y):
		super().__init__()
		self.width = width
		self.height = height
		self.sequence = []
		self.image = scale(img,  width, height)
		self.rect = self.image.get_rect()
		self.mask = pygame.mask.from_surface(self.image)
		self.rect.center = [x, y]
		self.count = 0
		self.displayExplosion = False
		self.playExplodeSound = pygame.mixer.Sound(f'{sounds_path}/boom.mp3')
		self.trigger = True
		self.triggerEx = True

	def update(self, dragonInfo):
		
		global game_over
		global score
		global deathHeart

		velocityWall = 1

		# same as Asteroid
		if not game_over:

			if score > 500:
				velocityWall = 1.2

			if score > 800:
				velocityWall = 1.4

			if score > 1000:
				velocityWall = 1.8

			self.rect.x -= velocityWall

			if self.rect.x < -self.width:
				self.kill()

			if self.rect.x < dragonInfo.rect.x - self.width and self.trigger:

				score += 30

				self.trigger = False


			# same as the class above
			if self.mask.overlap(dragonInfo.mask, (dragonInfo.rect.x - self.rect.x, dragonInfo.rect.y - self.rect.y)) and self.triggerEx:
				score -= 50
				self.triggerEx = False
				self.displayExplosion = True
				self.playExplodeSound.play()

			if self.displayExplosion:
				self.count += 1
				dragonInfo.image = scale(dragonPain, dragon_width, dragon_height)
				self.image = scale(explosion, 100, 100)

			if self.count > 80 and self.displayExplosion:
				self.displayExplosion = False
				dragonInfo.image = scale(dragonImg,dragon_width, dragon_height)
				deathHeart += 1
				self.kill()

		

class Heart(pygame.sprite.Sprite):
	def __init__(self, img, width, height, x, y, _id):
		super().__init__()
		self.image = scale(img, width, height)
		self.lifeImg = scale(heart, width, height)
		self.deathImg = scale(blackheart, width, height)
		self.mask = pygame.mask.from_surface(self.lifeImg)
		self.width = width
		self.height = height
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.id = _id
		self.reviveSound = pygame.mixer.Sound(f'{sounds_path}/gainlife.wav')
		self.ohnoSound = pygame.mixer.Sound(f'{sounds_path}/ohno.mp3')
		self.playONSound = True
		self.triggerH = True
		self.count = 0


	def update(self, dragonInfo):
		
		global deathHeart

		if deathHeart > 0 and self.id != None:
			for bh in range(deathHeart):
				if bh == self.id and self.id == 3 and self.playONSound:
					self.ohnoSound.play()
					self.playONSound = False

				hearts[bh].image = scale(self.deathImg, self.width, self.height)

		if self.id == None and not game_over:	# just to let the compu know that we r not refering about the 5 display life heart

			velocityH = 1.2

			self.rect.x -= velocityH

			if self.rect.x < -self.width:
				self.kill()

			# each time the dragon hit the heart, the dragon will gain another life
			if self.mask.overlap(dragonInfo.mask, (dragonInfo.rect.x - self.rect.x, dragonInfo.rect.y - self.rect.y)) and self.triggerH:
				self.reviveSound.play()
				self.triggerH = False
				for h in range(len(hearts)):
					hearts[h].image = scale(self.lifeImg, self.width, self.height)
				deathHeart -= 1
				self.kill()



class Button(pygame.sprite.Sprite):
	def __init__(self, img, width, height, x, y, _type):
		super().__init__()
		self.image = scale(img, width, height)
		self.type = _type
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.clicked = False


	def update(self, dragonInfo):

		pos = pygame.mouse.get_pos()
		
		if self.type == 'start':

			if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:

				self.clicked = True


		if self.type == 'restart':
			
			if pygame.key.get_pressed()[pygame.K_SPACE] or (self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1):

				self.clicked = True



class DrSkill(pygame.sprite.Sprite):
	def __init__(self, img, width, height, x, y, _type):
		super().__init__()
		self.initialImg = img
		self.image = scale(img, width, height)
		self.width = width
		self.height = height
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		if _type == 'fbr':
			self.standard = 5
			self.gray = scale(fbrBtGray, width, height)
			self.frequency = 8000
		else:
			self.standard = 3
			self.gray = scale(fbaBtGray, width, height)
			self.frequency = 12000
		self.countTimes = 0
		self.last_stop = 0
		self.time_now = 0
		self.trigger = True
		self.timeTrigger = True
		self.render = False


	def update(self):

		if self.countTimes >= self.standard:
			if self.timeTrigger:
				self.last_stop = pygame.time.get_ticks()
				self.timeTrigger = False

			self.render = True
			self.image = self.gray
			self.time_now = pygame.time.get_ticks()
			if self.time_now - self.last_stop > self.frequency:
				self.image = scale(self.initialImg, self.width, self.height)
				self.render = False
				self.timeTrigger = True
				self.countTimes = 0



class DrShot(pygame.sprite.Sprite):
	def __init__(self, img, width, height, x, y, _type):
		super().__init__()
		self.image = scale(img,  width, height)
		self.type = _type
		self.targetGroup = None
		self.afraidGroup = None
		self.rect = self.image.get_rect()
		self.mask = pygame.mask.from_surface(self.image)
		self.rect.center = [x, y]
		self.playExplodeSound = pygame.mixer.Sound(f'{sounds_path}/boom.mp3')
		self.count = 0
		self.displayExplosion = False
		self.trigger = True

	def update(self):
		
		velocityP = 3

		if not self.displayExplosion:
			self.rect.x += 3

		if self.rect.x > screen_width:
			self.kill()


		if self.type == 0:	# activate for firebreath
			self.targetGroup = asteroidGroup
			self.afraidGroup = wallGroup

		if self.type == 1:	# activate for fireball
			self.targetGroup = wallGroup
			self.afraidGroup = asteroidGroup

		if pygame.sprite.spritecollide(self, self.targetGroup, True, pygame.sprite.collide_mask) and self.trigger:
			self.trigger = False
			self.displayExplosion = True	# display explosion for more longer
			self.rect.x += 50
			self.playExplodeSound.play()

		if pygame.sprite.spritecollide(self, self.afraidGroup, False, pygame.sprite.collide_mask) and self.trigger:
			self.trigger = False
			self.kill()

		# display explosion when hit target
		if self.displayExplosion:
			self.count += 1 		# count till 80 => allow explosion effect last longer	
			self.image = scale(explosion, 100, 100)

		# end displaying
		if self.count > 80 and self.displayExplosion:
			self.displayExplosion = False
			self.kill()



# tiles for bg
tiles = math.ceil(screen_width/bg.get_width()) + 1

# button
buttonGroup = pygame.sprite.Group()
gOTextW = 700
gOTextH = 100
stTextW = 300
stTextH = 50

# dragon
dragon_width = 180
dragon_height = 140
dragonIntroW = 500 
dragonIntroH = 400
dragon = Dragon(scale(dragonImg, dragon_width, dragon_height), dragon_width, dragon_height, 200, screen_height/2 - dragon_height/2)
dragon_group = pygame.sprite.Group()
dragon_group.add(dragon)

# dragon power
dragonPower = pygame.sprite.Group()

# dragon power button 
drPowerBtWidth = 100
drPowerBtHeight = 100
distancePBt = 40
drPBtxr = screen_width - drPowerBtWidth*2 - distancePBt
drPBtyr = screen_height - drPowerBtHeight + 32
drPBtxa = screen_width - drPowerBtWidth
drPBtya = screen_height - drPowerBtHeight + 32
fbrButton = DrSkill(fbrBt, drPowerBtWidth, drPowerBtHeight, drPBtxr, drPBtyr, 'fbr')
fbaButton = DrSkill(fbaBt, drPowerBtWidth+28, drPowerBtHeight+28, drPBtxa, drPBtya, 'fba')
drPBttGroup = pygame.sprite.Group()
drPBttGroup.add(fbrButton)
drPBttGroup.add(fbaButton)

# death heart
deathHeart = 0

# count death for allowing to display dragon death for more long
countDeath = 0

# score
score = 0

#scoll value
scoll = 0
scoll_speed = 0.5

# game over value
game_over = False
displayGameOver = False
gameoverSound = pygame.mixer.Sound(f'{sounds_path}/gameoverSound.mp3')
playGOSound = False
playONSound = False
ohnoSound = pygame.mixer.Sound(f'{sounds_path}/ohno.mp3')
countStay = 0

# start Intro
startIntro = True
running = False
startGame = False
dragonGrowl = pygame.mixer.music.load(f'{sounds_path}/dragonGrowl.mp3')
triggerGrowl = True

startFrequency = 1500
clickOnce = True

drDodgeLabel = Button(gameOverText, gOTextW, gOTextH, (screen_width/2), (screen_height/2 - gOTextH/2)-150, None)
buttonGroup.add(drDodgeLabel)

startLabel = Button(startText, stTextW-60, stTextH+10, (screen_width/2), (screen_height/2 - gOTextH/2), 'start')
buttonGroup.add(startLabel)

dragon.image = scale(dragonSleep, dragonIntroW, dragonIntroH)

dragon.rect.x = screen_width/2 - dragonIntroW/2
dragon.rect.y = screen_height/2 - dragonIntroH/2 + 160

while startIntro:

	screen.blit(scale(pygame.image.load(f'{images_path}/hellbg.jpg'), screen_width, screen_height), (0,0))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			startIntro = False
			running = False

		if event.type == pygame.KEYDOWN and clickOnce:
			if event.key == pygame.K_SPACE and clickOnce:
				startGame = True
				clickOnce = False
				last_start = pygame.time.get_ticks()

		if startLabel.clicked and clickOnce:
			startGame = True
			clickOnce = False
			last_start = pygame.time.get_ticks()


	if startGame:
		countStay += 1
		if countStay > 80 and countStay < 120 and triggerGrowl:
			dragon.image = scale(dragonAwake, dragonIntroW, dragonIntroH)
			pygame.mixer.music.play()
			triggerGrowl = False

		if countStay > 120 and not pygame.mixer.music.get_busy():
			dragon.image = scale(dragonImg, dragon_width, dragon_height)
			dragon.rect.center = [200, screen_height/2 - dragon_height/2]

			buttonGroup.empty()

			startIntro = False
			running = True


	rText = remindText.render('press SPACE or click START to play game', True, (250,250,250))
	screen.blit(rText, (screen_width/2 - 150, screen_height-45))


	buttonGroup.draw(screen)
	buttonGroup.update(dragon)

	dragon_group.draw(screen)
	dragon_group.update()

	pygame.display.update()


countStay = 0


# asteroid
asteroidGroup = pygame.sprite.Group()
asWidth = 200
asHeight = 200
last_asteroid = pygame.time.get_ticks()
asteroidFrequency = 2000

# block (wall)
blockWidth = 120
blockHeight = 130
wallGroup = pygame.sprite.Group()
last_wall = pygame.time.get_ticks()
wallFrequency = 15000
sequenceWall = 4

# heart
heartWidth = 40 
heartHeight = 40
last_heart = pygame.time.get_ticks()
heartFrequency = 20000
rarityHR = 2000
hearts = []
heartGroup = pygame.sprite.Group()
numsHeart = 5
distanceHeart = 0
for i in range(numsHeart):
	xh = (screen_width - ((heartWidth+20)*5) + 40) + distanceHeart
	yh = 50

	heartOb = Heart(heart, heartWidth, heartHeight, xh, yh, i)
	heartGroup.add(heartOb)
	
	hearts.append(heartOb)

	distanceHeart += (heartWidth + 6)


# Play Game
while running:

	# this will make 3 tiles allow the background to move (3 bg attach to each other)
	for i in range(tiles):
		screen.blit(bg, (i * bg_width + scoll,0))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if not game_over:
			if event.type == pygame.KEYDOWN:
				# you can tell by reading it dumbass lazy shit
				if event.key == pygame.K_SPACE or event.key == pygame.K_r:
					dragon.image = scale(dragonFire, dragon_width, dragon_height)
					if event.key == pygame.K_SPACE and fbrButton.countTimes < 5 and fbrButton.trigger:
						dragon.breath()
						fbrButton.trigger = False
						fbrButton.countTimes += 1
					if event.key == pygame.K_r and fbaButton.countTimes < 3 and fbaButton.trigger:
						dragon.fireball()
						fbaButton.trigger = False
						fbaButton.countTimes += 1

			if event.type == pygame.KEYUP:
				# just make this more realistic
				if event.key == pygame.K_SPACE or event.key == pygame.K_r:
					dragon.image = scale(dragonImg, dragon_width, dragon_height)
					fbrButton.trigger = True
					fbaButton.trigger = True

				if event.key == pygame.K_UP:
					dragon.image = scale(dragonImg, dragon_width, dragon_height)
				
				if event.key == pygame.K_DOWN:
					dragon.image = scale(dragonImg, dragon_width, dragon_height)


	if not game_over:

		scoll -= scoll_speed

		time_now = pygame.time.get_ticks()
		# randomly spawn the asteroid
		if time_now - last_asteroid > asteroidFrequency:

			xa = screen_width
			ya = random.choices([random.randint(30, screen_height-asWidth), random.randint(screen_height - 120, screen_height - 80)], weights= (70, 30))[0]

			asteroid = Asteroid(asteroidImg, asWidth, asHeight, xa, ya)

			asteroidGroup.add(asteroid)

			last_asteroid = time_now

			if score > 500:
				asteroidFrequency = 1500

			if score > 1000:
				asteroidFrequency = 1000

			asteroidFrequency = random.randint(800, asteroidFrequency)


		# randomly spawn walls
		if time_now - last_wall > wallFrequency:

			xw = screen_width
			yw = random.randint(80, screen_height-blockHeight*4-10)

			distance = 0

			# make the wall the class Wall() just make block
			for i in range(sequenceWall):
				if i == 0  or i == sequenceWall-1:
					wall = Wall(wood, blockWidth, blockHeight, xw, yw + distance)
					wallGroup.add(wall)
				else:
					wall = Wall(cobblestone, blockWidth, blockHeight, xw, yw + distance)
					wallGroup.add(wall)

				distance += blockHeight

			last_wall = time_now

			if score > 500:
				wallFrequency = 14000

			if score > 1000:
				wallFrequency = 12000

			wallFrequency = random.randint(10000, wallFrequency)


		# randomly spawn reviveHeart
		if time_now - last_heart > heartFrequency:
			
			xrh = screen_width
			yrh = random.choice([random.randint(30, screen_height-heartHeight), random.randint(screen_height - 100, screen_height - 80)])

			reviveHeart = Heart(heart, heartWidth, heartHeight, xrh, yrh, None)

			heartGroup.add(reviveHeart)

			last_heart = time_now

			if score > 500:
				rarityHR = 10000

			if score > 1000:
				rarityHR = 15000

			heartFrequency = random.randint(20000-rarityHR, 45000-rarityHR)



	# reset the scoll if the background move full of its width
	if abs(scoll) > bg_width:
		scoll = 0

	# simply prevent minus score
	if score < 0:
		score = 0

	if score > highscore:
		highscore = score

	if deathHeart < 0:
		deathHeart = 0

	if deathHeart > 5:
		deathHeart = 5

	if deathHeart == 5:
		dragon.image = scale(dragonPain, dragon_width, dragon_height)
		game_over = True

		countDeath += 1

		# display game over scene
		if countDeath > 300 and countDeath < 700 and game_over:
			dragon.image = scale(dragonDeath, dragon_width, dragon_height)

		if countDeath > 380 and countDeath < 700 and game_over and not displayGameOver:	#dragon rotate 90
			rotateDeathDr = pygame.transform.rotate(dragonDeath, -90)
			if countDeath > 500 and game_over:
				dragon.image = scale(rotateDeathDr, dragon_width-20, dragon_height+40)
				if dragon.rect.bottom < screen_height:		# fall down and die
					dragon.rect.y += 2
					countDeath = 690
				if dragon.rect.bottom >= screen_height:
					if countStay > 100:
						countStay = 0
						displayGameOver = True
						createButton = True
						playGOSound = True
						hearts = []
						heartGroup.empty()
						wallGroup.empty()
						asteroidGroup.empty()
						drPBttGroup.empty()
					else:
						dragon.image = scale(dragonDeath, dragon_width, dragon_height)
						countDeath = 690

					countStay += 1


		if countDeath > 700 and displayGameOver and createButton:

			if playGOSound:
				gameoverSound.play()
				playGOSound = False
			
			dragon.image = scale(dragonDeath, dragon_width, dragon_height)
			bg = scale(pygame.image.load(f'{images_path}/hellbg.jpg').convert(), screen_width, screen_width)

			gameOverLabel = Button(gameOverText, gOTextW, gOTextH, (screen_width/2), (screen_height/2 - gOTextH/2)-150, None)
			buttonGroup.add(gameOverLabel)

			restartLabel = Button(restartText, stTextW, stTextH, (screen_width/2), (screen_height/2 - gOTextH/2), 'restart')
			buttonGroup.add(restartLabel)

			createButton = False


		if countDeath > 720:
			countDeath = 720

		if countDeath >= 720 and displayGameOver and not createButton:
		
			dragon.image = scale(dragonDeath, dragonIntroW, dragonIntroH)

			dragon.rect.x = screen_width/2 - dragonIntroW/2
			dragon.rect.y = screen_height/2 - dragonIntroH/2 + 160

			rText = remindText.render('press SPACE or click RESTART to play game', True, (250,250,250))
			screen.blit(rText, (screen_width/2 - 160, screen_height-45))

			buttonGroup.draw(screen)
			buttonGroup.update(dragon)

			if restartLabel.clicked:

				bg = scale(pygame.image.load(f'{images_path}/dragonBg.png').convert(), screen_width, screen_height)

				dragon.image = scale(dragonImg, dragon_width, dragon_height)
				dragon.rect.center = [200, screen_height/2 - dragon_height/2]

				score = 0

				distanceHeart = 0
				for i in range(numsHeart):
					xh = (screen_width - ((heartWidth+20)*5) + 40) + distanceHeart
					yh = 50

					heartOb = Heart(heart, heartWidth, heartHeight, xh, yh, i)
					heartGroup.add(heartOb)
					
					hearts.append(heartOb)

					distanceHeart += (heartWidth + 6)

				restartLabel.clicked = False

				buttonGroup.empty()

				fbrButton = DrSkill(fbrBt, drPowerBtWidth, drPowerBtHeight, drPBtxr, drPBtyr, 'fbr')
				fbaButton = DrSkill(fbaBt, drPowerBtWidth+28, drPowerBtHeight+28, drPBtxa, drPBtya, 'fba')
				drPBttGroup.add(fbrButton)
				drPBttGroup.add(fbaButton)

				deathHeart = 0
				countDeath = 0

				asteroidFrequency = 2000
				wallFrequency = 15000
				heartFrequency = 20000
				rarityHR = 5000

				velocityAs = 1
				velocityWall = 1

				last_asteroid = pygame.time.get_ticks()
				last_wall = pygame.time.get_ticks()
				last_heart = pygame.time.get_ticks()

				# problem: havent display heart and next game over suck?

				displayGameOver = False
				game_over = False



	wallGroup.draw(screen)
	wallGroup.update(dragon)

	asteroidGroup.draw(screen)
	asteroidGroup.update(dragon)

	dragonPower.draw(screen)
	dragonPower.update()

	dragon_group.draw(screen)
	dragon_group.update()

	scoreText = text.render(f"SCORE: {score}", True, (250,250,250))
	screen.blit(scoreText, (40, 25))

	highscoreText = text.render(f"HIGHSCORE: {highscore}", True, (250, 250, 250))
	screen.blit(highscoreText, (200 + 10*len(str(score)), 25))

	heartGroup.draw(screen)
	heartGroup.update(dragon)

	drPBttGroup.draw(screen)
	drPBttGroup.update()

	if not game_over:
		displayNumfbr = dPowerText.render(f'BLL: {fbrButton.countTimes}	LM: {fbrButton.standard}', True, (250, 250, 250))
		screen.blit(displayNumfbr, (fbrButton.rect.x + 12, fbrButton.rect.y - 25))
		displayNumfba = dPowerText.render(f'BLL: {fbaButton.countTimes}	LM: {fbaButton.standard}', True, (250, 250, 250))
		screen.blit(displayNumfba, (fbaButton.rect.x + 23, fbaButton.rect.y - 12))

		if fbrButton.render:	# will be activate when the dragon use all power times
			powerRenderfbr = powerText.render(str(8 - int(float(str(fbrButton.time_now - fbrButton.last_stop)[:-3]+'.0'))), True, (250,250,250))	# dont ask me why the 1st arg is awkward
			screen.blit(powerRenderfbr, (fbrButton.rect.x+38, fbrButton.rect.y+22))

		if fbaButton.render:
			powerRenderfba = powerText.render(str(12 - int(float(str(fbaButton.time_now - fbaButton.last_stop)[:-3]+'.0'))), True, (250,250,250))
			if len(str(12 - int(float(str(fbaButton.time_now - fbaButton.last_stop)[:-3]+'.0')))) <= 1:
				split = (len(str(12 - int(float(str(fbaButton.time_now - fbaButton.last_stop)[:-3]+'.0')))))*12		# this section prevent the text from awkward
			else:
				split = 0
			screen.blit(powerRenderfba, (fbaButton.rect.x+40+split, fbaButton.rect.y+36))

	pygame.display.update()


with open("dragonhighscore.txt", "w") as f:
	f.write(str(highscore))


pygame.quit()
