#!/usr/bin/env python3
"""
ResearcherRouter - Discord Bot for Research Paper Management
Main entry point for the application
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the bot
from bot.main import main

if __name__ == "__main__":
    main() 