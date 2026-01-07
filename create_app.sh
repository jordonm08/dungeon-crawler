#!/bin/bash
# Script to create a macOS .app bundle for Dungeon Crawler

APP_NAME="Dungeon Crawler"
GAME_DIR="/Users/jordonmyers/game"
APP_DIR="$GAME_DIR/$APP_NAME.app"

# Create the app bundle structure
mkdir -p "$APP_DIR/Contents/MacOS"
mkdir -p "$APP_DIR/Contents/Resources"

# Create the Info.plist
cat > "$APP_DIR/Contents/Info.plist" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>DungeonCrawler</string>
    <key>CFBundleIdentifier</key>
    <string>com.jordonmyers.dungeoncrawler</string>
    <key>CFBundleName</key>
    <string>Dungeon Crawler</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleSignature</key>
    <string>????</string>
</dict>
</plist>
EOF

# Create the executable launcher script
cat > "$APP_DIR/Contents/MacOS/DungeonCrawler" << 'EOF'
#!/bin/bash
cd "/Users/jordonmyers/game"
python3 dungeon_crawler.py
EOF

# Make the launcher executable
chmod +x "$APP_DIR/Contents/MacOS/DungeonCrawler"

echo "✅ Application bundle created at: $APP_DIR"
echo "You can now double-click 'Dungeon Crawler.app' to launch the game!"
