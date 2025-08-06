"""
Simplified AI Solver module for Math Tutor Bot
Focuses on core AI solving without complex OCR
"""

import os
import logging
from typing import Dict, Any, Optional
import asyncio
import json

import openai
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class AISolver:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.ai_provider = os.getenv('AI_MODEL_PROVIDER', 'openai').lower()
        
        # Initialize AI clients
        if self.ai_provider == 'openai':
            self.openai_client = openai.AsyncOpenAI(
                api_key=os.getenv('OPENAI_API_KEY')
            )
        elif self.ai_provider == 'gemini':
            genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
            self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
        
        self.logger.info("AISolver initialized with provider: %s", self.ai_provider)
    
    async def solve_problem(self, problem_text: str) -> Optional[Dict[str, Any]]:
        """
        Solve a math problem and return structured solution data
        
        Args:
            problem_text: The math problem as text
            
        Returns:
            Dictionary containing solution, steps, latex, and metadata
        """
        try:
            self.logger.info("Solving problem: %s...", problem_text[:100])
            
            # Create a detailed prompt for the AI
            prompt = self._create_solution_prompt(problem_text)
            
            if self.ai_provider == 'openai':
                response = await self._solve_with_openai(prompt)
            elif self.ai_provider == 'gemini':
                response = await self._solve_with_gemini(prompt)
            else:
                raise ValueError(f"Unsupported AI provider: {self.ai_provider}")
            
            # Parse and structure the response
            solution_data = self._parse_ai_response(response, problem_text)
            
            self.logger.info("Problem solved successfully")
            return solution_data
            
        except (ValueError, RuntimeError) as e:
            self.logger.error("Error solving problem: %s", str(e))
            return None
    
    async def extract_text_from_image(self, image_path: str) -> Optional[str]:
        """
        Simplified image text extraction
        This is a placeholder - for now just return None
        OCR functionality will be re-added later
        """
        self.logger.warning("OCR functionality temporarily disabled")
        return None
    
    def _create_solution_prompt(self, problem_text: str) -> str:
        """Create a detailed prompt for the AI to solve the math problem"""
        return f"""
You are an expert math tutor. Solve this math problem step by step and provide a detailed explanation.

Problem: {problem_text}

Please provide your response in JSON format with the following structure:
{{
  "problem_type": "algebra|calculus|geometry|statistics|other",
  "difficulty": "elementary|middle|high|college|advanced",
  "solution": "The final answer",
  "steps": [
    "Step 1: Clear explanation of first step",
    "Step 2: Clear explanation of second step",
    "..."
  ],
  "latex": "LaTeX representation of the solution",
  "explanation": "Detailed explanation of the concept and method used",
  "key_concepts": ["concept1", "concept2", "..."],
  "video_script": [
    "Script line 1 for video explanation",
    "Script line 2 for video explanation",
    "..."
  ],
  "common_mistakes": [
    "Common mistake 1",
    "Common mistake 2"
  ],
  "related_problems": [
    "Similar problem 1",
    "Similar problem 2"
  ]
}}

Make sure your response is valid JSON and provides educational value for students.
"""
    
    async def _solve_with_openai(self, prompt: str) -> str:
        """Solve using OpenAI GPT"""
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert math tutor."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            self.logger.error("OpenAI API error: %s", str(e))
            raise
    
    async def _solve_with_gemini(self, prompt: str) -> str:
        """Solve using Google Gemini"""
        try:
            # Gemini doesn't have async support yet, so we'll use asyncio.to_thread
            response = await asyncio.to_thread(
                self.gemini_model.generate_content, prompt
            )
            return response.text
        except Exception as e:
            self.logger.error("Gemini API error: %s", str(e))
            raise
    
    def _parse_ai_response(self, response_text: str, original_problem: str) -> Dict[str, Any]:
        """Parse AI response into structured data"""
        try:
            # Try to parse as JSON
            if response_text.strip().startswith('{'):
                parsed_data = json.loads(response_text.strip())
                
                # Check for error in response
                if 'error' in parsed_data:
                    self.logger.warning("AI reported error: %s", parsed_data['error'])
                    return None
                
                # Validate required fields
                required_fields = ['solution', 'steps']
                for field in required_fields:
                    if field not in parsed_data:
                        self.logger.warning("Missing required field: %s", field)
                        return None
                
                # Add metadata
                parsed_data['original_problem'] = original_problem
                parsed_data['ai_provider'] = self.ai_provider
                parsed_data['timestamp'] = asyncio.get_event_loop().time()
                
                return parsed_data
            
            else:
                # Fallback: try to extract solution from unstructured response
                return self._parse_unstructured_response(response_text, original_problem)
                
        except json.JSONDecodeError as e:
            self.logger.warning("JSON parsing failed: %s", str(e))
            return self._parse_unstructured_response(response_text, original_problem)
        except Exception as e:
            self.logger.error("Error parsing AI response: %s", str(e))
            return None
    
    def _parse_unstructured_response(self, response_text: str, original_problem: str) -> Dict[str, Any]:
        """Parse unstructured AI response"""
        try:
            # Simple fallback parsing
            lines = response_text.strip().split('\n')
            
            solution = "See explanation below"
            steps = []
            explanation = response_text
            
            # Try to identify solution and steps
            for line in lines:
                line = line.strip()
                if any(keyword in line.lower() for keyword in ['solution:', 'answer:', 'result:']):
                    solution = line.split(':', 1)[1].strip() if ':' in line else line
                elif any(keyword in line.lower() for keyword in ['step', 'first', 'second', 'then', 'next', 'finally']):
                    steps.append(line)
            
            if not steps:
                # If no clear steps found, split by sentences
                sentences = response_text.split('.')
                steps = [s.strip() + '.' for s in sentences if len(s.strip()) > 10][:10]  # Limit to 10 steps
            
            return {
                'solution': solution,
                'steps': steps,
                'explanation': explanation,
                'original_problem': original_problem,
                'ai_provider': self.ai_provider,
                'timestamp': asyncio.get_event_loop().time(),
                'problem_type': 'unknown',
                'difficulty': 'unknown'
            }
            
        except Exception as e:
            self.logger.error("Error in fallback parsing: %s", str(e))
            return None
