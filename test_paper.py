#!/usr/bin/env python3
"""
Test script to add a sample paper to the Qdrant collection
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.qdrant.qdrant import add_paper_to_collection
from datetime import datetime

# Sample test paper
test_paper = {
    'thread_id': 12345,
    'title': 'Introduction to Machine Learning',
    'content': 'A comprehensive guide to machine learning algorithms and their applications in modern AI systems.',
    'urls': ['https://arxiv.org/abs/example1', 'https://github.com/example/ml-project'],
    'poster_id': 67890,
    'messages': [
        'A comprehensive guide to machine learning algorithms and their applications in modern AI systems.',
        'This paper covers supervised learning, unsupervised learning, and reinforcement learning.',
        'Great introduction for beginners!'
    ],
    'summary': 'Introduction to basic ML concepts including supervised, unsupervised, and reinforcement learning algorithms.',
    'tags': ['machine-learning', 'tutorial', 'ai'],
    'timestamp': datetime.now().isoformat(),
    'participants': [67890, 11111, 22222]  # Multiple participants
}

# Add the test paper
add_paper_to_collection(test_paper)

print("✅ Test paper added successfully!")
print(f"Title: {test_paper['title']}")
print(f"Summary: {test_paper['summary']}")
print(f"Participants: {test_paper['participants']}") 