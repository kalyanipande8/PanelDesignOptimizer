import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.simulate_capture_panel import simulate
from src.panel_metrics import compute_all_metrics
from src.validation import validate_gc_bias_recovery
from src.visualizations import generate_all_plots


def test_panel_has_at_least_500_targets():
    df = simulate()
    assert len(df) >= 500


def test_metrics_are_in_valid_ranges():
    df = simulate()
    metrics = compute_all_metrics(df)
    assert 0 <= metrics["on_target_rate_pct"] <= 100
    assert 0 <= metrics["sensitivity_pct"] <= 100
    assert metrics["fold80_uniformity"] >= 1.0


def test_coverage_correlates_with_true_gc_efficiency():
    df = simulate()
    validation = validate_gc_bias_recovery(df)
    assert validation["pearson_r"] > 0.3


def test_plots_are_generated(tmp_path):
    df = simulate()
    paths = generate_all_plots(df, out_dir=str(tmp_path))
    assert len(paths) == 3
    for p in paths:
        assert os.path.exists(p)


def test_extreme_gc_targets_have_lower_coverage():
    df = simulate()
    extreme_gc = df[(df["gc_content"] < 0.3) | (df["gc_content"] > 0.7)]
    moderate_gc = df[(df["gc_content"] >= 0.45) & (df["gc_content"] <= 0.55)]
    assert extreme_gc["coverage_depth"].mean() < moderate_gc["coverage_depth"].mean()
