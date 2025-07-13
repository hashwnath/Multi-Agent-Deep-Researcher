class EducationalComparisonPrompts:
    """Specialized prompts for educational institution comparisons"""
    
    EDUCATIONAL_ANALYSIS_SYSTEM = """You are an educational consultant specializing in university and program comparisons.
                                    Focus on academic quality, career outcomes, admission requirements, and value for money."""
    
    @staticmethod
    def educational_analysis_user(institution_name: str, content: str) -> str:
        return f"""Institution: {institution_name}
                Content: {content[:2500]}

                Analyze this educational institution and provide:
                - ranking: Academic ranking or reputation level
                - admission_rate: Acceptance rate if mentioned
                - program_quality: Quality of academic programs
                - career_outcomes: Career prospects and outcomes
                - cost: Tuition and fees information
                - location: Geographic location
                - programs: Available academic programs
                - faculty_quality: Quality of faculty and teaching
                - research_opportunities: Research and internship opportunities

                Focus on factors that help students make informed educational decisions."""

    EDUCATIONAL_RECOMMENDATIONS_SYSTEM = """You are an educational advisor providing university and program recommendations.
                                          Consider academic fit, career goals, cost, and personal preferences."""

    @staticmethod
    def educational_recommendations_user(query: str, institution_data: str) -> str:
        return f"""Educational Query: {query}
                Institution Data: {institution_data}

                Provide educational recommendations covering:
                - Best academic fit based on goals and preferences
                - Cost-benefit analysis of different options
                - Career prospects and outcomes comparison
                - Admission strategy and requirements
                - Alternative options to consider

                Focus on helping students make informed educational choices."""


class ProductReviewPrompts:
    """Specialized prompts for product reviews and comparisons"""
    
    PRODUCT_ANALYSIS_SYSTEM = """You are a product review analyst specializing in consumer products and gadgets.
                                Focus on features, value for money, user experience, and alternatives."""
    
    @staticmethod
    def product_analysis_user(product_name: str, content: str) -> str:
        return f"""Product: {product_name}
                Content: {content[:2500]}

                Analyze this product and provide:
                - price: Current price and value proposition
                - rating: User rating or expert score
                - features: Key features and capabilities
                - pros: Advantages and strengths
                - cons: Disadvantages and limitations
                - alternatives: Similar products to consider
                - category: Product category and type
                - brand: Brand reputation and reliability
                - warranty: Warranty and support information
                - user_reviews: Key user feedback points

                Focus on helping consumers make informed purchase decisions."""

    PRODUCT_RECOMMENDATIONS_SYSTEM = """You are a consumer product advisor providing purchase recommendations.
                                       Consider value for money, features, user needs, and alternatives."""

    @staticmethod
    def product_recommendations_user(query: str, product_data: str) -> str:
        return f"""Product Query: {query}
                Product Data: {product_data}

                Provide product recommendations covering:
                - Best product for the specific use case
                - Value for money analysis
                - Feature comparison with alternatives
                - Purchase timing and pricing advice
                - Potential issues and considerations

                Focus on helping consumers make smart purchase decisions."""


class FinancialAnalysisPrompts:
    """Specialized prompts for financial analysis and investment recommendations"""
    
    FINANCIAL_ANALYSIS_SYSTEM = """You are a financial analyst specializing in investment analysis and market research.
                                  Focus on financial performance, risk assessment, and investment potential."""
    
    @staticmethod
    def financial_analysis_user(instrument_name: str, content: str) -> str:
        return f"""Financial Instrument: {instrument_name}
                Content: {content[:2500]}

                Analyze this financial instrument and provide:
                - symbol: Trading symbol if applicable
                - current_price: Current market price
                - market_cap: Market capitalization
                - pe_ratio: Price-to-earnings ratio
                - dividend_yield: Dividend yield if applicable
                - risk_level: Risk assessment (Low, Medium, High)
                - sector: Industry sector
                - performance_history: Recent performance trends
                - analyst_ratings: Analyst recommendations

                Focus on investment analysis and risk assessment."""

    INVESTMENT_RECOMMENDATIONS_SYSTEM = """You are an investment advisor providing financial recommendations.
                                          Consider risk tolerance, investment goals, and market conditions."""

    @staticmethod
    def investment_recommendations_user(query: str, financial_data: str) -> str:
        return f"""Investment Query: {query}
                Financial Data: {financial_data}

                Provide investment recommendations covering:
                - Best investment options for the query
                - Risk assessment and management
                - Investment timeline and strategy
                - Portfolio allocation advice
                - Market conditions and timing
                - Alternative investment options

                Focus on helping investors make informed financial decisions."""


