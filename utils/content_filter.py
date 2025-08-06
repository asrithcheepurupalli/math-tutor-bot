"""
Content filtering for Math Tutor Bot
Ensures appropriate content and educational focus
"""

import re
import logging
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

class ContentFilter:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Load configuration
        self.enabled = os.getenv('ENABLE_CONTENT_FILTER', 'true').lower() == 'true'
        blocked_keywords_str = os.getenv('BLOCKED_KEYWORDS', 'inappropriate,spam,violence')
        self.blocked_keywords = [kw.strip().lower() for kw in blocked_keywords_str.split(',')]
        
        # Mathematical terms that should always be allowed
        self.math_terms = {
            'algebra', 'calculus', 'geometry', 'trigonometry', 'statistics',
            'derivative', 'integral', 'equation', 'function', 'variable',
            'coefficient', 'polynomial', 'logarithm', 'exponential', 'matrix',
            'vector', 'angle', 'triangle', 'circle', 'square', 'rectangle',
            'probability', 'mean', 'median', 'mode', 'standard deviation',
            'solve', 'calculate', 'find', 'determine', 'evaluate', 'simplify',
            'factor', 'expand', 'graph', 'plot', 'limit', 'series', 'sequence'
        }
        
        # Patterns for mathematical expressions
        self.math_patterns = [
            r'[0-9]+[\+\-\*/\=\^\(\)x-z\s]*[0-9]*',  # Basic math expressions
            r'[a-z]\s*[\+\-\*/\=\^]\s*[0-9a-z]',      # Algebraic expressions
            r'\\[a-zA-Z]+\{[^}]*\}',                   # LaTeX commands
            r'\$[^$]+\$',                              # LaTeX inline math
            r'∫|∑|∏|√|π|θ|α|β|γ|δ|λ|μ|σ|∞',          # Mathematical symbols
        ]
        
        self.logger.info(f"Content filter initialized, enabled: {self.enabled}")
    
    def is_appropriate(self, text: str) -> bool:
        """
        Check if text content is appropriate for educational use
        
        Args:
            text: Text to check
            
        Returns:
            True if content is appropriate, False otherwise
        """
        if not self.enabled:
            return True
        
        try:
            text_lower = text.lower().strip()
            
            # Allow empty or very short messages
            if len(text_lower) < 3:
                return True
            
            # Check for blocked keywords
            if self._contains_blocked_content(text_lower):
                self.logger.warning(f"Blocked content detected: {text[:50]}...")
                return False
            
            # Check if it's math-related
            if self._is_math_related(text_lower):
                return True
            
            # Check for educational intent
            if self._has_educational_intent(text_lower):
                return True
            
            # If none of the above, it might not be appropriate for a math tutor
            # But we'll be lenient and allow it with a warning
            self.logger.info(f"Potentially non-math content: {text[:50]}...")
            return True
            
        except Exception as e:
            self.logger.error(f"Error in content filtering: {str(e)}")
            # In case of error, allow the content (fail open)
            return True
    
    def _contains_blocked_content(self, text: str) -> bool:
        """Check for explicitly blocked keywords"""
        for keyword in self.blocked_keywords:
            if keyword and keyword in text:
                return True
        return False
    
    def _is_math_related(self, text: str) -> bool:
        """Check if text contains mathematical terms or expressions"""
        # Check for mathematical terms
        for term in self.math_terms:
            if term in text:
                return True
        
        # Check for mathematical patterns
        for pattern in self.math_patterns:
            if re.search(pattern, text):
                return True
        
        # Check for common math question words
        math_question_words = [
            'solve', 'calculate', 'find', 'what is', 'how much', 'how many',
            'derive', 'prove', 'show that', 'simplify', 'factor', 'expand',
            'integrate', 'differentiate', 'graph', 'plot'
        ]
        
        for phrase in math_question_words:
            if phrase in text:
                return True
        
        return False
    
    def _has_educational_intent(self, text: str) -> bool:
        """Check if text has educational intent"""
        educational_indicators = [
            'help', 'learn', 'understand', 'explain', 'how', 'why', 'what',
            'homework', 'assignment', 'problem', 'question', 'exercise',
            'study', 'practice', 'review', 'test', 'exam', 'quiz'
        ]
        
        for indicator in educational_indicators:
            if indicator in text:
                return True
        
        return False
    
    def get_content_suggestions(self, text: str) -> List[str]:
        """
        Provide suggestions for improving content quality
        
        Args:
            text: Original text
            
        Returns:
            List of suggestions
        """
        suggestions = []
        
        if not self._is_math_related(text.lower()):
            suggestions.append(
                "Try including specific mathematical terms or expressions in your question."
            )
        
        if len(text) < 10:
            suggestions.append(
                "Provide more details about your math problem for better assistance."
            )
        
        if '?' not in text and not any(word in text.lower() for word in ['solve', 'find', 'calculate']):
            suggestions.append(
                "Frame your message as a clear question (e.g., 'Solve for x: ...' or 'What is...')."
            )
        
        return suggestions
    
    def sanitize_input(self, text: str) -> str:
        """
        Clean and sanitize user input
        
        Args:
            text: Input text to sanitize
            
        Returns:
            Sanitized text
        """
        # Remove excessive whitespace
        sanitized = ' '.join(text.split())
        
        # Remove potentially harmful characters while preserving math symbols
        # This is a basic implementation - expand as needed
        allowed_chars = re.compile(r'[a-zA-Z0-9\s\+\-\*/\=\(\)\[\]\{\}\^\.\,\?\!\:\;\'\"\\∫∑∏√π θα β γδλμσ∞≤≥≠≈°]')
        sanitized = ''.join(allowed_chars.findall(sanitized))
        
        # Limit length
        max_length = 1000
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length] + "..."
            self.logger.warning("Input truncated due to length")
        
        return sanitized.strip()
    
    def log_content_decision(self, text: str, approved: bool, reason: str = ""):
        """Log content filtering decisions for audit purposes"""
        self.logger.info(
            "Content filtering decision",
            extra={
                'content_preview': text[:100],
                'approved': approved,
                'reason': reason,
                'content_length': len(text)
            }
        )
