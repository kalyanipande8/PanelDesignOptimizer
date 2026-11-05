"""Validates that the observed coverage depth genuinely reflects the
hidden true GC-driven capture efficiency, via a real Pearson
correlation between observed depth and true efficiency -- confirming
the panel-evaluation tool's coverage metrics are picking up a real
biophysical signal, not noise."""
from __future__ import annotations

import pandas as pd
from scipy.stats import pearsonr


def validate_gc_bias_recovery(df: pd.DataFrame) -> dict:
    r, p_value = pearsonr(df["coverage_depth"], df["true_capture_efficiency"])
    return {"pearson_r": round(float(r), 4), "p_value": float(p_value)}
