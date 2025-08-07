# 🌍 Deploy to Cloud for 24/7 Operation

Your bot will sleep when your computer sleeps! For true 24/7 operation, deploy to the cloud.

## 🆓 **FREE Option 1: Render (Recommended)**

### Step 1: Prepare Your Repository
```bash
# Commit all changes
git add .
git commit -m "Prepare for cloud deployment"
git push origin main
```

### Step 2: Deploy to Render
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Connect your `math-tutor-bot` repository
5. Use these settings:
   ```
   Name: math-tutor-bot
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python bot.py
   ```

### Step 3: Add Environment Variables
In Render dashboard, add these environment variables:
```
BOT_TOKEN = your_telegram_bot_token_here
GEMINI_API_KEY = your_gemini_api_key_here
AI_MODEL_PROVIDER = gemini
LOG_LEVEL = INFO
```

### Step 4: Deploy!
- Click "Create Web Service"
- Wait 5-10 minutes for deployment
- Your bot will be online 24/7! 🎉

---

## 🆓 **FREE Option 2: Railway**

### Step 1: Deploy to Railway
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "Deploy from GitHub repo"
4. Select your `math-tutor-bot` repository

### Step 2: Add Environment Variables
```
BOT_TOKEN = your_telegram_bot_token_here
GEMINI_API_KEY = your_gemini_api_key_here
AI_MODEL_PROVIDER = gemini
```

### Step 3: Deploy!
- Railway will automatically detect Python and deploy
- Your bot runs 24/7 for free! 🚀

---

## 🆓 **FREE Option 3: Heroku**

### Step 1: Install Heroku CLI
```bash
# macOS
brew install heroku/brew/heroku

# Or download from heroku.com
```

### Step 2: Deploy
```bash
# Login to Heroku
heroku login

# Create app
heroku create your-math-tutor-bot

# Set environment variables
heroku config:set BOT_TOKEN=your_telegram_bot_token_here
heroku config:set GEMINI_API_KEY=your_gemini_api_key_here
heroku config:set AI_MODEL_PROVIDER=gemini

# Deploy
git push heroku main

# Scale worker (important!)
heroku ps:scale web=1
```

---

## 💰 **Paid Option: VPS ($5/month)**

### DigitalOcean/Linode/Vultr
```bash
# On your VPS (Ubuntu)
git clone https://github.com/yourusername/math-tutor-bot.git
cd math-tutor-bot

# Install dependencies
sudo apt update
sudo apt install python3-pip tesseract-ocr
pip3 install -r requirements.txt

# Create .env file
cp .env.example .env
nano .env  # Add your API keys

# Create systemd service for auto-restart
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
Environment=PATH=/usr/bin:/usr/local/bin
Environment=PYTHONPATH=/home/ubuntu/math-tutor-bot

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start
sudo systemctl enable mathbot
sudo systemctl start mathbot
sudo systemctl status mathbot
```

---

## 🐳 **Docker Option**

### Local Docker Test
```bash
# Build image
docker build -t math-tutor-bot .

# Run container
docker run -d --name mathbot \
  -e BOT_TOKEN=your_token \
  -e GEMINI_API_KEY=your_key \
  -e AI_MODEL_PROVIDER=gemini \
  --restart unless-stopped \
  math-tutor-bot
```

### Deploy to Cloud with Docker
- **Google Cloud Run**: Free tier available
- **AWS ECS**: More complex but powerful
- **DigitalOcean App Platform**: Easy Docker deployment

---

## 🏆 **Recommended Path**

### For Beginners: **Render** 
- ✅ Completely free
- ✅ No credit card required
- ✅ Easy GitHub integration
- ✅ Automatic HTTPS
- ❌ Goes to sleep after 15 minutes of inactivity (wakes up when messaged)

### For Always-On: **Railway** 
- ✅ Free tier with 500 hours/month
- ✅ Never sleeps
- ✅ Easy deployment
- ❌ Limited free hours

### For Production: **VPS ($5/month)**
- ✅ Always running
- ✅ Full control
- ✅ No limits
- ❌ Requires setup

---

## 🎯 **Quick Start: Deploy to Render Now!**

1. **Push your code:**
   ```bash
   git add .
   git commit -m "Ready for cloud deployment"
   git push origin main
   ```

2. **Go to [render.com](https://render.com)**

3. **Connect GitHub and deploy**

4. **Add your API keys**

5. **Your bot runs 24/7!** 🎉

**Even when your computer is off, sleeping, or broken - your bot keeps helping students with math!**
