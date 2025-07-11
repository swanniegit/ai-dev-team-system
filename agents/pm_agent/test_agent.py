#!/usr/bin/env python3
"""
Test script for PM Agent
"""

import sys
import os
import time
import requests

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api_client import APIClient
from issue_triage import triage_engine
from config import config


def test_api_connection():
    """Test connection to the API hub"""
    print("🔌 Testing API connection...")
    
    client = APIClient()
    
    # Test health check
    if client.health_check():
        print("✅ API hub is healthy")
        return True
    else:
        print("❌ API hub is not responding")
        return False


def test_agent_registration():
    """Test agent registration"""
    print("\n🤖 Testing agent registration...")
    
    client = APIClient()
    
    try:
        agent_data = client.register_agent()
        print(f"✅ Agent registered successfully!")
        print(f"   Agent ID: {agent_data['id']}")
        print(f"   Name: {agent_data['name']}")
        print(f"   Type: {agent_data['agent_type']}")
        return agent_data['id']
    except Exception as e:
        print(f"❌ Failed to register agent: {e}")
        return None


def test_issue_triage():
    """Test issue triage functionality"""
    print("\n📋 Testing issue triage...")
    
    # Sample issues to test
    test_issues = [
        {
            "id": "test-1",
            "title": "Critical security vulnerability in authentication",
            "description": "Users can bypass login with SQL injection attack. This is urgent and affects production."
        },
        {
            "id": "test-2", 
            "title": "Add new feature for user dashboard",
            "description": "Implement a new dashboard widget to show user statistics and analytics."
        },
        {
            "id": "test-3",
            "title": "Fix typo in documentation",
            "description": "There's a small typo in the README file that needs to be corrected."
        },
        {
            "id": "test-4",
            "title": "Performance issue with database queries",
            "description": "The user list page is loading slowly due to inefficient database queries."
        }
    ]
    
    # Triage the issues
    triaged_issues = triage_engine.triage_issues(test_issues)
    
    print(f"✅ Triaged {len(triaged_issues)} issues:")
    
    for issue in triaged_issues:
        analysis = issue['triage_analysis']
        print(f"   📝 {issue['title']}")
        print(f"      Priority: {analysis['priority']}")
        print(f"      Type: {analysis['issue_type']}")
        print(f"      Assign to: {analysis['assignee_type']}")
        print(f"      Labels: {', '.join(analysis['labels'])}")
        print()


def test_issue_creation():
    """Test creating issues via API"""
    print("\n📝 Testing issue creation...")
    
    client = APIClient()
    
    # Create a test issue
    test_issue = {
        "title": "Test issue from PM Agent",
        "description": "This is a test issue created by the PM Agent to verify functionality.",
        "priority": "medium",
        "labels": ["test", "pm-agent"],
        "metadata": {
            "created_by": "pm_agent_test",
            "test": True
        }
    }
    
    try:
        created_issue = client.create_issue(test_issue)
        if created_issue:
            print(f"✅ Issue created successfully!")
            print(f"   Issue ID: {created_issue['id']}")
            print(f"   Title: {created_issue['title']}")
            return created_issue['id']
        else:
            print("❌ Failed to create issue")
            return None
    except Exception as e:
        print(f"❌ Error creating issue: {e}")
        return None


def test_heartbeat():
    """Test heartbeat functionality"""
    print("\n💓 Testing heartbeat...")
    
    client = APIClient()
    
    # Register agent first
    try:
        agent_data = client.register_agent()
        agent_id = agent_data['id']
    except:
        print("❌ Cannot test heartbeat without registered agent")
        return False
    
    # Send heartbeat
    try:
        success = client.send_heartbeat(status="active", current_task="testing")
        if success:
            print("✅ Heartbeat sent successfully")
            return True
        else:
            print("❌ Failed to send heartbeat")
            return False
    except Exception as e:
        print(f"❌ Error sending heartbeat: {e}")
        return False


def main():
    """Run all tests"""
    print("🧪 PM Agent Test Suite")
    print("=" * 50)
    
    # Test 1: API Connection
    if not test_api_connection():
        print("❌ Cannot proceed without API connection")
        return
    
    # Test 2: Agent Registration
    agent_id = test_agent_registration()
    if not agent_id:
        print("❌ Cannot proceed without agent registration")
        return
    
    # Test 3: Issue Triage
    test_issue_triage()
    
    # Test 4: Issue Creation
    issue_id = test_issue_creation()
    
    # Test 5: Heartbeat
    test_heartbeat()
    
    print("\n🎉 All tests completed!")
    print("\nNext steps:")
    print("1. Start the PM Agent: python run.py")
    print("2. Create some issues via the API")
    print("3. Watch the agent triage and process them")


if __name__ == "__main__":
    main() 