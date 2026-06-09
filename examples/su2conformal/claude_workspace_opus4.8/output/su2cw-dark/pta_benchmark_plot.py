"""Benchmark spectrum vs PTA violins for su2cw-dark (dbf template)."""

import sys
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# violin loading deps
import natpy as nat
import la_forge.core as co

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
from fopt_model import compute_point  # noqa: E402
from pta_spectrum import h2OmegaGW, TEMPLATE  # noqa: E402

try:
    plt.rcParams["text.usetex"] = False
    plt.rcParams["mathtext.fontset"] = "cm"
except Exception:
    pass


# ---- copied verbatim from backend/plot_violins.py ----
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

    filename = "30fCP_30fiRN_2A.core" if correlations else "30fCP_30fiRN_2A.core"
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
        24 * np.pi**4 * (10**viol) ** 2 * 1 / np.repeat(dfreq, 1)
        * freqs**5 / (3 * H_0byh**2)
    )
    return h2_omega_viol, freqs


def plot_violins(ax, h2_omega_viol, N_f=14, border="silver"):
    Tspan = 505861299.1401644
    n_freq = min(N_f, h2_omega_viol.shape[1])
    freqs = np.arange(1, n_freq + 1) / Tspan
    v1 = ax.violinplot(
        h2_omega_viol[:, :n_freq], positions=np.log10(freqs),
        widths=0.05, showextrema=False,
    )
    for pc in v1["bodies"]:
        pc.set_facecolor("silver")
        pc.set_edgecolor(border)
        pc.set_linestyle("solid")
    return
# ------------------------------------------------------


BENCH = [
    ("lo_g",   0.85, 1.0,                 "tab:blue"),
    ("hi_g",   1.05, 0.5011872336272724,  "tab:orange"),
    ("lo_chi", 0.90, 0.3981071705534973,  "tab:green"),
    ("hi_chi", 0.85, 1.584893192461114,   "tab:red"),
]


def main():
    h2_omega_viol, _ = load_violins()
    fig, ax = plt.subplots(figsize=(7.2, 5.0))
    plot_violins(ax, h2_omega_viol)

    f = np.logspace(-9, -7, 400)
    logf = np.log10(f)
    for name, g, chi0, c in BENCH:
        res = compute_point(g, chi0)
        omega = h2OmegaGW(f, res["Treh"], res["alpha"], res["beta_H"])
        omega = np.where(np.isfinite(omega) & (omega > 0), omega, np.nan)
        ax.plot(logf, np.log10(omega), color=c, lw=2,
                label=r"$g=%.2f,\ \chi_0=%.2f$ GeV" % (g, chi0))

    ax.set_xlim(-9, -7)
    ax.set_ylim(-11, -6)
    ax.set_xlabel(r"$\log_{10}(f/\mathrm{Hz})$", fontsize=13)
    ax.set_ylabel(r"$\log_{10}(h^2\Omega_{\mathrm{GW}})$", fontsize=13)
    ax.set_title(r"su2cw-dark: dbf spectrum vs NANOGrav 15yr", fontsize=13)
    ax.legend(loc="lower left", fontsize=9, framealpha=0.9)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    out = _HERE / "pta_benchmark_spectrum.pdf"
    fig.savefig(out)
    print("wrote", out, "template", TEMPLATE)


if __name__ == "__main__":
    main()
