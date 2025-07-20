#!/usr/bin/env python3
"""
Simple script to run the web UI
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from app import app, init_workflow

def main():
    print("🚀 Starting Multi Agent Researcher Web UI...")
    print("=" * 50)
    
    # Load environment variables again to be sure
    load_dotenv()
    
    # Check environment
    required_vars = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_REGION', 'FIRECRAWL_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please check your .env file")
        print("Current working directory:", os.getcwd())
        print("Looking for .env file at:", os.path.join(os.getcwd(), '.env'))
        print("File exists:", os.path.exists('.env'))
        sys.exit(1)
    
    # Initialize workflow
    print("🔧 Initializing research workflow...")
    init_workflow()
    
    print("✅ Web UI ready!")
    print("🌐 Open your browser and go to: http://localhost:5005")
    print("=" * 50)
    
    # Run the app
    app.run(debug=False, host='0.0.0.0', port=5005)

if __name__ == '__main__':
    main()