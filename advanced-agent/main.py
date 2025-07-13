from dotenv import load_dotenv
from src.workflow import Workflow
from typing import List

load_dotenv()


def show_pdf_selection(workflow) -> List[str]:
    """Show available PDFs and let user select"""
    print("\n📚 Available PDFs in S3:")
    print("=" * 50)
    
    # Get available PDFs
    pdf_notetaker = workflow.pdf_notetaker
    available_pdfs = pdf_notetaker.get_available_pdfs_for_selection()
    
    if not available_pdfs:
        print("❌ No PDFs found in S3 bucket")
        return []
    
    # Display PDFs with selection numbers
    for i, pdf_info in enumerate(available_pdfs, 1):
        print(f"{i}. 📄 {pdf_info['filename']}")
        print(f"   📏 Size: {pdf_info['size_mb']} MB")
        print(f"   📅 Modified: {pdf_info['last_modified']}")
        print(f"   🔗 Key: {pdf_info['s3_key']}")
        print()
    
    # Get user selection
    print("Select PDFs to include in research (comma-separated numbers, or 'all' for all):")
    selection = input("Selection: ").strip()
    
    if selection.lower() == 'all':
        selected_keys = [pdf['s3_key'] for pdf in available_pdfs]
    else:
        try:
            # Parse comma-separated numbers
            indices = [int(x.strip()) - 1 for x in selection.split(',')]
            selected_keys = [available_pdfs[i]['s3_key'] for i in indices if 0 <= i < len(available_pdfs)]
        except (ValueError, IndexError):
            print("❌ Invalid selection. Using all PDFs.")
            selected_keys = [pdf['s3_key'] for pdf in available_pdfs]
    
    print(f"✅ Selected {len(selected_keys)} PDF(s) for research")
    return selected_keys

def show_relevant_pdfs(workflow, query: str) -> List[str]:
    """Show PDFs ranked by relevance to query"""
    print(f"\n🔍 Finding PDFs relevant to: '{query}'")
    print("=" * 50)
    
    # Get ranked PDFs
    pdf_notetaker = workflow.pdf_notetaker
    ranked_pdfs = pdf_notetaker.filter_and_rank_pdfs(query, max_pdfs=10)
    
    if not ranked_pdfs:
        print("❌ No relevant PDFs found")
        return []
    
    # Display ranked PDFs
    for i, pdf_info in enumerate(ranked_pdfs, 1):
        relevance = pdf_info.get('relevance_score', 0)
        relevance_bar = "█" * int(relevance * 10) + "░" * (10 - int(relevance * 10))
        print(f"{i}. 📄 {pdf_info['filename']}")
        print(f"   📊 Relevance: {relevance:.2f} {relevance_bar}")
        print(f"   📝 Summary: {pdf_info.get('summary', 'No summary')[:100]}...")
        print()
    
    # Get user selection
    print("Select relevant PDFs (comma-separated numbers, or 'all' for all):")
    selection = input("Selection: ").strip()
    
    if selection.lower() == 'all':
        selected_keys = [pdf['s3_key'] for pdf in ranked_pdfs]
    else:
        try:
            indices = [int(x.strip()) - 1 for x in selection.split(',')]
            selected_keys = [ranked_pdfs[i]['s3_key'] for i in indices if 0 <= i < len(ranked_pdfs)]
        except (ValueError, IndexError):
            print("❌ Invalid selection. Using top 3 relevant PDFs.")
            selected_keys = [pdf['s3_key'] for pdf in ranked_pdfs[:3]]
    
    print(f"✅ Selected {len(selected_keys)} PDF(s) for research")
    return selected_keys


