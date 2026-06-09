"""Benchmark spectrum vs PTA violins for u1conformal (dbf template)."""
import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import natpy as nat
import la_forge.core as co
from pathlib import Path

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
from pta_spectrum import spectrum_from_params, TEMPLATE  # noqa: E402


# ---- violin functions copied verbatim from backend/plot_violins.py ----
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

    viol = c0(labels)

    dfreq = np.diff(np.concatenate((np.array([0]), freqs[::1])))

    H_0byh = 100 * nat.convert(nat.km * nat.s**-1 * nat.Mpc**-1, nat.Hz)
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
# ----------------------------------------------------------------------


BENCHMARKS = [
    (0.7483, 0.560),
    (2.386, 0.510),
    (0.5084, 0.630),
    (0.3454, 0.540),
]


def main():
    try:
        plt.rcParams["text.usetex"] = False
        plt.rcParams["font.family"] = "serif"
        plt.rcParams["mathtext.fontset"] = "cm"

        h2_omega_viol, _ = load_violins()

        fig, ax = plt.subplots(figsize=(7.2, 5.2))
        plot_violins(ax, h2_omega_viol, N_f=14)

        f = np.logspace(-9, -7, 400)
        logf = np.log10(f)
        colors = ["C0", "C1", "C2", "C3"]
        for (v, g_D), c in zip(BENCHMARKS, colors):
            h2, res = spectrum_from_params(f, v, g_D, template=TEMPLATE)
            mask = h2 > 0
            ax.plot(logf[mask], np.log10(h2[mask]), color=c, lw=2.0,
                    label=(rf"$v={v*1e3:.0f}\,$MeV, $g_D={g_D:.2f}$, "
                           rf"$\alpha={res['alpha']:.1e}$"))

        ax.set_xlim(-9, -7)
        ax.set_ylim(-11, -6)
        ax.set_xlabel(r"$\log_{10}(f/\mathrm{Hz})$", fontsize=13)
        ax.set_ylabel(r"$\log_{10}(h^2\,\Omega_{\mathrm{GW}})$", fontsize=13)
        ax.set_title(r"Conformal $U(1)_D$ FOPT (dbf template) vs NANOGrav 15yr",
                     fontsize=12)
        ax.legend(fontsize=8.5, loc="lower left", framealpha=0.9)
        ax.grid(alpha=0.25, ls=":")
        fig.tight_layout()
        out = os.path.join(_HERE, "pta_benchmark_spectrum.pdf")
        fig.savefig(out, bbox_inches="tight")
        print("wrote", out)
    except Exception as e:
        print("PLOT_FAILED:", type(e).__name__, e)
        raise


if __name__ == "__main__":
    main()
