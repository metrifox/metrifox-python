#!/bin/bash
# Simple script to run the SDK test

cd "$(dirname "$0")"

# Activate virtual environment and run test
source venv/bin/activate
python3 test-app/test.py
