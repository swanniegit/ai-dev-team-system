"""
Test suite for QA Agent
Tests all QA behaviors and Claude integration
"""

import asyncio
import json
import unittest
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime

from main import QAAgent
from config import config
from claude_client import QAClaudeClient

class TestQAAgent(unittest.TestCase):
    """Test cases for QA Agent"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.agent = QAAgent()
    
    def test_agent_initialization(self):
        """Test QA Agent initialization"""
        self.assertEqual(self.agent.config.agent_name, "qa_agent")
        self.assertEqual(self.agent.config.agent_version, "1.0.0")
        self.assertEqual(self.agent.agent_status, "initializing")
        self.assertIsNotNone(self.agent.claude_client)
    
    def test_config_validation(self):
        """Test configuration validation"""
        # Test valid config
        self.assertIsNotNone(config.agent_name)
        self.assertIsNotNone(config.claude_model)
        self.assertGreater(config.min_test_coverage, 0)
        self.assertLess(config.min_test_coverage, 100)
    
    def test_behavior_configuration(self):
        """Test behavior configuration"""
        behaviors = config.behaviors
        
        # Check required behaviors exist
        required_behaviors = [
            "test_planning", "test_execution", "bug_tracking",
            "quality_reporting", "test_automation", "performance_testing",
            "security_testing", "accessibility_testing", "regression_testing",
            "test_coverage_analysis"
        ]
        
        for behavior in required_behaviors:
            self.assertIn(behavior, behaviors)
            self.assertIn("enabled", behaviors[behavior])
            self.assertIn("frequency", behaviors[behavior])
            self.assertIn("priority", behaviors[behavior])
    
    def test_should_run_behavior(self):
        """Test behavior frequency logic"""
        current_time = datetime.now()
        
        # Test continuous frequency
        self.assertTrue(self.agent._should_run_behavior("continuous", None, current_time))
        self.assertTrue(self.agent._should_run_behavior("continuous", current_time, current_time))
        
        # Test real_time frequency
        self.assertTrue(self.agent._should_run_behavior("real_time", None, current_time))
        
        # Test daily frequency
        self.assertTrue(self.agent._should_run_behavior("daily", None, current_time))
    
    def test_quality_metrics_calculation(self):
        """Test quality metrics calculation"""
        # Add some test results
        test_result = {
            "status": "passed",
            "duration": 2.5
        }
        
        self.agent._update_quality_metrics(test_result)
        
        metrics = self.agent.quality_metrics["quality_metrics"]
        self.assertEqual(metrics["total_tests"], 1)
        self.assertEqual(metrics["passed_tests"], 1)
        self.assertEqual(metrics["failed_tests"], 0)
        self.assertEqual(metrics["average_duration"], 2.5)
        
        # Add a failed test
        failed_result = {
            "status": "failed",
            "duration": 1.0
        }
        
        self.agent._update_quality_metrics(failed_result)
        
        metrics = self.agent.quality_metrics["quality_metrics"]
        self.assertEqual(metrics["total_tests"], 2)
        self.assertEqual(metrics["passed_tests"], 1)
        self.assertEqual(metrics["failed_tests"], 1)
        self.assertEqual(metrics["average_duration"], 1.75)  # (2.5 + 1.0) / 2
    
    def test_calculate_quality_metrics(self):
        """Test comprehensive quality metrics calculation"""
        # Set up some test data
        self.agent.quality_metrics["quality_metrics"] = {
            "total_tests": 10,
            "passed_tests": 8,
            "failed_tests": 2,
            "average_duration": 2.5
        }
        
        self.agent.bug_tracker = {
            "bug1": {"bug": {"id": "bug1"}},
            "bug2": {"bug": {"id": "bug2"}}
        }
        
        metrics = self.agent._calculate_quality_metrics()
        
        self.assertEqual(metrics["test_pass_rate"], 80.0)  # 8/10 * 100
        self.assertEqual(metrics["average_test_duration"], 2.5)
        self.assertEqual(metrics["total_tests_executed"], 10)
        self.assertEqual(metrics["bug_density"], 0.2)  # 2 bugs / 10 tests
        self.assertIn("last_updated", metrics)
    
    def test_get_status(self):
        """Test agent status retrieval"""
        status = self.agent.get_status()
        
        self.assertIn("agent_name", status)
        self.assertIn("agent_version", status)
        self.assertIn("status", status)
        self.assertIn("last_activity", status)
        self.assertIn("behaviors", status)
        self.assertIn("quality_metrics", status)
        self.assertIn("bug_count", status)
        
        self.assertEqual(status["agent_name"], "qa_agent")
        self.assertEqual(status["agent_version"], "1.0.0")
        self.assertEqual(status["bug_count"], 0)

class TestQAClaudeClient(unittest.TestCase):
    """Test cases for QA Claude Client"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.claude_client = QAClaudeClient()
    
    def test_claude_client_initialization(self):
        """Test Claude client initialization"""
        self.assertIsNotNone(self.claude_client.api_key)
        self.assertEqual(self.claude_client.model, "claude-3-5-sonnet-20241022")
        self.assertEqual(self.claude_client.max_tokens, 4000)
        self.assertEqual(self.claude_client.temperature, 0.1)
    
    def test_fallback_test_strategy(self):
        """Test fallback test strategy generation"""
        user_story = "As a user, I want to login to the system"
        acceptance_criteria = ["User can enter credentials", "User can submit form"]
        
        strategy = self.claude_client._fallback_test_strategy(user_story, acceptance_criteria)
        
        self.assertIn("test_strategy", strategy)
        self.assertIn("test_types", strategy["test_strategy"])
        self.assertIn("test_cases", strategy["test_strategy"])
        self.assertIn("test_data_requirements", strategy["test_strategy"])
        self.assertIn("risks", strategy["test_strategy"])
        self.assertIn("quality_gates", strategy["test_strategy"])
        self.assertIn("automation_opportunities", strategy["test_strategy"])
    
    def test_fallback_prioritization(self):
        """Test fallback test prioritization"""
        test_cases = [
            {"id": "TC001", "description": "Test 1"},
            {"id": "TC002", "description": "Test 2"}
        ]
        sprint_context = {"sprint": "Sprint 1"}
        
        result = self.claude_client._fallback_prioritization(test_cases, sprint_context)
        
        self.assertIn("prioritized_tests", result)
        self.assertIn("testing_recommendations", result)
        self.assertIn("risk_mitigation", result)
        
        self.assertEqual(len(result["prioritized_tests"]), 2)
        self.assertEqual(result["prioritized_tests"][0]["test_id"], "TC001")
        self.assertEqual(result["prioritized_tests"][1]["test_id"], "TC002")
    
    def test_fallback_bug_analysis(self):
        """Test fallback bug analysis"""
        bugs = [
            {"id": "bug1", "description": "Bug 1"},
            {"id": "bug2", "description": "Bug 2"}
        ]
        
        analysis = self.claude_client._fallback_bug_analysis(bugs)
        
        self.assertIn("bug_patterns", analysis)
        self.assertIn("high_risk_areas", analysis)
        self.assertIn("preventive_measures", analysis)
        self.assertIn("test_automation_opportunities", analysis)
        self.assertIn("process_improvements", analysis)
    
    def test_fallback_test_cases(self):
        """Test fallback test case generation"""
        feature_description = "User login feature"
        requirements = ["Secure authentication", "Password validation"]
        
        result = self.claude_client._fallback_test_cases(feature_description, requirements)
        
        self.assertIn("test_cases", result)
        self.assertIn("test_coverage_analysis", result)
        
        self.assertGreater(len(result["test_cases"]), 0)
        self.assertIn("id", result["test_cases"][0])
        self.assertIn("title", result["test_cases"][0])
        self.assertIn("category", result["test_cases"][0])
    
    def test_fallback_quality_assessment(self):
        """Test fallback quality assessment"""
        test_results = {"test1": "passed", "test2": "failed"}
        quality_metrics = {"coverage": 85.0}
        
        assessment = self.claude_client._fallback_quality_assessment(test_results, quality_metrics)
        
        self.assertIn("quality_gate_status", assessment)
        self.assertIn("recommendations", assessment)
        self.assertIn("blockers", assessment)
        self.assertIn("next_steps", assessment)
        
        self.assertEqual(assessment["quality_gate_status"]["overall_status"], "pass")

