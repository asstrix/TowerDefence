import pygame
from pygame.math import Vector2


class Enemy(pygame.sprite.Sprite):
	"""
	Represents an enemy in the game.
	Enemies follow a predefined path, take damage from towers, and have a health
	indicator. They can be slowed by Freezing Towers and contribute money to the
	player when defeated.
	"""
	def __init__(self, path, speed=2, health=10, image_path=None, game=None):
		"""
		Initialize an Enemy instance.
		Args:
			path (list): List of points representing the enemy's path.
			speed (float, optional): The speed of the enemy. Defaults to 2.
			health (int, optional): The initial health of the enemy. Defaults to 10.
			image_path (str, optional): Path to the image file for the enemy. Defaults to None.
			game: Reference to the main game instance.
		"""
		super().__init__()
		self.image = pygame.Surface((30, 40))
		self.image = pygame.image.load(image_path).convert_alpha()
		self.rect = self.image.get_rect()
		self.game = game
		self.path = path
		self.path_index = 0
		self.speed = speed
		self.default_speed = speed
		self.health = health
		self.max_health = health
		self.position = Vector2(path[0])
		self.rect.center = self.position
		self.health_indicator = pygame.Rect(self.position[0], self.position[1], 30, 5)

	def take_damage(self, amount):
		"""
		Reduce the enemy's health by the given amount.
		If the enemy's health drops to 0 or below, it is removed from the game,
		and the player gains money.
		Args:
			amount (int): The amount of damage to apply.
		"""
		self.health -= amount
		self.health_indicator.width = int(30 * (self.health / self.max_health))
		if self.health <= 0:
			self.kill()
			self.game.settings.starting_money += 20

	def update(self):
		"""
		Update the enemy's position and state.
		The enemy moves along its path, and its speed is adjusted if it is within
		the range of a Freezing Tower. If the enemy reaches the end of the path,
		it triggers the game-over condition.
		"""
		freezing_range = False
		for tower in self.game.level.towers:
			if tower.__class__.__name__ == "FreezingTower":
				distance_to_tower = self.position.distance_to(Vector2(tower.rect.center))
				if distance_to_tower <= tower.tower_range:
					freezing_range = True
					break
		if freezing_range:
			self.speed = self.default_speed - 0.2
		else:
			self.speed = self.default_speed

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
		"""
		Draw the enemy's health indicator on the screen.
		Args:
			screen: The game screen to draw on.
		"""
		pygame.draw.rect(screen, (0, 255, 0), self.health_indicator)
