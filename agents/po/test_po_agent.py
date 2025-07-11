"""
Simple test script for PO Agent
"""

import os
import sys
import logging

# Add parent directories to path
current_dir = os.path.dirname(__file__)
parent_dir = os.path.join(current_dir, '..')
sys.path.insert(0, parent_dir)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_po_config():
    """Test PO agent configuration"""
    try:
        from po.config import config
        logger.info("✅ PO config loaded successfully")
        logger.info(f"Agent name: {config.name}")
        logger.info(f"Enabled behaviors: {len([b for b in config.enabled_behaviors.values() if b])}")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to load PO config: {e}")
        return False

def test_claude_client():
    """Test Claude client (without API key)"""
    try:
        from po.claude_client import ClaudeClient
        client = ClaudeClient()
        
        # Test fallback story creation
        story = client.create_story("Test feature request")
        logger.info("✅ Claude client created fallback story")
        logger.info(f"Story title: {story.get('title', 'N/A')}")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to test Claude client: {e}")
        return False

def test_base_agent():
    """Test base agent import"""
    try:
        from base.agent_base import AgentBase
        logger.info("✅ Base agent imported successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to import base agent: {e}")
        return False

def main():
    """Run all tests"""
    logger.info("🧪 Testing PO Agent Components...")
    
    tests = [
        ("PO Config", test_po_config),
        ("Claude Client", test_claude_client),
        ("Base Agent", test_base_agent),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        logger.info(f"\n--- Testing {test_name} ---")
        if test_func():
            passed += 1
            logger.info(f"✅ {test_name} PASSED")
        else:
            logger.error(f"❌ {test_name} FAILED")
    
    logger.info(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! PO Agent is ready for deployment.")
        return True
    else:
        logger.error("💥 Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 