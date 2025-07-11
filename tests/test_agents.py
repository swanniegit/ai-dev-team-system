"""
Tests for agent endpoints
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_register_agent():
    """Test agent registration"""
    agent_data = {
        "name": "Test PM Agent",
        "agent_type": "project_manager",
        "capabilities": ["issue_triage", "sprint_planning"],
        "metadata": {"version": "1.0.0"}
    }
    
    response = client.post("/v1/agents/register", json=agent_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["name"] == agent_data["name"]
    assert data["agent_type"] == agent_data["agent_type"]
    assert "id" in data


def test_list_agents():
    """Test listing agents"""
    response = client.get("/v1/agents/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_ready_check():
    """Test readiness check endpoint"""
    response = client.get("/ready")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "ready" 