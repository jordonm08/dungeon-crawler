# Dungeon Crawler - Development Log

## Project Overview
A turn-based dungeon crawler game built with Python and Pygame, featuring pixel art graphics, procedural dungeon generation, and RPG mechanics.

**Repository:** https://github.com/jordonm08/dungeon-crawler.git

---

## Development Sessions

### Session 1 - Initial Setup & Core Mechanics

#### Phase 1: Project Setup
- Initialized git repository and connected to GitHub
- Configured SSH authentication for git push
- Installed pygame: `pip3 install pygame`
- Created basic game structure with Pygame

#### Phase 2: Responsive Controls
**User Request:** "can we build this in a way that the game is responsive immediately upon clicking a direction like 'W' instead of having to type 'w' and then enter?"

**Solution:** Switched from terminal `input()` to Pygame event-based input handling
- Implemented `pygame.event.get()` for instant keyboard response
- WASD and arrow keys for movement
- 60 FPS game loop with `pygame.time.Clock()`

#### Phase 3: Dungeon Generation
- Procedural dungeon generation using BSP-style room placement
- Rooms connected by corridors (horizontal + vertical tunnels)
- Non-overlapping room validation
- Default dungeon size: 50x30 tiles (expandable)

#### Phase 4: World Scale & Visual Centering
**User Request:** "each square on the grid is 1 meter" and "focus the player in the middle of the square"

**Solution:**
- Established: **1 tile = 1 meter = 24 pixels**
- Changed player from '@' character to large green circle (20px diameter)
- Used `pygame.draw.circle()` with center positioning for clear visual feedback

#### Phase 5: Turn-Based Combat System
**User Request:** "I actually want it to be turned based combat - and depending on the enemy should determine the radius with which the battle would begin"

**Features Implemented:**
- Detection-based battle triggers (automatic when player enters range)
- Enemy detection ranges:
  - Goblins: 3 meters
  - Orcs: 5 meters
  - Trolls: 7 meters
- Side panel UI (500px wide) for battle/exploration info
- Screen expanded to 1200px game view + 500px panel = 1700px total
- 4 Battle actions: Attack, Defend, Flee, Use Potion
- Battle log showing last 6 messages

#### Phase 6: Expanded UI & Enemy Descriptions
**User Request:** "We should make the screen larger. And the battle should have a log of what happened. Also whenever you come across an enemy and enter battle, there should be a description."

**Changes:**
- Screen expanded to 1700px total width (1200px game + 500px panel)
- Dungeon size increased to 50x30 tiles (50m x 30m)
- Added enemy descriptions that appear in battle:
  - Goblin: "A small, cowardly creature. Weak but cunning. Prefers to ambush the unwary."
  - Orc: "A brutish warrior with crude armor. Aggressive and territorial. Attacks on sight."
  - Troll: "A massive, hulking beast. Tough hide and crushing strength. Guards its domain fiercely."
- Battle log displays last 6 combat messages

#### Phase 7: Items & Progression System
**User Request:** "Enemies should also sometimes drop loot. The type will vary but we can start simple for now. We'll also want currency and XP at some point soon."

**Features Added:**
- Item system with 4 types: potions, weapons, armor, gold
- Inventory management
- XP and leveling system:
  - Players gain XP from defeating enemies
  - Level up increases: max HP (+5), damage (+1), full heal
  - XP requirement scales: `xp_to_next_level * 1.5` per level
- Enemy loot drops:
  - Always drops gold (amount varies by enemy type)
  - 30% chance for health potion
- Item spawning in rooms (40% chance per room)
- Equipment automatically applies (weapons boost damage, armor boosts max HP)
- Potions stored in inventory, usable in battle (4th action)

---

### Session 2 - Pixel Art & Settings System

#### Phase 8: Pixel Art Sprites
**User Request:** "would it be possible to make this game with like, pixel art?" → "yeah let's go ahead and try the pixel route"

