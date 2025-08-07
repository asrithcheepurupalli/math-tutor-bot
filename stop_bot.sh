#!/bin/bash

# Math Tutor Bot Stop Script
# This script stops the running bot

echo "🛑 Stopping Math Tutor Bot..."

# Check if PID file exists
if [ -f "bot.pid" ]; then
    BOT_PID=$(cat bot.pid)
    
    # Check if process is still running
    if ps -p $BOT_PID > /dev/null; then
        kill $BOT_PID
        echo "✅ Bot stopped (PID: $BOT_PID)"
        rm bot.pid
    else
        echo "⚠️  Bot process not found (PID: $BOT_PID)"
        rm bot.pid
    fi
else
    # Try to find and kill any running bot processes
    if pgrep -f "python.*bot.py" > /dev/null; then
        pkill -f "python.*bot.py"
        echo "✅ Bot processes stopped"
    else
        echo "ℹ️  No running bot found"
    fi
fi
