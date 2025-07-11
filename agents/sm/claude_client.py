"""
Claude 3.7 Sonnet Client for Scrum Master Agent
"""

import requests
import json
import logging
from typing import Dict, Any, List, Optional
from .config import config

logger = logging.getLogger(__name__)

class ClaudeClient:
    """Client for Claude 3.7 Sonnet API (Scrum Master)"""
    def __init__(self):
        self.api_key = config.claude_api_key
        self.model = config.claude_model
        self.base_url = "https://api.anthropic.com/v1/messages"
        self.headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01"
        }
    def facilitate_ceremony(self, ceremony_type: str, context: Dict[str, Any] = None) -> str:
        if not self.api_key:
            return f"[FAKE] Facilitated {ceremony_type} ceremony."
        prompt = f"You are a Scrum Master facilitating a {ceremony_type} ceremony. Context: {json.dumps(context or {}, indent=2)}. Provide a detailed agenda and facilitation tips."
        try:
            response = self._call_claude(prompt)
            if response:
                return response.strip()
        except Exception as e:
            logger.error(f"Error facilitating ceremony with Claude: {e}")
        return f"[FAKE] Facilitated {ceremony_type} ceremony."
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