class TechnicalDocumentationPrompts:
    """Specialized prompts for technical documentation analysis"""
    
    TECHNICAL_ANALYSIS_SYSTEM = """You are a technical documentation analyst specializing in API documentation, 
                                   code documentation, and technical specifications. Focus on implementation details, 
                                   technical architecture, and developer guidance."""
    
    @staticmethod
    def technical_analysis_user(spec_name: str, content: str) -> str:
        return f"""Technical Specification: {spec_name}
                Content: {content[:2500]}

                Analyze this technical documentation and provide:
                - api_endpoints: Available API endpoints and methods
                - authentication_methods: Authentication requirements
                - data_models: Key data structures and schemas
                - integration_points: How to integrate with this system
                - code_examples: Implementation examples and patterns
                - requirements: System requirements and dependencies
                - best_practices: Recommended implementation approaches
                - common_issues: Potential problems and solutions
                - sdk_availability: SDK and library availability
                - documentation_quality: Quality and completeness of docs

                Focus on practical implementation guidance for developers."""

    TECHNICAL_IMPLEMENTATION_SYSTEM = """You are a senior software engineer providing technical implementation guidance.
                                        Focus on practical code examples, integration patterns, and best practices."""

    @staticmethod
    def technical_implementation_user(query: str, technical_data: str) -> str:
        return f"""Technical Query: {query}
                Technical Documentation: {technical_data}

                Provide technical implementation guidance covering:
                - API integration patterns and examples
                - Authentication and security considerations
                - Data model implementation
                - Error handling and edge cases
                - Performance optimization tips
                - Testing strategies
                - Deployment considerations
                - Code examples and snippets

                Include practical step-by-step implementation guidance."""


class IndustryAnalysisPrompts:
    """Specialized prompts for industry analysis and market trends"""
    
    INDUSTRY_ANALYSIS_SYSTEM = """You are an industry analyst specializing in market research and sector analysis.
                                  Focus on market size, growth trends, key players, and industry dynamics."""
    
    @staticmethod
    def industry_analysis_user(sector_name: str, content: str) -> str:
        return f"""Industry Sector: {sector_name}
                Content: {content[:2500]}

                Analyze this industry sector and provide:
                - market_size: Total market size and value
                - growth_rate: Industry growth rate and trends
                - key_players: Major companies and players
                - trends: Current industry trends
                - opportunities: Market opportunities
                - threats: Industry threats and challenges
                - regulatory_environment: Regulatory factors
                - technology_drivers: Technology trends driving the sector

                Focus on comprehensive industry analysis and market insights."""

    INDUSTRY_RECOMMENDATIONS_SYSTEM = """You are an industry consultant providing market insights and strategic recommendations.
                                        Consider market dynamics, competitive landscape, and business opportunities."""

    @staticmethod
    def industry_recommendations_user(query: str, industry_data: str) -> str:
        return f"""Industry Query: {query}
                Industry Data: {industry_data}

                Provide industry recommendations covering:
                - Market opportunities and entry strategies
                - Competitive positioning analysis
                - Investment opportunities in the sector
                - Risk factors and challenges
                - Technology trends and adoption
                - Regulatory considerations
                - Strategic recommendations for businesses

                Focus on actionable business insights and strategic guidance.""" 