class TestQAIntegration(unittest.TestCase):
    """Integration tests for QA Agent"""
    
    @patch('requests.post')
    @patch('requests.get')
    def test_api_hub_registration(self, mock_get, mock_post):
        """Test API Hub registration"""
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"status": "success"}
        
        agent = QAAgent()
        
        # Test registration data structure
        registration_data = {
            "agent_name": agent.config.agent_name,
            "agent_version": agent.config.agent_version,
            "agent_description": agent.config.agent_description,
            "capabilities": list(agent.config.behaviors.keys()),
            "config": agent.config.to_dict()
        }
        
        self.assertIn("agent_name", registration_data)
        self.assertIn("agent_version", registration_data)
        self.assertIn("capabilities", registration_data)
        self.assertIn("config", registration_data)
        
        # Verify capabilities include all behaviors
        self.assertEqual(len(registration_data["capabilities"]), 10)
        self.assertIn("test_planning", registration_data["capabilities"])
        self.assertIn("test_execution", registration_data["capabilities"])
    
    def test_behavior_execution_flow(self):
        """Test behavior execution flow"""
        agent = QAAgent()
        
        # Test behavior status tracking
        for behavior_name in agent.behavior_status:
            self.assertIn("last_run", agent.behavior_status[behavior_name])
            self.assertIn("status", agent.behavior_status[behavior_name])
            self.assertEqual(agent.behavior_status[behavior_name]["status"], "idle")

def run_tests():
    """Run all QA Agent tests"""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestQAAgent))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestQAClaudeClient))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestQAIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"QA Agent Test Results")
    print(f"{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\nFailures:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print(f"\nErrors:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1) 