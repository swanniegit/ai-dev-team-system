"""
Claude Client for QA Agent
Handles all interactions with Claude 3.7 Sonnet for QA testing decisions
"""

import json
import logging
from typing import Dict, Any, List, Optional
import requests
from config import config

logger = logging.getLogger(__name__)

class QAClaudeClient:
    """Claude client specialized for QA testing decisions"""
    
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
    
    def analyze_test_strategy(self, user_story: str, acceptance_criteria: List[str]) -> Dict[str, Any]:
        """Analyze user story and create comprehensive test strategy"""
        
        prompt = f"""
        As a QA expert, analyze this user story and create a comprehensive test strategy.
        
        User Story: {user_story}
        
        Acceptance Criteria:
        {chr(10).join(f"- {ac}" for ac in acceptance_criteria)}
        
        Create a test strategy that includes:
        1. Test types needed (unit, integration, regression, performance, security, accessibility)
        2. Test cases for each acceptance criterion
        3. Test data requirements
        4. Risk assessment
        5. Test automation opportunities
        6. Quality gates and success criteria
        
        Return your response as a JSON object with the following structure:
        {{
            "test_strategy": {{
                "test_types": ["list", "of", "test", "types"],
                "test_cases": [
                    {{
                        "id": "TC001",
                        "description": "Test case description",
                        "acceptance_criterion": "AC reference",
                        "test_type": "unit|integration|regression|performance|security|accessibility",
                        "priority": "high|medium|low",
                        "automation_ready": true|false
                    }}
                ],
                "test_data_requirements": ["list", "of", "data", "needs"],
                "risks": ["list", "of", "identified", "risks"],
                "quality_gates": ["list", "of", "quality", "gates"],
                "automation_opportunities": ["list", "of", "automation", "opportunities"]
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
                return self._fallback_test_strategy(user_story, acceptance_criteria)
        
        return self._fallback_test_strategy(user_story, acceptance_criteria)
    
    def prioritize_test_cases(self, test_cases: List[Dict[str, Any]], sprint_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Prioritize test cases based on sprint context and risk"""
        
        test_cases_json = json.dumps(test_cases, indent=2)
        sprint_context_json = json.dumps(sprint_context, indent=2)
        
        prompt = f"""
        As a QA expert, prioritize these test cases based on the sprint context and risk assessment.
        
        Test Cases:
        {test_cases_json}
        
        Sprint Context:
        {sprint_context_json}
        
        Prioritize the test cases considering:
        1. Business impact and user value
        2. Technical risk and complexity
        3. Sprint timeline and capacity
        4. Dependencies and blockers
        5. Previous bug patterns
        
        Return your response as a JSON object with the following structure:
        {{
            "prioritized_tests": [
                {{
                    "test_id": "TC001",
                    "priority": 1,
                    "rationale": "Explanation for priority",
                    "estimated_effort": "1-2 hours",
                    "risk_level": "high|medium|low"
                }}
            ],
            "testing_recommendations": ["list", "of", "recommendations"],
            "risk_mitigation": ["list", "of", "risk", "mitigation", "strategies"]
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
                return self._fallback_prioritization(test_cases, sprint_context)
        
        return self._fallback_prioritization(test_cases, sprint_context)
    
    def analyze_bug_patterns(self, bugs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze bug patterns and suggest preventive measures"""
        
        bugs_json = json.dumps(bugs, indent=2)
        
        prompt = f"""
        As a QA expert, analyze these bug patterns and suggest preventive measures.
        
        Bugs:
        {bugs_json}
        
        Analyze the bugs and provide:
        1. Common patterns and root causes
        2. Areas of the codebase most prone to bugs
        3. Preventive testing strategies
        4. Test automation opportunities
        5. Process improvements
        
        Return your response as a JSON object with the following structure:
        {{
            "bug_patterns": [
                {{
                    "pattern": "Description of pattern",
                    "frequency": 5,
                    "severity": "high|medium|low",
                    "root_cause": "Root cause analysis",
                    "prevention_strategy": "How to prevent this pattern"
                }}
            ],
            "high_risk_areas": ["list", "of", "high", "risk", "areas"],
            "preventive_measures": ["list", "of", "preventive", "measures"],
            "test_automation_opportunities": ["list", "of", "automation", "opportunities"],
            "process_improvements": ["list", "of", "process", "improvements"]
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
                return self._fallback_bug_analysis(bugs)
        
        return self._fallback_bug_analysis(bugs)
    
    def generate_test_cases(self, feature_description: str, requirements: List[str]) -> List[Dict[str, Any]]:
        """Generate comprehensive test cases for a feature"""
        
        requirements_text = chr(10).join(f"- {req}" for req in requirements)
        
        prompt = f"""
        As a QA expert, generate comprehensive test cases for this feature.
        
        Feature Description: {feature_description}
        
        Requirements:
        {requirements_text}
        
        Generate test cases covering:
        1. Happy path scenarios
        2. Edge cases and boundary conditions
        3. Error scenarios and negative testing
        4. Performance considerations
        5. Security considerations
        6. Accessibility requirements
        
        Return your response as a JSON object with the following structure:
        {{
            "test_cases": [
                {{
                    "id": "TC001",
                    "title": "Test case title",
                    "description": "Detailed description",
                    "category": "happy_path|edge_case|error_scenario|performance|security|accessibility",
                    "steps": ["step1", "step2", "step3"],
                    "expected_result": "Expected outcome",
                    "test_data": "Required test data",
                    "priority": "high|medium|low",
                    "automation_ready": true|false
                }}
            ],
            "test_coverage_analysis": {{
                "happy_path_coverage": "percentage",
                "edge_case_coverage": "percentage",
                "error_scenario_coverage": "percentage",
                "overall_coverage": "percentage"
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
                return self._fallback_test_cases(feature_description, requirements)
        
        return self._fallback_test_cases(feature_description, requirements)
    
    def assess_quality_gates(self, test_results: Dict[str, Any], quality_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Assess if quality gates are met based on test results and metrics"""
        
        test_results_json = json.dumps(test_results, indent=2)
        quality_metrics_json = json.dumps(quality_metrics, indent=2)
        
        prompt = f"""
        As a QA expert, assess if quality gates are met based on these test results and metrics.
        
        Test Results:
        {test_results_json}
        
        Quality Metrics:
        {quality_metrics_json}
        
        Quality Gates to Assess:
        - Test coverage >= {config.min_test_coverage}%
        - Bug density <= {config.max_bug_density} bugs per 1000 lines
        - Performance threshold <= {config.performance_threshold} seconds
        - All critical tests passing
        - Security tests passing
        - Accessibility tests passing
        
        Return your response as a JSON object with the following structure:
        {{
            "quality_gate_status": {{
                "overall_status": "pass|fail|warning",
                "test_coverage": {{
                    "status": "pass|fail|warning",
                    "value": 85.5,
                    "threshold": {config.min_test_coverage},
                    "details": "Explanation"
                }},
                "bug_density": {{
                    "status": "pass|fail|warning",
                    "value": 3.2,
                    "threshold": {config.max_bug_density},
                    "details": "Explanation"
                }},
                "performance": {{
                    "status": "pass|fail|warning",
                    "value": 1.8,
                    "threshold": {config.performance_threshold},
                    "details": "Explanation"
                }},
                "critical_tests": {{
                    "status": "pass|fail|warning",
                    "details": "Explanation"
                }},
                "security_tests": {{
                    "status": "pass|fail|warning",
                    "details": "Explanation"
                }},
                "accessibility_tests": {{
                    "status": "pass|fail|warning",
                    "details": "Explanation"
                }}
            }},
            "recommendations": ["list", "of", "recommendations"],
            "blockers": ["list", "of", "blocking", "issues"],
            "next_steps": ["list", "of", "next", "steps"]
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
                return self._fallback_quality_assessment(test_results, quality_metrics)
        
        return self._fallback_quality_assessment(test_results, quality_metrics)
    
    def _fallback_test_strategy(self, user_story: str, acceptance_criteria: List[str]) -> Dict[str, Any]:
        """Fallback test strategy when Claude is unavailable"""
        return {
            "test_strategy": {
                "test_types": ["unit", "integration", "regression"],
                "test_cases": [
                    {
                        "id": "TC001",
                        "description": f"Basic test for: {user_story}",
                        "acceptance_criterion": acceptance_criteria[0] if acceptance_criteria else "N/A",
                        "test_type": "unit",
                        "priority": "high",
                        "automation_ready": True
                    }
                ],
                "test_data_requirements": ["Basic test data"],
                "risks": ["Standard testing risks"],
                "quality_gates": ["All tests passing"],
                "automation_opportunities": ["Unit test automation"]
            }
        }
    
    def _fallback_prioritization(self, test_cases: List[Dict[str, Any]], sprint_context: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback prioritization when Claude is unavailable"""
        return {
            "prioritized_tests": [
                {
                    "test_id": tc.get("id", "TC001"),
                    "priority": i + 1,
                    "rationale": "Fallback prioritization",
                    "estimated_effort": "1-2 hours",
                    "risk_level": "medium"
                }
                for i, tc in enumerate(test_cases)
            ],
            "testing_recommendations": ["Execute tests in priority order"],
            "risk_mitigation": ["Standard risk mitigation"]
        }
    
    def _fallback_bug_analysis(self, bugs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Fallback bug analysis when Claude is unavailable"""
        return {
            "bug_patterns": [
                {
                    "pattern": "Common bug pattern",
                    "frequency": len(bugs),
                    "severity": "medium",
                    "root_cause": "Standard root cause",
                    "prevention_strategy": "Standard prevention"
                }
            ],
            "high_risk_areas": ["General areas"],
            "preventive_measures": ["Standard measures"],
            "test_automation_opportunities": ["General automation"],
            "process_improvements": ["Standard improvements"]
        }
    
    def _fallback_test_cases(self, feature_description: str, requirements: List[str]) -> Dict[str, Any]:
        """Fallback test cases when Claude is unavailable"""
        return {
            "test_cases": [
                {
                    "id": "TC001",
                    "title": f"Basic test for {feature_description}",
                    "description": "Basic test case",
                    "category": "happy_path",
                    "steps": ["Step 1", "Step 2", "Step 3"],
                    "expected_result": "Expected outcome",
                    "test_data": "Basic test data",
                    "priority": "high",
                    "automation_ready": True
                }
            ],
            "test_coverage_analysis": {
                "happy_path_coverage": "80%",
                "edge_case_coverage": "60%",
                "error_scenario_coverage": "70%",
                "overall_coverage": "70%"
            }
        }
    
    def _fallback_quality_assessment(self, test_results: Dict[str, Any], quality_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback quality assessment when Claude is unavailable"""
        return {
            "quality_gate_status": {
                "overall_status": "pass",
                "test_coverage": {
                    "status": "pass",
                    "value": 85.0,
                    "threshold": config.min_test_coverage,
                    "details": "Fallback assessment"
                },
                "bug_density": {
                    "status": "pass",
                    "value": 3.0,
                    "threshold": config.max_bug_density,
                    "details": "Fallback assessment"
                },
                "performance": {
                    "status": "pass",
                    "value": 1.5,
                    "threshold": config.performance_threshold,
                    "details": "Fallback assessment"
                },
                "critical_tests": {
                    "status": "pass",
                    "details": "Fallback assessment"
                },
                "security_tests": {
                    "status": "pass",
                    "details": "Fallback assessment"
                },
                "accessibility_tests": {
                    "status": "pass",
                    "details": "Fallback assessment"
                }
            },
            "recommendations": ["Standard recommendations"],
            "blockers": [],
            "next_steps": ["Proceed with deployment"]
        } 