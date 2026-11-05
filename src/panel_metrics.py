"""Real capture-panel performance metrics computed purely from
observed coverage data: on-target rate, coverage uniformity
(fold-80 base penalty, the standard Picard-style uniformity metric),
sensitivity (fraction of targets meeting a minimum depth), and
enrichment efficiency."""
from __future__ import annotations

import numpy as np
import pandas as pd

MIN_ADEQUATE_DEPTH = 30


def on_target_rate(df: pd.DataFrame) -> float:
    on_target_total = df["on_target_reads"].sum()
    total = on_target_total + df.attrs.get("off_target_reads_total", 0)
    return round(100 * on_target_total / total, 3)


def fold80_uniformity(df: pd.DataFrame) -> float:
    """The standard Picard HsMetrics FOLD_80_BASE_PENALTY: the fold
    coverage increase needed so that 80% of targets reach the mean
    depth. A value near 1.0 means highly uniform coverage."""
    depths_sorted = np.sort(df["coverage_depth"].values)[::-1]
    cumulative = np.cumsum(depths_sorted)
    total = cumulative[-1]
    target_80 = 0.8 * total
    idx_80 = np.searchsorted(cumulative, target_80)
    mean_depth = df["coverage_depth"].mean()
    depth_at_80 = depths_sorted[min(idx_80, len(depths_sorted) - 1)]
    return round(float(mean_depth / depth_at_80), 3) if depth_at_80 > 0 else None


def sensitivity(df: pd.DataFrame, min_depth: int = MIN_ADEQUATE_DEPTH) -> float:
    return round(100 * (df["coverage_depth"] >= min_depth).mean(), 2)


def enrichment_efficiency(df: pd.DataFrame) -> float:
    """Mean on-target reads per bp of target length, normalized to a
    0-100 efficiency score relative to the theoretical maximum."""
    per_bp = df["on_target_reads"] / df["target_length_bp"]
    return round(100 * per_bp.mean() / per_bp.max(), 2)


def compute_all_metrics(df: pd.DataFrame) -> dict:
    return {
        "on_target_rate_pct": on_target_rate(df),
        "fold80_uniformity": fold80_uniformity(df),
        "sensitivity_pct": sensitivity(df),
        "enrichment_efficiency_pct": enrichment_efficiency(df),
        "mean_coverage_depth": round(float(df["coverage_depth"].mean()), 2),
        "n_targets": len(df),
    }
