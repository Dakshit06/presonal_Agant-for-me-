"""
LLM service for AI model interactions
"""

from openai import AsyncOpenAI
from src.config.settings import settings


class LLMService:
    """Service for interacting with LLM models"""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def generate_completion(self, prompt: str, model: str = None) -> str:
        """Generate completion from LLM"""
        
        model = model or settings.DEFAULT_LLM_MODEL
        
        response = await self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.choices[0].message.content
