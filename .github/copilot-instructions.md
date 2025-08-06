<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Math Tutor Bot - Copilot Instructions

This is a Python-based AI math tutoring chatbot with Google Veo integration. When working on this project, please follow these guidelines:

## Project Context
- **Purpose**: AI-powered math tutor bot for Telegram/WhatsApp that generates step-by-step solutions and educational videos
- **Architecture**: Modular design with separate components for bot logic, AI solving, and video generation
- **AI Integration**: OpenAI GPT-4 or Google Gemini for problem solving, Google Veo for video generation
- **Key Features**: OCR for image problems, LaTeX support, content filtering, rate limiting, conversation logging

## Code Style Guidelines
- Follow PEP 8 Python style guidelines
- Use type hints for all function parameters and return values
- Write descriptive docstrings for all functions and classes
- Use async/await patterns for I/O operations
- Implement proper error handling with try/catch blocks
- Use logging instead of print statements

## Architecture Patterns
- **Separation of Concerns**: Keep bot logic, AI solving, and video generation separate
- **Dependency Injection**: Pass dependencies through constructors
- **Configuration**: Use environment variables for all configurable settings
- **Error Handling**: Implement graceful fallbacks for API failures
- **Logging**: Use structured logging with appropriate log levels

## AI Integration Best Practices
- Always validate AI responses before processing
- Implement fallback mechanisms for API failures
- Use appropriate prompts for mathematical problem solving
- Parse structured responses when possible (JSON format preferred)
- Handle rate limiting and API errors gracefully

## Video Generation Guidelines
- Implement Google Veo integration with local fallback
- Keep video duration reasonable (under 60 seconds)
- Use clear, educational visual elements
- Implement proper cleanup of temporary files
- Handle video processing errors gracefully

## Security Considerations
- Validate and sanitize all user inputs
- Implement content filtering for educational focus
- Use rate limiting to prevent abuse
- Don't log sensitive information (API keys, tokens)
- Implement proper access controls where needed

## Testing Approach
- Write unit tests for utility functions
- Mock external API calls in tests
- Test error conditions and edge cases
- Validate OCR functionality with sample images
- Test video generation fallback mechanisms

## Performance Optimization
- Use async operations for I/O bound tasks
- Implement proper connection pooling for APIs
- Cache frequently used data where appropriate
- Clean up temporary files and old videos
- Monitor memory usage during video generation

## Dependencies Management
- Pin dependency versions in requirements.txt
- Use virtual environments for development
- Document system dependencies (Tesseract, etc.)
- Keep dependencies up to date for security

## Specific to Math Problems
- Support various mathematical notation formats
- Handle LaTeX expressions properly
- Provide clear step-by-step explanations
- Support multiple problem types (algebra, calculus, geometry, etc.)
- Validate mathematical expressions before processing

## Integration Patterns
- Use proper async patterns for Telegram bot integration
- Implement webhook handling for production deployment
- Handle file uploads and downloads properly
- Manage conversation state appropriately

When suggesting code improvements or new features, consider:
1. Impact on system performance and scalability
2. Educational value for users
3. Maintainability and code clarity
4. Security implications
5. User experience improvements
