"""
Google Gemini API integration utilities.
"""
import logging
from django.conf import settings

try:
    import google.generativeai as genai
except ImportError:
    genai = None

logger = logging.getLogger(__name__)


class GeminiClient:
    """Client for interacting with Google Gemini API."""
    
    def __init__(self, api_key=None, model=None):
        """
        Initialize Gemini client.
        
        Args:
            api_key: Optional API key override
            model: Optional model name override
        """
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.model_name = model or settings.GEMINI_MODEL
        self.model = None
        
        if genai is None:
            logger.error("google-generativeai package not installed")
            return
            
        if not self.api_key:
            logger.warning("Gemini API key not configured")
            return
            
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
            logger.info(f"Gemini client initialized with model: {self.model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {e}")
    
    def generate_content(self, prompt, **kwargs):
        """
        Generate content using Gemini.
        
        Args:
            prompt: Text prompt for generation
            **kwargs: Additional generation parameters
            
        Returns:
            Generated text content
        """
        if not self.model:
            logger.error("Gemini model not initialized")
            return None
            
        try:
            response = self.model.generate_content(prompt, **kwargs)
            return response.text
        except Exception as e:
            logger.error(f"Gemini generation error: {e}")
            return None
    
    def analyze_code(self, code, instructions=""):
        """
        Analyze code and provide feedback.
        
        Args:
            code: Code snippet to analyze
            instructions: Optional specific instructions
            
        Returns:
            Analysis results
        """
        prompt = f"""Analyze the following code and provide insights:

{code}

{instructions}

Please provide:
1. Code quality assessment
2. Potential improvements
3. Security concerns
4. Best practices recommendations
"""
        return self.generate_content(prompt)
    
    def generate_tasks(self, requirements):
        """
        Generate task list from requirements.
        
        Args:
            requirements: Project requirements text
            
        Returns:
            Generated task list
        """
        prompt = f"""Based on these requirements, create a detailed task list:

{requirements}

Please organize tasks by:
1. Priority (High/Medium/Low)
2. Estimated effort
3. Dependencies
4. Suggested order of implementation
"""
        return self.generate_content(prompt)


def get_gemini_client():
    """Get a configured Gemini client instance."""
    return GeminiClient()
