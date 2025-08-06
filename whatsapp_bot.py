"""
WhatsApp integration for Math Tutor Bot (alternative to Telegram)
"""

import os
import logging
from typing import Dict, Any, Optional
import json
from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from dotenv import load_dotenv

from ai_solver import AISolver
from video_generator import VideoGenerator
from utils.logger import setup_logger
from utils.content_filter import ContentFilter
from utils.rate_limiter import RateLimiter
from utils.conversation_logger import ConversationLogger

load_dotenv()

class WhatsAppBot:
    def __init__(self):
        self.logger = setup_logger(__name__)
        
        # Twilio configuration
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.whatsapp_number = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
        
        if self.account_sid and self.auth_token:
            self.client = Client(self.account_sid, self.auth_token)
        else:
            self.client = None
            self.logger.warning("Twilio credentials not configured")
        
        # Initialize components
        self.ai_solver = AISolver()
        self.video_generator = VideoGenerator()
        self.content_filter = ContentFilter()
        self.rate_limiter = RateLimiter()
        self.conversation_logger = ConversationLogger()
        
        # Flask app for webhook handling
        self.app = Flask(__name__)
        self._setup_routes()
        
        self.logger.info("WhatsApp bot initialized")
    
    def _setup_routes(self):
        """Setup Flask routes for WhatsApp webhook"""
        
        @self.app.route('/webhook/whatsapp', methods=['POST'])
        def handle_whatsapp_message():
            return self._handle_incoming_message()
        
        @self.app.route('/webhook/whatsapp', methods=['GET'])
        def verify_webhook():
            return self._verify_webhook()
        
        @self.app.route('/health', methods=['GET'])
        def health_check():
            return jsonify({'status': 'healthy', 'service': 'Math Tutor WhatsApp Bot'})
    
    def _verify_webhook(self):
        """Verify webhook for WhatsApp"""
        verify_token = os.getenv('WHATSAPP_VERIFY_TOKEN', 'math_tutor_verify')
        
        if request.args.get('hub.verify_token') == verify_token:
            return request.args.get('hub.challenge')
        else:
            return 'Invalid verification token', 403
    
    def _handle_incoming_message(self):
        """Handle incoming WhatsApp messages"""
        try:
            # Get message data
            from_number = request.form.get('From', '').replace('whatsapp:', '')
            message_body = request.form.get('Body', '').strip()
            media_url = request.form.get('MediaUrl0')  # For images
            
            if not from_number:
                return 'No sender information', 400
            
            # Create response object
            response = MessagingResponse()
            
            # Extract user ID from phone number (simplified)
            user_id = hash(from_number) % 1000000  # Convert phone to user ID
            
            # Check rate limiting
            if not self.rate_limiter.check_rate_limit(user_id):
                response.message("⏱️ You're sending messages too quickly. Please wait a moment.")
                return str(response)
            
            # Handle different message types
            if media_url:
                # Handle image message
                self._handle_image_message_async(user_id, from_number, media_url, response)
            elif message_body:
                # Handle text message
                if message_body.lower() in ['/start', 'start', 'hello', 'hi']:
                    self._send_welcome_message(response)
                elif message_body.lower() in ['/help', 'help']:
                    self._send_help_message(response)
                else:
                    self._handle_text_message_async(user_id, from_number, message_body, response)
            else:
                response.message("Please send a math problem as text or image for help!")
            
            return str(response)
            
        except Exception as e:
            self.logger.error(f"Error handling WhatsApp message: {str(e)}")
            response = MessagingResponse()
            response.message("Sorry, I encountered an error. Please try again later.")
            return str(response)
    
    def _send_welcome_message(self, response):
        """Send welcome message"""
        welcome_text = """
🧮 Welcome to Math Tutor Bot!

I can help you solve math problems step by step. Here's what I can do:

📝 *Text Problems*: Send me any math problem
📸 *Image Problems*: Send me a photo of a math problem
🎥 *Video Explanations*: I'll create educational videos

*Examples:*
• "Solve for x: 2x + 5 = 15"
• "Find the derivative of f(x) = x² + 3x + 2"

Just send me your math problem!
        """
        response.message(welcome_text.strip())
    
    def _send_help_message(self, response):
        """Send help message"""
        help_text = """
🆘 *Math Tutor Bot Help*

*How to use:*
1. Send a math problem as text
2. Or send a clear photo of the problem
3. I'll provide step-by-step solutions

*Supported topics:*
• Algebra, Calculus, Geometry
• Statistics, Trigonometry
• And more!

*Tips:*
• Be specific with questions
• Use clear images for photos
• One problem per message

Send "start" to see the welcome message again.
        """
        response.message(help_text.strip())
    
    def _handle_text_message_async(self, user_id: int, phone_number: str, message: str, response):
        """Handle text message (initiates async processing)"""
        try:
            # Content filtering
            if not self.content_filter.is_appropriate(message):
                response.message("❌ Please send math-related questions only.")
                return
            
            # Send initial response
            response.message("🤔 Analyzing your math problem... I'll send the solution shortly!")
            
            # Process async (in a real implementation, you'd use a task queue)
            import asyncio
            import threading
            
            def process_message():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(
                    self._process_text_message(user_id, phone_number, message)
                )
                loop.close()
            
            # Start processing in background thread
            thread = threading.Thread(target=process_message)
            thread.start()
            
        except Exception as e:
            self.logger.error(f"Error in async text handling: {str(e)}")
            response.message("❌ An error occurred. Please try again.")
    
    async def _process_text_message(self, user_id: int, phone_number: str, message: str):
        """Process text message asynchronously"""
        try:
            # Solve the problem
            solution_data = await self.ai_solver.solve_problem(message)
            
            if not solution_data:
                await self._send_whatsapp_message(
                    phone_number, 
                    "❌ I couldn't solve this problem. Please make sure it's a valid math question."
                )
                return
            
            # Format solution
            solution_text = self._format_solution(solution_data)
            
            # Send solution
            await self._send_whatsapp_message(phone_number, solution_text)
            
            # Generate video (optional, as WhatsApp has file size limits)
            try:
                video_path = await self.video_generator.create_explanation_video(
                    problem=message,
                    solution=solution_data['solution'],
                    steps=solution_data['steps'],
                    user_id=user_id
                )
                
                if video_path:
                    # Note: Video sending via WhatsApp API requires additional setup
                    await self._send_whatsapp_message(
                        phone_number, 
                        "🎥 Video explanation generated! (Video delivery coming soon)"
                    )
                    
                    # Clean up video file
                    if os.path.exists(video_path):
                        os.remove(video_path)
                        
            except Exception as e:
                self.logger.warning(f"Video generation failed: {str(e)}")
            
            # Log conversation
            await self.conversation_logger.log_interaction(
                user_id=user_id,
                username=phone_number,
                message_type="text_problem",
                content=message,
                response=solution_data,
                video_generated=bool(video_path)
            )
            
        except Exception as e:
            self.logger.error(f"Error processing text message: {str(e)}")
            await self._send_whatsapp_message(
                phone_number,
                "❌ An error occurred while processing your request."
            )
    
    def _handle_image_message_async(self, user_id: int, phone_number: str, media_url: str, response):
        """Handle image message (initiates async processing)"""
        try:
            response.message("📸 Processing your image... I'll extract the text and solve it!")
            
            # Process async
            import asyncio
            import threading
            
            def process_image():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(
                    self._process_image_message(user_id, phone_number, media_url)
                )
                loop.close()
            
            thread = threading.Thread(target=process_image)
            thread.start()
            
        except Exception as e:
            self.logger.error(f"Error in async image handling: {str(e)}")
            response.message("❌ An error occurred processing your image.")
    
    async def _process_image_message(self, user_id: int, phone_number: str, media_url: str):
        """Process image message asynchronously"""
        try:
            # Download image
            import requests
            response = requests.get(media_url)
            
            if response.status_code != 200:
                await self._send_whatsapp_message(
                    phone_number,
                    "❌ Failed to download image. Please try again."
                )
                return
            
            # Save image temporarily
            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                temp_file.write(response.content)
                image_path = temp_file.name
            
            try:
                # Extract text using OCR
                extracted_text = await self.ai_solver.extract_text_from_image(image_path)
                
                if not extracted_text:
                    await self._send_whatsapp_message(
                        phone_number,
                        "❌ I couldn't extract text from your image. Please ensure it's clear and readable."
                    )
                    return
                
                # Send extracted text
                await self._send_whatsapp_message(
                    phone_number,
                    f"✅ Text extracted: '{extracted_text}'\n\n🤔 Now solving..."
                )
                
                # Solve the problem
                solution_data = await self.ai_solver.solve_problem(extracted_text)
                
                if solution_data:
                    solution_text = f"**Extracted Problem:** {extracted_text}\n\n{self._format_solution(solution_data)}"
                    await self._send_whatsapp_message(phone_number, solution_text)
                    
                    # Log conversation
                    await self.conversation_logger.log_interaction(
                        user_id=user_id,
                        username=phone_number,
                        message_type="image_problem",
                        content=f"Image OCR: {extracted_text}",
                        response=solution_data
                    )
                else:
                    await self._send_whatsapp_message(
                        phone_number,
                        "❌ I couldn't solve the extracted problem."
                    )
                    
            finally:
                # Clean up temp file
                if os.path.exists(image_path):
                    os.remove(image_path)
                    
        except Exception as e:
            self.logger.error(f"Error processing image: {str(e)}")
            await self._send_whatsapp_message(
                phone_number,
                "❌ An error occurred processing your image."
            )
    
    async def _send_whatsapp_message(self, to_number: str, message: str):
        """Send message via WhatsApp"""
        try:
            if not self.client:
                self.logger.error("Twilio client not configured")
                return
            
            self.client.messages.create(
                from_=f'whatsapp:{self.whatsapp_number}',
                body=message,
                to=f'whatsapp:{to_number}'
            )
            
            self.logger.info(f"Message sent to {to_number}")
            
        except Exception as e:
            self.logger.error(f"Error sending WhatsApp message: {str(e)}")
    
    def _format_solution(self, solution_data: Dict[str, Any]) -> str:
        """Format solution data for WhatsApp"""
        formatted = f"*🎯 Solution:*\n{solution_data['solution']}\n\n"
        
        if solution_data.get('steps'):
            formatted += "*📋 Step-by-step:*\n"
            for i, step in enumerate(solution_data['steps'], 1):
                formatted += f"{i}. {step}\n"
        
        return formatted
    
    def run(self, host='0.0.0.0', port=5000, debug=False):
        """Run the WhatsApp bot server"""
        self.logger.info(f"Starting WhatsApp bot server on {host}:{port}")
        self.app.run(host=host, port=port, debug=debug)

if __name__ == "__main__":
    # For development/testing
    bot = WhatsAppBot()
    bot.run(debug=True)
