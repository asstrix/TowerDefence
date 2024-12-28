import pygame
from pygame.math import Vector2


class Bullet(pygame.sprite.Sprite):
    """
    Represents a bullet fired by a tower.
    Bullets travel towards a target enemy, deal damage on impact, and are removed
    if they reach the target or leave the screen boundaries.
    """
    def __init__(self, start_pos, target_pos, damage, game, tower=None):
        """
        Initialize a Bullet instance.
        Args:
            start_pos (tuple): The starting position of the bullet (x, y).
            target_pos (tuple): The position of the target enemy (x, y).
            damage (int): The amount of damage the bullet deals on impact.
            game: Reference to the main game instance.
            tower (Tower, optional): The tower that fired the bullet. Defaults to None.
        Attributes:
            position (Vector2): Current position of the bullet.
            target (Vector2): Position of the target enemy.
            speed (float): Speed of the bullet.
            damage (int): Damage dealt by the bullet.
            velocity (Vector2): Direction and speed of the bullet's movement.
            tower (Tower): Reference to the tower that fired the bullet.
        """
        super().__init__()
        self.game = game
        self.image = pygame.image.load('assets/bullets/basic_bullet.png').convert_alpha()
        self.rect = self.image.get_rect(center=start_pos)
        self.position = Vector2(start_pos)
        self.target = Vector2(target_pos)
        self.speed = 5
        self.damage = damage
        self.velocity = self.calculate_velocity()
        self.tower = tower

    def calculate_velocity(self):
        """
        Calculate the velocity vector for the bullet.
        Determines the direction and speed of the bullet based on its target.
        Returns:
            Vector2: The velocity vector for the bullet.
        """
        direction = (self.target - self.position).normalize()
        velocity = direction * self.speed
        return velocity

    def update(self):
        """
        Update the bullet's position and check for collisions or out-of-bounds conditions.
        Moves the bullet along its velocity vector. Removes the bullet if it is
        close to its target or exits the screen boundaries.
        """
        self.position += self.velocity
        self.rect.center = self.position
        if self.position.distance_to(self.target) < 10 or not self.game.is_position_inside(self.position):
            self.kill()

    def is_position_inside(self, pos):
        """
        Check if a given position is inside the screen boundaries.
        Args:
            pos (Vector2): The position to check.
        Returns:
            bool: True if the position is inside the screen, False otherwise.
        """
        return 0 <= pos.x <= self.game.settings.screen_width and 0 <= pos.y <= self.game.settings.screen_height
