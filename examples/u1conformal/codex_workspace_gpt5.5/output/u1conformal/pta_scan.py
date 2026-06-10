"""Benchmark PTA scan for the u1conformal FOPT model."""

from __future__ import annotations

import argparse
import csv
import itertools
import json
import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import natpy as nat
import la_forge.core as co
import numpy as np


HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parents[1]
BACKEND_DIR = PROJECT_ROOT / "backend"
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from pta_spectrum import SELECTED_TEMPLATE, evaluate_fopt, h2omega_from_fopt  # noqa: E402


WINDOWS_FILE = BACKEND_DIR / "pta_violin_windows.csv"
FOPT_CSV = HERE / "fopt_benchmarks.csv"
SCAN_CSV = HERE / "pta_benchmark_scan.csv"
SCAN_META = HERE / "pta_benchmark_scan_meta.json"
PLOT_FILE = HERE / "pta_benchmark_spectrum.pdf"
TOTAL_BINS = 14
TEMPLATES = ("dbf", "bf", "higgsless")


def load_violins(correlations=False):
    def find_core(filename: str) -> Path:
        repo_root = Path(__file__).resolve().parents[2]
        matches = list(repo_root.rglob(filename))
        if matches:
            return matches[0]
        matches = list(Path.cwd().rglob(filename))
        if matches:
            return matches[0]
        return None

    filename = "30fCP_30fiRN_3A.core" if correlations else "30fCP_30fiRN_2A.core"
    corepath = find_core(filename)
    label_correlations = correlations
    if corepath is None and not correlations:
        corepath = find_core("30fCP_30fiRN_3A.core")
        label_correlations = True
    if corepath is None:
        raise FileNotFoundError(f"Could not find PTA core file: {filename}")

    c0 = co.Core(corepath=str(corepath))
    if label_correlations:
        labels = [p for p in c0.params if "gw_hd" in p]
    else:
        labels = [p for p in c0.params if "rho" in p]
    if not labels:
        raise ValueError(f"No PTA violin parameters found in {corepath}")

    freqs = c0.rn_freqs  # array of frequencies

    # load free spec samples
    viol = c0(labels)  # this is now a numpy array of Nsamples x Nfreq

    dfreq = np.diff(np.concatenate((np.array([0]), freqs[::1])))

    H_0byh = 100 * nat.convert(nat.km * nat.s**-1 * nat.Mpc**-1, nat.Hz)  # H_0/h in Hz
    h2_omega_viol = np.log10(
        24
        * np.pi**4
        * (10**viol) ** 2
        * 1
        / np.repeat(dfreq, 1)
        * freqs**5
        / (3 * H_0byh**2)
    )
    return h2_omega_viol, freqs


def plot_violins(ax, h2_omega_viol, N_f=14, border="silver"):
    Tspan = 505861299.1401644
    n_freq = min(N_f, h2_omega_viol.shape[1])
    freqs = np.arange(1, n_freq + 1) / Tspan

    v1 = ax.violinplot(
        h2_omega_viol[:, :n_freq],
        positions=np.log10(freqs),
        widths=0.05,
        showextrema=False,
    )

    for pc in v1["bodies"]:
        pc.set_facecolor("silver")
        pc.set_edgecolor(border)
        pc.set_linestyle("solid")

    return


def read_windows() -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    with WINDOWS_FILE.open() as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            rows.append(
                {
                    "bin_i": int(row["bin_i"]),
                    "f_Hz": 10.0 ** float(row["log10_f_Hz"]),
                    "log10_f_Hz": float(row["log10_f_Hz"]),
                    "ymin": float(row["ymin_log10_h2OmegaGW"]),
                    "ymax": float(row["ymax_log10_h2OmegaGW"]),
                }
            )
    return rows


