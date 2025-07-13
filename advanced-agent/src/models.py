from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime


class CompanyAnalysis(BaseModel):
    """Structured output for LLM company analysis focused on developer tools"""
    pricing_model: str  # Free, Freemium, Paid, Enterprise, Unknown
    is_open_source: Optional[bool] = None
    tech_stack: List[str] = []
    description: str = ""
    api_available: Optional[bool] = None
    language_support: List[str] = []
    integration_capabilities: List[str] = []


class CompanyInfo(BaseModel):
    name: str
    description: str
    website: str
    pricing_model: Optional[str] = None
    is_open_source: Optional[bool] = None
    tech_stack: List[str] = []
    competitors: List[str] = []
    # Developer-specific fields
    api_available: Optional[bool] = None
    language_support: List[str] = []
    integration_capabilities: List[str] = []
    developer_experience_rating: Optional[str] = None  # Poor, Good, Excellent


# NEW: Market Research Models
class MarketEntity(BaseModel):
    """Generic entity for market research (companies, products, markets)"""
    name: str
    category: str  # company, product, market, technology, industry
    description: str
    website: Optional[str] = None
    
    # General business fields
    market_position: Optional[str] = None  # leader, challenger, niche, emerging
    market_share: Optional[float] = None
    revenue: Optional[str] = None
    employees: Optional[int] = None
    founded_year: Optional[int] = None
    headquarters: Optional[str] = None
    
    # Product review fields
    price: Optional[str] = None
    rating: Optional[str] = None
    brand: Optional[str] = None
    features: List[str] = []
    warranty: Optional[str] = None
    target_audience: Optional[str] = None
    alternatives: List[str] = []
    
    # Educational comparison fields
    ranking: Optional[str] = None
    admission_rate: Optional[str] = None
    programs: List[str] = []
    cost: Optional[str] = None
    location: Optional[str] = None
    career_outcomes: Optional[str] = None
    faculty_quality: Optional[str] = None
    student_life: Optional[str] = None
    international_reputation: Optional[str] = None
    
    # Financial analysis fields
    symbol: Optional[str] = None
    current_price: Optional[str] = None
    market_cap: Optional[str] = None
    pe_ratio: Optional[str] = None
    dividend_yield: Optional[str] = None
    risk_level: Optional[str] = None
    sector: Optional[str] = None
    performance_history: Optional[str] = None
    analyst_ratings: Optional[str] = None
    growth_potential: Optional[str] = None
    investment_thesis: Optional[str] = None
    
    # Technical documentation fields
    version: Optional[str] = None
    api_endpoints: Optional[str] = None
    authentication_methods: Optional[str] = None
    sdk_availability: Optional[str] = None
    documentation_quality: Optional[str] = None
    code_examples: Optional[str] = None
    integration_capabilities: Optional[str] = None
    rate_limits: Optional[str] = None
    best_practices: Optional[str] = None
    
    # Industry analysis fields
    market_size: Optional[str] = None
    growth_rate: Optional[str] = None
    key_players: List[str] = []
    trends: List[str] = []
    threats: Optional[str] = None
    regulatory_environment: Optional[str] = None
    technology_drivers: Optional[str] = None
    investment_opportunities: Optional[str] = None
    future_outlook: Optional[str] = None


class FinancialMetrics(BaseModel):
    """Financial performance metrics"""
    revenue: Optional[str] = None
    revenue_growth: Optional[str] = None  # Changed from float to str to handle "UNKNOWN"
    profit_margin: Optional[str] = None   # Changed from float to str to handle "UNKNOWN"
    market_cap: Optional[str] = None
    pe_ratio: Optional[str] = None       # Changed from float to str to handle "UNKNOWN"
    debt_to_equity: Optional[str] = None # Changed from float to str to handle "UNKNOWN"
    cash_flow: Optional[str] = None


class CompetitiveAnalysis(BaseModel):
    """Structured competitive analysis output"""
    competitive_advantages: List[str] = []
    weaknesses: List[str] = []
    market_opportunities: List[str] = []
    threats: List[str] = []
    key_competitors: List[str] = []
    market_position: str = "Unknown"
    strategic_initiatives: List[str] = []
    risk_factors: List[str] = []


class MarketInsights(BaseModel):
    """Market-level insights and analysis"""
    market_size: Optional[str] = None
    growth_rate: Optional[float] = None
    key_drivers: List[str] = []
    market_trends: List[str] = []
    regulatory_environment: Optional[str] = None
    customer_segments: List[str] = []
    distribution_channels: List[str] = []


# NEW: Technical Documentation Models
class APIEndpoint(BaseModel):
    """API endpoint information"""
    method: str  # GET, POST, PUT, DELETE
    path: str
    description: str
    parameters: List[str] = []
    response_format: str = ""
    authentication_required: bool = False


class TechnicalSpecification(BaseModel):
    """Technical specification details"""
    name: str
    version: str = ""
    description: str
    api_endpoints: List[APIEndpoint] = []
    authentication_methods: List[str] = []
    data_models: List[str] = []
    integration_points: List[str] = []
    code_examples: List[str] = []
    requirements: List[str] = []
    best_practices: List[str] = []
    common_issues: List[str] = []


class PDFDocument(BaseModel):
    """Represents a PDF document from S3"""
    s3_key: str
    filename: str
    content: str
    metadata: Dict[str, Any] = {}
    processed_at: Optional[datetime] = None
    relevance_score: Optional[float] = None  # 0-1 score for query relevance


class PDFNotes(BaseModel):
    """Structured notes extracted from PDF documents"""
    document_id: str
    summary: str
    key_points: List[str] = []
    technical_details: List[str] = []
    business_insights: List[str] = []
    recommendations: List[str] = []
    extracted_entities: List[str] = []  # companies, products, technologies
    relevance_score: Optional[float] = None  # 0-1 score for query relevance


class ResearchState(BaseModel):
    query: str
    research_type: str = "developer_tools"  # developer_tools, market_research, competitive_analysis
    # Intent Detection Data
    refined_query: str = ""
    research_focus: str = ""
    expected_output: str = ""
    search_keywords: str = ""
    context_notes: str = ""
    search_approach: str = ""
    analysis_focus: str = ""
    output_format: str = ""
    priority_metrics: List[str] = []
    # Research Data
    extracted_tools: List[str] = []  # Tools extracted from articles
    companies: List[CompanyInfo] = []
    # NEW: Market Research fields
    market_entities: List[MarketEntity] = []
    financial_metrics: Dict[str, FinancialMetrics] = {}
    competitive_analyses: List[CompetitiveAnalysis] = []
    market_insights: Optional[MarketInsights] = None
    # NEW: Technical Documentation fields
    technical_specifications: List[TechnicalSpecification] = []
    api_endpoints: List[APIEndpoint] = []
    search_results: List[Dict[str, Any]] = []
    # PDF Processing
    pdf_documents: List[PDFDocument] = []
    pdf_notes: List[PDFNotes] = []
    analysis: Optional[str] = None
