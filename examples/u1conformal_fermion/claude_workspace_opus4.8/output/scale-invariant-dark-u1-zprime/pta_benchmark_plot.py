"""Benchmark spectrum vs PTA violins for scale-invariant dark U(1)_D (CW)."""

import sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parents[1]
sys.path.insert(0, str(_HERE))
sys.path.insert(0, str(_ROOT / "backend"))

import natpy as nat
import la_forge.core as co
from fopt_model import evaluate_point
from pta_spectrum import omega_gw, TEMPLATE


# ---- violins (copied verbatim from backend/plot_violins.py) ----
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

    freqs = c0.rn_freqs

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


# ---- selected maximally-different 14/14 benchmark points ----
POINTS = [
    (0.5071, 0.0,    1.371241),
    (0.6024, 0.35,   0.5),
    (0.6857, 0.6833, 2.000001),
    (0.769,  0.85,   2.828428),
]

COLORS = ["#d62728", "#1f77b4", "#2ca02c", "#9467bd"]


def main():
    plt.rcParams.update({"text.usetex": False, "font.size": 12,
                         "mathtext.fontset": "cm"})
    fig, ax = plt.subplots(figsize=(8, 5.5))
    h2v, _ = load_violins()
    plot_violins(ax, h2v)

    f = np.logspace(-9, -7, 400)
    logf = np.log10(f)
    for (g_D, y, w), c in zip(POINTS, COLORS):
        r = evaluate_point(g_D, y, w)
        om = omega_gw(f, r["Treh"], r["alpha"], r["beta_H"])
        logom = np.log10(np.where(om > 0, om, 1e-300))
        lab = (rf"$g_D={g_D:.3g},\ y={y:.3g},\ w={w:.3g}\,$GeV "
               rf"($\alpha={r['alpha']:.1e},\ \beta/H={r['beta_H']:.1f}$)")
        ax.plot(logf, logom, color=c, lw=2, label=lab)

    ax.set_xlim(-9, -7)
    ax.set_ylim(-12, -6)
    ax.set_xlabel(r"$\log_{10}(f/\mathrm{Hz})$")
    ax.set_ylabel(r"$\log_{10}(h^2\Omega_{\mathrm{GW}})$")
    ax.set_title(r"Dark $U(1)_D$ CW FOPT: dbf spectra vs NANOGrav 15yr violins")
    ax.legend(fontsize=8, loc="lower left", framealpha=0.9)
    ax.grid(alpha=0.25)
    fig.tight_layout()
    out = _HERE / "pta_benchmark_spectrum.pdf"
    fig.savefig(out)
    print("wrote", out)


if __name__ == "__main__":
    main()
