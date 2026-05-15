from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class MarketTrend(BaseModel):
    topic: str
    channel: str
    growth_score: float = Field(ge=0, le=100)
    search_interest: float = Field(ge=0, le=100)
    sentiment_score: float = Field(ge=0, le=100)
    cpc: float = Field(ge=0)
    competitor_intensity: float = Field(ge=0, le=100)


class AudienceSegment(BaseModel):
    segment_name: str
    industry: str
    pain_points: str
    preferred_channels: str
    budget_potential: float = Field(ge=0)
    conversion_likelihood: float = Field(ge=0, le=100)
    message_tone: str


class StrategyOutput(BaseModel):
    company: str
    industry: str
    objective: str
    region: str
    positioning_statement: str
    executive_summary: str
    primary_segments: List[str]
    recommended_channels: List[str]
    trend_focus_areas: List[str]
    content_pillars: List[str]
    campaign_ideas: List[str]
    kpis: List[str]
    budget_allocation: Dict[str, float]
    action_plan: List[Dict[str, List[str] | str]]
    llm_enhancement: Optional[str] = None

