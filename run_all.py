import json
import os

from src.simulate_capture_panel import simulate
from src.panel_metrics import compute_all_metrics
from src.validation import validate_gc_bias_recovery
from src.visualizations import generate_all_plots


def main():
    df = simulate()
    metrics = compute_all_metrics(df)
    gc_validation = validate_gc_bias_recovery(df)
    plot_paths = generate_all_plots(df)

    summary = {"metrics": metrics, "gc_bias_validation": gc_validation, "n_plots_generated": len(plot_paths)}

    os.makedirs("results", exist_ok=True)
    with open("results/summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
