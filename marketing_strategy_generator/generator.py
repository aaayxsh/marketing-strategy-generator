from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from .analyzers import analyze_audience, analyze_market
from .models import AudienceSegment, MarketTrend, StrategyOutput


def _allocate_budget(budget: float, channels: List[str]) -> dict[str, float]:
    default_weights = [0.35, 0.25, 0.2, 0.2]
    selected_weights = default_weights[: len(channels)]
    weight_total = sum(selected_weights) or 1
    normalized = [item / weight_total for item in selected_weights]
    return {
        channel: round(budget * weight, 2)
        for channel, weight in zip(channels, normalized, strict=False)
    }


def _build_action_plan(objective: str, topics: List[str], segments: List[str]) -> list[dict[str, object]]:
    return [
        {
            "phase": "Days 1-30",
            "tasks": [
                f"Refine messaging around {topics[0]} for {segments[0]}." if topics and segments else "Refine core campaign messaging.",
                "Launch two landing page variants and connect lead capture analytics.",
                "Stand up channel dashboards for paid, content, and outbound performance.",
            ],
        },
        {
            "phase": "Days 31-60",
            "tasks": [
                f"Run channel experiments directly tied to the goal: {objective}.",
                "Publish one conversion-focused case study and one comparison asset.",
                "Retarget engaged visitors with segmented email and social sequences.",
            ],
        },
        {
            "phase": "Days 61-90",
            "tasks": [
                "Shift budget toward top-converting channels and pause weak campaigns.",
                "Package learnings into a repeatable campaign playbook.",
                "Create an executive review with KPI movement, CAC trends, and next-quarter bets.",
            ],
        },
    ]


def generate_strategy(
    company: str,
    industry: str,
    objective: str,
    budget: float,
    region: str,
    trends: List[MarketTrend],
    audience_segments: List[AudienceSegment],
    llm_client: Optional[object] = None,
    system_prompt_path: Optional[str | Path] = None,
) -> StrategyOutput:
    market = analyze_market(trends)
    audience = analyze_audience(audience_segments)

    recommended_channels = []
    for channel in market["top_channels"]:
        if channel not in recommended_channels:
            recommended_channels.append(channel)
    for channel in audience["preferred_channels"]:
        if channel not in recommended_channels:
            recommended_channels.append(channel)
    recommended_channels = recommended_channels[:4]

    trend_focus_areas = list(market["top_topics"])
    primary_segments = list(audience["primary_segments"])
    pain_points = list(audience["recurring_pain_points"])

    positioning_statement = (
        f"{company} helps {', '.join(primary_segments[:2]) or 'priority buyers'} in {industry} "
        f"solve {', '.join(pain_points[:2]) or 'high-value growth challenges'} with a focused, measurable approach."
    )
    executive_summary = (
        f"The market is currently {market['market_temperature']} with strongest traction in "
        f"{', '.join(recommended_channels[:3])}. The best near-term opportunity is to align {objective.lower()} "
        f"with pain-point-led campaigns for {', '.join(primary_segments[:2])} in {region}."
    )

    content_pillars = [
        f"Proof-driven education around {topic}" for topic in trend_focus_areas[:2]
    ] + [
        f"Buyer pain point deep-dives on {pain}" for pain in pain_points[:2]
    ]

    campaign_ideas = [
        f"Launch a gated benchmark report focused on {trend_focus_areas[0]}." if trend_focus_areas else "Launch a gated benchmark report.",
        f"Build a webinar series tailored to {primary_segments[0]}." if primary_segments else "Build a persona-specific webinar series.",
        "Create channel-specific retargeting flows for pricing-page and demo-page visitors.",
        "Test a competitor comparison campaign with proof points and ROI calculators.",
    ]

    kpis = [
        "Marketing qualified leads generated per month",
        "Landing page conversion rate",
        "Pipeline influenced by marketing campaigns",
        "Cost per qualified opportunity",
        "Email nurture reply or meeting-book rate",
    ]

    budget_allocation = _allocate_budget(budget, recommended_channels)
    action_plan = _build_action_plan(objective, trend_focus_areas, primary_segments)

    llm_enhancement = None
    if llm_client and getattr(llm_client, "is_available", lambda: False)():
        system_prompt = ""
        if system_prompt_path and Path(system_prompt_path).exists():
            system_prompt = Path(system_prompt_path).read_text(encoding="utf-8")
        user_prompt = (
            f"Company: {company}\n"
            f"Industry: {industry}\n"
            f"Objective: {objective}\n"
            f"Region: {region}\n"
            f"Budget: {budget}\n"
            f"Primary segments: {primary_segments}\n"
            f"Top channels: {recommended_channels}\n"
            f"Trend focus areas: {trend_focus_areas}\n"
            f"Pain points: {pain_points}\n"
            "Write a concise, practical expanded strategy in markdown with campaign sequencing and risk notes."
        )
        llm_enhancement = llm_client.generate_markdown(system_prompt, user_prompt)

    return StrategyOutput(
        company=company,
        industry=industry,
        objective=objective,
        region=region,
        positioning_statement=positioning_statement,
        executive_summary=executive_summary,
        primary_segments=primary_segments,
        recommended_channels=recommended_channels,
        trend_focus_areas=trend_focus_areas,
        content_pillars=content_pillars,
        campaign_ideas=campaign_ideas,
        kpis=kpis,
        budget_allocation=budget_allocation,
        action_plan=action_plan,
        llm_enhancement=llm_enhancement,
    )

