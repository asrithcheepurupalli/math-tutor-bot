#!/bin/bash

# Math Tutor Bot Startup Script
# This script starts the bot and keeps it running in the background

echo "🚀 Starting Math Tutor Bot..."

# Change to the script directory
cd "$(dirname "$0")"

# Check if bot is already running
if pgrep -f "python.*bot.py" > /dev/null; then
    echo "⚠️  Bot is already running!"
    echo "Process ID: $(pgrep -f 'python.*bot.py')"
    exit 1
fi

# Start the bot in background with nohup
nohup /Library/Frameworks/Python.framework/Versions/3.12/bin/python3 bot.py > bot_output.log 2>&1 &

# Get the process ID
BOT_PID=$!
echo "✅ Bot started successfully!"
echo "Process ID: $BOT_PID"
echo "Logs: bot_output.log"
echo "To stop: ./stop_bot.sh"

# Save PID for later use
echo $BOT_PID > bot.pid
