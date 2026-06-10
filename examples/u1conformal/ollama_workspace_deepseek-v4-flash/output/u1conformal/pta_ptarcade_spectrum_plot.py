"""
Plot MAP-point spectrum from PTArcade against PTA violins.

Reads the MAP estimates from ptarcade_bayes.json, computes the GW spectrum,
and plots it against the NANOGrav violins.

Usage:
    conda run -n ptarcade python3 output/u1conformal/pta_ptarcade_spectrum_plot.py
"""
import sys
import os
import numpy as np
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

# Add backend and model directories
_output_dir = os.path.dirname(os.path.abspath(__file__))
_backend_dir = os.path.join(_output_dir, "..", "..", "backend")
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)
if _output_dir not in sys.path:
    sys.path.insert(0, _output_dir)

from fopt_model import compute_fopt
from pta_spectrum import get_spectrum

# ============================================================
# Violin plotting functions (copied verbatim from backend/plot_violins.py)
# ============================================================

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

    import natpy as nat
    import la_forge.core as co

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


def main():
    # Load Bayesian estimates
    bayes_file = os.path.join(_output_dir, "ptarcade_bayes.json")
    if not os.path.exists(bayes_file):
        print(f"ERROR: Bayesian estimates file not found: {bayes_file}")
        print("Has the PTArcade campaign completed and ptarcade_plot.py been run?")
        return

    with open(bayes_file, "r") as f:
        bayes_data = json.load(f)

    map_est = bayes_data.get("map_est", {})
    bayes_est = bayes_data.get("bayes_est", {})

    print(f"MAP estimates: {map_est}")
    print(f"Bayesian estimates: {bayes_est}")

    # Get parameters
    # Try both underscore and hyphen keys (PTArcade replaces _ with - in chain output)
    log10_v_map = map_est.get("log10_v", map_est.get("log10-v", None))
    gD_map = map_est.get("g_D", map_est.get("g-D", None))

    if log10_v_map is None or gD_map is None:
        print("ERROR: MAP estimate missing parameters. Available keys:", list(map_est.keys()))
        return

    v_map = 10.0 ** float(log10_v_map)
    gD_map = float(gD_map)

    print(f"\nMAP point: v = {v_map:.6e} GeV, g_D = {gD_map:.4f}")

    # Compute spectrum
    f_log = np.linspace(-9, -7, 200)
    f_Hz = 10.0 ** f_log

    fopt_result = compute_fopt(v_map, gD_map)
    if fopt_result["status"] != "viable":
        print(f"WARNING: MAP point is not viable: {fopt_result.get('failure_reason', '')}")
        return

    alpha = fopt_result["alpha"]
    beta_H = fopt_result["beta_H"]
    Tr = fopt_result["Tr"]

    print(f"FOPT: alpha={alpha:.3e}, beta_H={beta_H:.3f}, Tr={Tr:.6e} GeV")

    h2Omega = get_spectrum(f_Hz, Tr, alpha, beta_H)
    log_h2Omega = np.log10(np.maximum(h2Omega, 1e-30))

    # Compute f_peak
    fopt_f_peak = fopt_result.get("f_peak_est", np.nan)
    print(f"f_peak_est = {fopt_f_peak:.3e} Hz")

    # Create plot
    fig, ax = plt.subplots(figsize=(8, 6))

    # Load and plot violins
    print("Loading PTA violins...")
    try:
        h2_omega_viol, freqs = load_violins()
        print(f"  Loaded {h2_omega_viol.shape[1]} violin frequency bins")
        plot_violins(ax, h2_omega_viol, N_f=14)
    except Exception as e:
        print(f"  Could not load violins from core file: {e}")
        # Fallback: use CSV
        violin_file = os.path.join(_backend_dir, "pta_violin_windows.csv")
        data = np.loadtxt(violin_file, delimiter=",", skiprows=1, usecols=(2, 3, 4))
        f_log_violin = data[:, 0]
        ymin = data[:, 1]
        ymax = data[:, 2]
        for i in range(len(f_log_violin)):
            ax.fill_betweenx([ymin[i], ymax[i]], f_log_violin[i] - 0.03, f_log_violin[i] + 0.03,
                             color="silver", alpha=0.8, edgecolor="gray")

    # Plot MAP spectrum
    ax.plot(f_log, log_h2Omega, color="#d62728", linewidth=2.5,
            label=f"MAP: v={v_map:.3f} GeV, g$_D$={gD_map:.3f}")

    # Mark peak frequency
    if np.isfinite(fopt_f_peak) and fopt_f_peak > 0:
        f_peak_log = np.log10(fopt_f_peak)
        peak_idx = np.argmin(np.abs(f_log - f_peak_log))
        ax.plot(f_peak_log, log_h2Omega[peak_idx], "v", color="#d62728", markersize=8,
                label=f"$f_{{\\mathrm{{peak}}}}$ = {fopt_f_peak:.2e} Hz")

    # Format axes
    ax.set_xlabel(r"$\log_{10}(f / \mathrm{Hz})$", fontsize=14)
    ax.set_ylabel(r"$\log_{10}(h^2 \Omega_{\mathrm{GW}})$", fontsize=14)
    ax.set_xlim(-9, -7)
    ax.tick_params(labelsize=12)
    ax.legend(fontsize=10, loc="lower left")

    # Add title
    ax.set_title("PTArcade MAP Point Spectrum vs PTA Violins", fontsize=12)

    plt.tight_layout()
    out_path = os.path.join(_output_dir, "pta_ptarcade_spectrum.pdf")
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    print(f"\nSaved PTArcade spectrum plot to: {out_path}")
    plt.close()


if __name__ == "__main__":
    main()