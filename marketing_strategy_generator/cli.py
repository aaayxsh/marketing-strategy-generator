from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - optional local convenience
    def load_dotenv() -> bool:
        return False

from .data_loader import load_audience_segments, load_market_trends
from .generator import generate_strategy
from .llm_client import OptionalOpenAIClient


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate a marketing strategy from trend and audience data.")
    parser.add_argument("--company", required=True)
    parser.add_argument("--industry", required=True)
    parser.add_argument("--objective", required=True)
    parser.add_argument("--budget", type=float, required=True)
    parser.add_argument("--region", default="Global")
    parser.add_argument("--market-data", default=str(Path("data") / "market_trends.csv"))
    parser.add_argument("--audience-data", default=str(Path("data") / "audience_segments.csv"))
    parser.add_argument("--use-llm", action="store_true")
    parser.add_argument("--json-output", action="store_true")
    return parser


def main() -> None:
    load_dotenv()
    parser = build_parser()
    args = parser.parse_args()

    trends = load_market_trends(args.market_data)
    audience = load_audience_segments(args.audience_data)
    llm_client = OptionalOpenAIClient(enabled=args.use_llm)
    strategy = generate_strategy(
        company=args.company,
        industry=args.industry,
        objective=args.objective,
        budget=args.budget,
        region=args.region,
        trends=trends,
        audience_segments=audience,
        llm_client=llm_client,
        system_prompt_path=Path("prompts") / "strategy_system_prompt.md",
    )

    if args.json_output:
        print(json.dumps(strategy.model_dump(), indent=2))
        return

    print(f"\nMarketing Strategy for {strategy.company}")
    print("=" * 60)
    print(f"Industry: {strategy.industry}")
    print(f"Objective: {strategy.objective}")
    print(f"Region: {strategy.region}")
    print(f"\nPositioning:\n{strategy.positioning_statement}")
    print(f"\nExecutive Summary:\n{strategy.executive_summary}")
    print(f"\nPrimary Segments: {', '.join(strategy.primary_segments)}")
    print(f"Recommended Channels: {', '.join(strategy.recommended_channels)}")
    print("\nBudget Allocation:")
    for channel, value in strategy.budget_allocation.items():
        print(f"- {channel}: ${value:,.2f}")
    print("\nCampaign Ideas:")
    for item in strategy.campaign_ideas:
        print(f"- {item}")
    print("\nKPIs:")
    for item in strategy.kpis:
        print(f"- {item}")

    if strategy.llm_enhancement:
        print("\nOpenAI Enhancement:\n")
        print(strategy.llm_enhancement)


if __name__ == "__main__":
    main()
