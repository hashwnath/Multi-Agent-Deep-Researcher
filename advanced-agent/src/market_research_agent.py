from typing import Dict, Any, List
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from .models import MarketEntity, FinancialMetrics, CompetitiveAnalysis, MarketInsights, ResearchState
from .firecrawl import FirecrawlService
from .prompts import DeveloperToolsPrompts


class MarketResearchAgent:
    """Agent for conducting market research and competitive analysis"""
    
    def __init__(self, llm: ChatAnthropic):
        self.llm = llm
        self.firecrawl = FirecrawlService()
        self.prompts = DeveloperToolsPrompts()
    
    def extract_market_entities(self, query: str, content: str) -> List[str]:
        """Extract market entities (companies, products, markets) from content"""
        messages = [
            SystemMessage(content=self.prompts.MARKET_ENTITY_EXTRACTION_SYSTEM),
            HumanMessage(content=self.prompts.market_entity_extraction_user(query, content))
        ]
        
        try:
            response = self.llm.invoke(messages)
            entity_names = [
                name.strip()
                for name in response.content.strip().split("\n")
                if name.strip()
            ]
            return entity_names
        except Exception as e:
            print(f"Error extracting market entities: {e}")
            return []
    
    def analyze_competitive_position(self, entity_name: str, content: str) -> CompetitiveAnalysis:
        """Analyze competitive position of a market entity"""
        structured_llm = self.llm.with_structured_output(CompetitiveAnalysis)
        
        messages = [
            SystemMessage(content=self.prompts.COMPETITIVE_ANALYSIS_SYSTEM),
            HumanMessage(content=self.prompts.competitive_analysis_user(entity_name, content))
        ]
        
        try:
            analysis = structured_llm.invoke(messages)
            return analysis
        except Exception as e:
            print(f"Error analyzing competitive position for {entity_name}: {e}")
            return CompetitiveAnalysis(
                competitive_advantages=[],
                weaknesses=[],
                market_opportunities=[],
                threats=[],
                key_competitors=[],
                market_position="Unknown",
                strategic_initiatives=[],
                risk_factors=[]
            )
    
    def analyze_financial_metrics(self, entity_name: str, content: str) -> FinancialMetrics:
        """Analyze financial metrics of a market entity"""
        structured_llm = self.llm.with_structured_output(FinancialMetrics)
        
        messages = [
            SystemMessage(content=self.prompts.FINANCIAL_ANALYSIS_SYSTEM),
            HumanMessage(content=self.prompts.financial_analysis_user(entity_name, content))
        ]
        
        try:
            metrics = structured_llm.invoke(messages)
            return metrics
        except Exception as e:
            print(f"Error analyzing financial metrics for {entity_name}: {e}")
            return FinancialMetrics()
    
    def analyze_market_insights(self, query: str, content: str) -> MarketInsights:
        """Analyze market-level insights"""
        structured_llm = self.llm.with_structured_output(MarketInsights)
        
        messages = [
            SystemMessage(content=self.prompts.MARKET_INSIGHTS_SYSTEM),
            HumanMessage(content=self.prompts.market_insights_user(query, content))
        ]
        
        try:
            insights = structured_llm.invoke(messages)
            return insights
        except Exception as e:
            print(f"Error analyzing market insights: {e}")
            return MarketInsights()
    
    def research_market_entities(self, query: str, state: ResearchState) -> Dict[str, Any]:
        """Research market entities and generate comprehensive analysis"""
        print(f"🔍 Researching market entities for: {query}")
        
        # Search for relevant articles
        search_query = f"{query} market analysis companies competitors"
        search_results = self.firecrawl.search_companies(search_query, num_results=3)
        
        all_content = ""
        for result in search_results.data:
            url = result.get("url", "")
            scraped = self.firecrawl.scrape_company_pages(url)
            if scraped:
                all_content += scraped.markdown[:1500] + "\n\n"
        
        # Extract market entities
        market_entities = self.extract_market_entities(query, all_content)
        print(f"Found market entities: {', '.join(market_entities[:5])}")
        
        # Research each entity
        entities_data = []
        financial_data = {}
        competitive_analyses = []
        
        for entity_name in market_entities[:2]:  # Limit to top 2 to avoid rate limits
            print(f"🔬 Researching: {entity_name}")
            
            # Search for entity-specific information
            entity_search = self.firecrawl.search_companies(f"{entity_name} company profile financial", num_results=1)
            
            if entity_search and entity_search.data:
                result = entity_search.data[0]
                url = result.get("url", "")
                
                # Create market entity
                entity = MarketEntity(
                    name=entity_name,
                    category="company",
                    description=result.get("markdown", "")[:200],
                    website=url
                )
                entities_data.append(entity)
                
                # Get detailed content
                scraped = self.firecrawl.scrape_company_pages(url)
                if scraped:
                    content = scraped.markdown
                    
                    # Analyze competitive position
                    competitive_analysis = self.analyze_competitive_position(entity_name, content)
                    competitive_analyses.append(competitive_analysis)
                    
                    # Analyze financial metrics
                    financial_metrics = self.analyze_financial_metrics(entity_name, content)
                    financial_data[entity_name] = financial_metrics
                    
                    print(f"✅ Analyzed {entity_name}")
        
        # Analyze market-level insights
        market_insights = self.analyze_market_insights(query, all_content)
        
        return {
            "market_entities": entities_data,
            "financial_metrics": financial_data,
            "competitive_analyses": competitive_analyses,
            "market_insights": market_insights
        }
    
    def generate_market_recommendations(self, query: str, market_data: str, pdf_insights: str = "") -> str:
        """Generate strategic market recommendations"""
        messages = [
            SystemMessage(content=self.prompts.MARKET_RECOMMENDATIONS_SYSTEM),
            HumanMessage(content=self.prompts.market_recommendations_user(query, market_data, pdf_insights))
        ]
        
        try:
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            print(f"Error generating market recommendations: {e}")
            return "Failed to generate market recommendations." 