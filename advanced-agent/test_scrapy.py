#!/usr/bin/env python3
"""
Test script for Scrapy research service
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_scrapy_service():
    """Test the Scrapy research service"""
    try:
        from scrapy_research_service import ScrapyResearchService
        
        print("🧪 Testing Scrapy Research Service...")
        print("=" * 50)
        
        # Create service instance
        service = ScrapyResearchService()
        
        # Test query
        test_query = "Python web frameworks"
        
        print(f"🔍 Testing with query: '{test_query}'")
        
        # Set up progress callback
        def progress_callback(message):
            print(f"📊 {message}")
        
        service.set_progress_callback(progress_callback)
        
        # Extract content (limited to 5 pages for testing)
        print("🚀 Starting Scrapy extraction...")
        results = service.extract_content(test_query, max_pages=5)
        
        print(f"✅ Extraction complete!")
        print(f"📊 Results: {len(results)} sources found")
        
        # Show statistics
        stats = service.get_search_statistics(results)
        print(f"📈 Statistics:")
        print(f"   - Total sources: {stats.get('total_sources', 0)}")
        print(f"   - Total content: {stats.get('total_content_chars', 0)} characters")
        print(f"   - Source types: {stats.get('source_types', {})}")
        
        # Show sample results
        if results:
            print(f"\n📄 Sample results:")
            for i, result in enumerate(results[:3]):
                print(f"   {i+1}. {result.title}")
                print(f"      URL: {result.url}")
                print(f"      Content: {len(result.content)} chars")
                print(f"      Relevance: {result.relevance_score:.2f}")
                print()
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_workflow_integration():
    """Test workflow integration"""
    try:
        from workflow import Workflow
        
        print("🧪 Testing Workflow Integration...")
        print("=" * 50)
        
        # Create workflow
        workflow = Workflow()
        
        # Test with Scrapy extraction
        test_query = "JavaScript frameworks"
        
        print(f"🔍 Testing workflow with query: '{test_query}'")
        
        # Set progress callback
        def progress_callback(message):
            print(f"📊 {message}")
        
        workflow.set_progress_callback(progress_callback)
        
        # Run with Scrapy extraction
        result = workflow.run_with_extraction_method(test_query, "scrapy")
        
        print(f"✅ Workflow test complete!")
        print(f"📊 Research type: {result.research_type}")
        print(f"📊 Extracted tools: {len(result.extracted_tools)}")
        print(f"📊 Search results: {len(result.search_results)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Workflow test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Scrapy Research Service Tests")
    print("=" * 60)
    
    # Test 1: Scrapy service
    test1_success = test_scrapy_service()
    
    print("\n" + "=" * 60)
    
    # Test 2: Workflow integration
    test2_success = test_workflow_integration()
    
    print("\n" + "=" * 60)
    
    if test1_success and test2_success:
        print("✅ All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 