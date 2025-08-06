# Math Tutor Bot with Google Veo Integration

A sophisticated AI-powered math tutoring chatbot that provides step-by-step solutions and creates personalized educational videos using Google Veo API.

## Features

### Core Capabilities
- **Multi-Platform Support**: Works on Telegram and WhatsApp
- **AI-Powered Solutions**: Uses OpenAI GPT or Google Gemini for step-by-step math problem solving
- **Video Explanations**: Generates educational videos using Google Veo API (with local fallback)
- **OCR Support**: Extracts math problems from images using Tesseract and EasyOCR
- **LaTeX Formatting**: Supports mathematical notation and expressions
- **Conversation Logging**: Tracks interactions for analytics and improvement

### Advanced Features
- **Content Filtering**: Ensures educational and appropriate content
- **Rate Limiting**: Prevents abuse with progressive penalties
- **Image Processing**: Accepts handwritten or printed math problems via photos
- **Modular Architecture**: Clean separation of concerns for easy maintenance
- **Error Handling**: Robust error handling with graceful fallbacks

## 🛠 Tech Stack

- **Backend**: Python 3.8+
- **Bot Framework**: python-telegram-bot
- **AI Models**: OpenAI GPT-4 / Google Gemini
- **Video Generation**: Google Veo API / MoviePy (fallback)
- **OCR**: Tesseract, EasyOCR
- **Database**: SQLite (configurable)
- **Image Processing**: OpenCV, PIL
- **Math Visualization**: Matplotlib, SymPy

## 📁 Project Structure

```
math-tutor/
├── bot.py                          # Main bot logic and message handling
├── ai_solver.py                    # AI model integration for problem solving
├── video_generator.py              # Google Veo API and local video generation
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── README.md                       # This file
│
├── utils/                          # Utility modules
│   ├── __init__.py
│   ├── logger.py                   # Logging configuration
│   ├── content_filter.py           # Content moderation
│   ├── rate_limiter.py             # Rate limiting and abuse prevention
│   └── conversation_logger.py      # Conversation tracking and analytics
│
├── logs/                           # Log files (created automatically)
├── generated_videos/               # Generated video files (created automatically)
└── temp/                           # Temporary files (created automatically)
```

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8 or higher
- Telegram Bot Token (from @BotFather)
- OpenAI API Key or Google Gemini API Key
- Google Cloud Project with Veo API access (optional)
- Tesseract OCR installed on your system

### 2. Installation

```bash
# Clone the repository
git clone <repository-url>
cd math-tutor

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

# Edit .env with your API keys and configuration
nano .env
```

**Required Environment Variables:**
```env
# Bot Configuration
BOT_TOKEN=your_telegram_bot_token_here
AI_MODEL_PROVIDER=openai  # or gemini

# AI API Keys
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here

# Google Veo (Optional)
GOOGLE_CLOUD_PROJECT_ID=your_project_id
GOOGLE_VEO_API_KEY=your_veo_api_key
```

### 4. Run the Bot

```bash
# Start the bot
python bot.py
```

The bot will start and begin listening for messages on Telegram.

## 📱 Usage

### Getting Started
1. Start a chat with your bot on Telegram
2. Send `/start` to see the welcome message
3. Send any math problem as text or image

### Example Interactions

**Text Problems:**
```
User: Solve for x: 2x + 5 = 15
Bot: [Provides step-by-step solution and video explanation]

User: Find the derivative of f(x) = x² + 3x + 2
Bot: [Shows differentiation steps with visual explanation]
```

**Image Problems:**
```
User: [Sends photo of handwritten math problem]
Bot: [Uses OCR to extract text, then solves and creates video]
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
   start - Welcome message and introduction
   help - Show help and usage instructions
   about - Information about the bot
   ```

### OpenAI API Setup

1. Visit [OpenAI API](https://platform.openai.com/api-keys)
2. Create an API key
3. Add to your `.env` file

### Google Gemini Setup

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create an API key
3. Add to your `.env` file

### Google Veo API Setup (Optional)

1. Create a Google Cloud Project
2. Enable the Video Intelligence API
3. Create a service account and download credentials
4. Set `GOOGLE_CLOUD_CREDENTIALS_PATH` in `.env`

*Note: Google Veo is still in limited preview. The bot includes a local video generation fallback using MoviePy.*

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
python bot.py
```

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

#### Using systemd (Linux)
```ini
[Unit]
Description=Math Tutor Bot
After=network.target

[Service]
Type=simple
User=mathbot
WorkingDirectory=/opt/math-tutor
ExecStart=/opt/math-tutor/venv/bin/python bot.py
Restart=always

[Install]
WantedBy=multi-user.target
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
DATABASE_URL=postgresql://user:pass@host:5432/mathtutor
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
- Check logs for errors

**OCR not working:**
- Ensure Tesseract is installed
- Check `TESSERACT_PATH` in `.env`
- Verify image quality

**Video generation failing:**
- Check Google Veo API credentials
- Verify MoviePy installation
- Check disk space in `VIDEO_OUTPUT_DIR`

**AI responses not working:**
- Verify API keys are correct
- Check API rate limits
- Monitor API usage

### Getting Help

1. Check the logs in the `logs/` directory
2. Review environment variable configuration
3. Test individual components separately
4. Create an issue on GitHub with error details

## 🔄 Updates and Maintenance

### Regular Maintenance
- Clean up old video files
- Monitor log file sizes
- Update dependencies regularly
- Review rate limiting settings

### Backup Recommendations
- Backup conversation database
- Save configuration files
- Document custom modifications

## 📈 Roadmap

### Planned Features
- [ ] WhatsApp integration
- [ ] Voice message support
- [ ] Multi-language support
- [ ] Advanced graphing capabilities
- [ ] Interactive problem sets
- [ ] Teacher dashboard
- [ ] Student progress tracking

### Version History
- **v1.0.0**: Initial release with Telegram support
- **v1.1.0**: Added Google Veo integration (planned)
- **v1.2.0**: WhatsApp support (planned)

---

**Made with ❤️ for students and educators worldwide**

For more information, visit our [documentation](docs/) or contact support.
# math-tutor-bot
