"""Simulate a custom capture panel of 520 genomic targets with real
GC-content-driven capture efficiency (a known real NGS hybrid-capture
bias: both very low and very high GC content reduce capture
efficiency) -- the ground truth a panel-evaluation tool must recover
from observed coverage depth alone."""
from __future__ import annotations

import numpy as np
import pandas as pd

N_TARGETS = 520
SEED = 773
TOTAL_READS = 20_000_000


def simulate(n_targets: int = N_TARGETS, total_reads: int = TOTAL_READS, seed: int = SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    gc_content = np.clip(rng.normal(0.5, 0.12, n_targets), 0.15, 0.85)
    target_length = rng.integers(100, 400, n_targets)

    # true capture efficiency: optimal near 50% GC, penalized by squared
    # deviation -- the real, known hybrid-capture GC-bias effect.
    true_efficiency = np.clip(1.0 - 4.0 * (gc_content - 0.5) ** 2, 0.05, 1.0)

    relative_capture = true_efficiency * target_length
    read_share = relative_capture / relative_capture.sum()
    on_target_reads = rng.poisson(read_share * total_reads * 0.75)
    off_target_reads_total = int(total_reads * 0.25)

    coverage_depth = on_target_reads * 100 / target_length  # reads -> approximate depth

    df = pd.DataFrame({
        "target_id": [f"TGT-{i:04d}" for i in range(n_targets)],
        "gc_content": np.round(gc_content, 3), "target_length_bp": target_length,
        "on_target_reads": on_target_reads, "coverage_depth": np.round(coverage_depth, 2),
        "true_capture_efficiency": np.round(true_efficiency, 4),
    })
    df.attrs["off_target_reads_total"] = off_target_reads_total
    df.attrs["total_reads"] = total_reads
    return df


if __name__ == "__main__":
    df = simulate()
    print(df.shape, df["coverage_depth"].describe())
