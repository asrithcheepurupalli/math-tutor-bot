# Math Tutor Bot - Development Guide

## Development Setup

### Prerequisites
1. Python 3.8+ installed
2. Tesseract OCR installed
3. Git (optional but recommended)
4. VS Code with Python extension

### Quick Start
```bash
# Clone and setup
git clone <repository-url>
cd math-tutor

# Run setup script
python setup.py

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Test components
python test_components.py

# Run the bot
python bot.py
```

## Architecture Overview

### Core Components

1. **bot.py** - Main Telegram bot logic
   - Message handling and routing
   - User interaction management
   - Integration with other modules

2. **ai_solver.py** - AI problem solving
   - OpenAI GPT / Google Gemini integration
   - OCR text extraction
   - Mathematical problem parsing

3. **video_generator.py** - Video creation
   - Google Veo API integration
   - Local video generation fallback
   - Educational content creation

4. **utils/** - Utility modules
   - Logging and monitoring
   - Content filtering and safety
   - Rate limiting and abuse prevention
   - Conversation tracking

### Data Flow

```
User Message → Content Filter → Rate Limiter → AI Solver → Video Generator → Response
                    ↓
               Conversation Logger
```

## Development Guidelines

### Code Style
- Follow PEP 8 Python style guidelines
- Use type hints for all functions
- Write comprehensive docstrings
- Implement proper error handling

### Testing
```bash
# Run component tests
python test_components.py

# Format code
python -m black .

# Lint code
python -m flake8 . --max-line-length=88 --extend-ignore=E203,W503

# Type checking
python -m mypy bot.py ai_solver.py video_generator.py
```

### Environment Variables

#### Required
- `BOT_TOKEN` - Telegram bot token
- `AI_MODEL_PROVIDER` - openai or gemini
- `OPENAI_API_KEY` or `GEMINI_API_KEY` - AI service API key

#### Optional
- `GOOGLE_VEO_API_KEY` - For video generation
- `LOG_LEVEL` - Logging verbosity
- `RATE_LIMIT_REQUESTS` - Max requests per minute
- `VIDEO_OUTPUT_DIR` - Video storage location

## Adding New Features

### 1. New AI Model Integration

```python
# In ai_solver.py
class AISolver:
    def __init__(self):
        # Add new provider
        if self.ai_provider == 'new_provider':
            self.new_client = NewProviderClient()
    
    async def _solve_with_new_provider(self, prompt: str) -> str:
        # Implement new provider logic
        pass
```

### 2. New Message Platform

```python
# Create new_platform_bot.py
class NewPlatformBot:
    def __init__(self):
        self.ai_solver = AISolver()
        self.video_generator = VideoGenerator()
        # Platform-specific setup
    
    async def handle_message(self, message):
        # Platform-specific message handling
        pass
```

### 3. New Video Generation Method

```python
# In video_generator.py
async def _create_with_new_method(self, script, problem, user_id):
    # Implement new video generation method
    pass
```

## Deployment Options

### 1. Local Development
```bash
python bot.py
```

### 2. Docker
```bash
# Build and run
docker build -t math-tutor-bot .
docker run -d --env-file .env math-tutor-bot

# Using docker-compose
docker-compose up -d
```

### 3. Cloud Deployment

#### Heroku
```bash
# Install Heroku CLI
heroku create math-tutor-bot
heroku config:set BOT_TOKEN=your_token
heroku config:set OPENAI_API_KEY=your_key
git push heroku main
```

#### Google Cloud Run
```bash
# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT_ID/math-tutor-bot
gcloud run deploy --image gcr.io/PROJECT_ID/math-tutor-bot
```

#### AWS EC2
```bash
# Setup on EC2 instance
sudo apt update
sudo apt install python3 python3-pip tesseract-ocr
git clone <repository>
cd math-tutor
python3 setup.py
```

## Monitoring and Maintenance

### Logs
- Application logs: `logs/math_tutor_bot.log`
- Conversation logs: `logs/conversations_YYYY_MM.jsonl`
- Error tracking in structured JSON format

### Performance Monitoring
```python
# Check bot statistics
from utils.conversation_logger import ConversationLogger
logger = ConversationLogger()
stats = await logger.get_analytics(days=7)
print(stats)
```

### Database Maintenance
```python
# Clean up old data
from utils.conversation_logger import ConversationLogger
logger = ConversationLogger()
logger.cleanup_old_logs(days_to_keep=90)

# Clean up old videos
from video_generator import VideoGenerator
generator = VideoGenerator()
generator.cleanup_old_videos(max_age_hours=24)
```

## Troubleshooting

### Common Issues

#### Bot not responding
1. Check bot token in `.env`
2. Verify internet connectivity
3. Check logs for errors: `tail -f logs/math_tutor_bot.log`

#### OCR not working
1. Verify Tesseract installation: `tesseract --version`
2. Check path in environment: `echo $TESSERACT_PATH`
3. Test with clear, high-contrast images

#### Video generation failing
1. Check Google Veo API credentials
2. Verify MoviePy installation
3. Check disk space in video output directory
4. Monitor memory usage during generation

#### AI responses failing
1. Verify API keys are correct and active
2. Check API rate limits and usage
3. Monitor API service status
4. Test with simpler problems first

### Debug Mode
```bash
# Run with debug logging
LOG_LEVEL=DEBUG python bot.py

# Test individual components
python -c "
import asyncio
from ai_solver import AISolver
solver = AISolver()
result = asyncio.run(solver.solve_problem('2+2'))
print(result)
"
```

### Performance Profiling
```python
# Profile video generation
import cProfile
import pstats

def profile_video_generation():
    # Your video generation code here
    pass

cProfile.run('profile_video_generation()', 'video_profile.stats')
stats = pstats.Stats('video_profile.stats')
stats.sort_stats('cumulative').print_stats(10)
```

## Contributing

### Development Workflow
1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Make changes following coding guidelines
4. Add tests for new functionality
5. Run test suite: `python test_components.py`
6. Format code: `python -m black .`
7. Commit changes with descriptive message
8. Push and create pull request

### Code Review Checklist
- [ ] Code follows PEP 8 style guidelines
- [ ] Type hints added to new functions
- [ ] Comprehensive error handling implemented
- [ ] Tests added for new functionality
- [ ] Documentation updated
- [ ] No hardcoded secrets or API keys
- [ ] Performance impact considered

### Release Process
1. Update version numbers
2. Update CHANGELOG.md
3. Create release branch
4. Run full test suite
5. Deploy to staging environment
6. Test with real users
7. Merge to main and tag release
8. Deploy to production

## Security Considerations

### API Key Management
- Never commit API keys to version control
- Use environment variables for all secrets
- Rotate keys regularly
- Monitor API usage for anomalies

### Input Validation
- Sanitize all user inputs
- Implement content filtering
- Rate limit requests per user
- Log suspicious activity

### Data Privacy
- Minimize data collection
- Implement data retention policies
- Encrypt sensitive data
- Comply with privacy regulations

## Support and Resources

### Documentation
- Main README: `README.md`
- API documentation: Generated from docstrings
- Environment setup: `.env.example`

### Community
- GitHub Issues: Report bugs and request features
- Discussions: Community questions and ideas
- Wiki: Extended documentation and guides

### External Resources
- [Telegram Bot API Documentation](https://core.telegram.org/bots/api)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Google AI Documentation](https://ai.google.dev/)
- [MoviePy Documentation](https://moviepy.readthedocs.io/)

---

**Happy coding! 🚀**
