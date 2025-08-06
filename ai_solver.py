"""
AI Solver module for Math Tutor Bot
Handles communication with LLMs for math problem solving
"""

import os
import logging
from typing import Dict, Any, List, Optional
import asyncio
import json

import openai
import google.generativeai as genai
import pytesseract
import easyocr
import cv2
import numpy as np
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
        
        # Initialize OCR readers
        try:
            # Handle SSL certificate issues that may occur on macOS
            import ssl
            try:
                _create_unverified_https_context = ssl._create_unverified_context
            except AttributeError:
                pass
            else:
                ssl._create_default_https_context = _create_unverified_https_context
            
            self.easyocr_reader = easyocr.Reader(['en'])
            self.logger.info("EasyOCR initialized successfully")
        except (ImportError, RuntimeError) as e:
            self.logger.warning("Failed to initialize EasyOCR: %s", str(e))
            self.logger.warning("OCR functionality will be disabled")
            self.easyocr_reader = None
        
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
        Extract text from an image using OCR
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Extracted text or None if extraction fails
        """
        try:
            self.logger.info("Extracting text from image: %s", image_path)
            
            # Load and preprocess the image
            image = cv2.imread(image_path)  # type: ignore
            if image is None:
                self.logger.error("Failed to load image")
                return None
            
            # Preprocess image for better OCR
            processed_image = self._preprocess_image(image)
            
            # Try multiple OCR approaches
            extracted_texts = []
            
            # Method 1: Tesseract
            try:
                tesseract_config = '--psm 6 -c tessedit_char_whitelist=0123456789+-*/=()[]{}.,ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz '
                tesseract_text = pytesseract.image_to_string(processed_image, config=tesseract_config).strip()
                if tesseract_text:
                    extracted_texts.append(('tesseract', tesseract_text))
            except Exception as e:
                self.logger.warning(f"Tesseract OCR failed: {str(e)}")
            
            # Method 2: EasyOCR
            try:
                if self.easyocr_reader is not None:
                    easyocr_results = self.easyocr_reader.readtext(processed_image)
                    easyocr_text = ' '.join([result[1] for result in easyocr_results if result[2] > 0.5])
                    if easyocr_text:
                        extracted_texts.append(('easyocr', easyocr_text))
                else:
                    self.logger.info("EasyOCR not available, skipping")
            except Exception as e:
                self.logger.warning(f"EasyOCR failed: {str(e)}")
            
            if not extracted_texts:
                self.logger.warning("No text extracted from image")
                return None
            
            # Choose the best extraction result
            best_text = self._choose_best_ocr_result(extracted_texts)
            
            # Post-process the extracted text
            cleaned_text = self._clean_extracted_text(best_text)
            
            self.logger.info("Successfully extracted text: %s...", cleaned_text[:100])
            return cleaned_text
            
        except (OSError, RuntimeError) as e:
            self.logger.error("Error extracting text from image: %s", str(e))
            return None
    
    def _preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """Preprocess image for better OCR results"""
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # type: ignore
        
        # Apply denoising
        denoised = cv2.fastNlMeansDenoising(gray)  # type: ignore
        
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(  # type: ignore
            denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2  # type: ignore
        )
        
        # Apply morphological operations to clean up
        kernel = np.ones((1, 1), np.uint8)
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)  # type: ignore
        
        return cleaned
    
    def _choose_best_ocr_result(self, extracted_texts: List[tuple]) -> str:
        """Choose the best OCR result from multiple methods"""
        if not extracted_texts:
            return ""
        
        # For now, prefer EasyOCR if available, otherwise use Tesseract
        for method, text in extracted_texts:
            if method == 'easyocr' and len(text.strip()) > 0:
                return text
        
        # Fall back to any available result
        return extracted_texts[0][1]
    
    def _clean_extracted_text(self, text: str) -> str:
        """Clean and normalize extracted text"""
        if not text:
            return ""
        
        # Remove excessive whitespace
        cleaned = ' '.join(text.split())
        
        # Fix common OCR errors in mathematical expressions
        # Handle quotes separately to avoid duplicate keys
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")
        
        replacements = {
            '×': '*',
            '÷': '/',
            '–': '-',
            '—': '-',
            '∫': 'integral of',
            '∂': 'partial derivative of',
            '∑': 'sum of',
            '∏': 'product of',
            '√': 'sqrt',
            '±': 'plus or minus',
            '≤': '<=',
            '≥': '>=',
            '≠': '!=',
            '≈': 'approximately',
            'π': 'pi',
            'θ': 'theta',
            'α': 'alpha',
            'β': 'beta',
            'γ': 'gamma',
            'δ': 'delta',
            'λ': 'lambda',
            'μ': 'mu',
            'σ': 'sigma',
            '°': ' degrees'
        }
        
        for old, new in replacements.items():
            cleaned = cleaned.replace(old, new)
        
        return cleaned
    
    def _create_solution_prompt(self, problem_text: str) -> str:
        """Create a detailed prompt for AI to solve the math problem"""
        return f"""