def main():
    workflow = Workflow()
    print("Research Agent (Multi-Type Research & Analysis)")

    while True:
        print("\n" + "="*60)
        print("🔍 Research Options:")
        print("1. Regular research (auto-select PDFs)")
        print("2. Select specific PDFs for research")
        print("3. Find relevant PDFs for query")
        print("4. Exit")
        print("="*60)
        
        choice = input("Choose option (1-4): ").strip()
        
        if choice == "4" or choice.lower() in {"quit", "exit"}:
            break
        
        # Get the research query
        query = input("\n🔍 Query: ").strip()
        if not query:
            continue
        
        # Handle PDF selection based on choice
        selected_pdf_keys = []
        if choice == "2":
            # User selects specific PDFs
            selected_pdf_keys = show_pdf_selection(workflow)
        elif choice == "3":
            # Find relevant PDFs for query
            selected_pdf_keys = show_relevant_pdfs(workflow, query)
        
        # Run research with selected PDFs
        if selected_pdf_keys:
            # Use user-selected PDFs
            result = workflow.run_with_selected_pdfs(query, selected_pdf_keys)
        else:
            # Use regular research (auto-select PDFs)
            result = workflow.run(query)
        
        # Display results
        print(f"\n📊 Results for: {query}")
        print("=" * 60)

        # Get the research type for specialized output
        research_type = getattr(result, "research_type", "developer_tools")
        original_type = getattr(result, "original_research_type", research_type)

        print(f"🎯 Output formatting: research_type={research_type}, original_type={original_type}")

        if research_type == "developer_tools":
            # Developer tools output
            for i, company in enumerate(result.companies[:3], 1):
                print(f"\n{i}. 🏢 {company.name}")
                print(f"   🌐 Website: {company.website}")
                print(f"   💰 Pricing: {company.pricing_model}")
                print(f"   📖 Open Source: {company.is_open_source}")

                if company.tech_stack:
                    print(f"   🛠️  Tech Stack: {', '.join(company.tech_stack[:5])}")

                if company.language_support:
                    print(f"   💻 Language Support: {', '.join(company.language_support[:5])}")

                if company.api_available is not None:
                    api_status = "✅ Available" if company.api_available else "❌ Not Available"
                    print(f"   🔌 API: {api_status}")

                if company.integration_capabilities:
                    print(f"   🔗 Integrations: {', '.join(company.integration_capabilities[:4])}")

                if company.description and company.description != "Analysis failed":
                    print(f"   📝 Description: {company.description}")

                print()

        elif research_type == "product_research":
            # Product review output
            for i, entity in enumerate(getattr(result, "market_entities", [])[:3], 1):
                print(f"\n{i}. 📱 {entity.name}")
                print(f"   🏷️ Category: {entity.category}")
                print(f"   🌐 Website: {entity.website}")
                print(f"   📝 Description: {entity.description}")
                
                # Product-specific fields
                if getattr(entity, "price", None) and entity.price != "Unknown":
                    print(f"   💰 Price: {entity.price}")
                if getattr(entity, "rating", None) and entity.rating != "Unknown":
                    print(f"   ⭐ Rating: {entity.rating}")
                if getattr(entity, "brand", None) and entity.brand != "Unknown":
                    print(f"   🏷️ Brand: {entity.brand}")
                if getattr(entity, "features", None) and entity.features:
                    print(f"   ✨ Features: {', '.join(entity.features[:3])}")
                if getattr(entity, "warranty", None) and entity.warranty != "Unknown":
                    print(f"   🛡️ Warranty: {entity.warranty}")
                if getattr(entity, "target_audience", None) and entity.target_audience != "Unknown":
                    print(f"   🎯 Target: {entity.target_audience}")
                if getattr(entity, "alternatives", None) and entity.alternatives:
                    print(f"   🔄 Alternatives: {', '.join(entity.alternatives[:3])}")

        elif research_type == "educational_research":
            # Educational comparison output
            for i, entity in enumerate(getattr(result, "market_entities", [])[:3], 1):
                print(f"\n{i}. 🎓 {entity.name}")
                print(f"   🏷️ Category: {entity.category}")
                print(f"   🌐 Website: {entity.website}")
                print(f"   📝 Description: {entity.description}")
                
                # Educational-specific fields
                if getattr(entity, "ranking", None) and entity.ranking != "Unknown":
                    print(f"   📊 Ranking: {entity.ranking}")
                if getattr(entity, "admission_rate", None) and entity.admission_rate != "Unknown":
                    print(f"   📈 Admission Rate: {entity.admission_rate}")
                if getattr(entity, "cost", None) and entity.cost != "Unknown":
                    print(f"   💰 Cost: {entity.cost}")
                if getattr(entity, "location", None) and entity.location != "Unknown":
                    print(f"   📍 Location: {entity.location}")
                if getattr(entity, "programs", None) and entity.programs:
                    print(f"   📚 Programs: {', '.join(entity.programs[:3])}")
                if getattr(entity, "career_outcomes", None) and entity.career_outcomes != "Unknown":
                    print(f"   🎯 Career Outcomes: {entity.career_outcomes}")
                if getattr(entity, "faculty_quality", None) and entity.faculty_quality != "Unknown":
                    print(f"   👨‍🏫 Faculty: {entity.faculty_quality}")
                if getattr(entity, "student_life", None) and entity.student_life != "Unknown":
                    print(f"   🏫 Student Life: {entity.student_life}")
                if getattr(entity, "international_reputation", None) and entity.international_reputation != "Unknown":
                    print(f"   🌍 International: {entity.international_reputation}")

        elif research_type == "financial_research":
            # Financial analysis output
            for i, entity in enumerate(getattr(result, "market_entities", [])[:3], 1):
                print(f"\n{i}. 💹 {entity.name}")
                print(f"   🏷️ Category: {entity.category}")
                print(f"   🌐 Website: {entity.website}")
                print(f"   📝 Description: {entity.description}")
                
                # Financial-specific fields
                if getattr(entity, "symbol", None) and entity.symbol != "Unknown":
                    print(f"   📊 Symbol: {entity.symbol}")
                if getattr(entity, "current_price", None) and entity.current_price != "Unknown":
                    print(f"   💰 Price: {entity.current_price}")
                if getattr(entity, "market_cap", None) and entity.market_cap != "Unknown":
                    print(f"   📈 Market Cap: {entity.market_cap}")
                if getattr(entity, "pe_ratio", None) and entity.pe_ratio != "Unknown":
                    print(f"   📊 P/E Ratio: {entity.pe_ratio}")
                if getattr(entity, "dividend_yield", None) and entity.dividend_yield != "Unknown":
                    print(f"   💸 Dividend: {entity.dividend_yield}")
                if getattr(entity, "risk_level", None) and entity.risk_level != "Unknown":
                    print(f"   ⚠️ Risk Level: {entity.risk_level}")
                if getattr(entity, "sector", None) and entity.sector != "Unknown":
                    print(f"   🏭 Sector: {entity.sector}")
                if getattr(entity, "performance_history", None) and entity.performance_history != "Unknown":
                    print(f"   📈 Performance: {entity.performance_history}")
                if getattr(entity, "analyst_ratings", None) and entity.analyst_ratings != "Unknown":
                    print(f"   📊 Analyst Rating: {entity.analyst_ratings}")
                if getattr(entity, "growth_potential", None) and entity.growth_potential != "Unknown":
                    print(f"   🚀 Growth: {entity.growth_potential}")
                if getattr(entity, "investment_thesis", None) and entity.investment_thesis != "Unknown":
                    print(f"   💡 Thesis: {entity.investment_thesis}")

        elif research_type == "technical_research":
            # Technical documentation output
            for i, entity in enumerate(getattr(result, "market_entities", [])[:3], 1):
                print(f"\n{i}. 🔧 {entity.name}")
                print(f"   🏷️ Category: {entity.category}")
                print(f"   🌐 Website: {entity.website}")
                print(f"   📝 Description: {entity.description}")
                
                # Technical-specific fields
                if getattr(entity, "version", None) and entity.version != "Unknown":
                    print(f"   📋 Version: {entity.version}")
                if getattr(entity, "api_endpoints", None) and entity.api_endpoints != "Unknown":
                    print(f"   🔌 API Endpoints: {entity.api_endpoints}")
                if getattr(entity, "authentication_methods", None) and entity.authentication_methods != "Unknown":
                    print(f"   🔐 Authentication: {entity.authentication_methods}")
                if getattr(entity, "sdk_availability", None):
                    sdk_status = "✅ Available" if entity.sdk_availability == "Available" else "❌ Not Available"
                    print(f"   📦 SDK: {sdk_status}")
                if getattr(entity, "documentation_quality", None) and entity.documentation_quality != "Unknown":
                    print(f"   📚 Docs Quality: {entity.documentation_quality}")
                if getattr(entity, "code_examples", None) and entity.code_examples != "Unknown":
                    print(f"   💻 Code Examples: {entity.code_examples}")
                if getattr(entity, "integration_capabilities", None) and entity.integration_capabilities != "Unknown":
                    print(f"   🔗 Integration: {entity.integration_capabilities}")
                if getattr(entity, "rate_limits", None) and entity.rate_limits != "Unknown":
                    print(f"   ⏱️ Rate Limits: {entity.rate_limits}")
                if getattr(entity, "best_practices", None) and entity.best_practices != "Unknown":
                    print(f"   ✅ Best Practices: {entity.best_practices}")

        elif research_type == "industry_research":
            # Industry analysis output
            for i, entity in enumerate(getattr(result, "market_entities", [])[:3], 1):
                print(f"\n{i}. 🏭 {entity.name}")
                print(f"   🏷️ Category: {entity.category}")
                print(f"   🌐 Website: {entity.website}")
                print(f"   📝 Description: {entity.description}")
                
                # Industry-specific fields
                if getattr(entity, "market_size", None) and entity.market_size != "Unknown":
                    print(f"   📊 Market Size: {entity.market_size}")
                if getattr(entity, "growth_rate", None) and entity.growth_rate != "Unknown":
                    print(f"   📈 Growth Rate: {entity.growth_rate}")
                if getattr(entity, "key_players", None) and entity.key_players:
                    print(f"   👥 Key Players: {', '.join(entity.key_players[:3])}")
                if getattr(entity, "trends", None) and entity.trends:
                    print(f"   📈 Trends: {', '.join(entity.trends[:3])}")
                if getattr(entity, "threats", None) and entity.threats != "Unknown":
                    print(f"   ⚠️ Threats: {entity.threats}")
                if getattr(entity, "regulatory_environment", None) and entity.regulatory_environment != "Unknown":
                    print(f"   📜 Regulations: {entity.regulatory_environment}")
                if getattr(entity, "technology_drivers", None) and entity.technology_drivers != "Unknown":
                    print(f"   🔬 Tech Drivers: {entity.technology_drivers}")
                if getattr(entity, "investment_opportunities", None) and entity.investment_opportunities != "Unknown":
                    print(f"   💰 Investment: {entity.investment_opportunities}")
                if getattr(entity, "future_outlook", None) and entity.future_outlook != "Unknown":
                    print(f"   🔮 Outlook: {entity.future_outlook}")

        elif research_type == "general_research":
            # General research output for uncategorized queries
            for i, entity in enumerate(getattr(result, "market_entities", [])[:3], 1):
                print(f"\n{i}. 🔍 {entity.name}")
                print(f"   🏷️ Category: {entity.category}")
                print(f"   📝 Description: {entity.description}")
                
                # General research fields
                if getattr(entity, "market_position", None):
                    print(f"   📊 Research Type: {entity.market_position}")
                if getattr(entity, "revenue", None):
                    print(f"   💰 Key Metrics: {entity.revenue}")
                if getattr(entity, "employees", None):
                    print(f"   👥 Scope: {entity.employees}")

        else:
            # General market research output
            for i, entity in enumerate(getattr(result, "market_entities", [])[:3], 1):
                print(f"\n{i}. 🏢 {entity.name}")
                print(f"   🏷️ Category: {entity.category}")
                print(f"   🌐 Website: {entity.website}")
                print(f"   📝 Description: {entity.description}")
                
                # Business/company info
                if getattr(entity, "market_position", None):
                    print(f"   📊 Market Position: {entity.market_position}")
                if getattr(entity, "revenue", None):
                    print(f"   💰 Revenue: {entity.revenue}")
                if getattr(entity, "employees", None):
                    print(f"   👥 Employees: {entity.employees}")

        # Print market insights if available (only for business queries)
        if getattr(result, "market_insights", None) and original_type not in ["product_review", "educational_comparison", "financial_analysis", "technical_documentation", "industry_analysis"]:
            insights = result.market_insights
            print("\nMarket Insights:")
            if insights.market_size:
                print(f"   🏦 Market Size: {insights.market_size}")
            if insights.growth_rate:
                print(f"   📈 Growth Rate: {insights.growth_rate}")
            if insights.key_drivers:
                print(f"   🚗 Key Drivers: {', '.join(insights.key_drivers)}")
            if insights.market_trends:
                print(f"   📊 Market Trends: {', '.join(insights.market_trends)}")

        # Print recommendations/analysis
        if result.analysis:
            print("\nRecommendations:")
            print("-" * 40)
            print(result.analysis)

if __name__ == "__main__":
    main()
