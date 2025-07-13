from typing import Dict, Any, List
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from .models import ResearchState
from .prompts import DeveloperToolsPrompts


class IntentDetectorAgent:
    """Agent for detecting research intent and refining queries"""
    
    def __init__(self, llm: ChatAnthropic):
        self.llm = llm
        self.prompts = DeveloperToolsPrompts()
    
    def detect_research_intent(self, query: str) -> Dict[str, Any]:
        """Analyze query and detect research intent with detailed context"""
        
        intent_analysis_prompt = f"""
        Analyze this user query and determine the research intent:

        Query: "{query}"

        Please provide:
        1. Research Type: Choose from:
           - "developer_tools" (for programming tools, frameworks, APIs, development platforms)
           - "product_review" (for consumer products, gadgets, purchases, product comparisons like "iPhone vs Samsung", "Tesla Model 3 vs Model Y")
           - "educational_comparison" (for universities, courses, programs, educational choices, university names like "Arizona State University", "Harvard", "MIT")
           - "financial_analysis" (for stocks, investments, financial products)
           - "industry_analysis" (for market trends, industry insights, sector analysis)
           - "technical_documentation" (for API docs, internal wikis, technical specs, code documentation)
           - "market_research" (for companies, competitive analysis, business decisions)
           - "general_research" (for weather, general knowledge, mixed topics, novel domains, or anything that doesn't fit the above categories)

        IMPORTANT RULES:
        - If the query mentions a university name (like "Arizona State University", "Harvard", "MIT", "Stanford"), choose "educational_comparison"
        - If the query compares specific products (like "Tesla Model 3 vs Model Y", "iPhone vs Samsung"), choose "product_review"
        - If the query is about stocks or investments, choose "financial_analysis"
        - If the query mentions educational programs, courses, or academic institutions, choose "educational_comparison"
        - If the query is about weather, general knowledge, mixed topics, or doesn't fit any specific category, choose "general_research"

        2. Refined Query: Create a comprehensive, detailed search query that includes:
           - Specific search terms and keywords
           - Time context (current year, recent trends)
           - Comparative elements if applicable
           - Industry-specific terminology
           - Market context and current events
           - Technical specifications if relevant
           Example: Instead of "iPhone vs Samsung", use "iPhone 15 Pro Max vs Samsung Galaxy S24 Ultra comparison 2024 specs features price performance camera battery"
           
        3. Research Focus: What specific aspects should be researched? (be detailed)
        4. Expected Output: What type of information should be returned? (be specific)
        5. Search Keywords: Provide 5-10 specific keywords for web search (comma-separated)
        6. Context Notes: Any additional context, constraints, or specific requirements?

        Return in this format:
        Research Type: [type]
        Refined Query: [comprehensive refined query with specific terms and context]
        Research Focus: [detailed focus areas]
        Expected Output: [specific output requirements]
        Search Keywords: [keyword1, keyword2, keyword3, keyword4, keyword5]
        Context Notes: [additional context and constraints]
        """
        
        messages = [
            SystemMessage(content="You are a research intent detection specialist. Analyze queries and determine the best research approach."),
            HumanMessage(content=intent_analysis_prompt)
        ]
        
        try:
            response = self.llm.invoke(messages)
            content = response.content
            
            # Parse the response
            lines = content.strip().split('\n')
            result = {}
            
            for line in lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    result[key.strip()] = value.strip()
            
            # Extract research type
            research_type = result.get('Research Type', 'market_research').lower()
            
            # Debug: Print what the AI detected
            print(f"🔍 AI detected research type: {research_type}")
            
            # Map to our internal types - preserve the original type for routing
            if research_type in ['developer_tools', 'dev_tools']:
                final_type = 'developer_tools'
            elif research_type in ['product_review', 'product_comparison']:
                final_type = 'product_research'  # Use specialized product research
            elif research_type in ['educational_comparison', 'university_comparison', 'educational']:
                final_type = 'educational_research'  # Use specialized educational research
            elif research_type in ['financial_analysis', 'investment_analysis', 'financial']:
                final_type = 'financial_research'  # Use specialized financial research
            elif research_type in ['technical_documentation', 'api_documentation', 'technical']:
                final_type = 'technical_research'  # Use specialized technical research
            elif research_type in ['industry_analysis', 'market_analysis', 'industry']:
                final_type = 'industry_research'  # Use specialized industry research
            elif research_type in ['general_research', 'general', 'weather', 'knowledge']:
                final_type = 'general_research'  # Use general research for uncategorized queries
            else:
                final_type = 'market_research'  # Default to market research
            
            print(f"🔍 Mapped to final type: {final_type}")
            
            return {
                "research_type": final_type,
                "original_research_type": research_type,  # Preserve original type
                "refined_query": result.get('Refined Query', query),
                "research_focus": result.get('Research Focus', ''),
                "expected_output": result.get('Expected Output', ''),
                "search_keywords": result.get('Search Keywords', ''),
                "context_notes": result.get('Context Notes', ''),
                "original_query": query
            }
            
        except Exception as e:
            print(f"Error in intent detection: {e}")
            # Fallback to simple detection
            return {
                "research_type": "market_research",
                "refined_query": query,
                "research_focus": "general research",
                "expected_output": "comprehensive analysis",
                "search_keywords": query,
                "context_notes": "fallback detection",
                "original_query": query
            }
    
    def get_research_strategy(self, intent_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate research strategy based on detected intent"""
        
        research_type = intent_data.get('research_type', 'market_research')
        original_type = intent_data.get('original_research_type', research_type)
        
        if research_type == 'developer_tools':
            strategy = {
                "search_approach": "Find developer tools, frameworks, and technical alternatives",
                "analysis_focus": "Technical capabilities, APIs, integrations, developer experience",
                "output_format": "Tool comparison with technical specifications",
                "priority_metrics": ["API availability", "Tech stack", "Language support", "Integration capabilities"]
            }
        elif original_type == 'educational_comparison':
            strategy = {
                "search_approach": "Find educational institutions, programs, and academic comparisons",
                "analysis_focus": "Academic reputation, program quality, admission requirements, career outcomes",
                "output_format": "Educational institution comparison with recommendations",
                "priority_metrics": ["Academic ranking", "Program quality", "Admission rate", "Career outcomes", "Cost"]
            }
        elif original_type == 'product_review':
            strategy = {
                "search_approach": "Find product reviews, specifications, and consumer feedback",
                "analysis_focus": "Product features, value for money, user experience, alternatives",
                "output_format": "Product analysis with purchase recommendations",
                "priority_metrics": ["Price", "Features", "User ratings", "Value for money", "Alternatives"]
            }
        elif original_type == 'financial_analysis':
            strategy = {
                "search_approach": "Find financial data, market analysis, and investment information",
                "analysis_focus": "Financial performance, market trends, risk assessment, investment potential",
                "output_format": "Financial analysis with investment recommendations",
                "priority_metrics": ["Revenue", "Growth rate", "Market cap", "Risk factors", "Investment potential"]
            }
        elif original_type == 'industry_analysis':
            strategy = {
                "search_approach": "Find industry trends, market data, and sector analysis",
                "analysis_focus": "Market size, growth trends, key players, industry dynamics",
                "output_format": "Industry analysis with market insights",
                "priority_metrics": ["Market size", "Growth rate", "Key players", "Trends", "Opportunities"]
            }
        elif original_type == 'technical_documentation':
            strategy = {
                "search_approach": "Find technical documentation, API docs, wikis, and technical specifications",
                "analysis_focus": "Technical implementation, API endpoints, system architecture, code structure",
                "output_format": "Technical documentation analysis with implementation guidance",
                "priority_metrics": ["API endpoints", "Authentication", "Data models", "Integration points", "Code examples"]
            }
        else:
            # General market research
            strategy = {
                "search_approach": "Find companies, products, market information, and competitive analysis",
                "analysis_focus": "Market position, competitive advantages, financial metrics, consumer value",
                "output_format": "Market analysis with recommendations",
                "priority_metrics": ["Market position", "Competitive advantages", "Financial performance", "Consumer value"]
            }
        
        return {
            **intent_data,
            **strategy
        } 