**Implementation:**
- Created `SpriteGenerator` class for procedural pixel art
- All sprites are 16x16 pixels, scaled to 24x24 for tiles
- Pixel data arrays define sprite appearance (0 = transparent, 1-4 = color indices)

**Sprites Created:**
- **Player:** Adventurer with brown hair, skin tone, green clothes, gray armor
- **Goblin:** Small green creature with yellow eyes, brown clothes
- **Orc:** Larger green warrior with red eyes, brown armor
- **Troll:** Biggest enemy, dark green with red eyes
- **Potion:** Red/pink health potion bottle
- **Gold:** Gold coin
- **Weapon:** Silver sword with brown handle
- **Armor:** Shield with purple emblem

**Technical Details:**
- Sprites cached in `self.sprites` dictionary at game init
- `pygame.transform.scale()` scales 16x16 to 24x24
- Replaced all `pygame.draw.circle()` and `pygame.draw.rect()` with `screen.blit(sprite, position)`

#### Phase 9: Resolution Options & Settings System
**User Request:** "can we make it so we can resize? like there should be an options system for this game"

**Settings System Features:**
1. **Resolution Options:**
   - 1920x1080 (Full HD) - default
   - 1600x900
   - 1366x768
   - 1280x720
   - 1024x768

2. **Fullscreen Toggle:** ON/OFF

3. **Dynamic Dungeon Sizing:**
   - Dungeon dimensions calculated from screen size: `(width - 500) // 24` tiles
   - Larger resolutions = bigger dungeons
   - Game regenerates dungeon when resolution changes

4. **Settings Menu UI:**
   - Semi-transparent overlay (alpha 230)
   - Centered panel (600x500)
   - Navigation: W/S or Up/Down arrows
   - Change settings: A/D or Left/Right arrows
   - Apply/Back: Enter or Space
   - ESC to open/close settings

5. **Controls:**
   - **ESC** - Open/close settings menu
   - **Q** - Quit game
   - **WASD/Arrows** - Move (exploration) or navigate (menus)
   - **Enter/Space** - Confirm action

**Bug Fixes:**
- Fixed ESC key initially closing game instead of opening settings
- Now ESC properly toggles settings menu on/off

---

## Current Game Architecture

### File Structure
```
/Users/jordonmyers/game/
├── dungeon_crawler.py    # Main game file (1025 lines)
├── README.md             # Repository readme
└── CLAUDE.md            # This file - development context
```

### Core Classes

#### `SpriteGenerator`
- Static methods for creating pixel art sprites
- Methods: `create_sprite()`, `create_player_sprite()`, `create_goblin_sprite()`, etc.
- Returns pygame Surface objects

#### `Settings`
- Manages game configuration
- Properties: resolution, fullscreen, music_volume, sfx_volume
- Method: `apply_resolution()` returns (width, height) tuple

#### `Item`
- Properties: x, y, item_type, name, value
- Types: 'potion', 'weapon', 'armor', 'gold'

#### `Rect` (Room)
- Properties: x1, y1, x2, y2
- Methods: `center()`, `intersects(other)`

#### `Enemy`
- Properties: x, y, name, hp, max_hp, damage, detection_range, description, xp_value, in_combat
- Method: `move_towards(target_x, target_y, dungeon, enemies, dungeon_width, dungeon_height)`
- Enemy types: Goblin (HP:5, DMG:2, XP:3), Orc (HP:8, DMG:3, XP:5), Troll (HP:12, DMG:4, XP:8)

#### `Player`
- Properties: x, y, hp, max_hp, damage, level, xp, xp_to_next_level, gold, inventory
- Methods: `move()`, `attack()`, `gain_xp()`, `level_up()`, `add_item()`, `use_potion()`
- Starting stats: HP:20, DMG:3, LVL:1

