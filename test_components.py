"""
Example usage and testing script for Math Tutor Bot
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_ai_solver():
    """Test the AI solver module"""
    from ai_solver import AISolver
    
    solver = AISolver()
    
    # Test text problem solving
    test_problems = [
        "Solve for x: 2x + 5 = 15",
        "Find the derivative of f(x) = x^2 + 3x + 2",
        "What is the area of a circle with radius 5?",
        "Solve the quadratic equation: x^2 - 5x + 6 = 0"
    ]
    
    print("Testing AI Solver...")
    for i, problem in enumerate(test_problems, 1):
        print(f"\n{i}. Problem: {problem}")
        try:
            solution = await solver.solve_problem(problem)
            if solution:
                print(f"   Solution: {solution['solution']}")
                print(f"   Steps: {len(solution.get('steps', []))} steps provided")
            else:
                print("   Failed to solve")
        except Exception as e:
            print(f"   Error: {str(e)}")

async def test_video_generator():
    """Test the video generator module"""
    from video_generator import VideoGenerator
    
    generator = VideoGenerator()
    
    print("\nTesting Video Generator...")
    
    # Test video creation
    test_problem = "Solve for x: 2x + 5 = 15"
    test_solution = "x = 5"
    test_steps = [
        "Start with the equation: 2x + 5 = 15",
        "Subtract 5 from both sides: 2x = 10",
        "Divide both sides by 2: x = 5",
        "Check: 2(5) + 5 = 15 ✓"
    ]
    
    try:
        video_path = await generator.create_explanation_video(
            problem=test_problem,
            solution=test_solution,
            steps=test_steps,
            user_id=12345
        )
        
        if video_path:
            print(f"   Video created: {video_path}")
            
            # Get video info
            video_info = await generator.get_video_info(video_path)
            print(f"   Video info: {video_info}")
        else:
            print("   Video generation failed")
            
    except Exception as e:
        print(f"   Error: {str(e)}")

def test_content_filter():
    """Test the content filter module"""
    from utils.content_filter import ContentFilter
    
    filter_instance = ContentFilter()
    
    print("\nTesting Content Filter...")
    
    test_inputs = [
        "Solve for x: 2x + 5 = 15",
        "What is the derivative of x^2?",
        "This is inappropriate content",
        "Hello, how are you?",
        "Find the area of a triangle with base 5 and height 3"
    ]
    
    for i, text in enumerate(test_inputs, 1):
        is_appropriate = filter_instance.is_appropriate(text)
        print(f"   {i}. '{text[:30]}...' - {'✓' if is_appropriate else '✗'}")
        
        if not is_appropriate:
            suggestions = filter_instance.get_content_suggestions(text)
            for suggestion in suggestions:
                print(f"      Suggestion: {suggestion}")

async def test_rate_limiter():
    """Test the rate limiter module"""
    from utils.rate_limiter import RateLimiter
    
    limiter = RateLimiter()
    
    print("\nTesting Rate Limiter...")
    
    test_user_id = 12345
    
    # Test normal usage
    for i in range(5):
        allowed = await limiter.check_rate_limit(test_user_id)
        print(f"   Request {i+1}: {'✓' if allowed else '✗'}")
    
    # Get user status
    status = limiter.get_user_status(test_user_id)
    print(f"   User status: {status}")
    
    # Test statistics
    stats = limiter.get_statistics()
    print(f"   System stats: {stats}")

async def test_conversation_logger():
    """Test the conversation logger module"""
    from utils.conversation_logger import ConversationLogger
    
    logger = ConversationLogger()
    
    print("\nTesting Conversation Logger...")
    
    # Test logging an interaction
    try:
        await logger.log_interaction(
            user_id=12345,
            username="testuser",
            message_type="text_problem",
            content="Solve for x: 2x + 5 = 15",
            response={"solution": "x = 5", "steps": ["Step 1", "Step 2"]},
            video_generated=True,
            processing_time=2.5
        )
        print("   ✓ Interaction logged successfully")
        
        # Test getting user history
        history = await logger.get_user_history(12345, limit=5)
        print(f"   ✓ Retrieved {len(history)} history records")
        
        # Test analytics
        analytics = await logger.get_analytics(days=30)
        print(f"   ✓ Analytics: {analytics}")
        
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")

def create_test_image():
    """Create a test image with math problem for OCR testing"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        import os
        
        # Create a simple image with math text
        img = Image.new('RGB', (400, 200), color='white')
        draw = ImageDraw.Draw(img)
        
        # Try to use a default font
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        text = "Solve for x:\n2x + 5 = 15"
        draw.text((50, 50), text, fill='black', font=font)
        
        # Create temp directory if it doesn't exist
        os.makedirs('temp', exist_ok=True)
        img_path = 'temp/test_math_problem.png'
        img.save(img_path)
        
        print(f"Test image created: {img_path}")
        return img_path
        
    except ImportError:
        print("PIL not available, skipping test image creation")
        return None
    except Exception as e:
        print(f"Error creating test image: {str(e)}")
        return None

async def test_ocr():
    """Test OCR functionality"""
    from ai_solver import AISolver
    
    # Create test image
    img_path = create_test_image()
    if not img_path:
        print("Skipping OCR test - no test image")
        return
    
    solver = AISolver()
    
    print("\nTesting OCR...")
    try:
        extracted_text = await solver.extract_text_from_image(img_path)
        if extracted_text:
            print(f"   ✓ Extracted text: '{extracted_text}'")
        else:
            print("   ✗ Failed to extract text")
    except Exception as e:
        print(f"   ✗ OCR Error: {str(e)}")
    
    # Clean up
    if os.path.exists(img_path):
        os.remove(img_path)

async def main():
    """Run all tests"""
    print("=" * 60)
    print("Math Tutor Bot - Component Testing")
    print("=" * 60)
    
    # Check if required environment variables are set
    required_env_vars = ['BOT_TOKEN', 'AI_MODEL_PROVIDER']
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"⚠️  Missing environment variables: {missing_vars}")
        print("Please set up your .env file before running tests.")
        return
    
    # Run tests
    try:
        await test_ai_solver()
        await test_video_generator()
        test_content_filter()
        await test_rate_limiter()
        await test_conversation_logger()
        await test_ocr()
        
        print("\n" + "=" * 60)
        print("✅ All tests completed!")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error during testing: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
