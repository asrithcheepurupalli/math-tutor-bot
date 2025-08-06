#!/usr/bin/env python3
"""
Simple bot test to verify the new features work
"""

import asyncio
import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

load_dotenv()

async def start(update: Update, context):
    """Test the new start command with demo questions"""
    user = update.effective_user
    welcome_message = f"""
🤖 **Welcome to Math Tutor Bot, {user.first_name}!**

I'm your AI-powered math tutor ready to help you solve problems step-by-step.

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

async def demo_callback(update: Update, context):
    """Handle demo button clicks"""
    query = update.callback_query
    await query.answer()
    
    demo_questions = {
        "demo_basic_addition": "**Demo:** 2 + 2 = 4\n\nThis is basic addition!",
        "demo_quadratic": "**Demo:** x² - 5x + 6 = 0\n\nFactoring: (x-2)(x-3) = 0\nSolutions: x = 2 or x = 3",
        "demo_derivative": "**Demo:** d/dx(x³ + 2x) = 3x² + 2",
        "demo_pythagoras": "**Demo:** For legs 3 and 4:\nc² = 3² + 4² = 9 + 16 = 25\nc = 5",
        "demo_fact": "**Math Fact:** π (pi) ≈ 3.14159... is the ratio of a circle's circumference to its diameter!"
    }
    
    if query.data in demo_questions:
        response = demo_questions[query.data]
        await query.edit_message_text(response, parse_mode='Markdown')

def main():
    """Run the simple test bot"""
    token = os.getenv('BOT_TOKEN')
    
    # Create application
    app = Application.builder().token(token).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(demo_callback))
    
    # Run the bot
    print("Starting simple test bot...")
    app.run_polling()

if __name__ == '__main__':
    main()
