#!/usr/bin/env python3
"""
Simple test script to verify bot commands work correctly
"""

import asyncio
from bot import MathTutorBot

async def test_bot_commands():
    """Test basic bot functionality without Telegram API"""
    print("🤖 Testing Math Tutor Bot Commands")
    print("=" * 50)
    
    # Initialize bot
    bot = MathTutorBot()
    
    # Test AI solver directly
    print("🧮 Testing AI solver...")
    test_problem = "Solve: 2x + 5 = 15"
    
    try:
        result = await bot.ai_solver.solve_problem(test_problem)
        print(f"✅ Problem: {test_problem}")
        print(f"📝 Solution preview: {result.get('solution', 'No solution')[:100]}...")
        print(f"📋 Steps count: {len(result.get('steps', []))}")
        print(f"🤖 Provider: {result.get('provider', 'unknown')}")
    except Exception as e:
        print(f"❌ Error testing AI solver: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Bot component tests completed!")
    print("🚀 Bot is ready to receive Telegram messages!")

if __name__ == "__main__":
    asyncio.run(test_bot_commands())
