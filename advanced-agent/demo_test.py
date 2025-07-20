#!/usr/bin/env python3
"""
Demo test to show the basic functionality of the Advanced Research Agent.
This test doesn't require API keys or AWS credentials.
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def demo_basic_functionality():
    """Demonstrate basic functionality without external dependencies."""
    print("🚀 Advanced Research Agent - Demo Test")
    print("=" * 50)
    
    try:
        # Test 1: Import core modules
        print("📦 Testing imports...")
        from models import ResearchState, PDFDocument, MarketEntity, CompanyInfo
        from prompts import DeveloperToolsPrompts
        print("✅ All core modules imported successfully")
        
        # Test 2: Create basic models
        print("\n🏗️ Testing model creation...")
        
        # Create a research state
        state = ResearchState(query="Best AI development tools")
        print(f"✅ Created ResearchState with query: '{state.query}'")
        
        # Create a PDF document
        pdf_doc = PDFDocument(
            s3_key="demo.pdf",
            filename="demo.pdf",
            content="This is a demo PDF content for testing purposes."
        )
        print(f"✅ Created PDFDocument: {pdf_doc.filename}")
        
        # Create a market entity
        entity = MarketEntity(
            name="Demo Company",
            category="technology",
            description="A demo technology company for testing",
            website="https://demo.com"
        )
        print(f"✅ Created MarketEntity: {entity.name}")
        
        # Create a company info
        company = CompanyInfo(
            name="Demo Tech",
            description="A demo technology company",
            website="https://demotech.com"
        )
        print(f"✅ Created CompanyInfo: {company.name}")
        
        # Test 3: Test prompt generation
        print("\n💬 Testing prompt generation...")
        prompts = DeveloperToolsPrompts()
        
        # Generate a tool extraction prompt
        tool_prompt = prompts.tool_extraction_user("AI development tools", "Demo content about AI tools")
        print(f"✅ Generated tool extraction prompt ({len(tool_prompt)} characters)")
        
        # Generate a tool analysis prompt
        analysis_prompt = prompts.tool_analysis_user("Demo Tool", "Demo tool content for analysis")
        print(f"✅ Generated tool analysis prompt ({len(analysis_prompt)} characters)")
        
        print("\n" + "=" * 50)
        print("🎉 All demo tests passed!")
        print("📝 This demonstrates the basic functionality without external dependencies.")
        print("🔑 To test with real data, you'll need to configure API keys in .env")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def show_usage_instructions():
    """Show how to use the system with real API keys."""
    print("\n📋 Usage Instructions:")
    print("=" * 30)
    print("1. Configure API keys in .env file:")
    print("   - ANTHROPIC_API_KEY=your_anthropic_key")
    print("   - FIRECRAWL_API_KEY=your_firecrawl_key")
    print("   - AWS credentials for PDF processing")
    print()
    print("2. Run the main application:")
    print("   python main.py")
    print()
    print("3. Example queries to test:")
    print("   - 'Best Python web frameworks'")
    print("   - 'Compare React vs Vue'")
    print("   - 'Top universities for computer science'")
    print("   - 'Stock analysis for tech companies'")

def main():
    """Run the demo test."""
    success = demo_basic_functionality()
    
    if success:
        show_usage_instructions()
        return 0
    else:
        print("❌ Demo test failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
