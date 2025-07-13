from typing import Dict, Any, List, Optional, Callable
from langgraph.graph import StateGraph, END
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from .models import ResearchState, CompanyInfo, CompanyAnalysis, MarketEntity, FinancialMetrics, CompetitiveAnalysis, MarketInsights
from .firecrawl import FirecrawlService
from .pdf_notetaker import PDFNotetakerAgent
from .market_research_agent import MarketResearchAgent
from .intent_detector import IntentDetectorAgent
from .prompts import DeveloperToolsPrompts
from .scrapy_research_service import ScrapyResearchService
import logging

logger = logging.getLogger(__name__)

class Workflow:
    """Enhanced workflow with multiple content extraction options"""
    
    def __init__(self):
        self.llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
        self.firecrawl_service = FirecrawlService()
        self.scrapy_service = ScrapyResearchService()
        self.pdf_notetaker = PDFNotetakerAgent(self.llm)
        self.intent_detector = IntentDetectorAgent(self.llm)
        self.market_research_agent = MarketResearchAgent(self.llm)
        self.prompts = DeveloperToolsPrompts()
        self.specialized_prompts = SpecializedPrompts()
        self.specialized_models = SpecializedModels()
        
        # Progress callback
        self.progress_callback = None
        
        # Build the workflow graph
        self.workflow = self._build_workflow()
    
    def set_progress_callback(self, callback: Callable[[str], None]):
        """Set progress callback for real-time updates"""
        self.progress_callback = callback
        self.scrapy_service.set_progress_callback(callback)
    
    def _build_workflow(self):
        """Build the workflow graph"""
        workflow = StateGraph(ResearchState)
        
        # Add nodes
        workflow.add_node("detect_intent", self._detect_intent_step)
        workflow.add_node("extract_content", self._extract_content_step)
        workflow.add_node("process_pdfs", self._process_pdfs_step)
        workflow.add_node("route_research", self._route_to_research_step)
        workflow.add_node("research", self._research_step)
        workflow.add_node("product_research", self._product_research_step)
        workflow.add_node("educational_research", self._educational_research_step)
        workflow.add_node("financial_research", self._financial_research_step)
        workflow.add_node("technical_research", self._technical_research_step)
        workflow.add_node("industry_research", self._industry_research_step)
        workflow.add_node("market_research", self._market_research_step)
        workflow.add_node("general_research", self._general_research_step)
        workflow.add_node("analyze", self._analyze_step)
        
        # Add edges
        workflow.add_edge("detect_intent", "extract_content")
        workflow.add_edge("extract_content", "process_pdfs")
        workflow.add_edge("process_pdfs", "route_research")
        workflow.add_edge("route_research", "research")
        workflow.add_edge("route_research", "product_research")
        workflow.add_edge("route_research", "educational_research")
        workflow.add_edge("route_research", "financial_research")
        workflow.add_edge("route_research", "technical_research")
        workflow.add_edge("route_research", "industry_research")
        workflow.add_edge("route_research", "market_research")
        workflow.add_edge("route_research", "general_research")
        workflow.add_edge("research", "analyze")
        workflow.add_edge("product_research", "analyze")
        workflow.add_edge("educational_research", "analyze")
        workflow.add_edge("financial_research", "analyze")
        workflow.add_edge("technical_research", "analyze")
        workflow.add_edge("industry_research", "analyze")
        workflow.add_edge("market_research", "analyze")
        workflow.add_edge("general_research", "analyze")
        workflow.add_edge("analyze", END)
        
        return workflow.compile()
    
    def _detect_intent_step(self, state: ResearchState) -> Dict[str, Any]:
        """Detect research intent"""
        if self.progress_callback:
            self.progress_callback("🎯 Detecting research intent...")
        
        intent_result = self.intent_detector.detect_research_intent(state.query)
        return intent_result
    
    def _extract_content_step(self, state: ResearchState) -> Dict[str, Any]:
        """Extract content using the selected method"""
        if self.progress_callback:
            self.progress_callback("🔍 Extracting web content...")
        
        # This will be overridden by specific extraction methods
        return {"extracted_tools": [], "search_results": []}
    
    def _process_pdfs_step(self, state: ResearchState) -> Dict[str, Any]:
        """Process PDFs"""
        if self.progress_callback:
            self.progress_callback("📄 Processing PDF documents...")
        
        pdf_result = self.pdf_notetaker.process_pdfs_for_query(state.query, state)
        return pdf_result
    
    def _route_to_research_step(self, state: ResearchState) -> str:
        """Route to appropriate research step"""
        research_type = state.research_type
        return research_type
    
    def _research_step(self, state: ResearchState) -> Dict[str, Any]:
        """Developer tools research"""
        if self.progress_callback:
            self.progress_callback("🛠️ Analyzing developer tools...")
        
        return self.market_research_agent.research(state)
    
    def _product_research_step(self, state: ResearchState) -> Dict[str, Any]:
        """Product research"""
        if self.progress_callback:
            self.progress_callback("📱 Analyzing products...")
        
        return self.market_research_agent.research(state)
    
    def _educational_research_step(self, state: ResearchState) -> Dict[str, Any]:
        """Educational research"""
        if self.progress_callback:
            self.progress_callback("🎓 Analyzing educational institutions...")
        
        return self.market_research_agent.research(state)
    
    def _financial_research_step(self, state: ResearchState) -> Dict[str, Any]:
        """Financial research"""
        if self.progress_callback:
            self.progress_callback("💰 Analyzing financial data...")
        
        return self.market_research_agent.research(state)
    
    def _technical_research_step(self, state: ResearchState) -> Dict[str, Any]:
        """Technical documentation research"""
        if self.progress_callback:
            self.progress_callback("🔧 Analyzing technical documentation...")
        
        return self.market_research_agent.research(state)
    
    def _industry_research_step(self, state: ResearchState) -> Dict[str, Any]:
        """Industry research"""
        if self.progress_callback:
            self.progress_callback("🏭 Analyzing industry trends...")
        
        return self.market_research_agent.research(state)
    
    def _market_research_step(self, state: ResearchState) -> Dict[str, Any]:
        """Market research"""
        if self.progress_callback:
            self.progress_callback("📊 Conducting market research...")
        
        return self.market_research_agent.research(state)
    
    def _general_research_step(self, state: ResearchState) -> Dict[str, Any]:
        """General research"""
        if self.progress_callback:
            self.progress_callback("🔍 Conducting general research...")
        
        return self.market_research_agent.research(state)
    
    def _analyze_step(self, state: ResearchState) -> Dict[str, Any]:
        """Analyze and synthesize results"""
        if self.progress_callback:
            self.progress_callback("📝 Generating final analysis...")
        
        # Generate comprehensive analysis
        analysis_prompt = f"""
        Based on the research results, provide a comprehensive analysis for: {state.query}
        
        Research Type: {state.research_type}
        Extracted Tools: {state.extracted_tools}
        Market Entities: {len(state.market_entities) if state.market_entities else 0}
        PDF Documents: {len(state.pdf_documents) if state.pdf_documents else 0}
        
        Please provide:
        1. Key insights and findings
        2. Recommendations
        3. Summary of the most important information
        """
        
        messages = [
            {"role": "user", "content": analysis_prompt}
        ]
        
        try:
            response = self.llm.invoke(messages)
            analysis = response.content[0].text
        except Exception as e:
            logger.error(f"Error generating analysis: {e}")
            analysis = "Analysis generation failed. Please review the extracted data manually."
        
        return {"analysis": analysis}
    
    def run_with_extraction_method(self, query: str, extraction_method: str) -> ResearchState:
        """Run research with specific extraction method"""
        initial_state = ResearchState(query=query)
        
        # Process the workflow steps
        state = initial_state
        
        # Detect intent
        intent_result = self._detect_intent_step(state)
        state = ResearchState(**{**state.dict(), **intent_result})
        
        # Extract content based on method
        if extraction_method == "firecrawl":
            content_result = self._extract_content_firecrawl(state)
        elif extraction_method == "scrapy":
            content_result = self._extract_content_scrapy(state)
        elif extraction_method == "hybrid":
            content_result = self._extract_content_hybrid(state)
        else:
            content_result = self._extract_content_firecrawl(state)  # Default
        
        state = ResearchState(**{**state.dict(), **content_result})
        
        # Process PDFs
        pdf_result = self._process_pdfs_step(state)
        state = ResearchState(**{**state.dict(), **pdf_result})
        
        # Route to appropriate research step
        research_step = self._route_to_research_step(state)
        
        # Execute research step
        if research_step == "research":
            research_result = self._research_step(state)
        elif research_step == "product_research":
            research_result = self._product_research_step(state)
        elif research_step == "educational_research":
            research_result = self._educational_research_step(state)
        elif research_step == "financial_research":
            research_result = self._financial_research_step(state)
        elif research_step == "technical_research":
            research_result = self._technical_research_step(state)
        elif research_step == "industry_research":
            research_result = self._industry_research_step(state)
        elif research_step == "market_research":
            research_result = self._market_research_step(state)
        elif research_step == "general_research":
            research_result = self._general_research_step(state)
        else:
            research_result = self._market_research_step(state)
        
        state = ResearchState(**{**state.dict(), **research_result})
        
        # Analyze and generate recommendations
        analyze_result = self._analyze_step(state)
        final_state = ResearchState(**{**state.dict(), **analyze_result})
        
        return final_state
    
    def _extract_content_firecrawl(self, state: ResearchState) -> Dict[str, Any]:
        """Extract content using Firecrawl"""
        if self.progress_callback:
            self.progress_callback("🚀 Using Firecrawl for content extraction...")
        
        try:
            extracted_tools = self.firecrawl_service.extract_tools(state.query)
            search_results = self.firecrawl_service.get_search_results()
            
            return {
                "extracted_tools": extracted_tools,
                "search_results": search_results
            }
        except Exception as e:
            logger.error(f"Firecrawl extraction failed: {e}")
            return {"extracted_tools": [], "search_results": []}
    
    def _extract_content_scrapy(self, state: ResearchState) -> Dict[str, Any]:
        """Extract content using Scrapy"""
        if self.progress_callback:
            self.progress_callback("🕷️ Using Scrapy for comprehensive content extraction...")
        
        try:
            # Extract content using Scrapy
            scraped_contents = self.scrapy_service.extract_content(state.query, max_pages=30)
            
            # Convert to expected format
            extracted_tools = []
            search_results = []
            
            for content in scraped_contents:
                # Extract potential tools/entities from content
                tools = self._extract_tools_from_content(content.content)
                extracted_tools.extend(tools)
                
                # Add to search results
                search_results.append({
                    'url': content.url,
                    'title': content.title,
                    'content': content.content,
                    'metadata': content.metadata,
                    'relevance_score': content.relevance_score
                })
            
            # Remove duplicates
            extracted_tools = list(set(extracted_tools))
            
            if self.progress_callback:
                stats = self.scrapy_service.get_search_statistics(scraped_contents)
                self.progress_callback(f"📊 Scrapy extracted {stats.get('total_sources', 0)} sources with {stats.get('total_content_chars', 0)} characters")
            
            return {
                "extracted_tools": extracted_tools,
                "search_results": search_results
            }
        except Exception as e:
            logger.error(f"Scrapy extraction failed: {e}")
            return {"extracted_tools": [], "search_results": []}
    
    def _extract_content_hybrid(self, state: ResearchState) -> Dict[str, Any]:
        """Extract content using both Firecrawl and Scrapy"""
        if self.progress_callback:
            self.progress_callback("🔄 Using hybrid approach (Firecrawl + Scrapy)...")
        
        # Get Firecrawl results
        firecrawl_result = self._extract_content_firecrawl(state)
        
        # Get Scrapy results
        scrapy_result = self._extract_content_scrapy(state)
        
        # Combine results
        combined_tools = list(set(firecrawl_result["extracted_tools"] + scrapy_result["extracted_tools"]))
        combined_results = firecrawl_result["search_results"] + scrapy_result["search_results"]
        
        if self.progress_callback:
            self.progress_callback(f"✅ Hybrid extraction complete: {len(combined_tools)} tools, {len(combined_results)} sources")
        
        return {
            "extracted_tools": combined_tools,
            "search_results": combined_results
        }
    
    def _extract_tools_from_content(self, content: str) -> List[str]:
        """Extract potential tools/entities from content"""
        # Simple keyword-based extraction
        # In a real implementation, you might use NER or LLM for this
        tools = []
        
        # Common tool-related keywords
        tool_keywords = [
            'api', 'sdk', 'framework', 'library', 'tool', 'platform',
            'service', 'software', 'application', 'system'
        ]
        
        words = content.lower().split()
        for i, word in enumerate(words):
            if word in tool_keywords and i > 0:
                # Try to extract the tool name
                potential_tool = words[i-1]
                if len(potential_tool) > 2 and potential_tool.isalpha():
                    tools.append(potential_tool.title())
        
        return list(set(tools))
    
    def run_with_selected_pdfs_and_extraction(self, query: str, selected_pdf_keys: List[str], extraction_method: str) -> ResearchState:
        """Run research with user-selected PDFs and specific extraction method"""
        initial_state = ResearchState(query=query)
        
        # Process the workflow steps
        state = initial_state
        
        # Detect intent
        intent_result = self._detect_intent_step(state)
        state = ResearchState(**{**state.dict(), **intent_result})
        
        # Extract content based on method
        if extraction_method == "firecrawl":
            content_result = self._extract_content_firecrawl(state)
        elif extraction_method == "scrapy":
            content_result = self._extract_content_scrapy(state)
        elif extraction_method == "hybrid":
            content_result = self._extract_content_hybrid(state)
        else:
            content_result = self._extract_content_firecrawl(state)  # Default
        
        state = ResearchState(**{**state.dict(), **content_result})
        
        # Process selected PDFs instead of auto-selecting
        pdf_result = self.pdf_notetaker.process_user_selected_pdfs(selected_pdf_keys, query)
        state = ResearchState(**{**state.dict(), **pdf_result})
        
        # Route to appropriate research step
        research_step = self._route_to_research_step(state)
        
        # Execute research step
        if research_step == "research":
            research_result = self._research_step(state)
        elif research_step == "product_research":
            research_result = self._product_research_step(state)
        elif research_step == "educational_research":
            research_result = self._educational_research_step(state)
        elif research_step == "financial_research":
            research_result = self._financial_research_step(state)
        elif research_step == "technical_research":
            research_result = self._technical_research_step(state)
        elif research_step == "industry_research":
            research_result = self._industry_research_step(state)
        elif research_step == "market_research":
            research_result = self._market_research_step(state)
        elif research_step == "general_research":
            research_result = self._general_research_step(state)
        else:
            research_result = self._market_research_step(state)
        
        state = ResearchState(**{**state.dict(), **research_result})
        
        # Analyze and generate recommendations
        analyze_result = self._analyze_step(state)
        final_state = ResearchState(**{**state.dict(), **analyze_result})
        
        return final_state
    
    def run(self, query: str) -> ResearchState:
        """Default run method (uses Firecrawl)"""
        return self.run_with_extraction_method(query, "firecrawl")
    
    def run_with_selected_pdfs(self, query: str, selected_pdf_keys: List[str]) -> ResearchState:
        """Default run with selected PDFs (uses Firecrawl)"""
        return self.run_with_selected_pdfs_and_extraction(query, selected_pdf_keys, "firecrawl")
