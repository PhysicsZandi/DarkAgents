"""
Plot PTA benchmark spectra against NANOGrav violins.

Usage:
    conda run -n ptarcade python3 output/u1conformal/pta_benchmark_plot.py
"""
import sys
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

# Add backend directory
_backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "backend")
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

# Import model and spectrum
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fopt_model import compute_fopt
from pta_spectrum import get_spectrum

# Output directory
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

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


# ============================================================
# Main plotting
# ============================================================

def main():
    # Selected diverse best points
    best_points = [
        {"v": 0.4305827, "g_D": 0.5326, "label": "BP1 (v=0.43 GeV, g$_D$=0.53)"},
        {"v": 0.7937005, "g_D": 0.5800, "label": "BP2 (v=0.79 GeV, g$_D$=0.58)"},
        {"v": 1.172034,  "g_D": 0.5400, "label": "BP3 (v=1.17 GeV, g$_D$=0.54)"},
        {"v": 1.730708,  "g_D": 0.5400, "label": "BP4 (v=1.73 GeV, g$_D$=0.54)"},
    ]

    # Compute spectrum for each point on a dense frequency grid
    f_log = np.linspace(-9, -7, 200)
    f_Hz = 10.0 ** f_log

    # Colors for different points
    colors = ["#1f77b4", "#d62728", "#2ca02c", "#ff7f0e"]

    print("Computing spectra for benchmark points...")
    all_spectra = []
    for i, bp in enumerate(best_points):
        v = bp["v"]
        gD = bp["g_D"]

        fopt_result = compute_fopt(v, gD)
        if fopt_result["status"] != "viable":
            print(f"  Point {i+1}: FAILED ({fopt_result.get('failure_reason', '')})")
            all_spectra.append(None)
            continue

        alpha = fopt_result["alpha"]
        beta_H = fopt_result["beta_H"]
        Tr = fopt_result["Tr"]

        print(f"  Point {i+1}: alpha={alpha:.3e}, beta_H={beta_H:.3f}, Tr={Tr:.6e} GeV")

        try:
            h2Omega = get_spectrum(f_Hz, Tr, alpha, beta_H)
            all_spectra.append(h2Omega)
            bp.update({"alpha": alpha, "beta_H": beta_H, "Tr": Tr})
        except Exception as e:
            print(f"    Spectrum failed: {e}")
            all_spectra.append(None)

    # Create the plot
    fig, ax = plt.subplots(figsize=(8, 6))

    # Load and plot violins
    print("Loading PTA violins...")
    try:
        h2_omega_viol, freqs = load_violins()
        print(f"  Loaded {h2_omega_viol.shape[1]} violin frequency bins")
        plot_violins(ax, h2_omega_viol, N_f=14)
    except Exception as e:
        print(f"  Could not load violins: {e}")
        # Fallback: use tabulated violin windows from CSV
        violin_file = os.path.join(_backend_dir, "pta_violin_windows.csv")
        data = np.loadtxt(violin_file, delimiter=",", skiprows=1, usecols=(2, 3, 4))
        f_log_violin = data[:, 0]
        ymin = data[:, 1]
        ymax = data[:, 2]
        for i in range(len(f_log_violin)):
            ax.fill_betweenx([ymin[i], ymax[i]], f_log_violin[i] - 0.03, f_log_violin[i] + 0.03,
                             color="silver", alpha=0.8, edgecolor="gray")

    # Plot spectra
    for i, (bp, h2Omega) in enumerate(zip(best_points, all_spectra)):
        if h2Omega is None:
            continue
        log_h2Omega = np.log10(np.maximum(h2Omega, 1e-30))
        ax.plot(f_log, log_h2Omega, color=colors[i], linewidth=2,
                label=bp["label"])

    # Format axes
    ax.set_xlabel(r"$\log_{10}(f / \mathrm{Hz})$", fontsize=14)
    ax.set_ylabel(r"$\log_{10}(h^2 \Omega_{\mathrm{GW}})$", fontsize=14)
    ax.set_xlim(-9, -7)
    ax.tick_params(labelsize=12)
    ax.legend(fontsize=10, loc="lower left")

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "pta_benchmark_spectrum.pdf")
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    print(f"\nSaved benchmark spectrum plot to: {out_path}")
    plt.close()


if __name__ == "__main__":
    main()