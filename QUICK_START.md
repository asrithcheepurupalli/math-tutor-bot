# 🚀 Quick Setup Guide for Math Tutor Bot

## ✅ Step-by-Step Setup

### 1. Get Your Telegram Bot Token
1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Use `/newbot` command
3. Follow the prompts to create your bot
4. **Save the token** BotFather gives you

### 2. Get an AI API Key
Choose **ONE** of these options:

#### Option A: OpenAI (Recommended)
1. Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Create an account if needed
3. Generate a new API key
4. **Save the key** (starts with `sk-`)

#### Option B: Google Gemini (Alternative)
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create an account if needed
3. Generate an API key
4. **Save the key**

### 3. Configure Your Bot
1. Open the `.env` file in this folder
2. Replace the placeholder values:

```bash
# Required Configuration
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz  # Your actual bot token
OPENAI_API_KEY=sk-your-actual-openai-key-here     # Your actual API key
AI_MODEL_PROVIDER=openai                          # Keep as 'openai' or change to 'gemini'

# Optional (can leave as-is for now)
LOG_LEVEL=INFO
VIDEO_OUTPUT_DIR=./generated_videos
MAX_VIDEO_DURATION=60
```

### 4. Test Your Bot
```bash
# Test if everything works
python test_components.py

# Start your bot
python bot.py
```

### 5. Try It Out!
1. Find your bot on Telegram (search for the username you created)
2. Send `/start` to begin
3. Try sending a math problem like: "Solve for x: 2x + 5 = 15"

## 🎯 Example Messages to Test

**Text Problems:**
- "What is 2 + 2?"
- "Solve for x: 3x - 7 = 14"
- "Find the derivative of x²"
- "What's the area of a circle with radius 5?"

**Commands:**
- `/start` - Welcome message
- `/help` - Show help
- `/about` - Bot information

## 🔧 Troubleshooting

**Bot not responding:**
- Check your bot token in `.env`
- Make sure you've started the bot with `python bot.py`
- Check the logs in `logs/` folder

**AI not working:**
- Verify your API key is correct
- Check your API account has credits/quota
- Try switching AI providers in `.env`

**Need help?**
- Check `README.md` for detailed documentation
- Look at error logs in `logs/math_tutor_bot.log`

## 🎉 You're Ready!

Once configured, your Math Tutor Bot will:
- ✅ Solve math problems step by step
- ✅ Generate educational videos (local fallback)
- ✅ Read math problems from images (OCR)
- ✅ Support multiple math subjects
- ✅ Filter content appropriately
- ✅ Rate limit users to prevent spam

**Have fun teaching math with AI! 🧮🤖**
