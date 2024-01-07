from settings import *
import pygame

# Player
class Plane:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.vel = 5
		self.img = PLANE
		self.mask = pygame.mask.from_surface(self.img)
		self.lives = 3
		self.score = 0

	def draw(self):
		win.blit(self.img, (self.x, self.y))

		for i in range(self.lives):
			win.blit(HEART, (30 + HEART.get_width() * 1.1 * i, 10))

		score = huge_font.render(f"Score: {self.score}", 1, WHITE)
		win.blit(score, (WIDTH - score.get_width() * 1, 10))

	# Move based on user input
	def move(self):
		keys = pygame.key.get_pressed()
		hor = 0
		ver = 0

		if keys[pygame.K_LEFT]:
			hor -= self.vel
		if keys[pygame.K_RIGHT]:
			hor += self.vel
		if keys[pygame.K_UP]:
			ver -= self.vel
		if keys[pygame.K_DOWN]:
			ver += self.vel

		self.x += hor
		self.y += ver

		if self.x < 0:
			self.x = 0
		elif self.x > WIDTH - self.img.get_width():
			self.x = WIDTH - self.img.get_width()
		if self.y < 0:
			self.y = 0
		elif self.y > HEIGHT - self.img.get_height():
			self.y = HEIGHT - self.img.get_height()

	def collision(self, mask, x, y):
		offset = (x - self.x, y - self.y)
		if self.mask.overlap(mask, offset):
			return True
		return False

# Missile class
class Missile:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.img = MISSILE
		self.mask = pygame.mask.from_surface(self.img)
		self.vel = 10

	def draw(self):
		win.blit(self.img, (self.x, self.y))

	# move to the left
	def move(self):
		self.x -= self.vel

	def off_screen(self):
		if self.x < 0 - self.img.get_width():
			return True
		return False