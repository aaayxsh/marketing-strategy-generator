from __future__ import annotations

import csv
from pathlib import Path
from typing import List

from .models import AudienceSegment, MarketTrend


def load_market_trends(path: str | Path) -> List[MarketTrend]:
    with open(path, "r", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    return [MarketTrend(**row) for row in rows]


def load_audience_segments(path: str | Path) -> List[AudienceSegment]:
    with open(path, "r", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    return [AudienceSegment(**row) for row in rows]

