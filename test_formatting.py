#!/usr/bin/env python3
"""
Test the bot formatting with problematic AI responses
"""

import asyncio
from bot import MathTutorBot

async def test_formatting():
    """Test the formatting function with known problematic data"""
    print("🧮 Testing Bot Message Formatting")
    print("=" * 50)
    
    bot = MathTutorBot()
    
    # Create test data that mimics the problematic response
    test_data = {
        'solution': 'x = 2 or x = 3',
        'steps': [
            '"steps": [',
            '"Step 1: **Factor the quadratic expression.** We are looking for two numbers that add up to -5 (the coefficient of x) and multiply to 6 (the constant term). These numbers are -2 and -3.  Therefore, we can rewrite the equation as (x - 2)(x - 3) = 0.",',
            '"Step 2: **Apply the Zero Product Property.** The Zero Product Property states that if the product of two factors is zero, then at least one of the factors must be zero.  This means either (x - 2) = 0 or (x - 3) = 0.",',
            '"Step 3: **Solve for x in each case.** For (x - 2) = 0, we add 2 to both sides to get x = 2. For (x - 3) = 0, we add 3 to both sides to get x = 3."'
        ],
        'latex': '\\(x^2 - 5x + 6 = 0\\)',
        'original_problem': 'Test problem'
    }
    
    print("🔧 Testing problematic formatting...")
    try:
        formatted_text = bot._format_solution(test_data)
        print("✅ Formatting successful!")
        print("📝 Formatted output:")
        print("-" * 40)
        print(formatted_text)
        print("-" * 40)
        print(f"📏 Length: {len(formatted_text)} characters")
        
        # Check for potential issues
        issues = []
        if '**' in formatted_text:
            issues.append("Contains unescaped markdown")
        if '"steps": [' in formatted_text:
            issues.append("Contains malformed JSON")
        if len(formatted_text) > 4096:
            issues.append("Message too long for Telegram")
            
        if issues:
            print(f"⚠️ Potential issues found: {', '.join(issues)}")
        else:
            print("✅ No formatting issues detected!")
            
    except Exception as e:
        print(f"❌ Formatting failed: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Formatting test completed!")

if __name__ == "__main__":
    asyncio.run(test_formatting())
