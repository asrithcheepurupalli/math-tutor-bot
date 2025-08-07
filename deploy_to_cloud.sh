#!/bin/bash

echo "🚀 DEPLOYING TO RENDER FOR 24/7 OPERATION"
echo "========================================"
echo ""
echo "This will prepare your bot for cloud deployment so it runs"
echo "even when your computer sleeps! 💤➡️☁️"
echo ""

# Check if git repo is clean
if [ -n "$(git status --porcelain)" ]; then
    echo "📝 Committing changes..."
    git add .
    git commit -m "Prepare for 24/7 cloud deployment

- Add Dockerfile for containerized deployment
- Add render.yaml for Render platform
- Add CLOUD_DEPLOY.md with step-by-step instructions
- Ready for 24/7 operation in the cloud"
    
    echo "📤 Pushing to GitHub..."
    git push origin main
else
    echo "✅ Git repository is clean and up to date"
fi

echo ""
echo "🎉 READY FOR CLOUD DEPLOYMENT!"
echo ""
echo "Next steps:"
echo "1. Go to https://render.com"
echo "2. Sign up with GitHub"
echo "3. Click 'New +' → 'Web Service'"
echo "4. Select your 'math-tutor-bot' repository"
echo "5. Use these settings:"
echo "   - Build Command: pip install -r requirements.txt"
echo "   - Start Command: python bot.py"
echo "6. Add environment variables:"
echo "   - BOT_TOKEN = $(grep BOT_TOKEN .env 2>/dev/null | cut -d'=' -f2 | tr -d ' ' || echo 'your_telegram_bot_token')"
echo "   - GEMINI_API_KEY = $(grep GEMINI_API_KEY .env 2>/dev/null | cut -d'=' -f2 | tr -d ' ' || echo 'your_gemini_api_key')"
echo "   - AI_MODEL_PROVIDER = gemini"
echo "7. Click 'Create Web Service'"
echo ""
echo "🌟 Your bot will then run 24/7 even when your computer sleeps!"
echo ""
echo "📖 For detailed instructions: cat CLOUD_DEPLOY.md"
