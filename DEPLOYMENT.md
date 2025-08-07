# 🚀 Keeping Your Math Tutor Bot Active 24/7

This guide shows you different ways to keep your Math Tutor Bot running continuously.

## ✅ Quick Start (Currently Active!)

Your bot is **already running**! Here's how to manage it:

```bash
# Check if bot is running
./status_bot.sh

# Start the bot (if not running)
./start_bot.sh

# Stop the bot
./stop_bot.sh

# View live logs
tail -f bot_output.log
```

## 🖥️ Local Development (Your Computer)

### Option 1: Simple Background Process ⭐ **RECOMMENDED**
```bash
# Start bot in background (survives terminal closure)
./start_bot.sh

# Check status anytime
./status_bot.sh

# Stop when needed
./stop_bot.sh
```

**Benefits:**
- ✅ Survives terminal closure
- ✅ Easy to start/stop
- ✅ Automatic log management
- ✅ Process tracking

**Limitations:**
- ❌ Stops when computer sleeps/shuts down
- ❌ No automatic restart on crashes

### Option 2: Keep Terminal Open
```bash
# Simple way - keep terminal window open
python bot.py
```

**Benefits:**
- ✅ See logs in real-time
- ✅ Easy to stop with Ctrl+C

**Limitations:**
- ❌ Stops if terminal closes
- ❌ Stops when computer sleeps

### Option 3: Screen/Tmux Session
```bash
# Install screen (if not installed)
brew install screen  # macOS
# sudo apt install screen  # Ubuntu

# Start screen session
screen -S mathbot

# Run bot inside screen
python bot.py

# Detach: Ctrl+A then D
# Reattach: screen -r mathbot
```

## ☁️ Production Deployment (24/7 Hosting)

### Option 1: Free Cloud Hosting

#### **Render (Recommended - Free)**
1. Fork your GitHub repo
2. Connect to [Render](https://render.com)
3. Create new "Web Service"
4. Use these settings:
   ```
   Build Command: pip install -r requirements.txt
   Start Command: python bot.py
   ```

#### **Railway (Free Tier)**
1. Connect GitHub to [Railway](https://railway.app)
2. Deploy from your repo
3. Add environment variables

#### **Heroku (Free Tier Limited)**
```bash
# Install Heroku CLI
# Create Procfile
echo "worker: python bot.py" > Procfile

# Deploy
heroku create your-math-bot
heroku config:set BOT_TOKEN=your_token
heroku config:set GEMINI_API_KEY=your_key
git push heroku main
heroku ps:scale worker=1
```

### Option 2: VPS Hosting

#### **DigitalOcean/Linode/Vultr ($5/month)**
```bash
# On your VPS
git clone https://github.com/yourusername/math-tutor-bot.git
cd math-tutor-bot
pip install -r requirements.txt

# Create systemd service
sudo nano /etc/systemd/system/mathbot.service
```

Systemd service file:
```ini
[Unit]
Description=Math Tutor Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/math-tutor-bot
ExecStart=/usr/bin/python3 bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable mathbot
sudo systemctl start mathbot
sudo systemctl status mathbot
```

### Option 3: Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install Tesseract
RUN apt-get update && apt-get install -y tesseract-ocr

COPY . .
CMD ["python", "bot.py"]
```

```bash
# Build and run
docker build -t math-tutor-bot .
docker run -d --name mathbot --restart unless-stopped math-tutor-bot
```

## 🔧 Auto-Start on Boot (macOS)

Create launch agent:
```bash
# Create plist file
mkdir -p ~/Library/LaunchAgents
cat > ~/Library/LaunchAgents/com.mathbot.plist << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.mathbot</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/$(whoami)/Downloads/math-tutor/start_bot.sh</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
EOF

# Load launch agent
launchctl load ~/Library/LaunchAgents/com.mathbot.plist
```

## 📊 Monitoring & Maintenance

### Check Bot Health
```bash
# Real-time status
./status_bot.sh

# Live logs
tail -f bot_output.log

# Error logs only
grep "ERROR" bot_output.log

# Recent activity
tail -50 bot_output.log | grep "INFO"
```

### Log Rotation
```bash
# Archive old logs (run weekly)
mv bot_output.log "bot_output_$(date +%Y%m%d).log"
touch bot_output.log
```

### Automatic Restart on Crash
```bash
# Create watchdog script
cat > watchdog.sh << 'EOF'
#!/bin/bash
while true; do
    if ! ./status_bot.sh | grep -q "Bot is RUNNING"; then
        echo "Bot crashed! Restarting..."
        ./start_bot.sh
    fi
    sleep 60  # Check every minute
done
EOF

chmod +x watchdog.sh
nohup ./watchdog.sh > watchdog.log 2>&1 &
```

## 🆘 Troubleshooting

### Bot Conflicts
```bash
# Kill all bot instances
pkill -f "python.*bot.py"
sleep 5
./start_bot.sh
```

### Network Issues
- Bot automatically reconnects on network issues
- Check logs for "httpx.ConnectError" messages
- Restart bot if network issues persist

### Resource Usage
```bash
# Check memory/CPU usage
ps aux | grep "python.*bot.py"

# Monitor system resources
top -p $(cat bot.pid)
```

## 📋 Current Status

✅ **Your bot is currently running with PID: $(cat bot.pid 2>/dev/null || echo "Not found")**

**Quick Commands:**
- `./status_bot.sh` - Check if running
- `./stop_bot.sh` - Stop the bot  
- `./start_bot.sh` - Start the bot
- `tail -f bot_output.log` - Watch logs

**Next Steps for 24/7 Operation:**
1. **Immediate**: Your bot runs until computer sleeps/restarts
2. **Better**: Set up auto-start on boot (see macOS section above)
3. **Best**: Deploy to cloud hosting for true 24/7 operation
