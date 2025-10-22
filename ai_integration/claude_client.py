"""
Claude (Anthropic) API integration utilities.
"""
import logging
from django.conf import settings

try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None

logger = logging.getLogger(__name__)


class ClaudeClient:
    """Client for interacting with Claude API in headless mode."""
    
    def __init__(self, api_key=None, model=None, headless=None):
        """
        Initialize Claude client.
        
        Args:
            api_key: Optional API key override
            model: Optional model name override
            headless: Optional headless mode override
        """
        self.api_key = api_key or settings.ANTHROPIC_API_KEY
        self.model_name = model or settings.CLAUDE_MODEL
        self.headless_mode = headless if headless is not None else settings.CLAUDE_HEADLESS_MODE
        self.client = None
        
        if Anthropic is None:
            logger.error("anthropic package not installed")
            return
            
        if not self.api_key:
            logger.warning("Anthropic API key not configured")
            return
            
        try:
            self.client = Anthropic(api_key=self.api_key)
            logger.info(f"Claude client initialized with model: {self.model_name}")
            logger.info(f"Headless mode: {self.headless_mode}")
        except Exception as e:
            logger.error(f"Failed to initialize Claude client: {e}")
    
    def send_message(self, prompt, system_message="", max_tokens=4096, **kwargs):
        """
        Send a message to Claude.
        
        Args:
            prompt: User prompt/message
            system_message: Optional system message
            max_tokens: Maximum tokens in response
            **kwargs: Additional API parameters
            
        Returns:
            Claude's response text
        """
        if not self.client:
            logger.error("Claude client not initialized")
            return None
            
        try:
            messages = [{"role": "user", "content": prompt}]
            
            params = {
                "model": self.model_name,
                "max_tokens": max_tokens,
                "messages": messages,
            }
            
            if system_message:
                params["system"] = system_message
            
            params.update(kwargs)
            
            response = self.client.messages.create(**params)
            return response.content[0].text
        except Exception as e:
            logger.error(f"Claude message error: {e}")
            return None
    
    def automate_code_task(self, task_description, codebase_context=""):
        """
        Automate a coding task using Claude in headless mode.
        
        Args:
            task_description: Description of the coding task
            codebase_context: Optional context about the codebase
            
        Returns:
            Generated code or solution
        """
        system_message = """You are an expert software engineer working in headless automation mode. 
Generate clean, production-ready code that follows best practices. 
Provide complete implementations without placeholders."""

        prompt = f"""Task: {task_description}

Codebase Context:
{codebase_context}

Please provide:
1. Complete implementation
2. Necessary imports
3. Error handling
4. Comments for complex logic
5. Any setup/configuration needed
"""
        return self.send_message(prompt, system_message=system_message, max_tokens=8192)
    
    def review_code(self, code, requirements=""):
        """
        Review code using Claude.
        
        Args:
            code: Code to review
            requirements: Optional requirements to check against
            
        Returns:
            Code review feedback
        """
        system_message = "You are an expert code reviewer. Provide constructive, actionable feedback."
        
        prompt = f"""Please review this code:

```
{code}
```

{f"Requirements to check: {requirements}" if requirements else ""}

Provide:
1. Code quality assessment
2. Potential bugs or issues
3. Security concerns
4. Performance optimization suggestions
5. Recommended improvements
"""
        return self.send_message(prompt, system_message=system_message)
    
    def generate_improvement_plan(self, codebase_analysis):
        """
        Generate improvement plan for codebase.
        
        Args:
            codebase_analysis: Analysis of the current codebase
            
        Returns:
            Improvement plan with prioritized tasks
        """
        system_message = """You are a technical architect creating improvement plans.
Focus on practical, incremental improvements that deliver value."""

        prompt = f"""Based on this codebase analysis:

{codebase_analysis}

Create a detailed improvement plan with:
1. Prioritized list of improvements
2. Estimated effort for each item
3. Dependencies between tasks
4. Expected benefits
5. Suggested implementation order
"""
        return self.send_message(prompt, system_message=system_message, max_tokens=8192)


def get_claude_client():
    """Get a configured Claude client instance."""
    return ClaudeClient()