def read_anchor_ranges() -> dict[str, float]:
    viable = []
    with FOPT_CSV.open() as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            if row.get("status") != "viable":
                continue
            try:
                f_peak = float(row["f_peak_est"])
                v = float(row["v"])
                g = float(row["g_D"])
            except Exception:
                continue
            if 1.0e-9 <= f_peak <= 1.0e-7:
                viable.append((v, g, f_peak))
    if not viable:
        return {"v_min": 0.003, "v_max": 3.0, "g_min": 0.45, "g_max": 1.05}
    vs = [x[0] for x in viable]
    gs = [x[1] for x in viable]
    return {
        "v_min": max(0.003, min(vs) / 3.0),
        "v_max": min(3.0, max(vs) * 3.0),
        "g_min": max(0.42, min(gs) - 0.12),
        "g_max": min(1.05, max(gs) + 0.12),
    }


def log_distance_to_window(y: float, ymin: float, ymax: float) -> float:
    if not math.isfinite(y):
        return 99.0
    if ymin <= y <= ymax:
        return 0.0
    if y < ymin:
        return ymin - y
    return y - ymax


def score_point(point: dict[str, object], windows: list[dict[str, float]], template: str) -> dict[str, object]:
    freqs = np.array([w["f_Hz"] for w in windows], dtype=float)
    omega = h2omega_from_fopt(freqs, point, template=template)
    log_omega = np.full_like(omega, -np.inf, dtype=float)
    positive = omega > 0.0
    log_omega[positive] = np.log10(omega[positive])
    distances = [
        log_distance_to_window(float(y), w["ymin"], w["ymax"])
        for y, w in zip(log_omega, windows)
    ]
    inside = [
        int(math.isfinite(float(y)) and w["ymin"] <= float(y) <= w["ymax"])
        for y, w in zip(log_omega, windows)
    ]
    score = int(sum(inside))
    penalty = float(sum(d * d for d in distances))
    if np.any(omega > 0.0):
        fine_f = np.logspace(windows[0]["log10_f_Hz"], windows[-1]["log10_f_Hz"], 256)
        fine_omega = h2omega_from_fopt(fine_f, point, template=template)
        peak_idx = int(np.nanargmax(fine_omega)) if np.any(np.isfinite(fine_omega)) else 0
        peak_frequency = float(fine_f[peak_idx])
        peak_h2omega = float(fine_omega[peak_idx])
    else:
        peak_frequency = None
        peak_h2omega = None
    return {
        "inside_bins": score,
        "total_bins": len(windows),
        "distance_penalty": penalty,
        "log10_h2omega_bins": [float(x) if math.isfinite(float(x)) else None for x in log_omega],
        "h2omega_bins": [float(x) for x in omega],
        "peak_frequency_Hz": peak_frequency,
        "peak_h2OmegaGW": peak_h2omega,
    }


