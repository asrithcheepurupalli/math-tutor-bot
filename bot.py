"""
Core bot logic for Math Tutor Bot
Handles messaging interface for both WhatsApp and Telegram
"""

import asyncio
import asyncio
import logging
import os
from typing import Optional, Dict, Any
from datetime import datetime

from telegram import Update, Message, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters, CallbackQueryHandler
from dotenv import load_dotenv
import json

from ai_solver import AISolver
from utils.logger import setup_logger
from utils.content_filter import ContentFilter
from utils.rate_limiter import RateLimiter
from utils.conversation_logger import ConversationLogger

# Load environment variables
load_dotenv()

class MathTutorBot:
    def __init__(self):
        self.bot_token = os.getenv('BOT_TOKEN')
        self.ai_solver = AISolver()
        self.content_filter = ContentFilter()
        self.rate_limiter = RateLimiter()
        self.conversation_logger = ConversationLogger()
        
        # Setup logging
        self.logger = setup_logger(__name__)
        
        # Initialize Telegram bot
        self.application = Application.builder().token(self.bot_token).build()
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup message and command handlers"""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("about", self.about_command))
        
        # Message handlers
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text_message))
        self.application.add_handler(MessageHandler(filters.PHOTO, self.handle_photo_message))
        
        # Callback query handler for demo questions
        self.application.add_handler(CallbackQueryHandler(self.handle_demo_question))
        
        # Error handler
        self.application.add_error_handler(self.error_handler)
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        welcome_message = f"""
� **Welcome to Math Tutor Bot, {user.first_name}!**

I'm your AI-powered math tutor ready to help you solve problems step-by-step.

**How to use:**
• Send me any math problem as text
• Upload a photo of handwritten math problems  
• Get detailed explanations and solutions

**🎥 Video explanations coming soon!**

**Try these demo questions to get started:**
👇 Click any button below to see a sample solution!
        """
        
        # Create inline keyboard with demo questions
        keyboard = [
            [InlineKeyboardButton("🔢 What is 2 + 2?", callback_data="demo_basic_addition")],
            [InlineKeyboardButton("📐 Solve: x² - 5x + 6 = 0", callback_data="demo_quadratic")],
            [InlineKeyboardButton("📊 Find derivative of x³ + 2x", callback_data="demo_derivative")],
            [InlineKeyboardButton("🔺 Pythagorean theorem example", callback_data="demo_pythagoras")],
            [InlineKeyboardButton("💡 Random math fact", callback_data="demo_fact")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_message, 
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
        
        # Log conversation
        await self.conversation_logger.log_interaction(
            user_id=user.id,
            username=user.username,
            message_type="command",
            content="/start",
            response=welcome_message
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_message = """
🆘 **Math Tutor Bot Help**

**Commands:**
• /start - Welcome message with demo questions
• /help - Show this help message
• /about - Information about the bot

**How to use:**
1. **Text Problems**: Simply type your math problem
2. **Photo Problems**: Send a clear photo of the math problem
3. **Demo Questions**: Use /start to try sample problems
4. **Supported Math Types**: Algebra, Calculus, Geometry, Statistics, and more

**Tips for better results:**
• Be specific with your questions
• Use proper mathematical notation when possible
• For photos, ensure good lighting and clear text
• One problem per message works best

**Example Questions:**
• "Solve: x² - 5x + 6 = 0"
• "Integrate: ∫(2x + 3)dx"
• "Find the slope of the line passing through (1,2) and (3,8)"

**🎥 Video explanations coming soon!**

