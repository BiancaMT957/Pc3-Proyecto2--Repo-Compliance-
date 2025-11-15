from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Dict

Finding = Dict[str, str]


def compute_compliance_percent(metrics: Dict[str, int]) -> float:
    total = metrics.get("total", 0)
    if total == 0:
        return 100.0
    # Cumplimiento = findings NO HIGH / total
    non_high = total - metrics["HIGH"]
    return round((non_high / total) * 100, 2)


def compute_trend(prev: Dict[str, int], current: Dict[str, int]) -> str:
    prev_high = prev.get("HIGH", 0)
    curr_high = current.get("HIGH", 0)

    if curr_high < prev_high:
        return "mejora"
    if curr_high > prev_high:
        return "empeora"
    return "estable"


def export_metrics_json(metrics: Dict, out_path: Path) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"generated_at": datetime.now().isoformat(), **metrics}
    out_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return out_path
