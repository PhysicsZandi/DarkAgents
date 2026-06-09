"""MAP-point spectrum vs PTA violins for u1conformal (dbf template)."""
import os
import sys
import json
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


def main():
    plt.rcParams["text.usetex"] = False
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["mathtext.fontset"] = "cm"

    with open(os.path.join(_HERE, "ptarcade_bayes.json")) as fh:
        bayes = json.load(fh)
    mp = bayes["map_est"]
    # keys may be log10_v / g_D or dashed variants
    def getk(d, *cands):
        for c in cands:
            if c in d:
                return d[c]
        raise KeyError(cands)
    log10_v = float(getk(mp, "log10_v", "log10-v"))
    g_D = float(getk(mp, "g_D", "g-D"))
    v = 10**log10_v

    h2_omega_viol, _ = load_violins()
    fig, ax = plt.subplots(figsize=(7.2, 5.2))
    plot_violins(ax, h2_omega_viol, N_f=14)

    f = np.logspace(-9, -7, 400)
    logf = np.log10(f)
    h2, res = spectrum_from_params(f, v, g_D, template=TEMPLATE)
    mask = h2 > 0
    ax.plot(logf[mask], np.log10(h2[mask]), color="crimson", lw=2.4,
            label=(rf"MAP: $v={v*1e3:.0f}\,$MeV, $g_D={g_D:.3f}$" "\n"
                   rf"$\alpha={res['alpha']:.1e}$, $\beta/H={res['beta_H']:.1f}$"))

    ax.set_xlim(-9, -7)
    ax.set_ylim(-11, -6)
    ax.set_xlabel(r"$\log_{10}(f/\mathrm{Hz})$", fontsize=13)
    ax.set_ylabel(r"$\log_{10}(h^2\,\Omega_{\mathrm{GW}})$", fontsize=13)
    ax.set_title(r"u1conformal PTArcade MAP spectrum (dbf) vs NANOGrav 15yr",
                 fontsize=12)
    ax.legend(fontsize=9.5, loc="lower left", framealpha=0.9)
    ax.grid(alpha=0.25, ls=":")
    fig.tight_layout()
    out = os.path.join(_HERE, "pta_ptarcade_spectrum.pdf")
    fig.savefig(out, bbox_inches="tight")
    print("wrote", out, "MAP v=", v, "g_D=", g_D)


if __name__ == "__main__":
    main()
