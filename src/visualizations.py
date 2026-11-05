"""Real matplotlib visualizations of panel performance: coverage
depth distribution, GC-content vs. coverage bias, and a per-target
Lorenz-style uniformity curve -- the automated performance reporting
the resume bullet describes."""
from __future__ import annotations

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_coverage_distribution(df: pd.DataFrame, out_path: str):
    fig, ax = plt.subplots()
    ax.hist(df["coverage_depth"], bins=40)
    ax.set_xlabel("Coverage depth")
    ax.set_ylabel("Number of targets")
    ax.set_title("Coverage depth distribution")
    fig.savefig(out_path, dpi=80)
    plt.close(fig)


def plot_gc_bias(df: pd.DataFrame, out_path: str):
    fig, ax = plt.subplots()
    ax.scatter(df["gc_content"], df["coverage_depth"], s=8, alpha=0.5)
    ax.set_xlabel("GC content")
    ax.set_ylabel("Coverage depth")
    ax.set_title("GC-content bias in capture efficiency")
    fig.savefig(out_path, dpi=80)
    plt.close(fig)


def plot_uniformity_curve(df: pd.DataFrame, out_path: str):
    depths_sorted = np.sort(df["coverage_depth"].values)[::-1]
    cumulative_pct = 100 * np.cumsum(depths_sorted) / depths_sorted.sum()
    target_pct = 100 * np.arange(1, len(depths_sorted) + 1) / len(depths_sorted)

    fig, ax = plt.subplots()
    ax.plot(target_pct, cumulative_pct)
    ax.plot([0, 100], [0, 100], linestyle="--", color="gray")
    ax.set_xlabel("% of targets (ranked by coverage)")
    ax.set_ylabel("Cumulative % of reads")
    ax.set_title("Coverage uniformity curve")
    fig.savefig(out_path, dpi=80)
    plt.close(fig)


def generate_all_plots(df: pd.DataFrame, out_dir: str = "output/plots") -> list:
    os.makedirs(out_dir, exist_ok=True)
    paths = [os.path.join(out_dir, "coverage_distribution.png"),
             os.path.join(out_dir, "gc_bias.png"),
             os.path.join(out_dir, "uniformity_curve.png")]

    plot_coverage_distribution(df, paths[0])
    plot_gc_bias(df, paths[1])
    plot_uniformity_curve(df, paths[2])
    return paths
