"""
pta_benchmark_plot.py -- Plot benchmark spectra against PTA violins.

This script copies the load_violins and plot_violins functions verbatim from
backend/plot_violins.py and overlays the GW spectrum curves.
"""

import sys
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

# Add backend to path
_backend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), "backend")
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

# Add output dir to path
_output_dir = os.path.dirname(os.path.abspath(__file__))
if _output_dir not in sys.path:
    sys.path.insert(0, _output_dir)

# ============================================================
# Verbatim copy of load_violins and plot_violins from backend/plot_violins.py
# ============================================================
import natpy as nat
import la_forge.core as co


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


# ============================================================
# Spectrum computation
# ============================================================
from fopt_model import compute_fopt, is_viable
from pta_spectrum import get_spectrum


def compute_spectrum_curve(g_D, y_psi, v, f, template="dbf"):
    """Compute GW spectrum for a given point."""
    fopt_result = compute_fopt(g_D, y_psi, v)
    if not is_viable(fopt_result):
        return None, None
    h2OmegaGW = get_spectrum(f, fopt_result["Treh"], fopt_result["alpha"],
                              fopt_result["beta_H"], template=template)
    return fopt_result, h2OmegaGW


def main():
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_pdf = os.path.join(output_dir, "pta_benchmark_spectrum.pdf")

    # Load PTA violins
    print("Loading PTA violins...")
    h2_omega_viol, freqs = load_violins()

    # Define benchmark points (maximally diverse 14/14 scorers)
    benchmark_points = [
        {
            'label': 'BP-A',
            'g_D': 0.6182,
            'y_psi': 0.2609,
            'v': 0.432876,
            'color': '#E41A1C',
            'linestyle': '-',
        },
        {
            'label': 'BP-B',
            'g_D': 0.6182,
            'y_psi': 0.5118,
            'v': 0.432876,
            'color': '#377EB8',
            'linestyle': '--',
        },
        {
            'label': 'BP-C',
            'g_D': 0.5429,
            'y_psi': 0.0500,
            'v': 0.464159,
            'color': '#4DAF4A',
            'linestyle': '-.',
        },
        {
            'label': 'BP-D',
            'g_D': 0.6182,
            'y_psi': 0.2609,
            'v': 1.000000,
            'color': '#984EA3',
            'linestyle': ':',
        },
    ]

    # Frequency array for spectrum evaluation (slightly expanded around PTA band)
    f = np.logspace(-9.5, -6.5, 1000)

    # Create plot
    fig, ax = plt.subplots(figsize=(8, 6))

    # Plot violins
    plot_violins(ax, h2_omega_viol, N_f=14)

    # Plot spectrum curves
    for bp in benchmark_points:
        print(f"Computing spectrum for {bp['label']}...")
        fopt_result, h2OmegaGW = compute_spectrum_curve(
            bp['g_D'], bp['y_psi'], bp['v'], f, template="dbf"
        )

        if h2OmegaGW is not None:
            log10_f = np.log10(f)
            log10_h2OmegaGW = np.log10(np.maximum(h2OmegaGW, 1e-30))

            # Create label with parameters
            label = (f"{bp['label']}: "
                     f"$g_D={bp['g_D']:.3f}$, "
                     f"$y_\\psi={bp['y_psi']:.3f}$, "
                     f"$v={bp['v']:.3f}$ GeV")

            ax.plot(log10_f, log10_h2OmegaGW, color=bp['color'],
                    linestyle=bp['linestyle'], linewidth=1.5, label=label, alpha=0.8)

    # Axis labels
    ax.set_xlabel(r'$\log_{10}(f / \mathrm{Hz})$', fontsize=14)
    ax.set_ylabel(r'$\log_{10}(h^2 \Omega_{\mathrm{GW}})$', fontsize=14)

    # Set axis limits
    ax.set_xlim(-9.0, -7.0)
    ax.set_ylim(-12, -5)

    # Legend
    ax.legend(fontsize=9, loc='lower left', framealpha=0.9)

    # Grid
    ax.grid(True, alpha=0.3, linestyle=':')

    # Title
    ax.set_title('Conformal U(1)$_D$ Dark Sector: GW Spectra vs PTA Violins',
                 fontsize=13)

    plt.tight_layout()
    plt.savefig(output_pdf, dpi=150, bbox_inches='tight')
    print(f"Saved benchmark spectrum plot to {output_pdf}")
    plt.close()


if __name__ == "__main__":
    main()
