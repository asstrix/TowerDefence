import pygame


class Grid:
    """
    Represents the game grid, where towers can be placed.
    This class manages the grid's available spots, handles placing and removing towers,
    and provides utility methods for interacting with the grid.
    """
    def __init__(self, game):
        """
        Initialize the Grid.
        Args:
            game: Reference to the main game instance.
        Attributes:
            settings: Reference to the game's settings.
            screen: Reference to the game's screen.
            available_spots (list): List of positions where towers can be placed.
            towers (list): List of towers currently placed on the grid.
        """
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.available_spots = self.settings.tower_positions
        self.towers = []

    def update(self):
        """
        Update the grid state.
        Currently, this method does nothing but can be extended for future functionality.
        """
        pass

    def draw(self):
        """
        Draw the available tower spots on the screen.
        Available spots are displayed as circles.
        """
        for spot in self.available_spots:
            pygame.draw.circle(self.screen, (255, 255, 0), spot, 15, 2)

    def place_tower(self, tower=None):
        """
        Attempt to place a tower on the grid.
        Checks if the position is available and not overlapping with an existing tower.
        Args:
            tower: The tower object to be placed.
        Returns:
            bool: True if the tower was successfully placed, False otherwise.
        """
        grid_pos = self.get_grid_position(tower.position)
        if grid_pos in self.available_spots and not any(tower.rect.collidepoint(grid_pos) for tower in self.towers):
            self.towers.append(tower)
            return True
        return False

    def remove_tower(self, tower):
        """
        Remove a tower from the grid.
        Args:
            tower: The tower object to be removed.
        """
        if tower in self.towers:
            self.towers.remove(tower)

    def get_grid_position(self, mouse_pos):
        """
        Get the grid position based on the mouse position.
        Converts the mouse coordinates into the center of the nearest grid cell.
        Args:
            mouse_pos (tuple): Mouse coordinates (x, y).
        Returns:
            tuple: The center coordinates of the nearest grid cell.
        """
        grid_x = mouse_pos[0] // 64 * 64 + 32
        grid_y = mouse_pos[1] // 64 * 64 + 32
        return grid_x, grid_y

    def is_spot_available(self, grid_pos):
        """
        Check if a grid position is available for placing a tower.
        Args:
            grid_pos (tuple): The grid position to check.
        Returns:
            bool: True if the position is available, False otherwise.
        """
        return grid_pos in self.available_spots and all(not tower.rect.collidepoint(grid_pos) for tower in self.towers)
