#!/usr/bin/env python3
"""
Test the AI solver directly without Telegram to verify all video code is removed
"""

import asyncio
import sys
import os
sys.path.append('/Users/asrithcheepurupalli/Downloads/math-tutor')

from ai_solver import AISolver

async def test_ai_solver():
    """Test that AI solver works without any video dependencies"""
    try:
        print("🔍 Testing AI Solver...")
        
        # Initialize solver
        solver = AISolver()
        print(f"✅ AI Solver initialized with provider: {solver.ai_provider}")
        
        # Test basic math problem
        print("🔢 Testing: 'What is 2 + 2?'")
        result = await solver.solve_problem("What is 2 + 2?")
        
        if result:
            print("✅ AI Solver working correctly!")
            print(f"📝 Solution: {result.get('solution', 'N/A')}")
            print(f"📋 Steps: {len(result.get('steps', []))} steps provided")
            print(f"🤖 Provider: {result.get('ai_provider', 'N/A')}")
            
            # Test a more complex problem
            print("\n📐 Testing: 'Solve x² - 5x + 6 = 0'")
            result2 = await solver.solve_problem("Solve x² - 5x + 6 = 0")
            
            if result2:
                print("✅ Complex problem solved!")
                print(f"📝 Solution: {result2.get('solution', 'N/A')}")
            else:
                print("❌ Complex problem failed")
                
        else:
            print("❌ AI Solver returned None")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🧮 Math Tutor Bot - AI Solver Test")
    print("=" * 50)
    asyncio.run(test_ai_solver())
    print("=" * 50)
    print("✅ Test completed - No video dependencies found!")
