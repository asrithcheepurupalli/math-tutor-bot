# Math Tutor Bot 🧮

An AI-powered math tutoring chatbot that provides step-by-step solutions using Google Gemini AI. Built for Telegram with interactive demo questions and OCR support for handwritten problems.

## ✨ Features

### 🎯 Core Capabilities
- **AI-Powered Solutions**: Uses Google Gemini for step-by-step math problem solving
- **Interactive Demo Questions**: Clickable buttons for easy testing
- **OCR Support**: Extracts math problems from images using Tesseract
- **Step-by-Step Explanations**: Clear, educational breakdowns for every problem
- **LaTeX Support**: Proper mathematical notation rendering
- **Content Filtering**: Ensures educational and appropriate content only

### 🛡️ Safety & Performance
- **Rate Limiting**: Prevents abuse with intelligent request limiting
- **Error Handling**: Robust error handling with graceful fallbacks
- **Conversation Logging**: Tracks interactions for analytics and improvement
- **Modular Architecture**: Clean, maintainable codebase

## 🛠 Tech Stack

- **Backend**: Python 3.8+
- **Bot Framework**: python-telegram-bot
- **AI Model**: Google Gemini Pro
- **OCR**: Tesseract OCR
- **Database**: SQLite
- **Image Processing**: PIL/Pillow
- **Math Processing**: SymPy (LaTeX support)

## 📁 Project Structure

```
math-tutor/
├── bot.py                          # Main bot logic with interactive demo questions
├── ai_solver.py                    # Google Gemini AI integration for problem solving
├── ai_solver_clean.py              # Minimal AI solver alternative
├── requirements.txt                # Python dependencies (clean, no video libraries)
├── .env.example                    # Environment variables template
├── README.md                       # This file
├── DEPLOYMENT.md                   # 24/7 hosting and deployment guide
├── start_bot.sh                    # Start bot in background
├── stop_bot.sh                     # Stop running bot
├── status_bot.sh                   # Check bot status
│
├── utils/                          # Utility modules
│   ├── __init__.py
│   ├── logger.py                   # Centralized logging system
│   ├── content_filter.py           # Content moderation and filtering
│   ├── rate_limiter.py             # Rate limiting and abuse prevention
│   └── conversation_logger.py      # Conversation tracking and analytics
│
├── tests/                          # Test files
│   ├── test_ai_only.py             # AI solver tests
│   ├── test_formatting.py          # Message formatting tests
│   ├── test_bot_commands.py        # Bot functionality tests
│   └── final_test.py               # Comprehensive test suite
│
├── logs/                           # Log files (created automatically)
└── temp/                           # Temporary files (created automatically)
```

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8 or higher
- Telegram Bot Token (from @BotFather)
- Google Gemini API Key
- Tesseract OCR (for image processing)

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/asrithcheepurupalli/math-tutor-bot.git
cd math-tutor-bot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Tesseract OCR
# On macOS:
brew install tesseract

# On Ubuntu/Debian:
sudo apt-get install tesseract-ocr

# On Windows:
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
```

### 3. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your API keys
nano .env
```

**Required Environment Variables:**
```env
# Bot Configuration
BOT_TOKEN=your_telegram_bot_token_here
AI_MODEL_PROVIDER=gemini

# AI API Key
GEMINI_API_KEY=your_gemini_api_key_here

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=math_tutor_bot.log

# Database Configuration
DATABASE_URL=sqlite:///math_tutor.db
```

### 4. Run the Bot

```bash
# Quick start (runs until terminal closes)
python bot.py

# OR: Start in background (recommended - survives terminal closure)
./start_bot.sh

# Check if bot is running
./status_bot.sh

# Stop the bot
./stop_bot.sh

# View live logs
tail -f bot_output.log
```

The bot will start and begin listening for messages on Telegram 24/7.

> 📖 **For 24/7 operation and deployment options, see [DEPLOYMENT.md](DEPLOYMENT.md)**

## 📱 Usage

### Getting Started
1. Start a chat with your bot on Telegram
2. Send `/start` to see welcome message and demo questions
3. Click on demo question buttons or type your own math problem
4. Send photos of handwritten math problems for OCR processing

### Bot Commands
- `/start` - Welcome message with interactive demo questions
- `/help` - Show usage instructions and examples  
- `/about` - Information about the bot and its features

### Example Interactions

**Demo Questions (Clickable Buttons):**
- "Solve: 2x + 5 = 15"
- "Factor: x² - 5x + 6"  
- "Find derivative of: x³ + 2x² - 5"

**Text Problems:**
```
User: Solve for x: 3x - 7 = 14
Bot: 🎯 Solution: x = 7

📋 Step-by-step explanation:
1. Add 7 to both sides: 3x - 7 + 7 = 14 + 7
2. Simplify: 3x = 21
3. Divide both sides by 3: x = 7
```

**Image Problems:**
```
User: [Sends photo of handwritten math problem]
Bot: [Uses OCR to extract text, then provides step-by-step solution]
```

**Supported Math Topics:**
- Algebra (equations, inequalities, polynomials)
- Calculus (derivatives, integrals, limits)
- Geometry (area, volume, angles)
- Trigonometry (sin, cos, tan functions)
- Statistics (mean, median, probability)
- And more!

