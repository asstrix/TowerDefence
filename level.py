import pygame
from random import choice, choices
from enemy import Enemy
from tower import BasicTower, SniperTower, FreezingTower


class Level:
    """
    Represents a game level, managing enemies, towers, bullets, and waves.
    This class handles spawning enemies, placing towers, managing bullets,
    and updating the state of the game level during gameplay.
    """
    def __init__(self, game):
        """
        Initialize the level.
        Args:
            game: Reference to the main game instance.
        Attributes:
            enemies (pygame.sprite.Group): Group containing all enemies in the level.
            towers (pygame.sprite.Group): Group containing all towers in the level.
            bullets (pygame.sprite.Group): Group containing all bullets in the level.
            enemy (list): List of enemy templates with their attributes.
            waves (list): List of waves, each containing enemy instances with paths.
            current_wave (int): Index of the current wave.
            spawned_enemies (int): Number of enemies spawned in the current wave.
            spawn_delay (int): Time delay between spawning enemies in milliseconds.
            last_spawn_time (int): Time when the last enemy was spawned.
            all_waves_complete (bool): Indicates if all waves are completed.
            font (pygame.font.Font): Font used for rendering tower stats.
        """
        self.game = game
        self.enemies = pygame.sprite.Group()
        self.towers = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemy = [
            {'speed': 1, 'health': 100, 'image_path': 'assets/enemies/basic_enemy.png'},
            {'speed': 1.5, 'health': 150, 'image_path': 'assets/enemies/fast_enemy.png'},
            {'speed': 0.75, 'health': 200, 'image_path': 'assets/enemies/strong_enemy.png'},
            {'speed': 0.65, 'health': 250, 'image_path': 'assets/enemies/strong_enemy.png'},
        ]
        self.waves = [
            [{'path': path, **enemy} for path in [choice(self.game.settings.enemy_path)] for enemy in
             choices(self.enemy, weights=[3, 2, 0, 0], k=5)],
            [{'path': path, **enemy} for path in [choice(self.game.settings.enemy_path)] for enemy in
             choices(self.enemy, weights=[2, 2, 1, 0], k=7)],
            [{'path': path, **enemy} for path in [choice(self.game.settings.enemy_path)] for enemy in
             choices(self.enemy, weights=[1, 1, 1, 1], k=4)],
            [{'path': path, **enemy} for path in [choice(self.game.settings.enemy_path)] for enemy in
             choices(self.enemy, weights=[0, 1, 2, 2], k=5)],
            [{'path': path, **enemy} for path in [choice(self.game.settings.enemy_path)] for enemy in
             choices(self.enemy, weights=[0, 2, 2, 2], k=6)],
            [{'path': path, **enemy} for path in [choice(self.game.settings.enemy_path)] for enemy in
             choices(self.enemy, weights=[0, 1, 3, 2], k=7)],
            [{'path': path, **enemy} for path in [choice(self.game.settings.enemy_path)] for enemy in
             choices(self.enemy, weights=[0, 1, 2, 3], k=6)],
            [{'path': path, **enemy} for path in [choice(self.game.settings.enemy_path)] for enemy in
             choices(self.enemy, weights=[0, 0, 4, 2], k=6)],
            [{'path': path, **enemy} for path in [choice(self.game.settings.enemy_path)] for enemy in
             choices(self.enemy, weights=[0, 0, 3, 3], k=6)]
        ]
        self.current_wave = 0
        self.spawned_enemies = 0
        self.spawn_delay = 1000
        self.last_spawn_time = pygame.time.get_ticks()
        self.all_waves_complete = False
        self.start_next_wave()
        self.font = pygame.font.SysFont("Arial", 24)

    def start_next_wave(self):
        """
        Start the next wave of enemies.
        Resets the enemy spawn counter and begins spawning enemies for the next wave.
        """
        if self.current_wave < len(self.waves):
            self.spawned_enemies = 0
            self.spawn_next_enemy()

    def spawn_next_enemy(self):
        """
        Spawn the next enemy in the current wave.
        Retrieves enemy data from the current wave and adds the enemy to the game.
        Plays a sound effect when an enemy spawns.
        """
        if self.spawned_enemies < len(self.waves[self.current_wave]):
            enemy_info = self.waves[self.current_wave][self.spawned_enemies]
            new_enemy = Enemy(**enemy_info, game=self.game)
            self.enemies.add(new_enemy)
            self.spawned_enemies += 1
            pygame.mixer.Sound(self.game.settings.enemy_appear).play()

    def attempt_place_tower(self, mouse_pos, tower_type):
        """
        Attempt to place a tower at the given position.
        Checks if the player has enough money and the spot is available. Deducts the
        tower cost if placement is successful.
        Args:
            mouse_pos (tuple): The position of the mouse click.
            tower_type (str): The type of tower to place (e.g., 'basic', 'sniper', 'freezer').
        """
        tower_classes = {'basic': BasicTower, 'sniper': SniperTower, 'freezer': FreezingTower}
        if tower_type in tower_classes and self.game.settings.starting_money >= self.game.settings.tower_cost:
            grid_pos = self.game.grid.get_grid_position(mouse_pos)
            if self.game.grid.is_spot_available(grid_pos):
                self.game.grid.available_spots.remove(grid_pos)
                self.game.settings.starting_money -= self.game.settings.tower_cost
                new_tower = tower_classes[tower_type](grid_pos, self.game)
                self.towers.add(new_tower)
                print("Tower placed.")
            else:
                print("Invalid position for tower.")
        else:
            print("Not enough money or unknown tower type.")

    def update(self):
        """
        Update the state of the level.
        Spawns enemies, updates positions of enemies and bullets, handles collisions,
        and checks for wave completion.
        """
        current_time = pygame.time.get_ticks()

        if self.current_wave < len(self.waves) and self.spawned_enemies < len(self.waves[self.current_wave]):
            if current_time - self.last_spawn_time > self.spawn_delay:
                enemy_info = self.waves[self.current_wave][self.spawned_enemies].copy()
                enemy_info['game'] = self.game
                new_enemy = Enemy(**enemy_info)
                self.enemies.add(new_enemy)
                self.spawned_enemies += 1
                self.last_spawn_time = current_time

        collisions = pygame.sprite.groupcollide(self.bullets, self.enemies, True, False)
        for bullet in collisions:
            for enemy in collisions[bullet]:
                enemy.take_damage(bullet.damage)

        self.enemies.update()
        for tower in self.towers:
            tower.update(self.enemies, current_time, self.bullets)
        self.bullets.update()

        if len(self.enemies) == 0 and self.current_wave < len(self.waves) - 1:
            self.current_wave += 1
            self.start_next_wave()
        elif len(self.enemies) == 0 and self.current_wave == len(self.waves) - 1:
            self.all_waves_complete = True

    def draw_path(self, screen):
        """
        Draw the enemy paths and tower positions.
        Args:
            screen: The game screen to draw on.
        """
        for i in self.game.settings.enemy_path:
            pygame.draw.lines(screen, (0, 128, 0), False, i, 5)
        for pos in self.game.settings.tower_positions:
            pygame.draw.circle(screen, (128, 0, 0), pos, 10)

    def draw(self, screen):
        """
        Render the level on the screen.
        This includes enemy paths, enemies, towers, bullets, and stats.
        Args:
            screen: The game screen to draw on.
        """
        self.draw_path(screen)
        self.enemies.draw(screen)
        for enemy in self.enemies:
            enemy.draw_health_indicator(screen)
        self.towers.draw(screen)
        for bullet in self.bullets:
            if not isinstance(bullet.tower, FreezingTower):
                screen.blit(bullet.image, bullet.rect)
        mouse_pos = pygame.mouse.get_pos()
        for tower in self.towers:
            tower.draw(screen)
            if tower.is_hovered(mouse_pos):
                tower_stats_text = self.font.render(f"Damage: {round(tower.damage)}, Range: {tower.tower_range}", True,
                                                    (255, 255, 255))
                screen.blit(tower_stats_text, (tower.rect.x, tower.rect.y - 20))