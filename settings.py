class Settings:
    """
    Represents the settings for the Tower Defense Game.
    This class stores configuration values such as screen dimensions, grid settings,
    tower costs, enemy paths, sprite assets, and game sounds.
    """
    def __init__(self):
        """
        Initialize the game's settings.
        Attributes:
            screen_width (int): Width of the game screen in pixels.
            screen_height (int): Height of the game screen in pixels.
            bg_color (tuple): Background color of the screen (RGB format).
            rows (int): Number of rows in the grid.
            cols (int): Number of columns in the grid.
            grid_size (tuple): Size of each grid cell (width, height).
            tower_cost (int): Cost to place a new tower.
            tower_upgrade_cost (int): Cost to upgrade a tower.
            tower_sell_percentage (float): Percentage of the original cost received when selling a tower.
            enemy_path (list): Predefined paths for enemies to follow. Each path is a list of (x, y) coordinates.
            enemy_health_indicator (dict): Settings for enemy health indicators, including:
                - 'colors' (list): Colors for the health bar (start and background).
                - 'width' (int): Width of the health bar in pixels.
                - 'height' (int): Height of the health bar in pixels.
            tower_sprites (dict): Dictionary mapping tower types to their sprite file paths.
            enemy_sprite (str): File path for the default enemy sprite.
            bullet_sprite (str): File path for the bullet sprite.
            background_image (str): File path for the background image.
            shoot_sound (str): File path for the sound played when a tower shoots.
            upgrade_sound (str): File path for the sound played when a tower is upgraded.
            sell_sound (str): File path for the sound played when a tower is sold.
            enemy_hit_sound (str): File path for the sound played when an enemy is hit.
            enemy_appear (str): File path for the sound played when an enemy spawns.
            background_music (str): File path for the background music.
            starting_money (int): Initial amount of money available to the player.
            lives (int): Number of lives the player starts with.
            tower_positions (list): List of available positions for placing towers, calculated
                based on the grid size and grid dimensions.
        """
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        self.rows = 10
        self.cols = 15
        self.grid_size = (64, 64)

        self.tower_cost = 100
        self.tower_upgrade_cost = 150
        self.tower_sell_percentage = 0.75

        self.enemy_path = [
            [
                (50, 380), (320, 380), (320, 190), (580, 190),
                (580, 580), (900, 580), (900, 320), (1150, 320)
            ],
            [
                (50, 260), (190, 260), (190, 320), (450, 320),
                (450, 510), (700, 510), (700, 320), (1150, 320)
            ],
            [
                (50, 575), (510, 575), (510, 255), (900, 255), (900, 320), (1150, 320)
            ]
        ]
        self.enemy_health_indicator = {'colors': [(0, 255, 0), (255, 255, 255)], 'width': 100, 'height': 10}

        self.tower_sprites = {
            'basic': 'assets/towers/basic_tower.png',
            'sniper': 'assets/towers/sniper_tower.png',
            'freezer': 'assets/towers/freezing_tower.png',
        }
        self.enemy_sprite = 'assets/enemies/basic_enemy.png'
        self.bullet_sprite = 'assets/bullets/basic_bullet.png'
        self.background_image = 'assets/backgrounds/game_background.png'

        self.shoot_sound = 'assets/sounds/shoot.wav'
        self.upgrade_sound = 'assets/sounds/upgrade.wav'
        self.sell_sound = 'assets/sounds/sell.wav'
        self.enemy_hit_sound = 'assets/sounds/enemy_hit.wav'
        self.enemy_appear = 'assets/sounds/enemy_appear.wav'
        self.background_music = 'assets/sounds/background_music.mp3'

        self.starting_money = 500
        self.lives = 20

        self.tower_positions = [(x * self.grid_size[0] + self.grid_size[0] // 2, y * self.grid_size[1] + self.grid_size[1] // 2)
                                for x in range(1, self.cols) for y in range(3, self.rows)]
