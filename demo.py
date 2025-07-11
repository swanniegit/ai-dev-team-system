#!/usr/bin/env python3
"""
Demo script for the Agentic Agile System API Hub
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def print_response(response, title):
    """Print formatted response"""
    print(f"\n{'='*50}")
    print(f"{title}")
    print(f"{'='*50}")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def demo_health_checks():
    """Demo health check endpoints"""
    print("\n🔍 Testing Health Checks...")
    
    # Health check
    response = requests.get(f"{BASE_URL}/health")
    print_response(response, "Health Check")
    
    # Ready check
    response = requests.get(f"{BASE_URL}/ready")
    print_response(response, "Ready Check")
    
    # Metrics
    response = requests.get(f"{BASE_URL}/metrics")
    print_response(response, "Metrics")

def demo_agent_management():
    """Demo agent management"""
    print("\n🤖 Testing Agent Management...")
    
    # Register a PM Agent
    pm_agent = {
        "name": "PM Agent Alpha",
        "agent_type": "project_manager",
        "capabilities": ["issue_triage", "sprint_planning"],
        "metadata": {"version": "1.0.0", "team": "Alpha"}
    }
    
    response = requests.post(f"{BASE_URL}/v1/agents/register", json=pm_agent)
    print_response(response, "Register PM Agent")
    
    if response.status_code == 201:
        agent_id = response.json()["id"]
        
        # Get agent status
        response = requests.get(f"{BASE_URL}/v1/agents/{agent_id}/status")
        print_response(response, "Agent Status")
        
        # Trigger agent action
        trigger_data = {
            "action": "triage_issues",
            "parameters": {"priority": "high"},
            "priority": 5
        }
        
        response = requests.post(f"{BASE_URL}/v1/agents/{agent_id}/trigger", json=trigger_data)
        print_response(response, "Trigger Agent Action")
    
    # List all agents
    response = requests.get(f"{BASE_URL}/v1/agents/")
    print_response(response, "List All Agents")

def demo_issue_management():
    """Demo issue management"""
    print("\n📋 Testing Issue Management...")
    
    # Create an issue
    issue = {
        "title": "Implement user authentication",
        "description": "Add JWT-based authentication to the API",
        "issue_type": "feature",
        "priority": "high",
        "labels": ["auth", "security"],
        "created_by": "user123"
    }
    
    response = requests.post(f"{BASE_URL}/v1/issues/", json=issue)
    print_response(response, "Create Issue")
    
    # Generate stories
    story_request = {
        "feature_description": "User dashboard with analytics",
        "acceptance_criteria": ["User can view metrics", "User can export data"],
        "story_points": 8,
        "priority": "medium"
    }
    
    response = requests.post(f"{BASE_URL}/v1/issues/generate-stories", json=story_request)
    print_response(response, "Generate Stories")
    
    # List issues
    response = requests.get(f"{BASE_URL}/v1/issues/")
    print_response(response, "List Issues")

def demo_wellness_tracking():
    """Demo wellness tracking"""
    print("\n💚 Testing Wellness Tracking...")
    
    # Create wellness check-in
    checkin = {
        "user_id": "user123",
        "mood_level": "good",
        "energy_level": 7,
        "stress_level": 4,
        "satisfaction_level": 8,
        "engagement_level": 9,
        "workload_level": 6,
        "notes": "Feeling productive today!"
    }
    
    response = requests.post(f"{BASE_URL}/v1/wellness/checkin", json=checkin)
    print_response(response, "Wellness Check-in")
    
    # Get wellness metrics
    response = requests.get(f"{BASE_URL}/v1/wellness/metrics")
    print_response(response, "Wellness Metrics")

def demo_dashboard():
    """Demo dashboard endpoints"""
    print("\n📊 Testing Dashboard...")
    
    # Get dashboard metrics
    response = requests.get(f"{BASE_URL}/v1/dashboard/metrics")
    print_response(response, "Dashboard Metrics")
    
    # Get analytics
    response = requests.get(f"{BASE_URL}/v1/dashboard/analytics")
    print_response(response, "Analytics")

def main():
    """Run the demo"""
    print("🚀 Agentic Agile System API Hub - Demo")
    print("=" * 60)
    
    try:
        # Test if API is running
        response = requests.get(f"{BASE_URL}/")
        if response.status_code != 200:
            print(f"❌ API is not running at {BASE_URL}")
            print("Please start the API first with: python start.py")
            return
        
        print("✅ API is running!")
        
        # Run demos
        demo_health_checks()
        demo_agent_management()
        demo_issue_management()
        demo_wellness_tracking()
        demo_dashboard()
        
        print("\n🎉 Demo completed successfully!")
        print(f"📖 API Documentation: {BASE_URL}/docs")
        
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to API at {BASE_URL}")
        print("Please start the API first with: python start.py")
    except Exception as e:
        print(f"❌ Error during demo: {e}")

if __name__ == "__main__":
    main() 