"""
Claude 3.7 Sonnet Client for Product Owner Agent
"""

import requests
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from .config import config

logger = logging.getLogger(__name__)

class ClaudeClient:
    """Client for Claude 3.7 Sonnet API"""
    
    def __init__(self):
        self.api_key = config.claude_api_key
        self.model = config.claude_model
        self.base_url = "https://api.anthropic.com/v1/messages"
        self.headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01"
        }
    
    def create_story(self, feature_request: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a user story from a feature request using Claude"""
        if not self.api_key:
            logger.warning("Claude API key not configured, using fallback story creation")
            return self._fallback_story_creation(feature_request)
        
        prompt = f"""
        You are a Product Owner in an agile development team. Create a user story from the following feature request.
        
        Feature Request: {feature_request}
        
        Context: {json.dumps(context or {}, indent=2)}
        
        Please create a user story with:
        1. A clear user story format: "As a [user], I want [feature] so that [benefit]"
        2. Detailed acceptance criteria (3-8 criteria)
        3. Story points estimation using Fibonacci sequence (1, 2, 3, 5, 8, 13, 21)
        4. Priority level (High, Medium, Low)
        5. Business value score (1-10)
        6. Risk assessment (Low, Medium, High)
        
        Return the response as a JSON object with these fields:
        - title: Story title
        - description: Full user story
        - acceptance_criteria: List of acceptance criteria
        - story_points: Estimated story points
        - priority: Priority level
        - business_value: Business value score
        - risk_level: Risk assessment
        - labels: Relevant labels/tags
        """
        
        try:
            response = self._call_claude(prompt)
            if response:
                return json.loads(response)
        except Exception as e:
            logger.error(f"Error creating story with Claude: {e}")
        
        return self._fallback_story_creation(feature_request)
    
    def write_acceptance_criteria(self, story_title: str, story_description: str) -> List[str]:
        """Write detailed acceptance criteria for a user story"""
        if not self.api_key:
            return self._fallback_acceptance_criteria(story_title)
        
        prompt = f"""
        You are a Product Owner writing acceptance criteria for a user story.
        
        Story Title: {story_title}
        Story Description: {story_description}
        
        Write 5-8 detailed acceptance criteria that clearly define when this story is complete.
        Each criterion should be specific, measurable, and testable.
        
        Return as a JSON array of strings.
        """
        
        try:
            response = self._call_claude(prompt)
            if response:
                return json.loads(response)
        except Exception as e:
            logger.error(f"Error writing acceptance criteria with Claude: {e}")
        
        return self._fallback_acceptance_criteria(story_title)
    
    def estimate_story_points(self, story_description: str, complexity_factors: List[str] = None) -> int:
        """Estimate story points using Claude's analysis"""
        if not self.api_key:
            return self._fallback_story_points(story_description)
        
        factors = complexity_factors or ["effort", "uncertainty", "dependencies"]
        fibonacci = config.behavior_params["story_pointing"]["fibonacci_sequence"]
        
        prompt = f"""
        You are a Product Owner estimating story points for a user story.
        
        Story: {story_description}
        Complexity Factors: {', '.join(factors)}
        Available Story Points: {fibonacci}
        
        Analyze the story considering:
        - Effort required
        - Technical uncertainty
        - Dependencies on other work
        - Team familiarity with the domain
        
        Return only the story point number (no explanation).
        """
        
        try:
            response = self._call_claude(prompt)
            if response:
                points = int(response.strip())
                # Ensure it's in the Fibonacci sequence
                if points in fibonacci:
                    return points
                else:
                    # Find closest Fibonacci number
                    return min(fibonacci, key=lambda x: abs(x - points))
        except Exception as e:
            logger.error(f"Error estimating story points with Claude: {e}")
        
        return self._fallback_story_points(story_description)
    
    def rank_priority(self, stories: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Rank stories by priority using Claude's analysis"""
        if not self.api_key:
            return self._fallback_priority_ranking(stories)
        
        stories_json = json.dumps(stories, indent=2)
        ranking_factors = config.behavior_params["priority_ranking"]["ranking_factors"]
        
        prompt = f"""
        You are a Product Owner ranking user stories by priority.
        
        Stories: {stories_json}
        Ranking Factors: {', '.join(ranking_factors)}
        
        Rank these stories by priority considering:
        - Business value and impact
        - Urgency and deadlines
        - Dependencies between stories
        - Effort and complexity
        
        Return the stories as a JSON array, sorted by priority (highest first).
        Add a "priority_score" field (1-10) to each story.
        """
        
        try:
            response = self._call_claude(prompt)
            if response:
                return json.loads(response)
        except Exception as e:
            logger.error(f"Error ranking priority with Claude: {e}")
            return self._fallback_priority_ranking(stories)
    
    def _call_claude(self, prompt: str) -> Optional[str]:
        """Make API call to Claude"""
        try:
            payload = {
                "model": self.model,
                "max_tokens": config.claude_max_tokens,
                "temperature": config.claude_temperature,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
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
    
    def _fallback_story_creation(self, feature_request: str) -> Dict[str, Any]:
        """Fallback story creation without Claude"""
        return {
            "title": f"Implement {feature_request}",
            "description": f"As a user, I want {feature_request} so that I can achieve my goals",
            "acceptance_criteria": [
                f"Feature {feature_request} is implemented",
                "Feature works as expected",
                "No breaking changes introduced"
            ],
            "story_points": 5,
            "priority": "Medium",
            "business_value": 5,
            "risk_level": "Medium",
            "labels": ["feature", "enhancement"]
        }
    
    def _fallback_acceptance_criteria(self, story_title: str) -> List[str]:
        """Fallback acceptance criteria without Claude"""
        return [
            f"Feature described in '{story_title}' is implemented",
            "Feature works as expected",
            "No breaking changes introduced",
            "Code follows team standards",
            "Documentation is updated"
        ]
    
    def _fallback_story_points(self, story_description: str) -> int:
        """Fallback story points estimation"""
        # Simple heuristic based on description length
        length = len(story_description)
        if length < 100:
            return 3
        elif length < 200:
            return 5
        else:
            return 8
    
    def _fallback_priority_ranking(self, stories: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Fallback priority ranking"""
        # Simple ranking by business value
        for story in stories:
            story["priority_score"] = story.get("business_value", 5)
        
        return sorted(stories, key=lambda x: x["priority_score"], reverse=True) 