Need help? Contact support or check our documentation.
        """
        
        await update.message.reply_text(help_message)
    
    async def about_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /about command"""
        about_message = """
🤖 **About Math Tutor Bot**

**Version**: 1.0.0
**Powered by**: Google Gemini AI
**Features**: AI-powered math solving with step-by-step explanations

**Current Capabilities:**
• Step-by-step problem solving
• OCR for handwritten problems
• LaTeX mathematical formatting
• Multiple math subjects support
• Interactive demo questions

**Upcoming Features:**
• 🎥 Video explanations (coming soon!)
• Advanced visualization
• Graphing capabilities

**Privacy & Safety:**
• Conversations are logged for improvement
• Content filtering for appropriate use
• Rate limiting to ensure fair usage

**Technology Stack:**
• AI: Google Gemini
• OCR: Tesseract & EasyOCR
• Platform: Python + Telegram Bot API

Created with ❤️ for students and math enthusiasts!
        """
        
        await update.message.reply_text(about_message)
    
    async def handle_text_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages containing math problems"""
        user = update.effective_user
        message_text = update.message.text
        
        self.logger.info(f"Received message from user {user.id}: {message_text}")
        
        try:
            # Check rate limiting
            if not await self.rate_limiter.check_rate_limit(user.id):
                await update.message.reply_text(
                    "⏱️ You're sending messages too quickly. Please wait a moment before trying again."
                )
                return
            
            # Content filtering
            if not self.content_filter.is_appropriate(message_text):
                await update.message.reply_text(
                    "❌ Your message contains inappropriate content. Please send math-related questions only."
                )
                return
            
            # Send "thinking" message
            thinking_message = await update.message.reply_text(
                "🤔 Analyzing your math problem... This may take a moment."
            )
            
            self.logger.info("About to call AI solver...")
            
            # Solve the math problem
            solution_data = await self.ai_solver.solve_problem(message_text)
            
            self.logger.info(f"AI solver returned: {type(solution_data)}, is None: {solution_data is None}")
            
            if not solution_data:
                self.logger.warning("Solution data is None or empty")
                await thinking_message.edit_text(
                    "❌ I couldn't solve this problem. Please make sure it's a valid math question and try again."
                )
                return
            
            # Send solution
            solution_text = self._format_solution(solution_data)
            await thinking_message.edit_text("✅ Solution ready!")
            await update.message.reply_text(solution_text)
            
            # Delete the thinking message after a moment
            await asyncio.sleep(1)
            await thinking_message.delete()
            
            # Log the conversation
            await self.conversation_logger.log_interaction(
                user_id=user.id,
                username=user.username,
                message_type="text_problem",
                content=message_text,
                response=solution_data,
                video_generated=False  # Video generation disabled for now
            )
            
        except Exception as e:
            self.logger.error(f"Error handling text message: {str(e)}")
            await update.message.reply_text(
                "❌ An error occurred while processing your request. Please try again later."
            )
    
    async def handle_photo_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle photo messages containing math problems"""
        user = update.effective_user
        
        try:
            # Check rate limiting
            if not await self.rate_limiter.check_rate_limit(user.id):
                await update.message.reply_text(
                    "⏱️ You're sending messages too quickly. Please wait a moment before trying again."
                )
                return
            
            # Send processing message
            processing_message = await update.message.reply_text(
                "📸 Processing your image... Extracting text using OCR..."
            )
            
            # Download and process the image
            photo = update.message.photo[-1]  # Get highest resolution
            file = await context.bot.get_file(photo.file_id)
            
            # Create temp directory if it doesn't exist
            os.makedirs("temp", exist_ok=True)
            image_path = f"temp/math_problem_{user.id}_{datetime.now().timestamp()}.jpg"
            
            await file.download_to_drive(image_path)
            
            # Extract text using OCR
            extracted_text = await self.ai_solver.extract_text_from_image(image_path)
            
            if not extracted_text:
                await processing_message.edit_text(
                    "❌ I couldn't extract text from your image. Please ensure the image is clear and contains readable math problems."
                )
                os.remove(image_path)
                return
            
            await processing_message.edit_text(
                f"✅ Text extracted: '{extracted_text}'\n\n🤔 Now solving the problem..."
            )
            
            # Solve the extracted problem
            solution_data = await self.ai_solver.solve_problem(extracted_text)
            
            if not solution_data:
                await processing_message.edit_text(
                    "❌ I couldn't solve the extracted problem. Please verify the image contains a valid math question."
                )
                os.remove(image_path)
                return
            
            # Update status
            await processing_message.edit_text(
                "✅ Solution found! Preparing response..."
            )
            
            # Send text solution
            solution_text = f"**Extracted Problem:** {extracted_text}\n\n{self._format_solution(solution_data)}"
            await update.message.reply_text(solution_text, parse_mode='Markdown')
            
            # Delete processing message
            await processing_message.delete()
            
            # Clean up
            os.remove(image_path)
            
            # Log conversation
            await self.conversation_logger.log_interaction(
                user_id=user.id,
                username=user.username,
                message_type="image_problem",
                content=f"Image OCR: {extracted_text}",
                response=solution_data,
                video_generated=False  # Video generation removed
            )
            
        except Exception as e:
            self.logger.error(f"Error handling photo message: {str(e)}")
            await update.message.reply_text(
                "❌ An error occurred while processing your image. Please try again."
            )
    
    async def handle_demo_question(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle demo question button clicks"""
        query = update.callback_query
        await query.answer()
        
        demo_questions = {
            "demo_basic_addition": "What is 2 + 2?",
            "demo_quadratic": "Solve: x² - 5x + 6 = 0",
            "demo_derivative": "Find the derivative of x³ + 2x",
            "demo_pythagoras": "In a right triangle, if one leg is 3 and the other is 4, what is the hypotenuse?",
            "demo_fact": "What is the mathematical constant π (pi)?"
        }
        
        if query.data in demo_questions:
            question = demo_questions[query.data]
            
            # Send the demo question as if user typed it
            await query.edit_message_text(
                f"📝 **Demo Question:** {question}\n\n🤔 Let me solve this for you..."
            )
            
            # Process the demo question
            await self._solve_and_respond(query, question, is_demo=True)

    async def _solve_and_respond(self, query_or_update, problem_text: str, is_demo: bool = False):
        """Common method to solve problems and respond"""
        try:
            # Solve the math problem
            solution_data = await self.ai_solver.solve_problem(problem_text)
            
            if not solution_data:
                if is_demo:
                    await query_or_update.edit_message_text(
                        "❌ I couldn't solve this demo problem. Please try again later."
                    )
                else:
                    await query_or_update.message.reply_text(
                        "❌ I couldn't solve this problem. Please make sure it's a valid math question and try again."
                    )
                return
            
            # Format and send solution
            solution_text = self._format_solution(solution_data)
            
            if is_demo:
                # For demo questions, edit the message
                await query_or_update.edit_message_text(solution_text, parse_mode='Markdown')
                
                # Add a "Try your own question" button
                keyboard = [[InlineKeyboardButton("❓ Ask your own question", callback_data="ask_own")]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await query_or_update.message.reply_text(
                    "✨ **Want to try your own question?** Just type any math problem!",
                    reply_markup=reply_markup
                )
            else:
                await query_or_update.message.reply_text(solution_text, parse_mode='Markdown')
                
        except Exception as e:
            self.logger.error(f"Error solving problem: {str(e)}")
            error_msg = "❌ An error occurred while processing your request. Please try again later."
            
            if is_demo:
                await query_or_update.edit_message_text(error_msg)
            else:
                await query_or_update.message.reply_text(error_msg)
    
    def _format_solution(self, solution_data: Dict[str, Any]) -> str:
        """Format solution data for display"""
        try:
            # Clean the solution
            solution = str(solution_data.get('solution', 'No solution provided'))
            
            formatted = f"🎯 Solution:\n{solution}\n\n"
            
            if solution_data.get('steps'):
                formatted += "📋 Step-by-step explanation:\n"
                step_count = 1
                for step in solution_data['steps']:
                    # Clean step text and remove malformed JSON parts
                    step_text = str(step).strip()
                    if step_text.startswith('"') and step_text.endswith('",'):
                        step_text = step_text[1:-2]  # Remove quotes and comma
                    elif step_text.startswith('"') and step_text.endswith('"'):
                        step_text = step_text[1:-1]  # Remove quotes
                    
                    # Skip malformed entries
                    if step_text in ['"steps": [', ''] or len(step_text) < 10:
                        continue
                        
                    # Remove bold markdown formatting
                    step_text = step_text.replace('**', '')
                    
                    formatted += f"{step_count}. {step_text}\n\n"
                    step_count += 1
            
            if solution_data.get('latex'):
                latex = str(solution_data['latex'])
                formatted += f"📐 LaTeX: {latex}"
            
            return formatted
            
        except Exception as e:
            self.logger.error(f"Error formatting solution: {str(e)}")
            return "❌ Error formatting the solution. The problem was solved but couldn't be displayed properly."
    
    def _escape_markdown(self, text: str) -> str:
        """Escape markdown characters for Telegram"""
        # Remove markdown formatting that might conflict
        text = text.replace('**', '')  # Remove bold markers
        text = text.replace('__', '')  # Remove underline markers
        text = text.replace('*', '\\*')  # Escape asterisks
        text = text.replace('_', '\\_')  # Escape underscores
        text = text.replace('[', '\\[')  # Escape square brackets
        text = text.replace(']', '\\]')  # Escape square brackets
        text = text.replace('(', '\\(')  # Escape parentheses
        text = text.replace(')', '\\)')  # Escape parentheses
        text = text.replace('`', '\\`')  # Escape backticks
        return text
    
    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        self.logger.error(f"Exception while handling an update: {context.error}")
    
    def run(self):
        """Start the bot"""
        self.logger.info("Starting Math Tutor Bot...")
        self.application.run_polling()

if __name__ == "__main__":
    bot = MathTutorBot()
    bot.logger.info("Starting Math Tutor Bot...")
    bot.application.run_polling()
