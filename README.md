# Marketing Strategy Generator

`Marketing Strategy Generator` is a usable AI-assisted project for building marketing plans from market trends and audience data.

It includes:

- A Streamlit app for interactive strategy generation
- A CLI for batch or terminal usage
- Local deterministic strategy logic so it works without an API key
- Optional OpenAI integration for richer campaign recommendations
- Sample CSV datasets for trends and audience segments

## Project Structure

```text
marketing_strategy_generator/
├── app.py
├── requirements.txt
├── .env.example
├── data/
│   ├── audience_segments.csv
│   └── market_trends.csv
├── prompts/
│   └── strategy_system_prompt.md
└── marketing_strategy_generator/
    ├── __init__.py
    ├── analyzers.py
    ├── cli.py
    ├── data_loader.py
    ├── generator.py
    ├── llm_client.py
    └── models.py
```

## Features

- Reads market trend signals such as channel growth, sentiment, CPC, and competitor intensity
- Reads audience segment data such as pain points, preferred channels, conversion likelihood, and budget potential
- Generates:
  - market summary
  - audience priorities
  - positioning statement
  - budget allocation
  - campaign ideas
  - content pillars
  - KPIs
  - a 30-60-90 day action plan

## Quick Start

### 1. Create environment and install dependencies

```powershell
cd "C:\Users\Ayush Srivastava\OneDrive\Documents\coding_files\projects\marketing_strategy_generator"
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Optional: add OpenAI key

Copy `.env.example` to `.env` and set:

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-5-mini
```

The app still works without this key using local strategy generation.

### 3. Run the Streamlit app

```powershell
streamlit run app.py
```

### 4. Run the CLI

```powershell
python -m marketing_strategy_generator.cli `
  --company "BrightPixel AI" `
  --industry "B2B SaaS" `
  --objective "Generate pipeline from mid-market marketing teams" `
  --budget 12000
```

## Data Inputs

### `data/market_trends.csv`

Expected columns:

- `topic`
- `channel`
- `growth_score`
- `search_interest`
- `sentiment_score`
- `cpc`
- `competitor_intensity`

### `data/audience_segments.csv`

Expected columns:

- `segment_name`
- `industry`
- `pain_points`
- `preferred_channels`
- `budget_potential`
- `conversion_likelihood`
- `message_tone`

## How It Works

1. The loader reads market and audience data.
2. The analyzers compute top channels, strongest themes, and highest-value segments.
3. The generator builds a practical marketing strategy.
4. If an OpenAI key is available, the app can also request an expanded narrative strategy from the model.

## Suggested Extensions

- Connect live Google Trends or social listening APIs
- Add campaign calendar export to CSV or Notion
- Store strategies in a database
- Add role-based prompts for product marketing, growth marketing, and brand marketing

