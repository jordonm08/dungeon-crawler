#!/bin/bash
# Dungeon Crawler Game Launcher

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the game directory
cd "$SCRIPT_DIR"

# Launch the game
python3 dungeon_crawler.py
