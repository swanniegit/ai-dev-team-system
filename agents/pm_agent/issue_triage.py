"""
Issue Triage Logic for PM Agent
"""

import re
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

from .config import config

logger = logging.getLogger(__name__)


class IssueTriageEngine:
    """Engine for triaging and categorizing issues"""
    
    def __init__(self):
        self.priority_keywords = config.priority_keywords
        self.auto_assign_rules = config.auto_assign_rules
    
    def analyze_issue(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze an issue and determine priority, type, and assignment"""
        
        title = issue.get("title", "").lower()
        description = issue.get("description", "").lower()
        full_text = f"{title} {description}"
        
        # Determine priority
        priority = self._determine_priority(full_text)
        
        # Determine issue type
        issue_type = self._determine_issue_type(full_text)
        
        # Determine assignment
        assignee_type = self._determine_assignment(issue_type, full_text)
        
        # Generate labels
        labels = self._generate_labels(full_text, priority, issue_type)
        
        return {
            "priority": priority,
            "issue_type": issue_type,
            "assignee_type": assignee_type,
            "labels": labels,
            "analysis": {
                "confidence": 0.85,  # TODO: Implement confidence scoring
                "reasoning": f"Priority: {priority} based on keywords. Type: {issue_type}. Assign to: {assignee_type}"
            }
        }
    
    def _determine_priority(self, text: str) -> str:
        """Determine issue priority based on keywords"""
        text_lower = text.lower()
        
        # Check for critical keywords
        for keyword in self.priority_keywords["critical"]:
            if keyword in text_lower:
                return "critical"
        
        # Check for high priority keywords
        for keyword in self.priority_keywords["high"]:
            if keyword in text_lower:
                return "high"
        
        # Check for low priority keywords
        for keyword in self.priority_keywords["low"]:
            if keyword in text_lower:
                return "low"
        
        # Default to medium
        return "medium"
    
    def _determine_issue_type(self, text: str) -> str:
        """Determine issue type based on content"""
        text_lower = text.lower()
        
        # Check for specific patterns
        if any(word in text_lower for word in ["bug", "error", "crash", "broken", "fails"]):
            return "bug"
        elif any(word in text_lower for word in ["feature", "new", "add", "implement"]):
            return "feature"
        elif any(word in text_lower for word in ["story", "user story", "as a user"]):
            return "story"
        elif any(word in text_lower for word in ["epic", "large", "major"]):
            return "epic"
        elif any(word in text_lower for word in ["task", "work", "do"]):
            return "task"
        else:
            return "task"  # Default
    
    def _determine_assignment(self, issue_type: str, text: str) -> str:
        """Determine which agent type should handle this issue"""
        
        # Use auto-assign rules
        if issue_type in self.auto_assign_rules:
            return self.auto_assign_rules[issue_type]
        
        # Fallback logic
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["test", "qa", "quality"]):
            return "qa_engineer"
        elif any(word in text_lower for word in ["design", "architecture", "arch"]):
            return "software_architect"
        elif any(word in text_lower for word in ["code", "implement", "develop"]):
            return "developer"
        else:
            return "product_owner"  # Default
    
    def _generate_labels(self, text: str, priority: str, issue_type: str) -> List[str]:
        """Generate appropriate labels for the issue"""
        labels = [priority, issue_type]
        
        text_lower = text.lower()
        
        # Add technology labels
        tech_keywords = {
            "frontend": ["react", "vue", "angular", "javascript", "typescript", "css", "html"],
            "backend": ["python", "java", "node", "api", "database", "sql"],
            "devops": ["docker", "kubernetes", "ci/cd", "deploy", "infrastructure"],
            "security": ["security", "auth", "authentication", "encryption", "vulnerability"]
        }
        
        for label, keywords in tech_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                labels.append(label)
        
        # Add urgency labels
        if priority in ["critical", "high"]:
            labels.append("urgent")
        
        return labels
    
    def triage_issues(self, issues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Triage a list of issues"""
        triaged_issues = []
        
        for issue in issues:
            try:
                analysis = self.analyze_issue(issue)
                triaged_issue = {
                    **issue,
                    "triage_analysis": analysis,
                    "triaged_at": datetime.utcnow().isoformat(),
                    "triaged_by": config.name
                }
                triaged_issues.append(triaged_issue)
                
                logger.info(f"Triaged issue {issue.get('id', 'unknown')}: {analysis['priority']} priority, {analysis['issue_type']} type")
                
            except Exception as e:
                logger.error(f"Failed to triage issue {issue.get('id', 'unknown')}: {e}")
                # Add issue with default analysis
                triaged_issues.append({
                    **issue,
                    "triage_analysis": {
                        "priority": "medium",
                        "issue_type": "task",
                        "assignee_type": "product_owner",
                        "labels": ["needs-review"],
                        "analysis": {"confidence": 0.0, "reasoning": "Failed to analyze"}
                    },
                    "triaged_at": datetime.utcnow().isoformat(),
                    "triaged_by": config.name
                })
        
        return triaged_issues


# Global triage engine instance
triage_engine = IssueTriageEngine() 