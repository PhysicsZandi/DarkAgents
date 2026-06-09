"""
PTArcade model for u1conformal: classically scale-invariant dark U(1)_D
strongly supercooled FOPT, GW spectrum via the dbf template (2511.15687).

Independent priors (model parameters ONLY):
  - log10_v : log10 of dark vev in GeV   (log-uniform; spans several orders)
  - g_D     : U(1)_D gauge coupling      (uniform; small range, perturbative)

Dependent (computed inside, NOT priors): lambda_Phi (CW-fixed), alpha, beta_H,
Treh -- all from the actual semianalytic FOPT backend.
"""
import os
import sys
from pathlib import Path
import numpy as np

from ptarcade.models_utils import prior

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parents[1]
sys.path.insert(0, str(_ROOT / "backend"))
sys.path.insert(0, str(_HERE))

from spectrum import Spectrum            # noqa: E402
from fopt_model import evaluate_point    # noqa: E402

name = "np_model"

_TEMPLATE = "dbf"
_SPEC = Spectrum(template=_TEMPLATE)

# Priors on independent model parameters only.
# 14/14 benchmark window: v in [0.35, 2.4] GeV, g_D in [0.51, 0.63].
# Priors are made much wider (v: ~2 orders beyond on each side; g_D: > 2x wider).
parameters = {
    "log10_v": prior("Uniform", np.log10(1e-3), np.log10(50.0)),  # GeV
    "g_D": prior("Uniform", 0.45, 0.90),
}


def _scalar(x):
    a = np.asarray(x)
    return float(a.item() if a.size == 1 else a.flat[0])


def spectrum(f, log10_v, g_D):
    f = np.asarray(f, dtype=float)
    log10_v = _scalar(log10_v)
    g_D = _scalar(g_D)

    zero = np.zeros_like(f)
    if not (np.isfinite(log10_v) and np.isfinite(g_D)):
        return zero
    v = 10.0**log10_v
    if v <= 0 or g_D <= 0:
        return zero

    res = evaluate_point(v, g_D, verbose=False)
    if res["status"] != "viable":
        return zero
    alpha = res["alpha"]
    beta_H = res["beta_H"]
    Treh = res["Treh"]
    if not (np.isfinite(alpha) and np.isfinite(beta_H) and np.isfinite(Treh)
            and alpha > 0 and beta_H > 0 and Treh > 0):
        return zero

    try:
        h2 = _SPEC.get_h2OmegaGW(f, Treh, alpha, beta_H)
    except Exception:
        return zero
    h2 = np.asarray(h2, dtype=float)
    h2 = np.where(np.isfinite(h2) & (h2 > 0), h2, 0.0)
    return h2
