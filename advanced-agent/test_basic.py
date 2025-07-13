#!/usr/bin/env python3
"""
Basic test to ensure the project can be imported and basic functionality works.
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all modules can be imported."""
    try:
        from models import ResearchState, PDFDocument, PDFNotes
        print("✅ Models imported successfully")
        
        from workflow import Workflow
        print("✅ Workflow imported successfully")
        
        from prompts import DeveloperToolsPrompts
        print("✅ Prompts imported successfully")
        
        from firecrawl import FirecrawlService
        print("✅ Firecrawl imported successfully")
        
        from pdf_notetaker import PDFNotetakerAgent
        print("✅ PDF Notetaker imported successfully")
        
        from s3_pdf_service import S3PDFService
        print("✅ S3 PDF Service imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_basic_models():
    """Test basic model creation."""
    try:
        from models import ResearchState, PDFDocument
        
        # Test ResearchState creation
        state = ResearchState(query="test query")
        assert state.query == "test query"
        print("✅ ResearchState creation successful")
        
        # Test PDFDocument creation
        pdf_doc = PDFDocument(
            s3_key="test.pdf",
            filename="test.pdf",
            content="test content"
        )
        assert pdf_doc.filename == "test.pdf"
        print("✅ PDFDocument creation successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Model test error: {e}")
        return False

def main():
    """Run basic tests."""
    print("🧪 Running basic tests...")
    print("=" * 40)
    
    # Test imports
    import_success = test_imports()
    
    # Test models
    model_success = test_basic_models()
    
    print("=" * 40)
    if import_success and model_success:
        print("✅ All basic tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 