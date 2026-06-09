"""PTArcade model for su2cw-dark FOPT GW signal (dbf template).

Independent model parameters (priors):
    g       : dark SU(2)_D gauge coupling      -- linear prior  [0.5, 1.5]
    log10_chi0 : log10(chi0/GeV)               -- uniform prior [-2, 2]

The benchmark 14/14 PTA-compatible region is g in [0.85, 1.05] and
chi0 in [0.40, 1.58] GeV. Priors here are deliberately much wider: g linear
covers the perturbative range a factor >2 each side; chi0 is log-scanned over
4 decades (1e-2 .. 1e2 GeV), i.e. ~2 decades beyond the benchmark window on
each side, so the posterior fall-off stays well inside the prior edges.

FOPT (alpha, beta_H, Treh) are computed by the actual backend pipeline
(fopt_model.compute_point). The GW spectrum uses the deterministic Spectrum
class (dbf template) via pta_spectrum.
"""

import sys
from pathlib import Path

import numpy as np

from ptarcade.models_utils import prior

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
sys.path.insert(0, str(_HERE.parents[1] / "backend"))

from fopt_model import compute_point  # noqa: E402
from pta_spectrum import h2OmegaGW as _h2OmegaGW  # noqa: E402

name = "np_model"

parameters = {
    "g": prior("Uniform", 0.5, 1.5),
    "log10_chi0": prior("Uniform", -2.0, 2.0),
}


def _scalar(x):
    a = np.asarray(x)
    return float(a.item() if a.size == 1 else a.flat[0])


def spectrum(f, g, log10_chi0):
    f = np.asarray(f, dtype=float)
    zero = np.zeros_like(f)
    try:
        g = _scalar(g)
        chi0 = 10.0 ** _scalar(log10_chi0)
        res = compute_point(g, chi0)
        if res["status"] != "viable":
            return zero
        alpha = res["alpha"]
        beta_H = res["beta_H"]
        Treh = res["Treh"]
        if not (np.isfinite(alpha) and np.isfinite(beta_H) and np.isfinite(Treh)):
            return zero
        if alpha <= 0 or beta_H <= 0 or Treh <= 0:
            return zero
        out = _h2OmegaGW(f, Treh, alpha, beta_H)
        out = np.asarray(out, dtype=float)
        if not np.all(np.isfinite(out)):
            out = np.where(np.isfinite(out), out, 0.0)
        return out
    except Exception:
        return zero
