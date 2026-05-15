from __future__ import annotations

from collections import defaultdict
from statistics import mean
from typing import Dict, List

from .models import AudienceSegment, MarketTrend


def analyze_market(trends: List[MarketTrend]) -> Dict[str, object]:
    channel_scores: Dict[str, float] = defaultdict(float)
    topic_scores: Dict[str, float] = {}

    for trend in trends:
        score = (
            trend.growth_score * 0.35
            + trend.search_interest * 0.25
            + trend.sentiment_score * 0.20
            - trend.competitor_intensity * 0.10
            - min(trend.cpc * 2, 20) * 0.10
        )
        channel_scores[trend.channel] += score
        topic_scores[trend.topic] = round(score, 2)

    top_channels = sorted(channel_scores, key=channel_scores.get, reverse=True)[:4]
    top_topics = sorted(topic_scores, key=topic_scores.get, reverse=True)[:5]

    average_growth = mean(item.growth_score for item in trends)
    average_sentiment = mean(item.sentiment_score for item in trends)
    market_temperature = "hot" if average_growth >= 75 else "steady" if average_growth >= 55 else "emerging"

    return {
        "top_channels": top_channels,
        "top_topics": top_topics,
        "channel_scores": {key: round(value, 2) for key, value in channel_scores.items()},
        "market_temperature": market_temperature,
        "average_growth": round(average_growth, 2),
        "average_sentiment": round(average_sentiment, 2),
    }


def analyze_audience(segments: List[AudienceSegment]) -> Dict[str, object]:
    ranked = sorted(
        segments,
        key=lambda item: item.budget_potential * 0.55 + item.conversion_likelihood * 0.45,
        reverse=True,
    )
    primary = ranked[:3]

    channel_frequency: Dict[str, int] = defaultdict(int)
    recurring_pain_points: Dict[str, int] = defaultdict(int)

    for segment in primary:
        for channel in [item.strip() for item in segment.preferred_channels.split(",") if item.strip()]:
            channel_frequency[channel] += 1
        for pain_point in [item.strip() for item in segment.pain_points.split(",") if item.strip()]:
            recurring_pain_points[pain_point] += 1

    return {
        "primary_segments": [item.segment_name for item in primary],
        "segment_details": [item.model_dump() for item in primary],
        "preferred_channels": sorted(channel_frequency, key=channel_frequency.get, reverse=True),
        "recurring_pain_points": sorted(recurring_pain_points, key=recurring_pain_points.get, reverse=True)[:5],
    }

