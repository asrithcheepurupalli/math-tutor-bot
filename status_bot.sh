#!/bin/bash

# Math Tutor Bot Status Script
# This script checks if the bot is running

echo "📊 Math Tutor Bot Status"
echo "======================="

# Check if PID file exists
if [ -f "bot.pid" ]; then
    BOT_PID=$(cat bot.pid)
    echo "PID file found: $BOT_PID"
    
    # Check if process is actually running
    if ps -p $BOT_PID > /dev/null; then
        echo "✅ Bot is RUNNING (PID: $BOT_PID)"
        
        # Show process details
        echo ""
        echo "Process details:"
        ps -p $BOT_PID -o pid,ppid,cmd,etime
        
        # Show recent logs
        if [ -f "bot_output.log" ]; then
            echo ""
            echo "Recent logs (last 10 lines):"
            tail -10 bot_output.log
        fi
    else
        echo "❌ Bot is NOT RUNNING (stale PID file)"
        rm bot.pid
    fi
else
    # Check for any running bot processes
    if pgrep -f "python.*bot.py" > /dev/null; then
        echo "⚠️  Bot appears to be running but no PID file found"
        echo "Process IDs: $(pgrep -f 'python.*bot.py' | tr '\n' ' ')"
    else
        echo "❌ Bot is NOT RUNNING"
    fi
fi

echo ""
echo "Commands:"
echo "  Start:  ./start_bot.sh"
echo "  Stop:   ./stop_bot.sh"
echo "  Status: ./status_bot.sh"