#### `Game`
- Main game loop and rendering
- Key methods:
  - `generate_dungeon()` - Procedural dungeon generation
  - `spawn_enemies()` - Place enemies in rooms (70% chance per room)
  - `spawn_items()` - Place items in rooms (40% chance per room)
  - `handle_input()` - Keyboard and menu navigation
  - `render()` - Draw everything (dungeon, sprites, UI panels, overlays)
  - `apply_settings()` - Resize window and regenerate dungeon
  - `execute_battle_action()` - Turn-based combat logic
  - `check_battle_trigger()` - Detection range checks

### Game Constants
```python
TILE_SIZE = 24                    # Pixels per tile (1 tile = 1 meter)
BATTLE_PANEL_WIDTH = 500          # Right side UI panel
RESOLUTIONS = {                   # Available screen sizes
    '1920x1080': (1920, 1080),
    '1600x900': (1600, 900),
    '1366x768': (1366, 768),
    '1280x720': (1280, 720),
    '1024x768': (1024, 768),
}
DEFAULT_RESOLUTION = '1920x1080'
```

### Game Flow
1. **Initialization:** Load settings → Create window → Generate dungeon → Spawn entities
2. **Game Loop:** Handle input → Update game state → Render frame → Tick clock (60 FPS)
3. **Exploration Mode:** Move player → Check item pickup → Check battle triggers
4. **Battle Mode:** Select action → Execute turn → Enemy attacks → Check victory/defeat
5. **Settings Mode:** Navigate options → Change settings → Apply or cancel

---

## Key Design Decisions

### Why Pygame Event-Based Input?
- User wanted instant response without pressing Enter
- Terminal input() requires Enter key confirmation
- Pygame events provide frame-by-frame key state checking

### Why Pixel Art?
- User preference for retro aesthetic
- Procedural generation allows easy creation/modification
- Lightweight (no external image files needed)
- Scalable with pygame.transform.scale()

### Why Dynamic Dungeon Sizing?
- Different screen sizes should feel proportionally similar
- Larger screens = more visible area = bigger dungeons
- Formula: `dungeon_tiles = (screen_pixels - panel_width) // tile_size`

### Why Detection Ranges Vary By Enemy?
- Adds strategic depth (avoid trolls from farther away)
- Larger/stronger enemies have better detection
- Creates risk/reward navigation decisions

### Why Side Panel UI?
- Keeps game view clean and unobstructed
- Dedicated space for stats, battle info, inventory
- Toggles between exploration panel and battle panel
- 500px width provides room for descriptions

---

## Game Mechanics Summary

### Combat System
- **Turn-based:** Player acts → Enemy acts → Repeat
- **Actions:** Attack (deal damage), Defend (reduce incoming damage 50%), Flee (50% chance), Use Potion (heal)
- **Defending:** Reduces both player damage output and enemy damage intake by 50% for one turn

### Progression System
- **XP Gain:** Defeat enemies to earn XP (Goblin:3, Orc:5, Troll:8)
- **Leveling:** XP threshold increases by 1.5x each level
- **Stat Growth:** +5 max HP, +1 damage, full heal on level up

### Item System
- **Potions:** Restore 10 HP (stackable in inventory)
- **Weapons:** Permanently increase damage (+2)
- **Armor:** Permanently increase max HP (+5)
- **Gold:** Currency (currently cosmetic, future: shops?)

### Dungeon Generation
- **Room Placement:** Random non-overlapping rooms (4-8 tiles wide/tall)
- **Corridors:** Connect room centers with L-shaped tunnels
- **Enemy Spawning:** 70% chance per room (skip first room)
- **Item Spawning:** 40% chance per room (potions 50%, weapons 25%, armor 15%, gold 10%)

---

## Technical Notes

### Resolution Scaling
When resolution changes:
1. Store old dimensions
2. Get new dimensions from settings
3. If changed: Recreate window → Recalculate dungeon size → Regenerate dungeon → Respawn everything
4. If unchanged but fullscreen toggled: Just recreate window with flag

