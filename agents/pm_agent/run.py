#!/usr/bin/env python3
"""
Run script for PM Agent
"""

import sys
import os

# Add the current directory to the path so we can import the agent
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import main

if __name__ == "__main__":
    main() 