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
		self.max_health = health
		self.position = Vector2(path[0])
		self.rect.center = self.position
		self.health_indicator = pygame.Rect(self.position[0], self.position[1], 30, 5)

	def take_damage(self, amount, speed=0):
		self.health -= amount
		self.health_indicator.width = int(30 * (self.health / self.max_health))
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

		self.health_indicator.x = self.position[0] - 15
		self.health_indicator.y = self.position[1] - 20

	def draw_health_indicator(self, screen):
		pygame.draw.rect(screen, (0, 255, 0), self.health_indicator)