You are a mathematics tutor AI. Please solve the following math problem step by step.

PROBLEM: {problem_text}

Please provide your response EXACTLY in the following JSON format. Do not include any text before or after the JSON:

{{
    "problem_type": "algebra|calculus|geometry|statistics|trigonometry|other",
    "difficulty": "elementary|middle_school|high_school|college|graduate", 
    "solution": "The final answer or solution (plain text, no formatting)",
    "steps": [
        "Step 1: Clear explanation of the first step (plain text)",
        "Step 2: Clear explanation of the second step (plain text)",
        "Step 3: Continue until solved (plain text)"
    ],
    "explanation": "A clear educational explanation suitable for students (plain text)",
    "key_concepts": ["concept1", "concept2", "concept3"]
}}

IMPORTANT:
- Use ONLY plain text in all fields (no ** or __ formatting)
- Make sure the JSON is valid and properly formatted
- Include 3-5 clear, detailed steps
- Keep explanations educational and appropriate for students
- If the problem is unclear or not mathematical, respond with: {{"error": "Unable to solve: reason"}}

Example for "2x + 5 = 15":
{{
    "problem_type": "algebra",
    "difficulty": "middle_school",
    "solution": "x = 5",
    "steps": [
        "Step 1: Subtract 5 from both sides: 2x + 5 - 5 = 15 - 5",
        "Step 2: Simplify: 2x = 10", 
        "Step 3: Divide both sides by 2: x = 5"
    ],
    "explanation": "This is a linear equation that we solve by isolating the variable x using inverse operations.",
    "key_concepts": ["Linear Equations", "Inverse Operations", "Solving for Variables"]
}}
"""
    
    async def _solve_with_openai(self, prompt: str) -> str:
        """Solve using OpenAI GPT"""
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert mathematics tutor."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            self.logger.error(f"OpenAI API error: {str(e)}")
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
            self.logger.error(f"Gemini API error: {str(e)}")
            raise
    
    def _parse_ai_response(self, response_text: str, original_problem: str) -> Dict[str, Any]:
        """Parse AI response into structured data"""
        try:
            # Clean the response text
            response_text = response_text.strip()
            
            # Look for JSON in the response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_text = response_text[json_start:json_end]
                
                try:
                    parsed_data = json.loads(json_text)
                    
                    # Check for error in response
                    if 'error' in parsed_data:
                        self.logger.warning(f"AI reported error: {parsed_data['error']}")
                        return None
                    
                    # Validate required fields
                    if 'solution' not in parsed_data or 'steps' not in parsed_data:
                        self.logger.warning("Missing required fields in AI response")
                        return self._parse_unstructured_response(response_text, original_problem)
                    
                    # Clean up the steps array
                    clean_steps = []
                    for step in parsed_data.get('steps', []):
                        step_text = str(step).strip()
                        if step_text and len(step_text) > 10 and not step_text.startswith('"'):
                            clean_steps.append(step_text)
                    
                    parsed_data['steps'] = clean_steps
                    
                    # Add metadata
                    parsed_data['original_problem'] = original_problem
                    parsed_data['ai_provider'] = self.ai_provider
                    parsed_data['timestamp'] = asyncio.get_event_loop().time()
                    
                    return parsed_data
                    
                except json.JSONDecodeError as e:
                    self.logger.warning(f"JSON parsing failed: {str(e)}")
                    return self._parse_unstructured_response(response_text, original_problem)
            
            else:
                # No JSON found, try unstructured parsing
                return self._parse_unstructured_response(response_text, original_problem)
                
        except Exception as e:
            self.logger.error(f"Error parsing AI response: {str(e)}")
            return self._parse_unstructured_response(response_text, original_problem)
    
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
            self.logger.error(f"Error in fallback parsing: {str(e)}")
            return None
