#!/bin/bash

# Setup Auto-Start on Boot for macOS
# This script creates a Launch Agent to start the bot automatically

USER_HOME="/Users/$(whoami)"
BOT_DIR="/Users/asrithcheepurupalli/Downloads/math-tutor"
LAUNCH_AGENTS_DIR="$USER_HOME/Library/LaunchAgents"
PLIST_FILE="$LAUNCH_AGENTS_DIR/com.mathtutor.bot.plist"

echo "🚀 Setting up Math Tutor Bot Auto-Start..."

# Create LaunchAgents directory if it doesn't exist
mkdir -p "$LAUNCH_AGENTS_DIR"

# Create the plist file
cat > "$PLIST_FILE" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.mathtutor.bot</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>$BOT_DIR/auto_restart.sh</string>
    </array>
    
    <key>WorkingDirectory</key>
    <string>$BOT_DIR</string>
    
    <key>RunAtLoad</key>
    <true/>
    
    <key>KeepAlive</key>
    <true/>
    
    <key>StandardOutPath</key>
    <string>$BOT_DIR/auto_restart.log</string>
    
    <key>StandardErrorPath</key>
    <string>$BOT_DIR/auto_restart.log</string>
    
    <key>ThrottleInterval</key>
    <integer>30</integer>
</dict>
</plist>
EOF

echo "✅ Created launch agent: $PLIST_FILE"

# Load the launch agent
launchctl unload "$PLIST_FILE" 2>/dev/null  # Unload if already loaded
launchctl load "$PLIST_FILE"

if [ $? -eq 0 ]; then
    echo "✅ Launch agent loaded successfully!"
    echo ""
    echo "🎉 Your Math Tutor Bot will now:"
    echo "   • Start automatically when you log in"
    echo "   • Restart automatically if it crashes"
    echo "   • Keep running 24/7 (while computer is on)"
    echo ""
    echo "Commands:"
    echo "   • Check status: ./status_bot.sh"
    echo "   • View logs: tail -f auto_restart.log"
    echo "   • Disable auto-start: launchctl unload $PLIST_FILE"
else
    echo "❌ Failed to load launch agent"
    exit 1
fi
