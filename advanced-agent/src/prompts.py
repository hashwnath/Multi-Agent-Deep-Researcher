
class DeveloperToolsPrompts:
    """Collection of prompts for analyzing developer tools and technologies"""

    # Tool extraction prompts
    TOOL_EXTRACTION_SYSTEM = """You are a tech researcher. Extract specific tool, library, platform, or service names from articles.
                            Focus on actual products/tools that developers can use, not general concepts or features."""

    @staticmethod
    def tool_extraction_user(query: str, content: str) -> str:
        return f"""Query: {query}
                Article Content: {content}

                Extract a list of specific tool/service names mentioned in this content that are relevant to "{query}".

                Rules:
                - Only include actual product names, not generic terms
                - Focus on tools developers can directly use/implement
                - Include both open source and commercial options
                - Limit to the 5 most relevant tools
                - Return just the tool names, one per line, no descriptions

                Example format:
                Supabase
                PlanetScale
                Railway
                Appwrite
                Nhost"""

    # Company/Tool analysis prompts
    TOOL_ANALYSIS_SYSTEM = """You are analyzing developer tools and programming technologies. 
                            Focus on extracting information relevant to programmers and software developers. 
                            Pay special attention to programming languages, frameworks, APIs, SDKs, and development workflows."""

    @staticmethod
    def tool_analysis_user(company_name: str, content: str) -> str:
        return f"""Company/Tool: {company_name}
                Website Content: {content[:2500]}

                Analyze this content from a developer's perspective and provide:
                - pricing_model: One of "Free", "Freemium", "Paid", "Enterprise", or "Unknown"
                - is_open_source: true if open source, false if proprietary, null if unclear
                - tech_stack: List of programming languages, frameworks, databases, APIs, or technologies supported/used
                - description: Brief 1-sentence description focusing on what this tool does for developers
                - api_available: true if REST API, GraphQL, SDK, or programmatic access is mentioned
                - language_support: List of programming languages explicitly supported (e.g., Python, JavaScript, Go, etc.)
                - integration_capabilities: List of tools/platforms it integrates with (e.g., GitHub, VS Code, Docker, AWS, etc.)

                Focus on developer-relevant features like APIs, SDKs, language support, integrations, and development workflows."""

    # Recommendation prompts
    RECOMMENDATIONS_SYSTEM = """You are a senior software engineer providing quick, concise tech recommendations. 
                            Keep responses brief and actionable - maximum 3-4 sentences total."""

    @staticmethod
    def recommendations_user(query: str, company_data: str) -> str:
        return f"""Developer Query: {query}
                Tools/Technologies Analyzed: {company_data}

                Provide a brief recommendation (3-4 sentences max) covering:
                - Which tool is best and why
                - Key cost/pricing consideration
                - Main technical advantage

                Be concise and direct - no long explanations needed."""

    # NEW: PDF Processing prompts
    PDF_ANALYSIS_SYSTEM = """You are a research analyst specializing in technical and business document analysis.
                            Extract key insights, technical details, and business implications from PDF documents.
                            Focus on information that would be valuable for competitive research and market analysis."""

    @staticmethod
    def pdf_analysis_user(query: str, pdf_content: str) -> str:
        return f"""Research Query: {query}
                PDF Content: {pdf_content[:3000]}

                Analyze this PDF document and provide structured insights:

                1. Executive Summary (2-3 sentences)
                2. Key Technical Points (bullet points)
                3. Business Insights (bullet points)
                4. Relevant Entities (companies, products, technologies mentioned)
                5. Recommendations (if applicable)
                6. Relevance Score (0-1, how relevant is this to the query)

                Focus on information relevant to: {query}
                
                Return in structured format for parsing."""

    # Enhanced recommendation prompts (now includes PDF context)
    ENHANCED_RECOMMENDATIONS_SYSTEM = """You are a senior research analyst providing comprehensive recommendations.
                            Consider both web research and PDF document analysis in your recommendations.
                            Keep responses concise but thorough."""

    @staticmethod
    def enhanced_recommendations_user(query: str, company_data: str, pdf_insights: str = "") -> str:
        return f"""Research Query: {query}
                Web Research Data: {company_data}
                PDF Document Insights: {pdf_insights}

                Provide a comprehensive recommendation covering:
                - Best options based on all available data
                - Key considerations from both web and document sources
                - Strategic advantages and trade-offs
                - Implementation recommendations

                Consider insights from both web research and PDF documents in your analysis."""

    # NEW: Market Research Prompts
    MARKET_ENTITY_EXTRACTION_SYSTEM = """You are a market research analyst. Extract specific company, product, or market entity names from articles.
                                        Focus on actual companies, products, or markets that are relevant to the research query."""

    @staticmethod
    def market_entity_extraction_user(query: str, content: str) -> str:
        return f"""Research Query: {query}
                Article Content: {content}

                Extract a list of specific companies, products, or market entities mentioned in this content that are relevant to "{query}".

                Rules:
                - Only include actual company/product names, not generic terms
                - Focus on entities relevant to the research query
                - Include both established and emerging players
                - Limit to the 5 most relevant entities
                - Return just the entity names, one per line, no descriptions

                Example format:
                Apple Inc
                Samsung Electronics
                Xiaomi Corporation
                Huawei Technologies
                OnePlus"""

    COMPETITIVE_ANALYSIS_SYSTEM = """You are a competitive intelligence analyst specializing in market research and competitive analysis.
                                    Focus on extracting information relevant to market positioning, competitive advantages, and strategic analysis."""

    @staticmethod
    def competitive_analysis_user(entity_name: str, content: str) -> str:
        return f"""Entity: {entity_name}
                Content: {content[:2500]}

                Analyze this content from a competitive intelligence perspective and provide:
                - competitive_advantages: List of competitive advantages or strengths
                - weaknesses: List of weaknesses or areas of concern
                - market_opportunities: List of market opportunities or growth areas
                - threats: List of threats or challenges
                - key_competitors: List of main competitors
                - market_position: One of "leader", "challenger", "niche", "emerging", or "unknown"
                - strategic_initiatives: List of strategic initiatives or recent moves
                - risk_factors: List of risk factors or challenges

                Focus on market positioning, competitive landscape, and strategic analysis."""

    MARKET_INSIGHTS_SYSTEM = """You are a market research analyst specializing in industry analysis and market insights.
                               Focus on market size, growth trends, key drivers, and market dynamics."""

    @staticmethod
    def market_insights_user(query: str, content: str) -> str:
        return f"""Market Query: {query}
                Content: {content[:3000]}

                Analyze this content and provide market-level insights:

                1. Market Size (if mentioned)
                2. Growth Rate (if available)
                3. Key Market Drivers (bullet points)
                4. Market Trends (bullet points)
                5. Regulatory Environment (if relevant)
                6. Customer Segments (if mentioned)
                7. Distribution Channels (if relevant)

                Focus on market-level analysis, not individual company analysis."""

    FINANCIAL_ANALYSIS_SYSTEM = """You are a financial analyst specializing in company financial performance analysis.
                                   Extract and analyze financial metrics and performance indicators."""

    @staticmethod
    def financial_analysis_user(entity_name: str, content: str) -> str:
        return f"""Entity: {entity_name}
                Content: {content[:2000]}

                Extract financial metrics and performance indicators:

                - revenue: Revenue figures (if mentioned)
                - revenue_growth: Revenue growth rate (if available)
                - profit_margin: Profit margin (if mentioned)
                - market_cap: Market capitalization (if available)
                - pe_ratio: Price-to-earnings ratio (if mentioned)
                - debt_to_equity: Debt-to-equity ratio (if available)
                - cash_flow: Cash flow information (if mentioned)

                Focus on quantitative financial metrics and performance indicators."""

    MARKET_RECOMMENDATIONS_SYSTEM = """You are a senior market research analyst providing strategic market insights and recommendations.
                                      Consider market dynamics, competitive landscape, and strategic implications."""

    @staticmethod
    def market_recommendations_user(query: str, market_data: str, pdf_insights: str = "") -> str:
        return f"""Market Research Query: {query}
                Market Analysis Data: {market_data}
                PDF Document Insights: {pdf_insights}

                Provide strategic market recommendations covering:
                - Market opportunities and threats
                - Competitive positioning analysis
                - Strategic recommendations for market entry or positioning
                - Key success factors and risk considerations
                - Market trends and future outlook

                Consider both market research data and document insights in your analysis."""

    # NEW: Technical Documentation Prompts
    TECHNICAL_DOCUMENTATION_SYSTEM = """You are a technical documentation analyst specializing in API documentation, 
                                       code documentation, and technical specifications. Focus on implementation details, 
                                       technical architecture, and developer guidance."""

    @staticmethod
    def technical_documentation_user(query: str, content: str) -> str:
        return f"""Technical Query: {query}
                Documentation Content: {content[:3000]}

                Analyze this technical documentation and provide:
                1. API Endpoints: List and describe available endpoints
                2. Authentication: Authentication methods and requirements
                3. Data Models: Key data structures and schemas
                4. Integration Points: How to integrate with this system
                5. Code Examples: Implementation examples and patterns
                6. Technical Requirements: System requirements and dependencies
                7. Best Practices: Recommended implementation approaches
                8. Common Issues: Potential problems and solutions

                Focus on practical implementation guidance for developers."""

    TECHNICAL_IMPLEMENTATION_SYSTEM = """You are a senior software engineer providing technical implementation guidance.
                                        Focus on practical code examples, integration patterns, and best practices."""

    @staticmethod
    def technical_implementation_user(query: str, technical_data: str, pdf_insights: str = "") -> str:
        return f"""Technical Query: {query}
                Technical Documentation: {technical_data}
                PDF Document Insights: {pdf_insights}

                Provide technical implementation guidance covering:
                - API integration patterns and examples
                - Authentication and security considerations
                - Data model implementation
                - Error handling and edge cases
                - Performance optimization tips
                - Testing strategies
                - Deployment considerations

                Include practical code examples and step-by-step implementation guidance."""
