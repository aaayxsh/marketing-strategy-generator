from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - optional local convenience
    def load_dotenv() -> bool:
        return False

from marketing_strategy_generator.data_loader import load_audience_segments, load_market_trends
from marketing_strategy_generator.generator import generate_strategy
from marketing_strategy_generator.llm_client import OptionalOpenAIClient


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
PROMPTS_DIR = BASE_DIR / "prompts"


def _format_currency(value: float) -> str:
    return f"${value:,.0f}"


def main() -> None:
    st.set_page_config(page_title="Marketing Strategy Generator", page_icon="📢", layout="wide")
    st.title("📢 Marketing Strategy Generator")
    st.caption("Develop marketing strategies from market trends and audience data.")

    with st.sidebar:
        st.header("Business Context")
        company = st.text_input("Company", value="BrightPixel AI")
        industry = st.text_input("Industry", value="B2B SaaS")
        objective = st.text_area(
            "Growth Objective",
            value="Generate qualified pipeline from marketing operations leaders in mid-market firms.",
        )
        budget = st.number_input("Monthly Budget", min_value=1000, value=12000, step=1000)
        region = st.text_input("Region", value="India + Remote Global")
        use_llm = st.toggle("Use OpenAI enhancement if configured", value=True)

    market_path = DATA_DIR / "market_trends.csv"
    audience_path = DATA_DIR / "audience_segments.csv"

    trends = load_market_trends(market_path)
    audience = load_audience_segments(audience_path)

    llm_client = OptionalOpenAIClient(enabled=use_llm)
    strategy = generate_strategy(
        company=company,
        industry=industry,
        objective=objective,
        budget=budget,
        region=region,
        trends=trends,
        audience_segments=audience,
        llm_client=llm_client,
        system_prompt_path=PROMPTS_DIR / "strategy_system_prompt.md",
    )

    left, right = st.columns((1.1, 0.9))

    with left:
        st.subheader("Market Trend Signals")
        trends_df = pd.DataFrame([item.model_dump() for item in trends])
        st.dataframe(trends_df, use_container_width=True)
        st.bar_chart(trends_df.set_index("channel")["growth_score"])

        st.subheader("Audience Segments")
        audience_df = pd.DataFrame([item.model_dump() for item in audience])
        st.dataframe(audience_df, use_container_width=True)

    with right:
        st.subheader("Generated Strategy")
        st.markdown(f"**Positioning:** {strategy.positioning_statement}")
        st.markdown(f"**Primary Audience:** {', '.join(strategy.primary_segments)}")
        st.markdown(f"**Top Channels:** {', '.join(strategy.recommended_channels)}")

        st.markdown("**Budget Allocation**")
        budget_df = pd.DataFrame(
            [{"channel": key, "budget": value} for key, value in strategy.budget_allocation.items()]
        )
        st.dataframe(
            budget_df.assign(budget=budget_df["budget"].map(_format_currency)),
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("**Content Pillars**")
        for item in strategy.content_pillars:
            st.write(f"- {item}")

        st.markdown("**Campaign Ideas**")
        for item in strategy.campaign_ideas:
            st.write(f"- {item}")

        st.markdown("**KPIs**")
        for item in strategy.kpis:
            st.write(f"- {item}")

    st.subheader("30-60-90 Day Action Plan")
    plan_cols = st.columns(3)
    for index, phase in enumerate(strategy.action_plan):
        with plan_cols[index]:
            st.markdown(f"**{phase['phase']}**")
            for task in phase["tasks"]:
                st.write(f"- {task}")

    st.subheader("Executive Summary")
    st.write(strategy.executive_summary)

    if strategy.llm_enhancement:
        st.subheader("OpenAI-Enhanced Narrative")
        st.markdown(strategy.llm_enhancement)


if __name__ == "__main__":
    main()
