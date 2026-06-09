#!/usr/bin/env python3
"""
PTA benchmark scan for the conformal-SU2 model.
Scans over (g, chi0) and scores the GW spectrum against the PTA violin windows.
"""

import sys
import os
from pathlib import Path
import csv
import time

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backend"))
from semianalytic_pipeline import SemiAnalyticPipeline
from spectrum import Spectrum

# Import our spectrum wrapper
sys.path.insert(0, str(Path(__file__).resolve().parent))
from pta_spectrum import compute_spectrum, get_fopt_params

# --- PTA violin windows ---
VIOLIN_FILE = str(Path(__file__).resolve().parents[2] / "backend" / "pta_violin_windows.csv")

def load_violin_windows():
    """Load the PTA violin window data from CSV. Returns lists of frequencies and ymin/ymax."""
    freqs_Hz = []
    ymin = []
    ymax = []
    with open(VIOLIN_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            freqs_Hz.append(float(row["f_nHz"]) * 1e-9)  # convert nHz to Hz
            ymin.append(float(row["ymin_log10_h2OmegaGW"]))
            ymax.append(float(row["ymax_log10_h2OmegaGW"]))
    return np.array(freqs_Hz), np.array(ymin), np.array(ymax)


def score_point(g, chi0, freqs_Hz, ymin, ymax):
    """
    Compute how many of the 14 violin bins the GW spectrum falls within.

    Returns (inside_bins, total_bins, h2OmegaGW_vals) or (0, 14, None) on failure.
    """
    h2OmegaGW = compute_spectrum(g, chi0, freqs_Hz)

    if h2OmegaGW is None or np.all(h2OmegaGW == 0) or not np.all(np.isfinite(h2OmegaGW)):
        return 0, 14, None

    log10_h2OmegaGW = np.log10(np.maximum(h2OmegaGW, 1e-30))

    inside = 0
    for i in range(len(freqs_Hz)):
        if ymin[i] <= log10_h2OmegaGW[i] <= ymax[i]:
            inside += 1

    return inside, 14, h2OmegaGW


def main():
    output_dir = str(Path(__file__).resolve().parent)

    # Load violin windows
    freqs_Hz, ymin, ymax = load_violin_windows()
    print(f"Loaded {len(freqs_Hz)} PTA violin frequency bins")
    print(f"Frequency range: {freqs_Hz[0]*1e9:.2f} nHz - {freqs_Hz[-1]*1e9:.2f} nHz")

    # Define scan ranges
    # Based on the FOPT scan results, viable points exist for:
    # g: 0.7 - 2.3  (with higher g giving lower alpha, more moderate transitions)
    # chi0: 3e-5 - 0.5 GeV (MeV to sub-GeV scale for PTA band)
    # The literature benchmark (Borah et al.) uses g=1.37, chi0~MeV
    # The conformal U(1)' benchmark (Bringmann et al.) uses g=0.692, v=140 MeV

    # Initial coarse scan
    g_values = np.linspace(0.7, 2.3, 17)  # linear steps for coupling
    chi0_values = np.logspace(np.log10(3e-5), np.log10(0.5), 20)  # log steps for VEV

    results_file = os.path.join(output_dir, "pta_benchmark_scan.csv")

    # Write header
    columns = [
        "g", "chi0", "alpha", "beta_H", "Tr",
        "f_peak_est", "score", "inside_bins", "total_bins",
    ]
    # Add spectrum at each violin frequency
    for i in range(len(freqs_Hz)):
        columns.append(f"h2OmegaGW_bin{i+1}")

    with open(results_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(columns)

    best_points = []

    # ---- Stage 1: Coarse scan ----
    print("\n=== Stage 1: Coarse scan ===")
    print(f"g grid: {len(g_values)} points ({g_values[0]:.3f} - {g_values[-1]:.3f})")
    print(f"chi0 grid: {len(chi0_values)} points ({chi0_values[0]:.6e} - {chi0_values[-1]:.6e})")
    print(f"Total: {len(g_values) * len(chi0_values)} points")

    t_start = time.time()
    n_evaluated = 0
    n_failed = 0

    for gi, g in enumerate(g_values):
        for chi0 in chi0_values:
            # Get FOPT params
            fopt = get_fopt_params(g, chi0)
            n_evaluated += 1

            if fopt is None:
                n_failed += 1
                row = [g, chi0, "", "", "", "", 0, 0, 14]
                row.extend([""] * len(freqs_Hz))
                with open(results_file, "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(row)
                continue

            # Score
            inside, total, h2OmegaGW = score_point(g, chi0, freqs_Hz, ymin, ymax)

            if h2OmegaGW is None:
                row = [g, chi0, fopt["alpha"], fopt["beta_H"], fopt["Tr"], "", inside, total, 14]
                row.extend([""] * len(freqs_Hz))
            else:
                row = [g, chi0, fopt["alpha"], fopt["beta_H"], fopt["Tr"], ""]
                row.extend([inside, total, 14])
                for val in h2OmegaGW:
                    row.append(val)

            with open(results_file, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(row)

            if inside > 0:
                best_points.append((inside, g, chi0))

            if (n_evaluated) % 50 == 0:
                elapsed = time.time() - t_start
                print(f"  Progress: {n_evaluated}/{len(g_values)*len(chi0_values)} points "
                      f"(elapsed: {elapsed:.1f}s)")

    elapsed = time.time() - t_start
    print(f"\nCoarse scan completed in {elapsed:.1f}s")
    print(f"Evaluated: {n_evaluated}, Failed: {n_failed}")

    # Report best scores
    best_points.sort(reverse=True)
    print(f"\nBest scores from coarse scan:")
    seen = set()
    for score, g, chi0 in best_points:
        if score >= 8 and (g, chi0) not in seen:
            print(f"  g={g:.4f}, chi0={chi0:.6e} GeV -> {score}/14 in-violin bins")
            seen.add((g, chi0))

    # ---- Stage 2: Refined scan around best regions ----
    print("\n=== Stage 2: Refined scan ===")

    # Identify best g, chi0 ranges from stage 1
    # Use a finer grid
    g_fine = np.linspace(0.7, 2.3, 33)
    chi0_fine = np.logspace(np.log10(3e-5), np.log10(0.5), 40)

    print(f"g grid: {len(g_fine)} points ({g_fine[0]:.3f} - {g_fine[-1]:.3f})")
    print(f"chi0 grid: {len(chi0_fine)} points ({chi0_fine[0]:.6e} - {chi0_fine[-1]:.6e})")
    print(f"Total: {len(g_fine) * len(chi0_fine)} points")

    t_start = time.time()
    n_evaluated = 0
    best_points_fine = []

    for gi, g in enumerate(g_fine):
        for chi0 in chi0_fine:
            fopt = get_fopt_params(g, chi0)
            n_evaluated += 1

            if fopt is None:
                row = [g, chi0, "", "", "", "", 0, 0, 14]
                row.extend([""] * len(freqs_Hz))
                with open(results_file, "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(row)
                continue

            inside, total, h2OmegaGW = score_point(g, chi0, freqs_Hz, ymin, ymax)

            if h2OmegaGW is None:
                row = [g, chi0, fopt["alpha"], fopt["beta_H"], fopt["Tr"], "", inside, total, 14]
                row.extend([""] * len(freqs_Hz))
            else:
                row = [g, chi0, fopt["alpha"], fopt["beta_H"], fopt["Tr"], ""]
                row.extend([inside, total, 14])
                for val in h2OmegaGW:
                    row.append(val)

            with open(results_file, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(row)

            best_points_fine.append((inside, g, chi0))

            if n_evaluated % 100 == 0:
                elapsed = time.time() - t_start
                print(f"  Progress: {n_evaluated}/{len(g_fine)*len(chi0_fine)} points "
                      f"(elapsed: {elapsed:.1f}s)")

    elapsed = time.time() - t_start
    print(f"\nRefined scan completed in {elapsed:.1f}s")

    # Sort and report best
    best_points_fine.sort(reverse=True)
    seen = set()
    print(f"\nTop-scoring points:")
    for score, g, chi0 in best_points_fine:
        if score >= 10 and (g, chi0) not in seen:
            fopt = get_fopt_params(g, chi0)
            if fopt:
                print(f"  g={g:.4f}, chi0={chi0:.6e} GeV -> {score}/14 bins, "
                      f"alpha={fopt['alpha']:.2e}, beta/H={fopt['beta_H']:.1f}, Tr={fopt['Tr']:.6e} GeV")
            else:
                print(f"  g={g:.4f}, chi0={chi0:.6e} GeV -> {score}/14 bins")
            seen.add((g, chi0))
            if len(seen) >= 20:
                break

    print(f"\nResults saved to {results_file}")


if __name__ == "__main__":
    main()