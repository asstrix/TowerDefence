import pygame
from bullet import Bullet
import math


class Tower(pygame.sprite.Sprite):
    """
    Base class for all tower types in the game.
    Towers can attack enemies, be upgraded, and display their information.
    """
    def __init__(self, position, game):
        super().__init__()
        self.position = pygame.math.Vector2(position)
        self.game = game

        self.image = None
        self.rect = None
        self.tower_range = 0
        self.damage = 0
        self.rate_of_fire = 0
        self.last_shot_time = pygame.time.get_ticks()
        self.level = 1
        self.original_image = self.image
        self.upgrade_arrow_rect = None

    def upgrade_cost(self):
        return 50 * self.level

    def draw(self, screen):
        """
        Draw the tower on the screen, including upgrade options.
        Args:
            screen: The game screen to draw on.
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.is_hovered(mouse_pos):
            level_text = self.game.font.render(f"Level: {self.level}", True, (255, 255, 255))
            upgrade_cost_text = self.game.font.render(f"Upgrade: ${self.upgrade_cost()  }", True, (255, 255, 255))

            level_text_pos = (self.position.x, self.position.y + 20)
            upgrade_cost_pos = (self.position.x, self.position.y + 40)

            screen.blit(level_text, level_text_pos)
            screen.blit(upgrade_cost_text, upgrade_cost_pos)
        if self.game.settings.starting_money > self.upgrade_cost() and self.level < 2:
            upgrade_arrow_img = pygame.image.load('assets/towers/level_up.png').convert_alpha()
            self.upgrade_arrow_rect = upgrade_arrow_img.get_rect(center=(self.position.x + 30, self.position.y - 30))
            screen.blit(upgrade_arrow_img, self.upgrade_arrow_rect)

    def update(self, enemies, current_time, bullets_group):
        """
        Update the tower's state, including attacking enemies.
        Args:
            enemies (list): List of enemies on the field.
            current_time (int): Current game time in milliseconds.
            bullets_group (pygame.sprite.Group): Group to add bullets to.
        """
        if current_time - self.last_shot_time > self.rate_of_fire:
            target = self.find_target(enemies)
            if target:
                if not isinstance(self, FreezingTower):
                    self.rotate_towards_target(target)
                    pygame.mixer.Sound(self.game.settings.shoot_sound).play()
                self.shoot(target, bullets_group)
                self.last_shot_time = current_time

    def is_hovered(self, mouse_pos):
        """
        Check if the tower is being hovered over by the mouse.
        Args:
            mouse_pos (tuple): Current position of the mouse.
        Returns:
            bool: True if the mouse is hovering over the tower, False otherwise.
        """
        return self.rect.collidepoint(mouse_pos)

    def shoot(self, target, bullets_group):
        """
        Shoot a bullet at a target enemy.
        This method is meant to be overridden by subclasses.
        Args:
            target: The enemy being targeted.
            bullets_group (pygame.sprite.Group): Group to add bullets to.
        """
        pass

    def rotate_towards_target(self, target):
        """
        Rotate the tower's image to face the target.
        Args:
            target: The enemy being targeted.
        """
        dx = target.position.x - self.position.x
        dy = target.position.y - self.position.y
        # Вычисляем угол в радианах
        angle_rad = math.atan2(dy, dx)
        # Преобразуем радианы в градусы
        angle_deg = math.degrees(angle_rad)
        angle_deg = -angle_deg - 90
        self.image = pygame.transform.rotate(self.original_image, angle_deg)
        self.rect = self.image.get_rect(center=self.position)

    def find_target(self, enemies):
        """
        Find the nearest enemy within the tower's range.
        Args:
            enemies (list): List of enemies on the field.
        Returns:
            Enemy: The closest enemy within range, or None if no enemy is found.
        """
        nearest_enemy = None
        min_distance = float('inf')
        for enemy in enemies:
            distance = self.position.distance_to(enemy.position)
            if distance < min_distance and distance <= self.tower_range:
                nearest_enemy = enemy
                min_distance = distance
        return nearest_enemy

    def upgrade(self, tower):
        """
        Upgrade the tower, increasing its level and improving stats.
        Args:
            tower (Tower): The tower to be upgraded.
        """
        self.level += 1
        self.game.settings.starting_money -= self.upgrade_cost()
        if isinstance(tower, (BasicTower, SniperTower, FreezingTower)):
            tower.damage *= 1.2
            tower.rate_of_fire *= 0.8
        if isinstance(tower, BasicTower):
            tower.image = pygame.image.load('assets/towers/basic_tower2.png').convert_alpha()
            tower.original_image = tower.image
        if isinstance(tower, SniperTower):
            tower.image = pygame.image.load('assets/towers/sniper_tower2.png').convert_alpha()
            tower.original_image = tower.image
        if isinstance(tower, FreezingTower):
            tower.tower_range *= 1.2


class BasicTower(Tower):
    """
    Basic tower with moderate range and damage.
    """
    def __init__(self, position, game):
        """
        Initialize a Basic Tower.
        Args:
            position (tuple): The (x, y) position of the tower on the grid.
            game: Reference to the main game instance.
        """
        super().__init__(position, game)
        self.image = pygame.image.load('assets/towers/basic_tower.png').convert_alpha()
        self.original_image = self.image
        self.rect = self.image.get_rect(center=self.position)
        self.tower_range = 150
        self.damage = 20
        self.rate_of_fire = 1000

    def shoot(self, target, bullets_group):
        """
       Shoot a bullet at a target enemy.
       Args:
           target: The enemy being targeted.
           bullets_group (pygame.sprite.Group): Group to add bullets to.
       """
        new_bullet = Bullet(self.position, target.position, self.damage, self.game)
        bullets_group.add(new_bullet)


class SniperTower(Tower):
    """
    Long-range tower with high damage, targeting the healthiest enemy.
    """
    def __init__(self, position, game):
        """
        Initialize a Sniper Tower.
        Args:
            position (tuple): The (x, y) position of the tower on the grid.
            game: Reference to the main game instance.
        """
        super().__init__(position, game)
        self.image = pygame.image.load('assets/towers/sniper_tower.png').convert_alpha()
        self.image = pygame.transform.rotate(self.image, 90)
        self.original_image = self.image
        self.rect = self.image.get_rect(center=self.position)
        self.tower_range = 300
        self.damage = 40
        self.rate_of_fire = 2000

    def find_target(self, enemies):
        """
        Find the healthiest enemy within the tower's range.
        Args:
            enemies (list): List of enemies on the field.
        Returns:
            Enemy: The healthiest enemy within range, or None if no enemy is found.
        """
        healthiest_enemy = None
        max_health = 0
        for enemy in enemies:
            if self.position.distance_to(enemy.position) <= self.tower_range and enemy.health > max_health:
                healthiest_enemy = enemy
                max_health = enemy.health
        return healthiest_enemy

    def shoot(self, target, bullets_group):
        """
       Shoot a bullet at a target enemy.
       Args:
           target: The enemy being targeted.
           bullets_group (pygame.sprite.Group): Group to add bullets to.
       """
        new_bullet = Bullet(self.position, target.position, self.damage, self.game)
        bullets_group.add(new_bullet)


class FreezingTower(Tower):
    """
    Tower that slows enemies instead of dealing high damage.
    """
    def __init__(self, position, game):
        """
        Initialize a Freezing Tower.
        Args:
            position (tuple): The (x, y) position of the tower on the grid.
            game: Reference to the main game instance.
        """
        super().__init__(position, game)
        self.image = pygame.image.load('assets/towers/freezing_tower.png').convert_alpha()
        self.original_image = self.image
        self.rect = self.image.get_rect(center=self.position)
        self.tower_range = 50
        self.damage = 5
        self.rate_of_fire = 2000

    def shoot(self, target, bullets_group):
        """
        Shoot a freezing bullet at a target enemy.
        Args:
            target: The enemy being targeted.
            bullets_group (pygame.sprite.Group): Group to add bullets to.
        """
        new_bullet = Bullet(self.position, target.position, self.damage, self.game, tower=self)
        bullets_group.add(new_bullet)

