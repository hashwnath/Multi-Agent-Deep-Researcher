from typing import List, Optional, Dict, Any
from pydantic import BaseModel


# Educational Comparison Models
class EducationalInstitution(BaseModel):
    """Educational institution information"""
    name: str
    ranking: Optional[int] = None
    admission_rate: Optional[float] = None
    program_quality: Optional[str] = None
    career_outcomes: List[str] = []
    cost: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    programs: List[str] = []
    faculty_quality: Optional[str] = None
    research_opportunities: List[str] = []


class ProgramComparison(BaseModel):
    """Program comparison details"""
    program_name: str
    duration: Optional[str] = None
    cost: Optional[str] = None
    admission_requirements: List[str] = []
    curriculum: List[str] = []
    career_prospects: List[str] = []
    alumni_network: Optional[str] = None


# Product Review Models
class ProductReview(BaseModel):
    """Product review information"""
    name: str
    price: Optional[str] = None
    rating: Optional[float] = None
    features: List[str] = []
    pros: List[str] = []
    cons: List[str] = []
    alternatives: List[str] = []
    category: Optional[str] = None
    brand: Optional[str] = None
    warranty: Optional[str] = None
    user_reviews: List[str] = []


class ProductComparison(BaseModel):
    """Product comparison details"""
    product_name: str
    price_comparison: Optional[str] = None
    feature_comparison: List[str] = []
    value_rating: Optional[float] = None
    recommendation: Optional[str] = None


# Financial Analysis Models
class FinancialInstrument(BaseModel):
    """Financial instrument information"""
    name: str
    symbol: Optional[str] = None
    current_price: Optional[str] = None
    market_cap: Optional[str] = None
    pe_ratio: Optional[float] = None
    dividend_yield: Optional[float] = None
    risk_level: Optional[str] = None
    sector: Optional[str] = None
    performance_history: List[str] = []
    analyst_ratings: List[str] = []


class InvestmentAnalysis(BaseModel):
    """Investment analysis details"""
    instrument_name: str
    investment_thesis: Optional[str] = None
    risk_assessment: Optional[str] = None
    growth_potential: Optional[str] = None
    time_horizon: Optional[str] = None
    recommended_allocation: Optional[str] = None


# Technical Documentation Models
class APIEndpoint(BaseModel):
    """API endpoint information"""
    method: str  # GET, POST, PUT, DELETE
    path: str
    description: str
    parameters: List[str] = []
    response_format: str = ""
    authentication_required: bool = False
    rate_limits: Optional[str] = None
    examples: List[str] = []


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
    sdk_availability: Optional[bool] = None
    documentation_quality: Optional[str] = None


# Industry Analysis Models
class IndustrySector(BaseModel):
    """Industry sector information"""
    name: str
    market_size: Optional[str] = None
    growth_rate: Optional[float] = None
    key_players: List[str] = []
    trends: List[str] = []
    opportunities: List[str] = []
    threats: List[str] = []
    regulatory_environment: Optional[str] = None
    technology_drivers: List[str] = []


class MarketTrend(BaseModel):
    """Market trend analysis"""
    trend_name: str
    description: str
    impact_level: Optional[str] = None  # High, Medium, Low
    time_horizon: Optional[str] = None
    affected_sectors: List[str] = []
    business_implications: List[str] = [] 