"""
Simple Dungeon Crawler Game
A turn-based ASCII roguelike adventure with Pygame
"""

import pygame
import sys
import random

# Game constants
TILE_SIZE = 24  # Size of each tile in pixels (1 tile = 1 meter in game world)
FONT_SIZE = 18
PLAYER_SIZE = 20  # Size of player circle/sprite in pixels
BATTLE_PANEL_WIDTH = 500  # Width of the battle UI panel

# Available resolutions
RESOLUTIONS = {
    '1920x1080': (1920, 1080),
    '1600x900': (1600, 900),
    '1366x768': (1366, 768),
    '1280x720': (1280, 720),
    '1024x768': (1024, 768),
}

# Default settings
DEFAULT_RESOLUTION = '1920x1080'

# World scale: 1 tile = 1 meter
# This means a 40x20 dungeon is 40m x 20m in the game world

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (50, 50, 50)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
BLUE = (100, 150, 255)
CYAN = (0, 255, 255)
PURPLE = (200, 100, 255)

# Tile types
FLOOR = '.'
WALL = '#'
PLAYER = '@'

class SpriteGenerator:
    """Generates pixel art sprites procedurally"""
    @staticmethod
    def create_sprite(width, height, pixel_data, colors):
        """Create a sprite surface from pixel data"""
        sprite = pygame.Surface((width, height))
        sprite.set_colorkey(BLACK)  # Make black transparent
        sprite.fill(BLACK)

        for y, row in enumerate(pixel_data):
            for x, pixel in enumerate(row):
                if pixel > 0:
                    sprite.set_at((x, y), colors[pixel - 1])

        return sprite

    @staticmethod
    def create_player_sprite():
        """Create player sprite - simple adventurer"""
        # 16x16 pixel sprite
        # 0 = transparent, 1 = skin, 2 = hair, 3 = clothes, 4 = armor
        pixel_data = [
            [0,0,0,0,2,2,2,2,2,2,2,2,0,0,0,0],
            [0,0,0,2,2,2,2,2,2,2,2,2,2,0,0,0],
            [0,0,2,1,1,1,2,2,2,2,1,1,1,2,0,0],
            [0,0,1,1,1,1,1,2,2,1,1,1,1,1,0,0],
            [0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
            [0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0],
            [0,0,0,0,3,3,3,3,3,3,3,3,0,0,0,0],
            [0,0,0,3,3,4,3,3,3,3,4,3,3,0,0,0],
            [0,0,0,3,3,3,3,3,3,3,3,3,3,0,0,0],
            [0,0,3,3,3,3,3,3,3,3,3,3,3,3,0,0],
            [0,0,3,3,3,3,3,3,3,3,3,3,3,3,0,0],
            [0,0,0,3,3,3,3,3,3,3,3,3,3,0,0,0],
            [0,0,0,1,1,3,3,3,3,3,3,1,1,0,0,0],
            [0,0,0,1,1,3,3,0,0,3,3,1,1,0,0,0],
            [0,0,0,3,3,3,0,0,0,0,3,3,3,0,0,0],
            [0,0,0,3,3,0,0,0,0,0,0,3,3,0,0,0],
        ]
        colors = [(245, 220, 180), (101, 67, 33), (100, 200, 100), (150, 150, 150)]
        return SpriteGenerator.create_sprite(16, 16, pixel_data, colors)

    @staticmethod
    def create_goblin_sprite():
        """Create goblin enemy sprite"""
        pixel_data = [
            [0,0,0,0,0,2,2,2,2,2,2,0,0,0,0,0],
            [0,0,0,0,2,2,2,2,2,2,2,2,0,0,0,0],
            [0,0,0,2,1,1,2,2,2,2,1,1,2,0,0,0],
            [0,0,2,1,3,1,2,2,2,2,1,3,1,2,0,0],
            [0,0,2,1,1,1,1,2,2,1,1,1,1,2,0,0],
            [0,0,0,2,1,1,1,1,1,1,1,1,2,0,0,0],
            [0,0,0,0,2,1,1,1,1,1,1,2,0,0,0,0],
            [0,0,0,0,4,4,2,2,2,2,4,4,0,0,0,0],
            [0,0,0,4,4,4,4,2,2,4,4,4,4,0,0,0],
            [0,0,4,4,4,4,4,4,4,4,4,4,4,4,0,0],
            [0,0,4,4,4,4,4,4,4,4,4,4,4,4,0,0],
            [0,0,0,4,4,4,4,4,4,4,4,4,4,0,0,0],
            [0,0,0,4,4,4,4,0,0,4,4,4,4,0,0,0],
            [0,0,0,4,4,4,0,0,0,0,4,4,4,0,0,0],
            [0,0,0,0,4,4,0,0,0,0,4,4,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        ]
        colors = [(120, 180, 100), (50, 100, 50), (255, 255, 0), (80, 60, 30)]
        return SpriteGenerator.create_sprite(16, 16, pixel_data, colors)

    @staticmethod
    def create_orc_sprite():
        """Create orc enemy sprite"""
        pixel_data = [
            [0,0,0,2,2,2,2,2,2,2,2,2,2,0,0,0],
            [0,0,2,2,2,2,2,2,2,2,2,2,2,2,0,0],
            [0,2,1,1,2,2,2,2,2,2,2,2,1,1,2,0],
            [0,2,1,3,1,2,2,2,2,2,2,1,3,1,2,0],
            [0,2,1,1,1,1,2,2,2,2,1,1,1,1,2,0],
            [0,0,2,1,1,1,1,1,1,1,1,1,1,2,0,0],
            [0,0,0,2,1,1,1,1,1,1,1,1,2,0,0,0],
            [0,0,0,4,4,4,2,2,2,2,4,4,4,0,0,0],
            [0,0,4,4,4,4,4,2,2,4,4,4,4,4,0,0],
            [0,4,4,4,4,4,4,4,4,4,4,4,4,4,4,0],
            [0,4,4,4,4,4,4,4,4,4,4,4,4,4,4,0],
            [0,0,4,4,4,4,4,4,4,4,4,4,4,4,0,0],
            [0,0,4,4,4,4,4,0,0,4,4,4,4,4,0,0],
            [0,0,4,4,4,4,0,0,0,0,4,4,4,4,0,0],
            [0,0,0,4,4,0,0,0,0,0,0,4,4,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        ]
        colors = [(100, 140, 80), (60, 80, 40), (255, 0, 0), (120, 80, 50)]
        return SpriteGenerator.create_sprite(16, 16, pixel_data, colors)

    @staticmethod
    def create_troll_sprite():
        """Create troll enemy sprite - larger and meaner"""
        pixel_data = [
            [0,0,2,2,2,2,2,2,2,2,2,2,2,2,0,0],
            [0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0],
            [2,1,1,2,2,2,2,2,2,2,2,2,2,1,1,2],
            [2,1,3,1,2,2,2,2,2,2,2,2,1,3,1,2],
            [2,1,1,1,1,2,2,2,2,2,2,1,1,1,1,2],
            [0,2,1,1,1,1,1,2,2,1,1,1,1,1,2,0],
            [0,0,2,1,1,1,1,1,1,1,1,1,1,2,0,0],
            [0,0,4,4,4,4,2,2,2,2,4,4,4,4,0,0],
            [0,4,4,4,4,4,4,2,2,4,4,4,4,4,4,0],
            [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],
            [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],
            [0,4,4,4,4,4,4,4,4,4,4,4,4,4,4,0],
            [0,4,4,4,4,4,4,0,0,4,4,4,4,4,4,0],
            [0,4,4,4,4,4,0,0,0,0,4,4,4,4,4,0],
            [0,0,4,4,4,0,0,0,0,0,0,4,4,4,0,0],
            [0,0,0,4,4,0,0,0,0,0,0,4,4,0,0,0],
        ]
        colors = [(80, 120, 70), (40, 60, 30), (255, 100, 100), (100, 70, 50)]
        return SpriteGenerator.create_sprite(16, 16, pixel_data, colors)

    @staticmethod
    def create_potion_sprite():
        """Create health potion sprite"""
        pixel_data = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,2,2,2,2,2,2,0,0,0,0,0],
            [0,0,0,0,0,2,2,2,2,2,2,0,0,0,0,0],
            [0,0,0,0,2,1,1,1,1,1,1,2,0,0,0,0],
            [0,0,0,0,2,1,1,1,1,1,1,2,0,0,0,0],
            [0,0,0,2,1,1,1,1,1,1,1,1,2,0,0,0],
            [0,0,2,1,1,1,1,1,1,1,1,1,1,2,0,0],
            [0,0,2,1,1,1,1,1,1,1,1,1,1,2,0,0],
            [0,0,2,1,1,1,1,1,1,1,1,1,1,2,0,0],
            [0,0,0,2,1,1,1,1,1,1,1,1,2,0,0,0],
            [0,0,0,0,2,2,2,2,2,2,2,2,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        ]
        colors = [(255, 0, 100), (100, 50, 50)]
        return SpriteGenerator.create_sprite(16, 16, pixel_data, colors)

    @staticmethod
    def create_gold_sprite():
        """Create gold coin sprite"""
        pixel_data = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,2,2,2,2,2,2,0,0,0,0,0],
            [0,0,0,0,2,1,1,1,1,1,1,2,0,0,0,0],
            [0,0,0,2,1,1,1,1,1,1,1,1,2,0,0,0],
            [0,0,2,1,1,1,1,1,1,1,1,1,1,2,0,0],
            [0,0,2,1,1,1,1,1,1,1,1,1,1,2,0,0],
            [0,0,2,1,1,1,1,1,1,1,1,1,1,2,0,0],
            [0,0,0,2,1,1,1,1,1,1,1,1,2,0,0,0],
            [0,0,0,0,2,1,1,1,1,1,1,2,0,0,0,0],
            [0,0,0,0,0,2,2,2,2,2,2,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        ]
        colors = [(255, 215, 0), (180, 140, 0)]
        return SpriteGenerator.create_sprite(16, 16, pixel_data, colors)

    @staticmethod
    def create_weapon_sprite():
        """Create weapon (sword) sprite"""
        pixel_data = [
            [0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,2,1,2,0,0],
            [0,0,0,0,0,0,0,0,0,0,2,1,1,2,0,0],
            [0,0,0,0,0,0,0,0,0,2,1,1,2,0,0,0],
            [0,0,0,0,0,0,0,0,2,1,1,2,0,0,0,0],
            [0,0,0,0,0,0,0,2,1,1,2,0,0,0,0,0],
            [0,0,0,0,0,0,2,1,1,2,0,0,0,0,0,0],
            [0,0,0,0,0,2,1,1,2,0,0,0,0,0,0,0],
            [0,0,0,0,2,1,1,2,0,0,0,0,0,0,0,0],
            [0,0,0,2,1,1,2,0,0,0,0,0,0,0,0,0],
            [0,0,2,1,1,2,0,0,0,0,0,0,0,0,0,0],
            [0,0,2,3,2,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,3,3,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,3,3,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        ]
        colors = [(200, 200, 220), (100, 100, 120), (120, 80, 40)]
        return SpriteGenerator.create_sprite(16, 16, pixel_data, colors)

    @staticmethod
    def create_armor_sprite():
        """Create armor (shield) sprite"""
        pixel_data = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,2,2,2,2,2,2,0,0,0,0,0],
            [0,0,0,0,2,1,1,1,1,1,1,2,0,0,0,0],
            [0,0,0,2,1,1,1,1,1,1,1,1,2,0,0,0],
            [0,0,2,1,1,1,3,3,3,3,1,1,1,2,0,0],
            [0,0,2,1,1,3,3,3,3,3,3,1,1,2,0,0],
            [0,0,2,1,1,3,3,3,3,3,3,1,1,2,0,0],
            [0,0,2,1,1,3,3,3,3,3,3,1,1,2,0,0],
            [0,0,2,1,1,1,3,3,3,3,1,1,1,2,0,0],
            [0,0,0,2,1,1,1,1,1,1,1,1,2,0,0,0],
            [0,0,0,0,2,1,1,1,1,1,1,2,0,0,0,0],
            [0,0,0,0,0,2,2,1,1,2,2,0,0,0,0,0],
            [0,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        ]
        colors = [(150, 150, 170), (80, 80, 90), (100, 50, 150)]
        return SpriteGenerator.create_sprite(16, 16, pixel_data, colors)

class Item:
    """Represents an item in the game"""
    def __init__(self, x, y, item_type, name, value):
        self.x = x
        self.y = y
        self.item_type = item_type  # 'potion', 'weapon', 'armor', 'gold'
        self.name = name
        self.value = value  # HP restore, damage boost, gold amount, etc.

class Rect:
    """Represents a rectangular room in the dungeon"""
    def __init__(self, x, y, width, height):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    def center(self):
        """Return the center coordinates of the room"""
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2
        return (center_x, center_y)

    def intersects(self, other):
        """Check if this room overlaps with another room"""
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

class Enemy:
    """Represents an enemy creature with D&D-style stats"""
    def __init__(self, x, y, name, strength, constitution, intelligence, detection_range, description, xp_value):
        self.x = x
        self.y = y
        self.name = name
        self.detection_range = detection_range
        self.description = description
        self.xp_value = xp_value
        self.in_combat = False

        # Base stats (D&D style)
        self.strength = strength
        self.constitution = constitution
        self.intelligence = intelligence

        # Derived stats (calculated from base stats)
        self.max_hp = self.calculate_max_hp()
        self.hp = self.max_hp
        self.max_mana = self.calculate_max_mana()
        self.mana = self.max_mana
        self.damage = self.calculate_damage()

    def calculate_max_hp(self):
        """Calculate max HP from constitution: 8 + (CON * 2)"""
        return 8 + (self.constitution * 2)

    def calculate_damage(self):
        """Calculate base damage from strength: 1 + (STR // 3)"""
        return 1 + (self.strength // 3)

    def calculate_max_mana(self):
        """Calculate max mana from intelligence: 3 + (INT * 2)"""
        return 3 + (self.intelligence * 2)

    def move_towards(self, target_x, target_y, dungeon, enemies, dungeon_width, dungeon_height):
        """Move one step towards the target position"""
        dx = 0
        dy = 0

        # Determine direction to move
        if self.x < target_x:
            dx = 1
        elif self.x > target_x:
            dx = -1

        if self.y < target_y:
            dy = 1
        elif self.y > target_y:
            dy = -1

        # Try to move, prioritize one direction
        new_x = self.x + dx
        new_y = self.y + dy

        # Check if position is valid and not occupied by another enemy
        if (0 <= new_x < dungeon_width and
            0 <= new_y < dungeon_height and
            dungeon[new_y][new_x] == FLOOR and
            not any(e.x == new_x and e.y == new_y for e in enemies if e != self)):
            self.x = new_x
            self.y = new_y
            return True
        return False

class Player:
    """Represents the player character"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.level = 1
        self.xp = 0
        self.xp_to_next_level = 10
        self.gold = 0
        self.inventory = []  # List of items (potions, weapons, etc.)

        # Base stats (D&D style)
        self.strength = 5      # Affects damage
        self.constitution = 5  # Affects HP
        self.intelligence = 5  # Affects mana

        # Derived stats (calculated from base stats)
        self.max_hp = self.calculate_max_hp()
        self.hp = self.max_hp
        self.max_mana = self.calculate_max_mana()
        self.mana = self.max_mana
        self.damage = self.calculate_damage()

    def calculate_max_hp(self):
        """Calculate max HP from constitution: 10 + (CON * 2)"""
        return 10 + (self.constitution * 2)

    def calculate_damage(self):
        """Calculate base damage from strength: 1 + (STR // 3)"""
        return 1 + (self.strength // 3)

    def calculate_max_mana(self):
        """Calculate max mana from intelligence: 5 + (INT * 2)"""
        return 5 + (self.intelligence * 2)

    def move(self, dx, dy, dungeon, dungeon_width, dungeon_height):
        """Move the player if the target position is walkable"""
        new_x = self.x + dx
        new_y = self.y + dy

        # Check if the new position is within bounds and walkable
        if (0 <= new_x < dungeon_width and
            0 <= new_y < dungeon_height and
            dungeon[new_y][new_x] == FLOOR):
            self.x = new_x
            self.y = new_y
            return True
        return False

    def attack(self, enemy):
        """Attack an enemy"""
        enemy.hp -= self.damage
        return self.damage

    def gain_xp(self, amount):
        """Gain experience points and check for level up"""
        self.xp += amount
        leveled_up = False
        while self.xp >= self.xp_to_next_level:
            self.level_up()
            leveled_up = True
        return leveled_up

    def level_up(self):
        """Increase player level and stats"""
        self.level += 1
        self.xp -= self.xp_to_next_level
        self.xp_to_next_level = int(self.xp_to_next_level * 1.5)

        # Increase base stats
        self.strength += 1
        self.constitution += 1
        self.intelligence += 1

        # Recalculate derived stats
        old_max_hp = self.max_hp
        old_max_mana = self.max_mana

        self.max_hp = self.calculate_max_hp()
        self.max_mana = self.calculate_max_mana()
        self.damage = self.calculate_damage()

        # Heal by the amount of HP/mana gained
        self.hp += (self.max_hp - old_max_hp)
        self.mana += (self.max_mana - old_max_mana)

    def add_item(self, item):
        """Add an item to inventory"""
        if item.item_type == 'gold':
            self.gold += item.value
        else:
            self.inventory.append(item)

    def use_potion(self):
        """Use a health potion from inventory"""
        for item in self.inventory:
            if item.item_type == 'potion':
                heal_amount = min(item.value, self.max_hp - self.hp)
                self.hp += heal_amount
                self.inventory.remove(item)
                return heal_amount
        return 0

class Settings:
    """Game settings and configuration"""
    def __init__(self):
        self.resolution = DEFAULT_RESOLUTION
        self.fullscreen = False
        self.music_volume = 0.5
        self.sfx_volume = 0.5

    def apply_resolution(self):
        """Get the current resolution dimensions"""
        return RESOLUTIONS[self.resolution]

class Game:
    """Main game class that handles the game loop and rendering"""
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Load settings
        self.settings = Settings()

        # Get resolution from settings
        self.window_width, self.window_height = self.settings.apply_resolution()

        # Calculate dungeon dimensions based on current resolution
        self.game_view_width = self.window_width - BATTLE_PANEL_WIDTH
        self.dungeon_width = self.game_view_width // TILE_SIZE
        self.dungeon_height = self.window_height // TILE_SIZE

        # Create the window
        flags = pygame.FULLSCREEN if self.settings.fullscreen else 0
        self.screen = pygame.display.set_mode((self.window_width, self.window_height), flags)
        pygame.display.set_caption("Dungeon Crawler")

        # Set window icon (32x32 sword and shield icon)
        icon_surface = self.create_window_icon()
        pygame.display.set_icon(icon_surface)

        # Set up the font
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.ui_font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 32)

        # Load and cache all sprites (scaled to TILE_SIZE)
        self.sprites = {
            'player': pygame.transform.scale(SpriteGenerator.create_player_sprite(), (TILE_SIZE, TILE_SIZE)),
            'goblin': pygame.transform.scale(SpriteGenerator.create_goblin_sprite(), (TILE_SIZE, TILE_SIZE)),
            'orc': pygame.transform.scale(SpriteGenerator.create_orc_sprite(), (TILE_SIZE, TILE_SIZE)),
            'troll': pygame.transform.scale(SpriteGenerator.create_troll_sprite(), (TILE_SIZE, TILE_SIZE)),
            'potion': pygame.transform.scale(SpriteGenerator.create_potion_sprite(), (TILE_SIZE, TILE_SIZE)),
            'gold': pygame.transform.scale(SpriteGenerator.create_gold_sprite(), (TILE_SIZE, TILE_SIZE)),
            'weapon': pygame.transform.scale(SpriteGenerator.create_weapon_sprite(), (TILE_SIZE, TILE_SIZE)),
            'armor': pygame.transform.scale(SpriteGenerator.create_armor_sprite(), (TILE_SIZE, TILE_SIZE)),
        }

        # Game objects
        self.rooms = []
        self.dungeon = self.generate_dungeon()
        # Place player in the center of the first room
        first_room_center = self.rooms[0].center()
        self.player = Player(first_room_center[0], first_room_center[1])
        self.enemies = []
        self.items = []
        self.spawn_enemies()
        self.spawn_items()
        self.running = True
        self.game_over = False
        self.victory = False
        self.clock = pygame.time.Clock()
        self.messages = []  # General game messages

        # Battle system
        self.in_battle = False
        self.current_enemy = None
        self.battle_log = []
        self.player_defending = False
        self.selected_action = 0  # 0=Attack, 1=Defend, 2=Flee, 3=Use Item

        # Settings menu
        self.in_settings = False
        self.settings_selected = 0  # Selected setting option

        # Screen shake for animations
        self.screen_shake_amount = 0
        self.screen_shake_duration = 0

        # Continuous movement
        self.move_delay = 150  # milliseconds between moves when holding key
        self.last_move_time = 0

    def create_window_icon(self):
        """Create a 32x32 sword and shield icon for the window"""
        icon = pygame.Surface((32, 32))
        icon.fill((30, 30, 40))  # Dark background

        # Shield circle
        pygame.draw.circle(icon, (60, 60, 70), (16, 16), 12)
        pygame.draw.circle(icon, (120, 120, 140), (16, 16), 12, 2)

        # Sword
        pygame.draw.line(icon, (200, 200, 220), (16, 6), (16, 20), 3)  # Blade
        pygame.draw.line(icon, (120, 80, 40), (11, 20), (21, 20), 2)  # Guard
        pygame.draw.line(icon, (80, 50, 30), (16, 20), (16, 26), 2)  # Handle

        return icon

    def create_room(self, room, dungeon):
        """Carve out a room in the dungeon (make it floor tiles)"""
        for y in range(room.y1 + 1, room.y2):
            for x in range(room.x1 + 1, room.x2):
                dungeon[y][x] = FLOOR

    def create_horizontal_tunnel(self, x1, x2, y, dungeon):
        """Create a horizontal corridor"""
        for x in range(min(x1, x2), max(x1, x2) + 1):
            dungeon[y][x] = FLOOR

    def create_vertical_tunnel(self, y1, y2, x, dungeon):
        """Create a vertical corridor"""
        for y in range(min(y1, y2), max(y1, y2) + 1):
            dungeon[y][x] = FLOOR

    def generate_dungeon(self):
        """Generate a dungeon with random rooms and corridors"""
        # Start with all walls
        dungeon = [[WALL for x in range(self.dungeon_width)] for y in range(self.dungeon_height)]

        # Room generation parameters
        max_rooms = 10
        room_min_size = 4
        room_max_size = 8

        for _ in range(max_rooms):
            # Random room dimensions
            width = random.randint(room_min_size, room_max_size)
            height = random.randint(room_min_size, room_max_size)

            # Random position (with buffer from edges)
            x = random.randint(1, self.dungeon_width - width - 1)
            y = random.randint(1, self.dungeon_height - height - 1)

            # Create the room
            new_room = Rect(x, y, width, height)

            # Check if it overlaps with existing rooms
            overlaps = False
            for other_room in self.rooms:
                if new_room.intersects(other_room):
                    overlaps = True
                    break

            if not overlaps:
                # This room is valid, carve it out
                self.create_room(new_room, dungeon)

                # Get center coordinates
                new_x, new_y = new_room.center()

                if len(self.rooms) > 0:
                    # Connect to the previous room with corridors
                    prev_x, prev_y = self.rooms[-1].center()

                    # Randomly choose whether to go horizontal then vertical, or vice versa
                    if random.randint(0, 1) == 1:
                        # Horizontal tunnel, then vertical
                        self.create_horizontal_tunnel(prev_x, new_x, prev_y, dungeon)
                        self.create_vertical_tunnel(prev_y, new_y, new_x, dungeon)
                    else:
                        # Vertical tunnel, then horizontal
                        self.create_vertical_tunnel(prev_y, new_y, prev_x, dungeon)
                        self.create_horizontal_tunnel(prev_x, new_x, new_y, dungeon)

                # Add room to the list
                self.rooms.append(new_room)

        return dungeon

    def spawn_enemies(self):
        """Spawn enemies in rooms (skip the first room where player starts)"""
        for room in self.rooms[1:]:  # Skip first room
            # 70% chance to spawn an enemy in each room
            if random.random() < 0.7:
                # Random position in the room
                x = random.randint(room.x1 + 1, room.x2 - 1)
                y = random.randint(room.y1 + 1, room.y2 - 1)

                # Random enemy type
                enemy_type = random.choice(['goblin', 'orc', 'troll'])

                if enemy_type == 'goblin':
                    # Goblin: Low STR, low CON, medium INT (sneaky but weak)
                    # Stats: STR=2, CON=2, INT=4
                    # Results: HP=12, DMG=1, Mana=11
                    enemy = Enemy(x, y, 'Goblin',
                                strength=2, constitution=2, intelligence=4,
                                detection_range=3,
                                description="A small, cowardly creature. Weak but cunning. Prefers to ambush the unwary.",
                                xp_value=3)
                elif enemy_type == 'orc':
                    # Orc: High STR, medium CON, low INT (strong brute)
                    # Stats: STR=6, CON=4, INT=1
                    # Results: HP=16, DMG=3, Mana=5
                    enemy = Enemy(x, y, 'Orc',
                                strength=6, constitution=4, intelligence=1,
                                detection_range=5,
                                description="A brutish warrior with crude armor. Aggressive and territorial. Attacks on sight.",
                                xp_value=5)
                else:  # troll
                    # Troll: Very high STR and CON, very low INT (tank)
                    # Stats: STR=9, CON=7, INT=1
                    # Results: HP=22, DMG=4, Mana=5
                    enemy = Enemy(x, y, 'Troll',
                                strength=9, constitution=7, intelligence=1,
                                detection_range=7,
                                description="A massive, hulking beast. Tough hide and crushing strength. Guards its domain fiercely.",
                                xp_value=8)

                self.enemies.append(enemy)

    def spawn_items(self):
        """Spawn items in some rooms"""
        for room in self.rooms[1:]:  # Skip first room
            # 40% chance to spawn an item in each room
            if random.random() < 0.4:
                # Random position in the room
                x = random.randint(room.x1 + 1, room.x2 - 1)
                y = random.randint(room.y1 + 1, room.y2 - 1)

                # Random item type
                item_roll = random.random()
                if item_roll < 0.5:  # 50% health potion
                    item = Item(x, y, 'potion', 'Health Potion', 10)
                elif item_roll < 0.75:  # 25% weapon
                    item = Item(x, y, 'weapon', 'Iron Sword', 2)
                elif item_roll < 0.9:  # 15% armor
                    item = Item(x, y, 'armor', 'Leather Armor', 5)
                else:  # 10% gold
                    item = Item(x, y, 'gold', 'Gold Coins', random.randint(5, 15))

                self.items.append(item)

    def drop_enemy_loot(self, enemy):
        """Drop items when an enemy is defeated"""
        # Always drop some gold
        gold_amount = random.randint(2, 8)
        if enemy.name == 'Goblin':
            gold_amount = random.randint(2, 5)
        elif enemy.name == 'Orc':
            gold_amount = random.randint(5, 10)
        elif enemy.name == 'Troll':
            gold_amount = random.randint(10, 20)

        gold_item = Item(enemy.x, enemy.y, 'gold', 'Gold Coins', gold_amount)
        self.items.append(gold_item)

        # Chance for additional loot
        loot_chance = random.random()
        if loot_chance < 0.3:  # 30% chance for potion
            self.items.append(Item(enemy.x, enemy.y, 'potion', 'Health Potion', 10))

    def player_move(self, dx, dy):
        """Handle player movement, item pickup, and battle detection"""
        if self.game_over or self.in_battle:
            return

        # Calculate target position
        target_x = self.player.x + dx
        target_y = self.player.y + dy

        # Check if there's an enemy at the target position
        for enemy in self.enemies:
            if enemy.x == target_x and enemy.y == target_y:
                # Bump into enemy - start battle with screen shake!
                self.screen_shake_amount = 5
                self.screen_shake_duration = 10
                self.start_battle(enemy)
                return

        # No enemy at target - try to move normally
        if self.player.move(dx, dy, self.dungeon, self.dungeon_width, self.dungeon_height):
            # Check for items at new position
            self.check_item_pickup()

    def check_item_pickup(self):
        """Check if player is standing on an item and pick it up"""
        items_to_remove = []
        for item in self.items:
            if item.x == self.player.x and item.y == self.player.y:
                self.player.add_item(item)
                items_to_remove.append(item)

                if item.item_type == 'gold':
                    self.add_message(f"Picked up {item.value} gold!")
                elif item.item_type == 'potion':
                    self.add_message(f"Picked up {item.name}!")
                elif item.item_type == 'weapon':
                    old_damage = self.player.damage
                    self.player.damage += item.value
                    self.add_message(f"Equipped {item.name}! Damage: {old_damage} -> {self.player.damage}")
                elif item.item_type == 'armor':
                    old_max_hp = self.player.max_hp
                    self.player.max_hp += item.value
                    self.player.hp += item.value
                    self.add_message(f"Equipped {item.name}! Max HP: {old_max_hp} -> {self.player.max_hp}")

        for item in items_to_remove:
            self.items.remove(item)

    def add_message(self, message):
        """Add a message to the general message log"""
        self.messages.append(message)
        if len(self.messages) > 3:
            self.messages.pop(0)

    def start_battle(self, enemy):
        """Initialize a battle with an enemy"""
        self.in_battle = True
        self.current_enemy = enemy
        enemy.in_combat = True
        self.battle_log = [f"You encounter a {enemy.name}!"]
        self.selected_action = 0
        self.player_defending = False

    def execute_battle_action(self):
        """Execute the selected battle action"""
        if not self.in_battle or not self.current_enemy:
            return

        enemy = self.current_enemy

        # Player's turn
        if self.selected_action == 0:  # Attack
            damage = self.player.damage
            if self.player_defending:
                damage = max(1, damage // 2)  # Half damage if previously defending

            enemy.hp -= damage
            self.battle_log.append(f"You attack for {damage} damage!")

            if enemy.hp <= 0:
                self.battle_log.append(f"{enemy.name} defeated!")
                # Drop loot
                self.drop_enemy_loot(enemy)
                # Give XP
                leveled_up = self.player.gain_xp(enemy.xp_value)
                self.battle_log.append(f"Gained {enemy.xp_value} XP!")
                if leveled_up:
                    self.battle_log.append(f"LEVEL UP! Now level {self.player.level}!")
                self.enemies.remove(enemy)
                self.end_battle(victory=True)
                return

        elif self.selected_action == 1:  # Defend
            self.player_defending = True
            self.battle_log.append("You brace for the enemy's attack!")

        elif self.selected_action == 2:  # Flee
            # 50% chance to flee
            if random.random() < 0.5:
                self.battle_log.append("You successfully fled!")
                self.end_battle(victory=False)
                return
            else:
                self.battle_log.append("Couldn't escape!")

        elif self.selected_action == 3:  # Use Item (Potion)
            heal_amount = self.player.use_potion()
            if heal_amount > 0:
                self.battle_log.append(f"Used potion! Healed {heal_amount} HP!")
            else:
                self.battle_log.append("No potions to use!")
                return  # Don't take a turn if no potion

        # Enemy's turn
        enemy_damage = enemy.damage
        if self.player_defending:
            enemy_damage = max(1, enemy_damage // 2)
            self.battle_log.append(f"{enemy.name} attacks but you block some damage!")
        else:
            self.battle_log.append(f"{enemy.name} attacks!")

        self.player.hp -= enemy_damage
        self.battle_log.append(f"You take {enemy_damage} damage!")

        # Reset defense
        self.player_defending = False

        if self.player.hp <= 0:
            self.game_over = True
            self.battle_log.append("You died!")

        # Keep only last 5 messages
        if len(self.battle_log) > 5:
            self.battle_log = self.battle_log[-5:]

    def end_battle(self, victory):
        """End the current battle"""
        self.in_battle = False
        if self.current_enemy:
            self.current_enemy.in_combat = False
        self.current_enemy = None
        self.player_defending = False

        # Check for overall victory
        if victory and len(self.enemies) == 0:
            self.victory = True

    def apply_settings(self):
        """Apply current settings and restart the game"""
        # Store current game state
        old_width = self.window_width
        old_height = self.window_height

        # Get new resolution
        self.window_width, self.window_height = self.settings.apply_resolution()

        # Only restart if resolution actually changed
        if old_width != self.window_width or old_height != self.window_height:
            # Recreate window with new dimensions
            flags = pygame.FULLSCREEN if self.settings.fullscreen else 0
            self.screen = pygame.display.set_mode((self.window_width, self.window_height), flags)

            # Recalculate dungeon dimensions
            self.game_view_width = self.window_width - BATTLE_PANEL_WIDTH
            self.dungeon_width = self.game_view_width // TILE_SIZE
            self.dungeon_height = self.window_height // TILE_SIZE

            # Regenerate dungeon
            self.rooms = []
            self.dungeon = self.generate_dungeon()
            first_room_center = self.rooms[0].center()
            self.player.x = first_room_center[0]
            self.player.y = first_room_center[1]
            self.enemies = []
            self.items = []
            self.spawn_enemies()
            self.spawn_items()
        else:
            # Just update fullscreen
            flags = pygame.FULLSCREEN if self.settings.fullscreen else 0
            self.screen = pygame.display.set_mode((self.window_width, self.window_height), flags)

    def handle_input(self):
        """Handle pygame events and keyboard input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Handle key presses
            if event.type == pygame.KEYDOWN:
                # Q quits the game
                if event.key == pygame.K_q and not self.in_settings:
                    self.running = False

                # ESC opens/closes settings menu
                if event.key == pygame.K_ESCAPE:
                    if self.in_settings:
                        self.in_settings = False
                    else:
                        self.in_settings = True

                if self.in_settings:
                    # Settings menu controls
                    resolution_options = list(RESOLUTIONS.keys())
                    current_res_idx = resolution_options.index(self.settings.resolution)

                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.settings_selected = max(0, self.settings_selected - 1)
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        self.settings_selected = min(3, self.settings_selected + 1)
                    elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        # Change setting left
                        if self.settings_selected == 0:  # Resolution
                            new_idx = max(0, current_res_idx - 1)
                            self.settings.resolution = resolution_options[new_idx]
                        elif self.settings_selected == 1:  # Fullscreen
                            self.settings.fullscreen = not self.settings.fullscreen
                    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        # Change setting right
                        if self.settings_selected == 0:  # Resolution
                            new_idx = min(len(resolution_options) - 1, current_res_idx + 1)
                            self.settings.resolution = resolution_options[new_idx]
                        elif self.settings_selected == 1:  # Fullscreen
                            self.settings.fullscreen = not self.settings.fullscreen
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        # Activate selected option
                        if self.settings_selected == 2:  # Apply Changes
                            self.apply_settings()
                            self.in_settings = False
                        elif self.settings_selected == 3:  # Back to Game
                            self.in_settings = False

                elif self.in_battle:
                    # Battle controls
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.selected_action = max(0, self.selected_action - 1)
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        self.selected_action = min(3, self.selected_action + 1)  # 4 actions now
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        self.execute_battle_action()
                else:
                    # Movement controls - immediate response on key press
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.player_move(0, -1)
                        self.last_move_time = pygame.time.get_ticks()
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        self.player_move(0, 1)
                        self.last_move_time = pygame.time.get_ticks()
                    elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        self.player_move(-1, 0)
                        self.last_move_time = pygame.time.get_ticks()
                    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.player_move(1, 0)
                        self.last_move_time = pygame.time.get_ticks()

        # Continuous movement - check for held keys
        if not self.in_battle and not self.in_settings and not self.game_over:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_move_time >= self.move_delay:
                keys = pygame.key.get_pressed()
                moved = False

                # Check movement keys (WASD and arrows)
                if keys[pygame.K_w] or keys[pygame.K_UP]:
                    self.player_move(0, -1)
                    moved = True
                elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                    self.player_move(0, 1)
                    moved = True
                elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
                    self.player_move(-1, 0)
                    moved = True
                elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                    self.player_move(1, 0)
                    moved = True

                # Update last move time if we actually moved
                if moved:
                    self.last_move_time = current_time

    def render(self):
        """Draw the dungeon and player to the screen"""
        # Clear screen with dark background
        self.screen.fill(DARK_GRAY)

        # Calculate screen shake offset
        shake_x = 0
        shake_y = 0
        if self.screen_shake_duration > 0:
            shake_x = random.randint(-self.screen_shake_amount, self.screen_shake_amount)
            shake_y = random.randint(-self.screen_shake_amount, self.screen_shake_amount)
            self.screen_shake_duration -= 1

        # Draw the dungeon
        for y in range(self.dungeon_height):
            for x in range(self.dungeon_width):
                # Calculate pixel position with screen shake
                pixel_x = x * TILE_SIZE + shake_x
                pixel_y = y * TILE_SIZE + shake_y

                # Determine what to draw
                tile = self.dungeon[y][x]

                # Draw background
                if tile == FLOOR:
                    color = BLACK
                elif tile == WALL:
                    color = GRAY

                pygame.draw.rect(self.screen, color,
                               (pixel_x, pixel_y, TILE_SIZE, TILE_SIZE))

                # Check for entities at this position
                entity_drawn = False

                # Draw player
                if x == self.player.x and y == self.player.y:
                    self.screen.blit(self.sprites['player'], (pixel_x, pixel_y))
                    entity_drawn = True

                # Draw items
                if not entity_drawn:
                    for item in self.items:
                        if item.x == x and item.y == y:
                            # Use sprite based on item type
                            sprite = self.sprites.get(item.item_type)
                            if sprite:
                                self.screen.blit(sprite, (pixel_x, pixel_y))
                            entity_drawn = True
                            break

                # Draw enemies
                if not entity_drawn:
                    for enemy in self.enemies:
                        if enemy.x == x and enemy.y == y:
                            # Use sprite based on enemy name
                            sprite_key = enemy.name.lower()
                            sprite = self.sprites.get(sprite_key)
                            if sprite:
                                self.screen.blit(sprite, (pixel_x, pixel_y))
                            entity_drawn = True
                            break

                # Draw tile characters if no entity
                if not entity_drawn:
                    char = tile
                    char_color = WHITE if tile == WALL else DARK_GRAY
                    text_surface = self.font.render(char, True, char_color)
                    text_rect = text_surface.get_rect(center=(pixel_x + TILE_SIZE//2,
                                                              pixel_y + TILE_SIZE//2))
                    self.screen.blit(text_surface, text_rect)

        # Draw battle panel on the right side
        panel_x = self.game_view_width
        pygame.draw.rect(self.screen, BLACK, (panel_x, 0, BATTLE_PANEL_WIDTH, self.window_height))

        if self.in_battle and self.current_enemy:
            # Battle panel
            y_offset = 20

            # Title
            title = self.title_font.render("BATTLE!", True, RED)
            self.screen.blit(title, (panel_x + 20, y_offset))
            y_offset += 50

            # Enemy info
            enemy_name = self.ui_font.render(self.current_enemy.name, True, YELLOW)
            self.screen.blit(enemy_name, (panel_x + 20, y_offset))
            y_offset += 30

            # Enemy description (wrapped text)
            desc_words = self.current_enemy.description.split()
            line = ""
            for word in desc_words:
                test_line = line + word + " "
                if self.font.size(test_line)[0] < 450:
                    line = test_line
                else:
                    desc_surface = self.font.render(line, True, GRAY)
                    self.screen.blit(desc_surface, (panel_x + 20, y_offset))
                    y_offset += 18
                    line = word + " "
            if line:
                desc_surface = self.font.render(line, True, GRAY)
                self.screen.blit(desc_surface, (panel_x + 20, y_offset))
                y_offset += 25

            # Enemy base stats
            base_stats = self.font.render(f"STR: {self.current_enemy.strength}  CON: {self.current_enemy.constitution}  INT: {self.current_enemy.intelligence}", True, GRAY)
            self.screen.blit(base_stats, (panel_x + 20, y_offset))
            y_offset += 20

            # Enemy combat stats
            stats_text = self.font.render(f"Damage: {self.current_enemy.damage} | Range: {self.current_enemy.detection_range}m", True, YELLOW)
            self.screen.blit(stats_text, (panel_x + 20, y_offset))
            y_offset += 25

            # Enemy HP bar
            hp_label = self.font.render(f"HP: {self.current_enemy.hp}/{self.current_enemy.max_hp}", True, WHITE)
            self.screen.blit(hp_label, (panel_x + 20, y_offset))
            y_offset += 20

            bar_width = 450
            bar_height = 20
            pygame.draw.rect(self.screen, RED, (panel_x + 20, y_offset, bar_width, bar_height))
            enemy_hp_width = int((self.current_enemy.hp / self.current_enemy.max_hp) * bar_width)
            pygame.draw.rect(self.screen, ORANGE, (panel_x + 20, y_offset, enemy_hp_width, bar_height))
            y_offset += 35

            # Separator
            pygame.draw.line(self.screen, GRAY, (panel_x + 20, y_offset), (panel_x + 480, y_offset), 2)
            y_offset += 15

            # Player HP
            player_hp_text = self.ui_font.render(f"Your HP: {self.player.hp}/{self.player.max_hp}", True, GREEN)
            self.screen.blit(player_hp_text, (panel_x + 20, y_offset))
            y_offset += 20

            bar_width = 450
            pygame.draw.rect(self.screen, RED, (panel_x + 20, y_offset, bar_width, bar_height))
            player_hp_width = int((self.player.hp / self.player.max_hp) * bar_width)
            pygame.draw.rect(self.screen, GREEN, (panel_x + 20, y_offset, player_hp_width, bar_height))
            y_offset += 35

            # Separator
            pygame.draw.line(self.screen, GRAY, (panel_x + 20, y_offset), (panel_x + 480, y_offset), 2)
            y_offset += 15

            # Actions
            actions_title = self.ui_font.render("Actions:", True, WHITE)
            self.screen.blit(actions_title, (panel_x + 20, y_offset))
            y_offset += 30

            # Count potions
            potion_count = sum(1 for item in self.player.inventory if item.item_type == 'potion')

            actions = ["Attack", "Defend", "Flee", f"Use Potion ({potion_count})"]
            action_y = y_offset
            for i, action in enumerate(actions):
                color = WHITE if i == self.selected_action else GRAY
                action_text = self.ui_font.render(f"> {action}" if i == self.selected_action else f"  {action}", True, color)
                self.screen.blit(action_text, (panel_x + 30, action_y))
                action_y += 32

            y_offset = action_y + 15

            # Controls hint
            hint = self.font.render("W/S: Select | Enter/Space: Confirm", True, DARK_GRAY)
            self.screen.blit(hint, (panel_x + 30, y_offset))
            y_offset += 30

            # Separator
            pygame.draw.line(self.screen, GRAY, (panel_x + 20, y_offset), (panel_x + 480, y_offset), 2)
            y_offset += 15

            # Battle log
            log_title = self.ui_font.render("Battle Log:", True, WHITE)
            self.screen.blit(log_title, (panel_x + 20, y_offset))
            y_offset += 25

            for message in self.battle_log[-6:]:  # Show last 6 messages
                msg_surface = self.font.render(message, True, GRAY)
                self.screen.blit(msg_surface, (panel_x + 20, y_offset))
                y_offset += 20

        else:
            # Exploration panel
            y_offset = 20

            # Title
            title = self.title_font.render("EXPLORATION", True, GREEN)
            self.screen.blit(title, (panel_x + 20, y_offset))
            y_offset += 50

            # Player stats
            stats_title = self.ui_font.render("Player Stats", True, WHITE)
            self.screen.blit(stats_title, (panel_x + 20, y_offset))
            y_offset += 25

            level_text = self.font.render(f"Level: {self.player.level}", True, YELLOW)
            self.screen.blit(level_text, (panel_x + 20, y_offset))
            gold_text = self.font.render(f"Gold: {self.player.gold}", True, YELLOW)
            self.screen.blit(gold_text, (panel_x + 250, y_offset))
            y_offset += 25

            # XP Bar
            xp_label = self.font.render(f"XP: {self.player.xp}/{self.player.xp_to_next_level}", True, WHITE)
            self.screen.blit(xp_label, (panel_x + 20, y_offset))
            y_offset += 18

            bar_width = 450
            bar_height = 15
            pygame.draw.rect(self.screen, DARK_GRAY, (panel_x + 20, y_offset, bar_width, bar_height))
            xp_width = int((self.player.xp / self.player.xp_to_next_level) * bar_width)
            pygame.draw.rect(self.screen, CYAN, (panel_x + 20, y_offset, xp_width, bar_height))
            y_offset += 20

            # HP
            hp_text = self.font.render(f"HP: {self.player.hp}/{self.player.max_hp}", True, WHITE)
            self.screen.blit(hp_text, (panel_x + 20, y_offset))
            y_offset += 18

            bar_height = 20
            pygame.draw.rect(self.screen, RED, (panel_x + 20, y_offset, bar_width, bar_height))
            player_hp_width = int((self.player.hp / self.player.max_hp) * bar_width)
            pygame.draw.rect(self.screen, GREEN, (panel_x + 20, y_offset, player_hp_width, bar_height))
            y_offset += 25

            # Mana bar
            mana_text = self.font.render(f"Mana: {self.player.mana}/{self.player.max_mana}", True, WHITE)
            self.screen.blit(mana_text, (panel_x + 20, y_offset))
            y_offset += 18

            pygame.draw.rect(self.screen, DARK_GRAY, (panel_x + 20, y_offset, bar_width, bar_height))
            player_mana_width = int((self.player.mana / self.player.max_mana) * bar_width) if self.player.max_mana > 0 else 0
            pygame.draw.rect(self.screen, BLUE, (panel_x + 20, y_offset, player_mana_width, bar_height))
            y_offset += 25

            # Base stats
            stats_text = self.font.render(f"STR: {self.player.strength}  CON: {self.player.constitution}  INT: {self.player.intelligence}", True, GRAY)
            self.screen.blit(stats_text, (panel_x + 20, y_offset))
            y_offset += 20

            damage_text = self.font.render(f"Damage: {self.player.damage}", True, WHITE)
            self.screen.blit(damage_text, (panel_x + 20, y_offset))
            y_offset += 30

            # Separator
            pygame.draw.line(self.screen, GRAY, (panel_x + 20, y_offset), (panel_x + 480, y_offset), 2)
            y_offset += 15

            # Inventory
            inv_title = self.ui_font.render("Inventory", True, WHITE)
            self.screen.blit(inv_title, (panel_x + 20, y_offset))
            y_offset += 25

            potion_count = sum(1 for item in self.player.inventory if item.item_type == 'potion')
            inv_text = self.font.render(f"Potions: {potion_count}", True, CYAN)
            self.screen.blit(inv_text, (panel_x + 20, y_offset))
            y_offset += 30

            # Messages
            for message in self.messages:
                msg_surface = self.font.render(message, True, YELLOW)
                self.screen.blit(msg_surface, (panel_x + 20, y_offset))
                y_offset += 20

            # Separator
            pygame.draw.line(self.screen, GRAY, (panel_x + 20, y_offset), (panel_x + 480, y_offset), 2)
            y_offset += 15

            # Position and Enemies
            pos_text = self.font.render(f"Position: ({self.player.x}m, {self.player.y}m)", True, GRAY)
            self.screen.blit(pos_text, (panel_x + 20, y_offset))
            y_offset += 20

            enemies_text = self.font.render(f"Enemies: {len(self.enemies)}", True, YELLOW)
            self.screen.blit(enemies_text, (panel_x + 20, y_offset))
            y_offset += 30

            # Controls
            pygame.draw.line(self.screen, GRAY, (panel_x + 20, y_offset), (panel_x + 480, y_offset), 2)
            y_offset += 15

            controls_title = self.font.render("WASD/Arrows - Move | ESC - Settings | Q - Quit", True, GRAY)
            self.screen.blit(controls_title, (panel_x + 20, y_offset))

        # Settings menu overlay
        if self.in_settings:
            overlay = pygame.Surface((self.window_width, self.window_height))
            overlay.set_alpha(230)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))

            # Settings panel
            panel_width = 600
            panel_height = 500
            panel_x = (self.window_width - panel_width) // 2
            panel_y = (self.window_height - panel_height) // 2

            pygame.draw.rect(self.screen, DARK_GRAY, (panel_x, panel_y, panel_width, panel_height))
            pygame.draw.rect(self.screen, WHITE, (panel_x, panel_y, panel_width, panel_height), 3)

            y_offset = panel_y + 20

            # Title
            title = self.title_font.render("SETTINGS", True, WHITE)
            title_rect = title.get_rect(center=(self.window_width // 2, y_offset))
            self.screen.blit(title, title_rect)
            y_offset += 60

            # Resolution setting
            resolution_options = list(RESOLUTIONS.keys())
            current_res_idx = resolution_options.index(self.settings.resolution)

            settings_items = [
                f"Resolution: < {self.settings.resolution} >",
                f"Fullscreen: {'ON' if self.settings.fullscreen else 'OFF'}",
                "Apply Changes",
                "Back to Game"
            ]

            for i, item in enumerate(settings_items):
                color = YELLOW if i == self.settings_selected else WHITE
                item_text = self.ui_font.render(f"> {item}" if i == self.settings_selected else f"  {item}", True, color)
                item_rect = item_text.get_rect(center=(self.window_width // 2, y_offset))
                self.screen.blit(item_text, item_rect)
                y_offset += 50

            # Controls hint
            y_offset += 30
            hint = self.font.render("W/S: Navigate | A/D: Change | Enter: Select | ESC: Back", True, GRAY)
            hint_rect = hint.get_rect(center=(self.window_width // 2, y_offset))
            self.screen.blit(hint, hint_rect)

        # Game over / Victory overlay
        elif self.game_over:
            overlay = pygame.Surface((self.game_view_width, self.window_height))
            overlay.set_alpha(200)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))

            game_over_text = self.title_font.render("GAME OVER", True, RED)
            text_rect = game_over_text.get_rect(center=(self.game_view_width // 2, self.window_height // 2))
            self.screen.blit(game_over_text, text_rect)

            hint_text = self.font.render("Press Q to quit", True, WHITE)
            hint_rect = hint_text.get_rect(center=(self.game_view_width // 2, self.window_height // 2 + 40))
            self.screen.blit(hint_text, hint_rect)

        elif self.victory:
            overlay = pygame.Surface((self.game_view_width, self.window_height))
            overlay.set_alpha(200)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))

            victory_text = self.title_font.render("VICTORY!", True, GREEN)
            text_rect = victory_text.get_rect(center=(self.game_view_width // 2, self.window_height // 2))
            self.screen.blit(victory_text, text_rect)

            hint_text = self.font.render("All enemies defeated! Press Q to quit", True, WHITE)
            hint_rect = hint_text.get_rect(center=(self.game_view_width // 2, self.window_height // 2 + 40))
            self.screen.blit(hint_text, hint_rect)

        # Update the display
        pygame.display.flip()

    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_input()
            self.render()
            self.clock.tick(60)  # 60 FPS

        pygame.quit()
        sys.exit()

def main():
    """Entry point for the game"""
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
