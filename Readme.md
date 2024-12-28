# Tower Defense Game

A Python-based Tower Defense game built with the **Pygame** library. This game challenges players to strategically place towers on a grid to stop waves of enemies from reaching their destination.

## Table of Contents

- [Features](#features)
- [Game Mechanics](#game-mechanics)
- [Installation](#installation)
- [How to Play](#how-to-play)
- [Folder Structure](#folder-structure)
- [Screenshots](#screenshots)

---

## Features

- **Tower Types**: 
  - Basic Tower: Moderate range and damage.
  - Sniper Tower: Long range, high damage.
  - Freezing Tower: Slows enemies in range.

- **Enemy Waves**:
  - Multiple enemy types with varying speeds, health, and damage resistances.
  - Enemies follow predefined paths.

- **Upgrades and Strategy**:
  - Towers can be upgraded to increase damage, range, or other attributes.
  - Players earn money by defeating enemies, which can be used to place or upgrade towers.

- **Dynamic Gameplay**:
  - Real-time enemy movement and collision detection.
  - Health bars for enemies, bullet tracking, and more.

---

## Game Mechanics

1. **Grid System**:
   - The game uses a grid-based layout for tower placement.
   - Towers can only be placed in available spots.

2. **Enemy Movement**:
   - Enemies move along predefined paths.
   - If an enemy reaches the end of the path, the player loses lives.

3. **Bullets**:
   - Towers shoot bullets that deal damage to enemies.
   - Bullets are removed after hitting a target or leaving the screen.

4. **Winning and Losing**:
   - Win: Survive all waves of enemies.
   - Lose: Lives reach zero.

---

## Installation

### Requirements

- Python 3.8 or higher
- Pygame library

### Steps

1. Clone this repository:
    ```bash
    git clone https://github.com/your_username/tower-defense-game.git
    cd tower-defense-game
    ```

2. Install required dependencies:
    ```bash
    pip install pygame
    ```

3. Run the game:
    ```bash
    python main.py
    ```

---

## How to Play

1. Start the game and choose a tower type using the keys:
    - `1`: Basic Tower
    - `2`: Sniper Tower
    - `3`: Freezing Tower

2. Place a tower by **right-clicking** on the grid. Ensure you have enough money and are placing the tower on a valid spot.

3. Upgrade towers by **left-clicking** on the upgrade arrow above the tower. Upgrades improve tower attributes like damage and rate of fire.

4. Defend against waves of enemies:
    - Earn money for each enemy defeated.
    - Prevent enemies from reaching the end of the path to avoid losing lives.

5. Win by defeating all waves of enemies or lose if lives reach zero.

---

## Folder Structure
```
tower-defense-game/ 
│ ├── assets/ 
│ ├── backgrounds/ 
│ ├── bullets/ 
│ ├── enemies/ 
│ ├── sounds/ 
│ ├── towers/ 
├── main.py # Entry point of the game 
├── settings.py # Contains game configuration and settings 
├── level.py # Handles game levels and enemy waves 
├── grid.py # Manages the grid and tower placements 
├── tower.py # Contains tower classes and logic 
├── enemy.py # Contains enemy logic and movement 
└── bullet.py # Handles bullet movement and behavior
```
## ScreenShots