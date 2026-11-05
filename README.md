# PanelDesignOptimizer

A tool evaluating custom NGS capture panel designs across 520
simulated genomic targets for on-target rate and coverage uniformity,
with automated performance reporting and visualizations.

> Built a tool evaluating custom capture panel designs across 520
> simulated genomic targets for on-target rate (75.0%) and uniformity
> (FOLD_80 1.027, near-ideal). Automated performance reporting with
> visualizations for sensitivity (100%), coverage depth, and
> enrichment efficiency (93.6%); recovered the panel's true GC-content
> capture bias with r=0.997.

## What's real vs. synthetic — read this first

**Real:** `src/panel_metrics.py` computes real, standard capture-panel
QC metrics purely from observed coverage data: on-target rate, the
Picard-style FOLD_80_BASE_PENALTY uniformity metric, sensitivity (% of
targets at adequate depth), and enrichment efficiency.
`src/visualizations.py` generates 3 real matplotlib plots (coverage
distribution, GC-bias scatter, uniformity curve) from the actual data.
`src/validation.py` computes a real Pearson correlation between
observed coverage and the simulation's hidden true GC-driven capture
efficiency — because that correlation is computed independently
(the metrics never see `true_capture_efficiency` directly), the
r=0.997 recovery is a real, measured result confirming the tool
correctly picks up the real GC-bias signal from coverage data alone.

**Synthetic:** there is no real sequencing run or capture panel in
this environment. `src/simulate_capture_panel.py` generates 520
genomic targets with GC content and target length, and simulates
on-target read counts using the real, well-documented hybrid-capture
GC-bias effect (capture efficiency drops away from ~50% GC).

## Results (real, from `run_all.py`)

```
520 targets

On-target rate:         75.003%
Coverage uniformity (FOLD_80): 1.027 (near-ideal; 1.0 = perfectly uniform)
Sensitivity (>=30x):     100.0%
Enrichment efficiency:   93.64%
Mean coverage depth:     11,244x

GC-bias recovery: Pearson r = 0.9966 (p ~ 0) between observed
  coverage and the hidden true GC-driven capture efficiency
```

`tests/test_pipeline.py` (5 tests, all passing) checks target count
>=500, all metrics fall in valid ranges, coverage correlates with true
GC efficiency, all 3 plots are generated as real files, and targets
with extreme GC content show genuinely lower coverage than moderate-GC
targets.

## Usage

```bash
pip install -r requirements.txt
python3 run_all.py
python3 -m pytest tests/ -v
```

## Project structure

```
src/
  simulate_capture_panel.py   # 520-target simulation with real GC-bias effect
  panel_metrics.py            # on-target rate, uniformity, sensitivity, enrichment
  validation.py                # GC-bias recovery check
  visualizations.py            # 3 real matplotlib performance plots
run_all.py
tests/test_pipeline.py
```

## Tech stack

Python 3.11, scipy (Pearson correlation), matplotlib, pandas, numpy,
pytest.

## Limitations

- No real sequencing run or capture panel is used.
- The GC-bias model is a single quadratic penalty around 50% GC; real
  hybrid-capture chemistries have more complex, probe-specific bias
  profiles.
