#!/bin/bash

# Auto-restart Math Tutor Bot
# This script monitors the bot and restarts it if it stops

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🔄 Starting Bot Auto-Restart Monitor..."
echo "This will keep your bot running 24/7"
echo "Press Ctrl+C to stop monitoring"
echo ""

# Function to check if bot is running
is_bot_running() {
    if [ -f "bot.pid" ]; then
        BOT_PID=$(cat bot.pid)
        if ps -p $BOT_PID > /dev/null 2>&1; then
            return 0  # Bot is running
        fi
    fi
    return 1  # Bot is not running
}

# Main monitoring loop
while true; do
    if ! is_bot_running; then
        echo "⚠️  Bot stopped! Restarting... $(date)"
        
        # Clean up any stale processes
        pkill -f "python.*bot.py" 2>/dev/null
        sleep 2
        
        # Start the bot
        ./start_bot.sh
        
        if is_bot_running; then
            echo "✅ Bot restarted successfully!"
        else
            echo "❌ Failed to restart bot. Retrying in 30 seconds..."
            sleep 30
            continue
        fi
    else
        echo "✅ Bot is running ($(date))"
    fi
    
    # Check every 60 seconds
    sleep 60
done