## 🔧 API Configuration

### Telegram Bot Setup

1. Message @BotFather on Telegram
2. Create a new bot with `/newbot`
3. Get your bot token
4. Set bot commands (optional):
   ```
   /setcommands
   start - Welcome message with demo questions
   help - Show help and usage instructions
   about - Information about the bot
   ```

### Google Gemini Setup

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create an API key
3. Add `GEMINI_API_KEY=your_key_here` to your `.env` file

*Note: OpenAI integration is available but Gemini is the primary provider for this project.*

## 🔒 Security Features

### Content Filtering
- Blocks inappropriate content
- Focuses on educational math content
- Configurable keyword filtering

### Rate Limiting
- Prevents spam and abuse
- Progressive penalties for violations
- Per-user request tracking

### Privacy
- Conversation logging for improvement
- No storage of sensitive user data
- Configurable data retention policies

## 📊 Monitoring and Analytics

### Logging
- Structured JSON logging
- Conversation tracking
- Performance monitoring
- Error tracking

### Analytics Dashboard
Access analytics via the conversation logger:
```python
from utils.conversation_logger import ConversationLogger
logger = ConversationLogger()
analytics = await logger.get_analytics(days=30)
```

## 🚀 Deployment

### Local Development
```bash
# Quick start
python bot.py

# Background operation (recommended)
./start_bot.sh          # Start in background
./status_bot.sh         # Check status  
./stop_bot.sh           # Stop bot
tail -f bot_output.log  # View logs
```

### 24/7 Production Hosting
For continuous operation, see **[DEPLOYMENT.md](DEPLOYMENT.md)** for detailed guides on:

- 🆓 **Free Cloud Hosting** (Render, Railway, Heroku)
- 💰 **VPS Deployment** (DigitalOcean, AWS, etc.)
- 🐳 **Docker Containers**
- 🔄 **Auto-restart & Monitoring**
- 🖥️ **Local Auto-start on Boot**

### Production Deployment

#### Using Docker (Recommended)
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

#### Cloud Deployment Options
- **Heroku**: Use the included `Procfile`
- **Google Cloud Run**: Containerized deployment
- **AWS EC2**: Virtual machine deployment
- **DigitalOcean**: Droplet deployment

### Environment Variables for Production
```env
# Production settings
LOG_LEVEL=INFO
ENABLE_CONTENT_FILTER=true
RATE_LIMIT_REQUESTS=10
RATE_LIMIT_WINDOW=60
DATABASE_URL=sqlite:///math_tutor.db
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests if applicable
5. Commit changes: `git commit -am 'Add feature'`
6. Push to branch: `git push origin feature-name`
7. Submit a pull request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add type hints to new functions
- Write tests for new features
- Update documentation as needed

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Troubleshooting

### Common Issues

**Bot not responding:**
- Check bot token in `.env`
- Verify internet connection  
- Check logs for errors: `tail -f math_tutor_bot.log`

**OCR not working:**
- Ensure Tesseract is installed: `tesseract --version`
- Verify image quality (clear, well-lit photos work best)
- Check supported image formats (PNG, JPG, WebP)

**AI responses not working:**
- Verify Gemini API key is correct
- Check API usage limits and quotas
- Monitor API rate limiting

**Formatting issues:**
- Bot now uses plain text formatting to avoid Telegram parsing errors
- Check recent logs for specific error messages

### Getting Help

1. Check the logs in `math_tutor_bot.log`
2. Review environment variable configuration in `.env`
3. Test individual components with the test scripts:
   - `python test_ai_only.py` - Test AI solver
   - `python final_test.py` - Comprehensive test
4. Create an issue on GitHub with error details

## 🔄 Updates and Maintenance

### Regular Maintenance
- Monitor log file sizes: `ls -lah *.log`
- Update dependencies regularly: `pip install -r requirements.txt --upgrade`
- Review rate limiting settings based on usage
- Clean up temporary files

### Backup Recommendations
- Backup conversation database (`math_tutor.db`)
- Save configuration files (`.env`)
- Document custom modifications

## 📈 Roadmap

### Completed Features ✅
- [x] Google Gemini AI integration
- [x] Interactive demo questions with clickable buttons
- [x] OCR support for handwritten problems  
- [x] Step-by-step solution explanations
- [x] Robust error handling and message formatting
- [x] Rate limiting and content filtering
- [x] Comprehensive test suite

### Planned Features 🚧
- [ ] WhatsApp integration
- [ ] Voice message support
- [ ] Multi-language support
- [ ] Advanced graphing capabilities
- [ ] Interactive problem sets
- [ ] Video explanations (future enhancement)
- [ ] Teacher dashboard
- [ ] Student progress tracking

### Version History
- **v1.0.0**: Initial release with Telegram and Gemini AI
- **v1.1.0**: Interactive demo questions and improved formatting  
- **v1.2.0**: WhatsApp support (planned)
- **v2.0.0**: Video generation re-integration (planned)

---

**🎓 Made with ❤️ for students and educators worldwide**

**Repository**: https://github.com/asrithcheepurupalli/math-tutor-bot

For questions or support, please create an issue on GitHub.
