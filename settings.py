class Settings:
    def __init__(self):
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
