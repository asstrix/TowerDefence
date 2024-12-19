import pygame
from pygame.math import Vector2


class Enemy(pygame.sprite.Sprite):
	def __init__(self, path, speed=2, health=10, image_path=None, game=None):

		super().__init__()
		self.image = pygame.Surface((30, 40))
		self.image = pygame.image.load(image_path).convert_alpha()
		self.rect = self.image.get_rect()
		self.game = game
		self.path = path
		self.path_index = 0
		self.speed = speed
		self.health = health
		self.position = Vector2(path[0])
		self.rect.center = self.position
		self.health_indicator = pygame.Rect(self.position[0] - self.health // 2, self.position[1] - 30 - 20, self.health, 10)

	def take_damage(self, amount, speed=0):
		self.health -= amount
		if self.health <= 0:
			self.kill()
			self.game.settings.starting_money += 20

	def update(self):
		if self.path_index < len(self.path) - 1:
			start_point = Vector2(self.path[self.path_index])
			end_point = Vector2(self.path[self.path_index + 1])
			direction = (end_point - start_point).normalize()

			self.position += direction * self.speed
			self.rect.center = self.position

			if self.position.distance_to(end_point) < self.speed:
				self.path_index += 1

			if self.path_index >= len(self.path) - 1:
				self.game.game_over()
				self.kill()

