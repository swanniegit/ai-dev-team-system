"""
Claude 3.7 Sonnet Client for Developer Agent
"""

import requests
import json
import logging
from typing import Dict, Any, List, Optional
from .config import config

logger = logging.getLogger(__name__)

class ClaudeClient:
    """Client for Claude 3.7 Sonnet API (Developer)"""
    def __init__(self):
        self.api_key = config.claude_api_key
        self.model = config.claude_model
        self.base_url = "https://api.anthropic.com/v1/messages"
        self.headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01"
        }
    def scaffold_code(self, feature_description: str, tech_stack: str = "Python/FastAPI") -> str:
        if not self.api_key:
            return f"# Scaffolded code for: {feature_description}\n# Tech stack: {tech_stack}\n# TODO: Implement actual code"
        prompt = f"You are a senior developer. Scaffold code for: {feature_description}. Tech stack: {tech_stack}. Return clean, production-ready code with comments."
        try:
            response = self._call_claude(prompt)
            if response:
                return response.strip()
        except Exception as e:
            logger.error(f"Error scaffolding code with Claude: {e}")
        return f"# Scaffolded code for: {feature_description}\n# Tech stack: {tech_stack}\n# TODO: Implement actual code"
    def review_code(self, code: str, context: str = "") -> str:
        if not self.api_key:
            return f"[FAKE] Code review completed for {len(code)} lines of code."
        prompt = f"You are a senior developer doing code review. Code:\n{code}\nContext: {context}\nProvide detailed review with suggestions for improvement."
        try:
            response = self._call_claude(prompt)
            if response:
                return response.strip()
        except Exception as e:
            logger.error(f"Error reviewing code with Claude: {e}")
        return f"[FAKE] Code review completed for {len(code)} lines of code."
    def _call_claude(self, prompt: str) -> Optional[str]:
        try:
            payload = {
                "model": self.model,
                "max_tokens": config.claude_max_tokens,
                "temperature": config.claude_temperature,
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            return result["content"][0]["text"]
        except Exception as e:
            logger.error(f"Claude API call failed: {e}")
            return None 