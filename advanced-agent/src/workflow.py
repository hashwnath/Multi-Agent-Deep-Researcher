from typing import Dict, Any, List
from langgraph.graph import StateGraph, END
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from .models import ResearchState, CompanyInfo, CompanyAnalysis, MarketEntity, FinancialMetrics, CompetitiveAnalysis, MarketInsights
from .firecrawl import FirecrawlService
from .pdf_notetaker import PDFNotetakerAgent
from .market_research_agent import MarketResearchAgent
from .intent_detector import IntentDetectorAgent
from .prompts import DeveloperToolsPrompts


class Workflow:
    def __init__(self):
        self.firecrawl = FirecrawlService()
        self.llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0.1)
        self.prompts = DeveloperToolsPrompts()
        self.intent_detector = IntentDetectorAgent(self.llm)
        self.pdf_notetaker = PDFNotetakerAgent(self.llm)
        self.market_research_agent = MarketResearchAgent(self.llm)
        self.workflow = self._build_workflow()

    def _build_workflow(self):
        graph = StateGraph(ResearchState)
        graph.add_node("detect_intent", self._detect_intent_step)
        graph.add_node("extract_content", self._extract_content_step)
        graph.add_node("process_pdfs", self._process_pdfs_step)
        graph.add_node("research", self._research_step)
        graph.add_node("product_research", self._product_research_step)
        graph.add_node("educational_research", self._educational_research_step)
        graph.add_node("financial_research", self._financial_research_step)
        graph.add_node("technical_research", self._technical_research_step)
        graph.add_node("industry_research", self._industry_research_step)
        graph.add_node("market_research", self._market_research_step)
        graph.add_node("general_research", self._general_research_step)
        graph.add_node("analyze", self._analyze_step)
        
        # Set entry point
        graph.set_entry_point("detect_intent")
        
        # Add edges
        graph.add_edge("detect_intent", "extract_content")
        graph.add_edge("extract_content", "process_pdfs")
        
        # Conditional routing based on research type
        graph.add_conditional_edges(
            "process_pdfs",
            self._route_to_research_step,
            {
                "research": "research",
                "product_research": "product_research", 
                "educational_research": "educational_research",
                "financial_research": "financial_research",
                "technical_research": "technical_research",
                "industry_research": "industry_research",
                "market_research": "market_research",
                "general_research": "general_research"
            }
        )
        
        graph.add_edge("research", "analyze")
        graph.add_edge("product_research", "analyze")
        graph.add_edge("educational_research", "analyze")
        graph.add_edge("financial_research", "analyze")
        graph.add_edge("technical_research", "analyze")
        graph.add_edge("industry_research", "analyze")
        graph.add_edge("market_research", "analyze")
        graph.add_edge("general_research", "analyze")
        graph.add_edge("analyze", END)
        
        return graph.compile()

    def _general_research_step(self, state: ResearchState) -> Dict[str, Any]:
        """General research step for uncategorized or mixed research types"""
        print(f"🔍 Conducting general research for: {state.query}")
        
        # Use the refined query if available
        search_query = getattr(state, 'refined_query', state.query) or state.query
        
        # Create a flexible research prompt
        research_prompt = f"""
        Conduct comprehensive research on: {search_query}
        
        Based on the query, determine the most appropriate research approach and provide:
        1. Key findings and insights
        2. Relevant entities, companies, or topics
        3. Comparative analysis if applicable
        4. Recommendations or conclusions
        5. Additional context or background information
        
        Focus on providing actionable, well-researched information that addresses the user's query.
        """
        
        messages = [
            SystemMessage(content="You are a comprehensive research specialist. Analyze the query and provide detailed, well-structured research findings."),
            HumanMessage(content=research_prompt)
        ]
        
        try:
            response = self.llm.invoke(messages)
            analysis = response.content
            
            # Create a generic market entity for the results
            generic_entity = MarketEntity(
                name=search_query,
                category="general_research",
                description=f"Research results for: {search_query}",
                website="",
                market_position="General Research",
                revenue="",
                employees=""
            )
            
            return {
                "market_entities": [generic_entity],
                "analysis": analysis
            }
            
        except Exception as e:
            print(f"Error in general research: {e}")
            return {
                "market_entities": [],
                "analysis": f"Research failed for: {search_query}"
            }

    def _route_to_research_step(self, state: ResearchState) -> str:
        """Route to the appropriate research step based on research type"""
        research_type = getattr(state, "research_type", "market_research")
        original_type = getattr(state, "original_research_type", research_type)
        
        print(f"🔀 Routing: research_type={research_type}, original_type={original_type}")
        
        # Route based on the research_type (which now contains the specialized type)
        if research_type == "developer_tools":
            return "research"
        elif research_type == "product_research":
            return "product_research"
        elif research_type == "educational_research":
            return "educational_research"
        elif research_type == "financial_research":
            return "financial_research"
        elif research_type == "technical_research":
            return "technical_research"
        elif research_type == "industry_research":
            return "industry_research"
        elif research_type == "market_research":
            return "market_research"
        else:
            # Handle uncategorized or general research queries
            return "general_research"

    def _analyze_company_content(self, company_name: str, content: str) -> CompanyAnalysis:
        structured_llm = self.llm.with_structured_output(CompanyAnalysis)

        messages = [
            SystemMessage(content=self.prompts.TOOL_ANALYSIS_SYSTEM),
            HumanMessage(content=self.prompts.tool_analysis_user(company_name, content))
        ]

        try:
            analysis = structured_llm.invoke(messages)
            return analysis
        except Exception as e:
            print(e)
            return CompanyAnalysis(
                pricing_model="Unknown",
                is_open_source=None,
                tech_stack=[],
                description="Failed",
                api_available=None,
                language_support=[],
                integration_capabilities=[],
            )

    def _analyze_product_content(self, product_name: str, content: str) -> Dict[str, Any]:
        """Analyze product content for reviews and comparisons"""
        product_analysis_prompt = f"""
        Analyze this product information for {product_name}:

        Content: {content[:2000]}

        Extract the following information:
        1. Price range and pricing model
        2. Key features and specifications
        3. Pros and advantages
        4. Cons and disadvantages
        5. User ratings (if available)
        6. Brand and manufacturer
        7. Warranty and support
        8. Target audience
        9. Alternatives and competitors

        Return in this format:
        Price: [price info]
        Features: [key features]
        Pros: [advantages]
        Cons: [disadvantages]
        Rating: [rating if available]
        Brand: [brand name]
        Warranty: [warranty info]
        Target: [target audience]
        Alternatives: [alternatives]
        """

        messages = [
            SystemMessage(content="You are a product analysis specialist. Extract detailed product information from content."),
            HumanMessage(content=product_analysis_prompt)
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
            
            return result
        except Exception as e:
            print(f"Error analyzing product content: {e}")
            return {}

    def _analyze_educational_content(self, institution_name: str, content: str) -> Dict[str, Any]:
        """Analyze educational institution content"""
        educational_analysis_prompt = f"""
        Analyze this educational institution information for {institution_name}:

        Content: {content[:2000]}

        Extract the following information:
        1. Academic ranking and reputation
        2. Admission rate and requirements
        3. Program quality and offerings
        4. Cost and financial aid
        5. Location and campus
        6. Career outcomes and alumni network
        7. Faculty quality and research opportunities
        8. Student life and facilities
        9. International reputation

        Return in this format:
        Ranking: [ranking info]
        Admission Rate: [admission rate]
        Programs: [program offerings]
        Cost: [cost information]
        Location: [location]
        Career Outcomes: [career outcomes]
        Faculty: [faculty quality]
        Student Life: [student life]
        International: [international reputation]
        """

        messages = [
            SystemMessage(content="You are an educational institution analysis specialist. Extract detailed academic information from content."),
            HumanMessage(content=educational_analysis_prompt)
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
            
            return result
        except Exception as e:
            print(f"Error analyzing educational content: {e}")
            return {}

    def _analyze_financial_content(self, instrument_name: str, content: str) -> Dict[str, Any]:
        """Analyze financial instrument content"""
        financial_analysis_prompt = f"""
        Analyze this financial instrument information for {instrument_name}:

        Content: {content[:2000]}

        Extract the following information:
        1. Current price and market cap
        2. P/E ratio and dividend yield
        3. Risk level and volatility
        4. Sector and industry
        5. Performance history
        6. Analyst ratings and recommendations
        7. Growth potential and outlook
        8. Investment thesis
        9. Key financial metrics

        Return in this format:
        Price: [current price]
        Market Cap: [market cap]
        P/E Ratio: [P/E ratio]
        Dividend: [dividend yield]
        Risk Level: [risk assessment]
        Sector: [sector]
        Performance: [performance history]
        Analyst Rating: [analyst ratings]
        Growth: [growth potential]
        Thesis: [investment thesis]
        """

        messages = [
            SystemMessage(content="You are a financial analysis specialist. Extract detailed financial information from content."),
            HumanMessage(content=financial_analysis_prompt)
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
            
            return result
        except Exception as e:
            print(f"Error analyzing financial content: {e}")
            return {}

    def _analyze_technical_content(self, tech_name: str, content: str) -> Dict[str, Any]:
        """Analyze technical documentation content"""
        technical_analysis_prompt = f"""
        Analyze this technical documentation for {tech_name}:

        Content: {content[:2000]}

        Extract the following information:
        1. API endpoints and methods
        2. Authentication methods
        3. SDK availability and languages
        4. Documentation quality
        5. Code examples and tutorials
        6. Integration capabilities
        7. Rate limits and pricing
        8. Version and updates
        9. Best practices and common issues

        Return in this format:
        API Endpoints: [endpoint info]
        Authentication: [auth methods]
        SDK: [SDK availability]
        Documentation: [doc quality]
        Examples: [code examples]
        Integration: [integration capabilities]
        Rate Limits: [rate limit info]
        Version: [version info]
        Best Practices: [best practices]
        """

        messages = [
            SystemMessage(content="You are a technical documentation specialist. Extract detailed technical information from content."),
            HumanMessage(content=technical_analysis_prompt)
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
            
            return result
        except Exception as e:
            print(f"Error analyzing technical content: {e}")
            return {}

    def _analyze_industry_content(self, industry_name: str, content: str) -> Dict[str, Any]:
        """Analyze industry sector content"""
        industry_analysis_prompt = f"""
        Analyze this industry information for {industry_name}:

        Content: {content[:2000]}

        Extract the following information:
        1. Market size and growth rate
        2. Key players and market leaders
        3. Trends and opportunities
        4. Threats and challenges
        5. Regulatory environment
        6. Technology drivers
        7. Investment opportunities
        8. Future outlook
        9. Competitive landscape

        Return in this format:
        Market Size: [market size]
        Growth Rate: [growth rate]
        Key Players: [key players]
        Trends: [trends]
        Threats: [threats]
        Regulations: [regulatory environment]
        Technology: [tech drivers]
        Investment: [investment opportunities]
        Outlook: [future outlook]
        """

        messages = [
            SystemMessage(content="You are an industry analysis specialist. Extract detailed industry information from content."),
            HumanMessage(content=industry_analysis_prompt)
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
            
            return result
        except Exception as e:
            print(f"Error analyzing industry content: {e}")
            return {}

    def _research_step(self, state: ResearchState) -> Dict[str, Any]:
        """Developer tools research - exhaustive Firecrawl usage"""
        extracted_tools = getattr(state, "extracted_tools", [])

        if not extracted_tools:
            print("⚠️ No extracted tools found, falling back to direct search")
            search_results = self.firecrawl.search_companies(state.query, num_results=4)
            tool_names = [
                result.get("metadata", {}).get("title", "Unknown")
                for result in search_results.data
            ]
        else:
            tool_names = extracted_tools[:4]

        print(f"🔬 Researching specific tools: {', '.join(tool_names)}")

        companies = []
        for tool_name in tool_names:
            tool_search_results = self.firecrawl.search_companies(tool_name + " official site", num_results=1)

            if tool_search_results:
                result = tool_search_results.data[0]
                url = result.get("url", "")

                company = CompanyInfo(
                    name=tool_name,
                    description=result.get("markdown", ""),
                    website=url,
                    tech_stack=[],
                    competitors=[]
                )

                scraped = self.firecrawl.scrape_company_pages(url)
                if scraped:
                    content = scraped.markdown
                    analysis = self._analyze_company_content(company.name, content)

                    company.pricing_model = analysis.pricing_model
                    company.is_open_source = analysis.is_open_source
                    company.tech_stack = analysis.tech_stack
                    company.description = analysis.description
                    company.api_available = analysis.api_available
                    company.language_support = analysis.language_support
                    company.integration_capabilities = analysis.integration_capabilities

                companies.append(company)

        return {"companies": companies}

    def _product_research_step(self, state: ResearchState) -> Dict[str, Any]:
        """Product review research - using content from extract_content_step"""
        extracted_products = getattr(state, "extracted_tools", [])
        detailed_content = getattr(state, "detailed_content", "")

        if not extracted_products:
            print("⚠️ No extracted products found, falling back to direct search")
            search_results = self.firecrawl.search_companies(state.query, num_results=4)
            product_names = [
                result.get("metadata", {}).get("title", "Unknown")
                for result in search_results.data
            ]
        else:
            product_names = extracted_products[:3]

        print(f"📱 Researching specific products: {', '.join(product_names)}")

        products = []
        for product_name in product_names:
            # Use detailed content if available, otherwise search
            if detailed_content:
                content = detailed_content
                url = "Content from previous search"
            else:
                # Fallback to search if no content available
                product_search_results = self.firecrawl.search_companies(f"{product_name} official site specifications", num_results=1)
                if product_search_results:
                    result = product_search_results.data[0]
                    url = result.get("url", "")
                    scraped = self.firecrawl.scrape_company_pages(url)
                    content = scraped.markdown if scraped else ""
                else:
                    content = ""
                    url = ""

            # Create product entity
            product = MarketEntity(
                name=product_name,
                category="product",
                description=content[:200] if content else "No description available",
                website=url
            )

            # Analyze content if available
            if content:
                analysis = self._analyze_product_content(product_name, content)

                # Add product-specific fields
                product.price = analysis.get("Price", "Unknown")
                product.rating = analysis.get("Rating", "Unknown")
                product.brand = analysis.get("Brand", "Unknown")
                product.features = analysis.get("Features", "").split(", ") if analysis.get("Features") else []
                product.warranty = analysis.get("Warranty", "Unknown")
                product.target_audience = analysis.get("Target", "Unknown")
                product.alternatives = analysis.get("Alternatives", "").split(", ") if analysis.get("Alternatives") else []

            products.append(product)

        return {"market_entities": products}

    def _educational_research_step(self, state: ResearchState) -> Dict[str, Any]:
        """Educational comparison research - using content from extract_content_step"""
        extracted_institutions = getattr(state, "extracted_tools", [])
        detailed_content = getattr(state, "detailed_content", "")

        if not extracted_institutions:
            print("⚠️ No extracted institutions found, falling back to direct search")
            search_results = self.firecrawl.search_companies(state.query, num_results=4)
            institution_names = [
                result.get("metadata", {}).get("title", "Unknown")
                for result in search_results.data
            ]
        else:
            institution_names = extracted_institutions[:3]

        print(f"🎓 Researching educational institutions: {', '.join(institution_names)}")

        institutions = []
        for institution_name in institution_names:
            # Use detailed content if available, otherwise search
            if detailed_content:
                content = detailed_content
                url = "Content from previous search"
            else:
                # Fallback to search if no content available
                institution_search_results = self.firecrawl.search_companies(f"{institution_name} official site programs", num_results=1)
                if institution_search_results:
                    result = institution_search_results.data[0]
                    url = result.get("url", "")
                    scraped = self.firecrawl.scrape_company_pages(url)
                    content = scraped.markdown if scraped else ""
                else:
                    content = ""
                    url = ""

            # Create educational entity
            institution = MarketEntity(
                name=institution_name,
                category="university",
                description=content[:200] if content else "No description available",
                website=url
            )

            # Analyze content if available
            if content:
                analysis = self._analyze_educational_content(institution_name, content)

                # Add educational-specific fields
                institution.ranking = analysis.get("Ranking", "Unknown")
                institution.admission_rate = analysis.get("Admission Rate", "Unknown")
                institution.programs = analysis.get("Programs", "").split(", ") if analysis.get("Programs") else []
                institution.cost = analysis.get("Cost", "Unknown")
                institution.location = analysis.get("Location", "Unknown")
                institution.career_outcomes = analysis.get("Career Outcomes", "Unknown")
                institution.faculty_quality = analysis.get("Faculty", "Unknown")
                institution.student_life = analysis.get("Student Life", "Unknown")
                institution.international_reputation = analysis.get("International", "Unknown")

            institutions.append(institution)

        return {"market_entities": institutions}

    def _financial_research_step(self, state: ResearchState) -> Dict[str, Any]:
        """Financial analysis research - using content from extract_content_step"""
        extracted_instruments = getattr(state, "extracted_tools", [])
        detailed_content = getattr(state, "detailed_content", "")

        if not extracted_instruments:
            print("⚠️ No extracted financial instruments found, falling back to direct search")
            search_results = self.firecrawl.search_companies(state.query, num_results=4)
            instrument_names = [
                result.get("metadata", {}).get("title", "Unknown")
                for result in search_results.data
            ]
        else:
            instrument_names = extracted_instruments[:3]

        print(f"💹 Researching financial instruments: {', '.join(instrument_names)}")

        instruments = []
        for instrument_name in instrument_names:
            # Use detailed content if available, otherwise search
            if detailed_content:
                content = detailed_content
                url = "Content from previous search"
            else:
                # Fallback to search if no content available
                instrument_search_results = self.firecrawl.search_companies(f"{instrument_name} financial data stock price", num_results=1)
                if instrument_search_results:
                    result = instrument_search_results.data[0]
                    url = result.get("url", "")
                    scraped = self.firecrawl.scrape_company_pages(url)
                    content = scraped.markdown if scraped else ""
                else:
                    content = ""
                    url = ""

            # Create financial entity
            instrument = MarketEntity(
                name=instrument_name,
                category="financial",
                description=content[:200] if content else "No description available",
                website=url
            )

            # Analyze content if available
            if content:
                analysis = self._analyze_financial_content(instrument_name, content)

                # Add financial-specific fields
                instrument.symbol = analysis.get("Price", "Unknown")
                instrument.current_price = analysis.get("Price", "Unknown")
                instrument.market_cap = analysis.get("Market Cap", "Unknown")
                instrument.pe_ratio = analysis.get("P/E Ratio", "Unknown")
                instrument.dividend_yield = analysis.get("Dividend", "Unknown")
                instrument.risk_level = analysis.get("Risk Level", "Unknown")
                instrument.sector = analysis.get("Sector", "Unknown")
                instrument.performance_history = analysis.get("Performance", "Unknown")
                instrument.analyst_ratings = analysis.get("Analyst Rating", "Unknown")
                instrument.growth_potential = analysis.get("Growth", "Unknown")
                instrument.investment_thesis = analysis.get("Thesis", "Unknown")

            instruments.append(instrument)

        return {"market_entities": instruments}

    def _technical_research_step(self, state: ResearchState) -> Dict[str, Any]:
        """Technical documentation research - exhaustive Firecrawl usage"""
        extracted_tech = getattr(state, "extracted_tools", [])

        if not extracted_tech:
            print("⚠️ No extracted technical entities found, falling back to direct search")
            search_results = self.firecrawl.search_companies(state.query, num_results=4)
            tech_names = [
                result.get("metadata", {}).get("title", "Unknown")
                for result in search_results.data
            ]
        else:
            tech_names = extracted_tech[:3]

        print(f"🔧 Researching technical documentation: {', '.join(tech_names)}")

        tech_entities = []
        for tech_name in tech_names:
            # Search for technical documentation
            tech_search_results = self.firecrawl.search_companies(f"{tech_name} API documentation", num_results=1)

            if tech_search_results:
                result = tech_search_results.data[0]
                url = result.get("url", "")

                # Create technical entity
                tech_entity = MarketEntity(
                    name=tech_name,
                    category="technical",
                    description=result.get("markdown", "")[:200],
                    website=url
                )

                # Get detailed content
                scraped = self.firecrawl.scrape_company_pages(url)
                if scraped:
                    content = scraped.markdown
                    analysis = self._analyze_technical_content(tech_name, content)

                    # Add technical-specific fields
                    tech_entity.version = analysis.get("Version", "Unknown")
                    tech_entity.api_endpoints = analysis.get("API Endpoints", "Unknown")
                    tech_entity.authentication_methods = analysis.get("Authentication", "Unknown")
                    tech_entity.sdk_availability = "Available" if "SDK" in analysis.get("SDK", "") else "Not Available"
                    tech_entity.documentation_quality = analysis.get("Documentation", "Unknown")
                    tech_entity.code_examples = analysis.get("Examples", "Unknown")
                    tech_entity.integration_capabilities = analysis.get("Integration", "Unknown")
                    tech_entity.rate_limits = analysis.get("Rate Limits", "Unknown")
                    tech_entity.best_practices = analysis.get("Best Practices", "Unknown")

                tech_entities.append(tech_entity)

        return {"market_entities": tech_entities}

    def _industry_research_step(self, state: ResearchState) -> Dict[str, Any]:
        """Industry analysis research - exhaustive Firecrawl usage"""
        extracted_industries = getattr(state, "extracted_tools", [])

        if not extracted_industries:
            print("⚠️ No extracted industries found, falling back to direct search")
            search_results = self.firecrawl.search_companies(state.query, num_results=4)
            industry_names = [
                result.get("metadata", {}).get("title", "Unknown")
                for result in search_results.data
            ]
        else:
            industry_names = extracted_industries[:3]

        print(f"🏭 Researching industry sectors: {', '.join(industry_names)}")

        industries = []
        for industry_name in industry_names:
            # Search for industry-specific information
            industry_search_results = self.firecrawl.search_companies(f"{industry_name} industry analysis market trends", num_results=1)

            if industry_search_results:
                result = industry_search_results.data[0]
                url = result.get("url", "")

                # Create industry entity
                industry = MarketEntity(
                    name=industry_name,
                    category="industry",
                    description=result.get("markdown", "")[:200],
                    website=url
                )

                # Get detailed content
                scraped = self.firecrawl.scrape_company_pages(url)
                if scraped:
                    content = scraped.markdown
                    analysis = self._analyze_industry_content(industry_name, content)

                    # Add industry-specific fields
                    industry.market_size = analysis.get("Market Size", "Unknown")
                    industry.growth_rate = analysis.get("Growth Rate", "Unknown")
                    industry.key_players = analysis.get("Key Players", "").split(", ") if analysis.get("Key Players") else []
                    industry.trends = analysis.get("Trends", "").split(", ") if analysis.get("Trends") else []
                    industry.threats = analysis.get("Threats", "Unknown")
                    industry.regulatory_environment = analysis.get("Regulations", "Unknown")
                    industry.technology_drivers = analysis.get("Technology", "Unknown")
                    industry.investment_opportunities = analysis.get("Investment", "Unknown")
                    industry.future_outlook = analysis.get("Outlook", "Unknown")

                industries.append(industry)

        return {"market_entities": industries}

    def _analyze_step(self, state: ResearchState) -> Dict[str, Any]:
        print("Generating recommendations")

        # Get PDF insights summary
        pdf_insights = self.pdf_notetaker.get_pdf_insights_summary(state.pdf_notes)

        if state.research_type == "market_research":
            # Market research analysis
            market_data = ""
            if state.market_entities:
                market_data = ", ".join([entity.json() for entity in state.market_entities])
            
            if state.competitive_analyses:
                market_data += "\nCompetitive Analysis: " + ", ".join([analysis.json() for analysis in state.competitive_analyses])
            
            if state.market_insights:
                market_data += f"\nMarket Insights: {state.market_insights.json()}"
            
            # Use market research agent for recommendations
            analysis = self.market_research_agent.generate_market_recommendations(
                state.query, market_data, pdf_insights
            )
        else:
            # Developer tools analysis
            company_data = ", ".join([
                company.json() for company in state.companies
            ])

            # Use enhanced recommendations that include PDF context
            messages = [
                SystemMessage(content=self.prompts.ENHANCED_RECOMMENDATIONS_SYSTEM),
                HumanMessage(content=self.prompts.enhanced_recommendations_user(state.query, company_data, pdf_insights))
            ]

            response = self.llm.invoke(messages)
            analysis = response.content

        return {"analysis": analysis}

    def _detect_intent_step(self, state: ResearchState) -> Dict[str, Any]:
        """Detect research intent and refine query using AI"""
        print(f"🧠 Analyzing intent for: {state.query}")
        
        # Use Intent Detector Agent
        intent_data = self.intent_detector.detect_research_intent(state.query)
        strategy = self.intent_detector.get_research_strategy(intent_data)
        
        print(f"📋 Detected: {strategy['research_type']} research")
        print(f"🔍 Refined query: {strategy['refined_query']}")
        print(f"🎯 Focus: {strategy['research_focus']}")
        
        return {
            "research_type": strategy['research_type'],
            "original_research_type": strategy['original_research_type'],  # Add this line
            "refined_query": strategy['refined_query'],
            "research_focus": strategy['research_focus'],
            "expected_output": strategy['expected_output'],
            "search_keywords": strategy['search_keywords'],
            "context_notes": strategy['context_notes'],
            "search_approach": strategy['search_approach'],
            "analysis_focus": strategy['analysis_focus'],
            "output_format": strategy['output_format'],
            "priority_metrics": strategy['priority_metrics']
        }

    def _extract_content_step(self, state: ResearchState) -> Dict[str, Any]:
        """Extract content based on research type"""
        # Use refined query if available, otherwise use original
        search_query = getattr(state, 'refined_query', state.query) or state.query
        
        if state.research_type == "market_research":
            print(f"🏢 Finding market entities for: {search_query}")
            
            # Use search keywords if available, otherwise generate
            if getattr(state, 'search_keywords', ''):
                search_query = f"{state.search_keywords} market analysis companies competitors"
            else:
                search_query = f"{search_query} market analysis companies competitors"
            
            search_results = self.firecrawl.search_companies(search_query, num_results=2)
            
            all_content = ""
            for result in search_results.data:
                url = result.get("url", "")
                scraped = self.firecrawl.scrape_company_pages(url)
                if scraped:
                    all_content += scraped.markdown[:1500] + "\n\n"
            
            # Use market research agent to extract entities
            market_entities = self.market_research_agent.extract_market_entities(state.query, all_content)
            print(f"Found market entities: {', '.join(market_entities[:5])}")
            
            return {
                "extracted_tools": market_entities,
                "detailed_content": all_content  # Pass detailed content for reuse
            }
        else:
            # Handle different research types with appropriate extraction
            research_type = getattr(state, 'research_type', 'developer_tools')
            
            if research_type == "educational_research":
                print(f"🎓 Finding educational institutions for: {search_query}")
                # Use search keywords if available, otherwise use refined query
                search_keywords = getattr(state, 'search_keywords', '')
                if search_keywords:
                    article_query = f"{search_keywords} university college institution"
                else:
                    article_query = f"{search_query} university college institution"
            elif research_type == "product_research":
                print(f"📱 Finding products for: {search_query}")
                # Use search keywords if available, otherwise use refined query
                search_keywords = getattr(state, 'search_keywords', '')
                if search_keywords:
                    article_query = f"{search_keywords} product review comparison"
                else:
                    article_query = f"{search_query} product review comparison"
            elif research_type == "financial_research":
                print(f"💹 Finding financial instruments for: {search_query}")
                # Use more specific search terms for financial research
                if "stock" in search_query.lower() or "investment" in search_query.lower():
                    # For specific stock queries, search for that stock first
                    if any(word in search_query.upper() for word in ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'TTWK', 'NVDA', 'META']):
                        # Extract stock symbol and search specifically
                        stock_symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'TTWK', 'NVDA', 'META']
                        found_symbols = [sym for sym in stock_symbols if sym in search_query.upper()]
                        if found_symbols:
                            article_query = f"{' '.join(found_symbols)} stock analysis price target 2024"
                        else:
                            # Use search keywords if available, otherwise use refined query
                            search_keywords = getattr(state, 'search_keywords', '')
                            if search_keywords:
                                article_query = f"{search_keywords} stock investment analysis"
                            else:
                                article_query = f"{search_query} top stocks companies 2024 2025 best investments"
                    else:
                        # Use search keywords if available, otherwise use refined query
                        search_keywords = getattr(state, 'search_keywords', '')
                        if search_keywords:
                            article_query = f"{search_keywords} stock investment analysis"
                        else:
                            article_query = f"{search_query} top stocks companies 2024 2025 best investments"
                else:
                    article_query = f"{search_query} stock investment financial"
            elif research_type == "technical_research":
                print(f"🔧 Finding technical documentation for: {search_query}")
                # Use search keywords if available, otherwise use refined query
                search_keywords = getattr(state, 'search_keywords', '')
                if search_keywords:
                    article_query = f"{search_keywords} API documentation technical"
                else:
                    article_query = f"{search_query} API documentation technical"
            elif research_type == "industry_research":
                print(f"🏭 Finding industry sectors for: {search_query}")
                # Use search keywords if available, otherwise use refined query
                search_keywords = getattr(state, 'search_keywords', '')
                if search_keywords:
                    article_query = f"{search_keywords} industry market analysis"
                else:
                    article_query = f"{search_query} industry market analysis"
            elif research_type == "general_research":
                print(f"🔍 Finding general information for: {search_query}")
                # Use search keywords if available, otherwise use refined query
                search_keywords = getattr(state, 'search_keywords', '')
                if search_keywords:
                    article_query = f"{search_keywords} information facts details"
                else:
                    article_query = f"{search_query} information facts details"
            else:
                # Developer tools extraction (existing logic)
                print(f"🔍 Finding articles about: {search_query}")
                if getattr(state, 'search_keywords', ''):
                    article_query = f"{state.search_keywords} tools comparison best alternatives"
                else:
                    article_query = f"{search_query} tools comparison best alternatives"

            search_results = self.firecrawl.search_companies(article_query, num_results=4)  # Increased from 2 to 4

            all_content = ""
            for result in search_results.data:
                url = result.get("url", "")
                scraped = self.firecrawl.scrape_company_pages(url)
                if scraped:
                    all_content += scraped.markdown[:1500] + "\n\n"

            # Use appropriate extraction prompt based on research type
            if research_type == "educational_research":
                extraction_prompt = f"""
                Extract educational institutions, universities, and academic entities from this content:
                
                Content: {all_content}
                
                Return only the names of educational institutions, one per line.
                """
            elif research_type == "product_research":
                extraction_prompt = f"""
                Extract product names and brands from this content:
                
                Content: {all_content}
                
                Return only the names of products and brands, one per line.
                """
            elif research_type == "financial_research":
                extraction_prompt = f"""
                Extract financial instruments, stocks, and investment entities from this content:
                
                Content: {all_content}
                
                Focus on:
                1. The specific stock/company mentioned in the query (if any)
                2. Major publicly traded companies (Apple, Microsoft, Google, Amazon, Tesla, etc.)
                3. Growth stocks and value stocks
                4. Sector ETFs and investment funds
                5. Companies mentioned in investment recommendations
                6. Top performing stocks and market leaders
                
                If the query mentions a specific stock symbol (like TTWK, AAPL, MSFT), prioritize that stock.
                If no specific stock is found, list major companies and investment opportunities.
                
                Return only the names of financial instruments and companies, one per line.
                Prioritize well-known companies and major stocks.
                """
            elif research_type == "technical_research":
                extraction_prompt = f"""
                Extract technical tools, APIs, and documentation from this content:
                
                Content: {all_content}
                
                Return only the names of technical tools and APIs, one per line.
                """
            elif research_type == "industry_research":
                extraction_prompt = f"""
                Extract industry sectors and market entities from this content:
                
                Content: {all_content}
                
                Return only the names of industries and sectors, one per line.
                """
            elif research_type == "general_research":
                extraction_prompt = f"""
                Extract relevant entities, topics, or key information from this content:
                
                Content: {all_content}
                
                Return only the names of relevant entities or topics, one per line.
                """
            else:
                # Default to tool extraction for developer_tools
                messages = [
                    SystemMessage(content=self.prompts.TOOL_EXTRACTION_SYSTEM),
                    HumanMessage(content=self.prompts.tool_extraction_user(state.query, all_content))
                ]
                
                try:
                    response = self.llm.invoke(messages)
                    tool_names = [
                        name.strip()
                        for name in response.content.strip().split("\n")
                        if name.strip()
                    ]
                    print(f"Extracted tools: {', '.join(tool_names[:5])}")
                    return {"extracted_tools": tool_names}
                except Exception as e:
                    print(e)
                    return {"extracted_tools": []}

            # Use generic extraction for specialized types
            messages = [
                SystemMessage(content="You are a content extraction specialist. Extract relevant entities from the provided content."),
                HumanMessage(content=extraction_prompt)
            ]

            try:
                response = self.llm.invoke(messages)
                entity_names = [
                    name.strip()
                    for name in response.content.strip().split("\n")
                    if name.strip()
                ]
                print(f"Extracted entities: {', '.join(entity_names[:5])}")
                return {
                    "extracted_tools": entity_names,
                    "detailed_content": all_content
                }
            except Exception as e:
                print(e)
                return {
                    "extracted_tools": [],
                    "detailed_content": all_content
                }

    def _market_research_step(self, state: ResearchState) -> Dict[str, Any]:
        """Conduct market research and competitive analysis"""
        print(f"📊 Conducting market research for: {state.query}")
        
        # Use market research agent
        market_results = self.market_research_agent.research_market_entities(state.query, state)
        
        return market_results

    def _process_pdfs_step(self, state: ResearchState) -> Dict[str, Any]:
        """Process PDFs and generate structured notes"""
        print(f"📄 Processing PDFs for: {state.query}")
        
        # Use the PDF Notetaker agent to process PDFs
        pdf_results = self.pdf_notetaker.process_pdfs_for_query(state.query, state)
        
        return pdf_results

    def run(self, query: str) -> ResearchState:
        initial_state = ResearchState(query=query)
        final_state = self.workflow.invoke(initial_state)
        return ResearchState(**final_state)

    def run_with_selected_pdfs(self, query: str, selected_pdf_keys: List[str]) -> ResearchState:
        """Run research with user-selected PDFs"""
        initial_state = ResearchState(query=query)
        
        # Process the workflow steps
        state = initial_state
        
        # Detect intent
        intent_result = self._detect_intent_step(state)
        state = ResearchState(**{**state.dict(), **intent_result})
        
        # Extract content
        content_result = self._extract_content_step(state)
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