def evaluate_grid(
    v_values: np.ndarray,
    g_values: np.ndarray,
    phase: str,
    windows: list[dict[str, float]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for idx, (v, g) in enumerate(itertools.product(v_values, g_values), start=1):
        point = evaluate_fopt(float(v), float(g))
        for template in TEMPLATES:
            scoring = score_point(point, windows, template)
            row = {
                "scan_pass": phase,
                "template": template,
                "v": float(v),
                "g_D": float(g),
                **point,
                **scoring,
            }
            rows.append(row)
        if idx % 20 == 0:
            print(f"{phase}: evaluated {idx}/{len(v_values) * len(g_values)} model points", flush=True)
    return rows


def row_rank_key(row: dict[str, object]) -> tuple[float, float]:
    return (-float(row["inside_bins"]), float(row["distance_penalty"]))


def touches_boundary(row: dict[str, object], ranges: dict[str, float]) -> list[str]:
    touched = []
    v = float(row["v"])
    g = float(row["g_D"])
    if math.isclose(v, ranges["v_min"]) or math.isclose(v, ranges["v_max"]):
        touched.append("v")
    if math.isclose(g, ranges["g_min"]) or math.isclose(g, ranges["g_max"]):
        touched.append("g_D")
    return touched


def choose_diverse(rows: list[dict[str, object]], max_points: int = 4) -> list[dict[str, object]]:
    selected: list[dict[str, object]] = []
    candidates = sorted(rows, key=row_rank_key)
    if not candidates:
        return selected
    selected.append(candidates[0])
    while len(selected) < max_points and len(selected) < len(candidates):
        best = None
        best_dist = -1.0
        for row in candidates:
            if row in selected:
                continue
            d = min(
                (math.log10(float(row["v"])) - math.log10(float(sel["v"]))) ** 2
                + (float(row["g_D"]) - float(sel["g_D"])) ** 2
                for sel in selected
            )
            if d > best_dist:
                best = row
                best_dist = d
        if best is None:
            break
        selected.append(best)
    return selected


def write_csv(rows: list[dict[str, object]], windows: list[dict[str, float]]) -> None:
    fieldnames = [
        "scan_pass",
        "template",
        "v",
        "g_D",
        "status",
        "failure_reason",
        "alpha",
        "beta_H",
        "Tn",
        "Tp",
        "Treh",
        "g_star",
        "f_peak_est",
        "inside_bins",
        "total_bins",
        "distance_penalty",
        "peak_frequency_Hz",
        "peak_h2OmegaGW",
    ]
    for w in windows:
        fieldnames.append(f"h2OmegaGW_bin_{w['bin_i']:02d}")
        fieldnames.append(f"log10_h2OmegaGW_bin_{w['bin_i']:02d}")
    with SCAN_CSV.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            out = {k: row.get(k) for k in fieldnames}
            for i, w in enumerate(windows):
                out[f"h2OmegaGW_bin_{w['bin_i']:02d}"] = row["h2omega_bins"][i]
                out[f"log10_h2OmegaGW_bin_{w['bin_i']:02d}"] = row["log10_h2omega_bins"][i]
            writer.writerow(out)


def plot_best(selected: list[dict[str, object]], windows: list[dict[str, float]]) -> None:
    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    h2_omega_viol, _ = load_violins(correlations=False)
    plot_violins(ax, h2_omega_viol, N_f=TOTAL_BINS)
    fine_f = np.logspace(windows[0]["log10_f_Hz"] - 0.08, windows[-1]["log10_f_Hz"] + 0.08, 400)
    colors = ["#1b9e77", "#d95f02", "#7570b3", "#e7298a"]
    for idx, row in enumerate(selected):
        point = evaluate_fopt(float(row["v"]), float(row["g_D"]))
        omega = h2omega_from_fopt(fine_f, point, template=str(row["template"]))
        mask = omega > 0.0
        label = (
            f"{row['template']} #{idx + 1}: "
            f"v={float(row['v']):.3g} GeV, g_D={float(row['g_D']):.3f}, "
            f"{int(row['inside_bins'])}/{int(row['total_bins'])}"
        )
        ax.plot(np.log10(fine_f[mask]), np.log10(omega[mask]), lw=2.0, color=colors[idx % len(colors)], label=label)
    ax.set_xlabel(r"$\log_{10}(f/{\rm Hz})$")
    ax.set_ylabel(r"$\log_{10}(h^2\Omega_{\rm GW})$")
    ax.set_xlim(windows[0]["log10_f_Hz"] - 0.1, windows[-1]["log10_f_Hz"] + 0.1)
    ax.set_ylim(-12.5, -5.2)
    ax.grid(True, alpha=0.25)
    ax.legend(fontsize=7.5, frameon=False, loc="lower right")
    fig.tight_layout()
    fig.savefig(PLOT_FILE)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true", help="smaller scan for smoke testing")
    args = parser.parse_args()
    windows = read_windows()
    ranges = read_anchor_ranges()
    if args.quick:
        v_values = np.geomspace(ranges["v_min"], ranges["v_max"], 5)
        g_values = np.linspace(ranges["g_min"], ranges["g_max"], 5)
    else:
        v_values = np.geomspace(ranges["v_min"], ranges["v_max"], 11)
        g_values = np.linspace(ranges["g_min"], ranges["g_max"], 11)
    rows = evaluate_grid(v_values, g_values, "anchor_wide", windows)
    selected_template_rows = [r for r in rows if r["template"] == SELECTED_TEMPLATE]
    best = sorted(selected_template_rows, key=row_rank_key)[0]
    expansions = []
    touched = touches_boundary(best, ranges)
    if touched and not args.quick:
        old = dict(ranges)
        if "v" in touched:
            ranges["v_min"] = max(1.0e-4, ranges["v_min"] / 3.0)
            ranges["v_max"] = min(10.0, ranges["v_max"] * 3.0)
        if "g_D" in touched:
            ranges["g_min"] = max(0.2, ranges["g_min"] - 0.15)
            ranges["g_max"] = min(1.2, ranges["g_max"] + 0.15)
        expansions.append({"reason": "best point touched scan boundary", "touched": touched, "old": old, "new": dict(ranges)})
        v_values = np.geomspace(ranges["v_min"], ranges["v_max"], 13)
        g_values = np.linspace(ranges["g_min"], ranges["g_max"], 13)
        rows.extend(evaluate_grid(v_values, g_values, "boundary_expanded", windows))
    selected_template_rows = [r for r in rows if r["template"] == SELECTED_TEMPLATE]
    top = sorted(selected_template_rows, key=row_rank_key)[:12]
    if top and not args.quick:
        v_center = float(top[0]["v"])
        g_center = float(top[0]["g_D"])
        v_min = max(1.0e-4, v_center / 2.5)
        v_max = min(10.0, v_center * 2.5)
        g_min = max(0.2, g_center - 0.12)
        g_max = min(1.2, g_center + 0.12)
        rows.extend(
            evaluate_grid(
                np.geomspace(v_min, v_max, 15),
                np.linspace(g_min, g_max, 15),
                "best_refine",
                windows,
            )
        )
    selected_template_rows = [r for r in rows if r["template"] == SELECTED_TEMPLATE]
    selected_template_rows = sorted(selected_template_rows, key=row_rank_key)
    diverse = choose_diverse(selected_template_rows[: max(12, min(50, len(selected_template_rows)))])
    write_csv(rows, windows)
    plot_best(diverse, windows)
    meta = {
        "selected_template": SELECTED_TEMPLATE,
        "windows_file": str(WINDOWS_FILE),
        "scan_csv": str(SCAN_CSV),
        "plot_file": str(PLOT_FILE),
        "boundary_expansions": expansions,
        "total_rows": len(rows),
        "total_model_points": len({(round(float(r["v"]), 14), round(float(r["g_D"]), 14)) for r in rows}),
        "selected_best_rows": [
            {
                "rank": i + 1,
                "template": r["template"],
                "v": r["v"],
                "g_D": r["g_D"],
                "alpha": r.get("alpha"),
                "beta_H": r.get("beta_H"),
                "Treh": r.get("Treh"),
                "inside_bins": r["inside_bins"],
                "total_bins": r["total_bins"],
                "distance_penalty": r["distance_penalty"],
                "peak_frequency_Hz": r["peak_frequency_Hz"],
                "peak_h2OmegaGW": r["peak_h2OmegaGW"],
            }
            for i, r in enumerate(diverse)
        ],
        "template_comparison": {
            template: {
                "best_inside_bins": int(max((r["inside_bins"] for r in rows if r["template"] == template), default=0)),
                "best_distance_penalty": float(min((r["distance_penalty"] for r in rows if r["template"] == template), default=float("inf"))),
            }
            for template in TEMPLATES
        },
    }
    SCAN_META.write_text(json.dumps(meta, indent=2, sort_keys=True))
    print(json.dumps(meta, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