### Sprite Rendering Priority
1. Check for player at position → Draw player sprite
2. Check for items → Draw item sprite (first match)
3. Check for enemies → Draw enemy sprite (first match)
4. Default → Draw tile character (. or #)

### Battle Detection
- Checked every time player moves
- Manhattan distance: `abs(enemy.x - player.x) + abs(enemy.y - player.y)`
- If distance ≤ detection_range: `start_battle(enemy)`

---

## Future Enhancements (Discussed but Not Implemented)

### Phase 6: Progression System (Pending)
- Stairs to descend to deeper levels
- Multiple dungeon floors with increasing difficulty
- Floor counter display
- Escape stairs to return to town?

### Other Potential Features Mentioned
- Fog of war (only see what's lit/explored)
- Traps (damage or effects when stepped on)
- Locked doors (require keys)
- Environmental elements (water, lava, etc.)
- Shops/merchants (spend gold)
- More enemy variety
- Boss encounters
- Character classes
- Magic/abilities system
- Sound effects and music (settings already have volume controls)

---

## Git Workflow

### Repository Setup
```bash
# Initial setup
git remote add origin git@github.com:jordonm08/dungeon-crawler.git
git push -u origin main

# Standard workflow
git add .
git commit -m "Description"
git push
```

### Commit History
1. Initial commit - Repository setup
2. Add pixel art sprites and settings system - Full game implementation

---

## Controls Reference

### Exploration Mode
- **W / ↑** - Move up
- **S / ↓** - Move down
- **A / ←** - Move left
- **D / →** - Move right
- **ESC** - Open settings menu
- **Q** - Quit game

### Battle Mode
- **W / ↑** - Select previous action
- **S / ↓** - Select next action
- **Enter / Space** - Confirm action
- **Q** - Quit game

### Settings Menu
- **W / ↑** - Navigate up
- **S / ↓** - Navigate down
- **A / ←** - Decrease value / Toggle off
- **D / →** - Increase value / Toggle on
- **Enter / Space** - Select "Apply Changes" or "Back to Game"
- **ESC** - Close settings menu

---

## Dependencies

### Required Python Packages
```bash
pip3 install pygame
```

### Python Version
- Python 3.x (developed with Python 3.x)
- Pygame 2.x

### Platform
- Developed on macOS (Darwin 24.6.0)
- Should work on Windows/Linux with Python + Pygame installed

---

## Development Philosophy

### User-Driven Design
- Every feature came from explicit user requests
- No over-engineering or premature optimization
- Simple solutions preferred over complex abstractions

### Iterative Development
1. User describes desired feature
2. Implement minimal viable version
3. User provides feedback
4. Refine based on feedback
5. Move to next feature

### Code Quality
- Clear variable names and function purposes
- Comments explain "why" not "what"
- Modular class structure for easy expansion
- Consistent code style throughout

---

## Current Status

### Completed Features ✅
- [x] Responsive keyboard controls
- [x] Procedural dungeon generation
- [x] Turn-based combat system
- [x] Enemy AI with detection ranges
- [x] Item system (potions, weapons, armor, gold)
- [x] Inventory management
- [x] XP and leveling system
- [x] Enemy loot drops
- [x] Pixel art sprites for all entities
- [x] Settings menu with resolution options
- [x] Fullscreen toggle
- [x] Dynamic dungeon resizing

### Next Up 🎯
- [ ] Phase 6: Progression system (stairs, multiple floors, difficulty scaling)

### Ideas for Later 💡
- Fog of war
- Traps and environmental hazards
- Locked doors and keys
- Shops and economy
- More enemy types
- Boss encounters
- Sound effects and music

---

## Session Notes Template

### Session X - [Date] - [Topic]

#### What We Built
- Feature 1
- Feature 2

#### Key Decisions
- Decision and rationale

#### Code Changes
- File: location
  - What changed and why

#### User Feedback
- Quote user requests
- Document responses

---

*Last Updated: Session 2 - 2026-01-07*
