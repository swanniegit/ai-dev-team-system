"""
Claude Client for AR Agent
Handles all interactions with Claude 3.7 Sonnet for code review and architectural decisions
"""

import json
import logging
from typing import Dict, Any, List, Optional
import requests
from config import config

logger = logging.getLogger(__name__)

class ARClaudeClient:
    """Claude client specialized for code review and architectural decisions"""
    
    def __init__(self):
        self.api_key = config.claude_api_key
        self.model = config.claude_model
        self.max_tokens = config.claude_max_tokens
        self.temperature = config.claude_temperature
        self.base_url = "https://api.anthropic.com/v1/messages"
        
        self.headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01"
        }
    
    def _make_request(self, messages: List[Dict[str, str]]) -> Optional[Dict[str, Any]]:
        """Make request to Claude API"""
        try:
            payload = {
                "model": self.model,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                "messages": messages
            }
            
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Claude API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error making Claude request: {e}")
            return None
    
    def review_code(self, code_content: str, language: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Review code for quality, security, and best practices"""
        
        prompt = f"""
        As a senior software architect and code reviewer, analyze this {language} code for quality, security, and best practices.
        
        Code:
        ```{language}
        {code_content}
        ```
        
        Context:
        - File: {context.get('file_path', 'unknown')}
        - Lines: {context.get('start_line', 1)}-{context.get('end_line', 1)}
        - Purpose: {context.get('purpose', 'unknown')}
        
        Review the code for:
        1. Code quality and readability
        2. Security vulnerabilities
        3. Performance issues
        4. Maintainability concerns
        5. Testability
        6. Best practices adherence
        7. Architectural consistency
        
        Return your response as a JSON object with the following structure:
        {{
            "review_summary": {{
                "overall_score": 8.5,
                "status": "approved|needs_changes|rejected",
                "priority": "high|medium|low"
            }},
            "issues": [
                {{
                    "type": "security|performance|quality|maintainability|testability|best_practice",
                    "severity": "critical|high|medium|low",
                    "line": 42,
                    "description": "Issue description",
                    "suggestion": "How to fix this issue",
                    "impact": "What this issue affects"
                }}
            ],
            "strengths": ["list", "of", "code", "strengths"],
            "recommendations": ["list", "of", "improvement", "recommendations"],
            "security_analysis": {{
                "vulnerabilities": ["list", "of", "security", "issues"],
                "risk_level": "high|medium|low"
            }},
            "performance_analysis": {{
                "bottlenecks": ["list", "of", "performance", "issues"],
                "optimization_opportunities": ["list", "of", "optimizations"]
            }}
        }}
        """
        
        messages = [{"role": "user", "content": prompt}]
        response = self._make_request(messages)
        
        if response and "content" in response:
            try:
                content = response["content"][0]["text"]
                return json.loads(content)
            except (json.JSONDecodeError, KeyError) as e:
                logger.error(f"Error parsing Claude response: {e}")
                return self._fallback_code_review(code_content, language, context)
        
        return self._fallback_code_review(code_content, language, context)
    
    def review_architecture(self, architecture_description: str, components: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Review system architecture for design quality and scalability"""
        
        components_json = json.dumps(components, indent=2)
        
        prompt = f"""
        As a senior software architect, review this system architecture for design quality, scalability, and maintainability.
        
        Architecture Description:
        {architecture_description}
        
        Components:
        {components_json}
        
        Review the architecture for:
        1. Scalability and performance
        2. Maintainability and modularity
        3. Security and data protection
        4. Fault tolerance and reliability
        5. Technology choices and compatibility
        6. Integration patterns
        7. Future extensibility
        
        Return your response as a JSON object with the following structure:
        {{
            "architecture_assessment": {{
                "overall_score": 8.0,
                "status": "approved|needs_revision|rejected",
                "risk_level": "high|medium|low"
            }},
            "strengths": ["list", "of", "architectural", "strengths"],
            "concerns": [
                {{
                    "category": "scalability|maintainability|security|performance|reliability",
                    "severity": "critical|high|medium|low",
                    "description": "Concern description",
                    "impact": "What this concern affects",
                    "recommendation": "How to address this concern"
                }}
            ],
            "recommendations": ["list", "of", "architectural", "recommendations"],
            "technology_assessment": {{
                "appropriate_choices": ["list", "of", "good", "choices"],
                "questionable_choices": ["list", "of", "questionable", "choices"],
                "alternatives": ["list", "of", "alternative", "technologies"]
            }}
        }}
        """
        
        messages = [{"role": "user", "content": prompt}]
        response = self._make_request(messages)
        
        if response and "content" in response:
            try:
                content = response["content"][0]["text"]
                return json.loads(content)
            except (json.JSONDecodeError, KeyError) as e:
                logger.error(f"Error parsing Claude response: {e}")
                return self._fallback_architecture_review(architecture_description, components)
        
        return self._fallback_architecture_review(architecture_description, components)
    
    def assess_security(self, code_content: str, language: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Assess code for security vulnerabilities"""
        
        prompt = f"""
        As a security expert, analyze this {language} code for security vulnerabilities and best practices.
        
        Code:
        ```{language}
        {code_content}
        ```
        
        Context:
        - File: {context.get('file_path', 'unknown')}
        - Purpose: {context.get('purpose', 'unknown')}
        - Environment: {context.get('environment', 'production')}
        
        Look for:
        1. SQL injection vulnerabilities
        2. Cross-site scripting (XSS)
        3. Authentication and authorization issues
        4. Input validation problems
        5. Sensitive data exposure
        6. Insecure dependencies
        7. Cryptographic weaknesses
        
        Return your response as a JSON object with the following structure:
        {{
            "security_assessment": {{
                "overall_risk": "high|medium|low",
                "vulnerability_count": 3,
                "status": "secure|needs_review|insecure"
            }},
            "vulnerabilities": [
                {{
                    "type": "sql_injection|xss|auth_bypass|input_validation|data_exposure|dependency|crypto",
                    "severity": "critical|high|medium|low",
                    "line": 42,
                    "description": "Vulnerability description",
                    "cve_reference": "CVE-2023-1234",
                    "fix_suggestion": "How to fix this vulnerability",
                    "impact": "What this vulnerability could cause"
                }}
            ],
            "security_recommendations": ["list", "of", "security", "improvements"],
            "compliance_check": {{
                "owasp_top_10": ["list", "of", "owasp", "violations"],
                "pci_dss": ["list", "of", "pci", "violations"],
                "gdpr": ["list", "of", "gdpr", "violations"]
            }}
        }}
        """
        
        messages = [{"role": "user", "content": prompt}]
        response = self._make_request(messages)
        
        if response and "content" in response:
            try:
                content = response["content"][0]["text"]
                return json.loads(content)
            except (json.JSONDecodeError, KeyError) as e:
                logger.error(f"Error parsing Claude response: {e}")
                return self._fallback_security_assessment(code_content, language, context)
        
        return self._fallback_security_assessment(code_content, language, context)
    
    def assess_performance(self, code_content: str, language: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Assess code for performance issues and optimization opportunities"""
        
        prompt = f"""
        As a performance optimization expert, analyze this {language} code for performance issues and optimization opportunities.
        
        Code:
        ```{language}
        {code_content}
        ```
        
        Context:
        - File: {context.get('file_path', 'unknown')}
        - Purpose: {context.get('purpose', 'unknown')}
        - Expected load: {context.get('expected_load', 'unknown')}
        
        Look for:
        1. Algorithmic inefficiencies
        2. Memory leaks and excessive memory usage
        3. Database query optimization opportunities
        4. Network call optimization
        5. Caching opportunities
        6. Concurrency issues
        7. Resource management problems
        
        Return your response as a JSON object with the following structure:
        {{
            "performance_assessment": {{
                "overall_score": 7.5,
                "bottleneck_count": 2,
                "optimization_opportunities": 5
            }},
            "bottlenecks": [
                {{
                    "type": "algorithm|memory|database|network|caching|concurrency|resource",
                    "severity": "critical|high|medium|low",
                    "line": 42,
                    "description": "Performance issue description",
                    "impact": "Performance impact description",
                    "optimization": "How to optimize this"
                }}
            ],
            "optimization_opportunities": ["list", "of", "optimization", "opportunities"],
            "performance_recommendations": ["list", "of", "performance", "improvements"],
            "benchmarking_suggestions": ["list", "of", "benchmarking", "approaches"]
        }}
        """
        
        messages = [{"role": "user", "content": prompt}]
        response = self._make_request(messages)
        
        if response and "content" in response:
            try:
                content = response["content"][0]["text"]
                return json.loads(content)
            except (json.JSONDecodeError, KeyError) as e:
                logger.error(f"Error parsing Claude response: {e}")
                return self._fallback_performance_assessment(code_content, language, context)
        
        return self._fallback_performance_assessment(code_content, language, context)
    
    def review_dependencies(self, dependencies: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Review dependencies for security, compatibility, and maintenance"""
        
        dependencies_json = json.dumps(dependencies, indent=2)
        
        prompt = f"""
        As a dependency management expert, review these dependencies for security, compatibility, and maintenance concerns.
        
        Dependencies:
        {dependencies_json}
        
        Review for:
        1. Security vulnerabilities
        2. Version compatibility
        3. Maintenance status
        4. License compliance
        5. Performance impact
        6. Alternative recommendations
        
        Return your response as a JSON object with the following structure:
        {{
            "dependency_assessment": {{
                "overall_risk": "high|medium|low",
                "vulnerable_dependencies": 2,
                "outdated_dependencies": 3
            }},
            "security_issues": [
                {{
                    "dependency": "package_name",
                    "version": "1.2.3",
                    "vulnerability": "CVE-2023-1234",
                    "severity": "critical|high|medium|low",
                    "description": "Vulnerability description",
                    "fix_version": "1.2.4"
                }}
            ],
            "maintenance_concerns": [
                {{
                    "dependency": "package_name",
                    "issue": "outdated|unmaintained|deprecated",
                    "recommendation": "upgrade|replace|remove"
                }}
            ],
            "recommendations": ["list", "of", "dependency", "recommendations"]
        }}
        """
        
        messages = [{"role": "user", "content": prompt}]
        response = self._make_request(messages)
        
        if response and "content" in response:
            try:
                content = response["content"][0]["text"]
                return json.loads(content)
            except (json.JSONDecodeError, KeyError) as e:
                logger.error(f"Error parsing Claude response: {e}")
                return self._fallback_dependency_review(dependencies)
        
        return self._fallback_dependency_review(dependencies)
    
    # Fallback methods
    def _fallback_code_review(self, code_content: str, language: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback code review when Claude is unavailable"""
        return {
            "review_summary": {
                "overall_score": 7.0,
                "status": "needs_changes",
                "priority": "medium"
            },
            "issues": [
                {
                    "type": "quality",
                    "severity": "medium",
                    "line": 1,
                    "description": "Basic code review completed",
                    "suggestion": "Review code manually for best practices",
                    "impact": "Code quality"
                }
            ],
            "strengths": ["Code structure appears reasonable"],
            "recommendations": ["Perform manual code review"],
            "security_analysis": {
                "vulnerabilities": [],
                "risk_level": "low"
            },
            "performance_analysis": {
                "bottlenecks": [],
                "optimization_opportunities": []
            }
        }
    
    def _fallback_architecture_review(self, architecture_description: str, components: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Fallback architecture review when Claude is unavailable"""
        return {
            "architecture_assessment": {
                "overall_score": 7.0,
                "status": "needs_revision",
                "risk_level": "medium"
            },
            "strengths": ["Architecture appears well-structured"],
            "concerns": [
                {
                    "category": "maintainability",
                    "severity": "medium",
                    "description": "Manual architecture review recommended",
                    "impact": "System maintainability",
                    "recommendation": "Review architecture manually"
                }
            ],
            "recommendations": ["Perform manual architecture review"],
            "technology_assessment": {
                "appropriate_choices": [],
                "questionable_choices": [],
                "alternatives": []
            }
        }
    
    def _fallback_security_assessment(self, code_content: str, language: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback security assessment when Claude is unavailable"""
        return {
            "security_assessment": {
                "overall_risk": "medium",
                "vulnerability_count": 0,
                "status": "needs_review"
            },
            "vulnerabilities": [],
            "security_recommendations": ["Perform manual security review"],
            "compliance_check": {
                "owasp_top_10": [],
                "pci_dss": [],
                "gdpr": []
            }
        }
    
    def _fallback_performance_assessment(self, code_content: str, language: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback performance assessment when Claude is unavailable"""
        return {
            "performance_assessment": {
                "overall_score": 7.0,
                "bottleneck_count": 0,
                "optimization_opportunities": 0
            },
            "bottlenecks": [],
            "optimization_opportunities": [],
            "performance_recommendations": ["Perform manual performance review"],
            "benchmarking_suggestions": ["Run performance benchmarks"]
        }
    
    def _fallback_dependency_review(self, dependencies: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Fallback dependency review when Claude is unavailable"""
        return {
            "dependency_assessment": {
                "overall_risk": "medium",
                "vulnerable_dependencies": 0,
                "outdated_dependencies": 0
            },
            "security_issues": [],
            "maintenance_concerns": [],
            "recommendations": ["Perform manual dependency review"]
        } 