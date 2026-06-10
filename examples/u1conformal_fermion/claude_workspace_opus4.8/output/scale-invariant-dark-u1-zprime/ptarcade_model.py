"""PTArcade model: scale-invariant dark U(1)_D (Coleman-Weinberg) FOPT.

Independent free parameters (priors):
    g_D : dark gauge coupling, Uniform[0.1, 2.0]
    y   : dark Yukawa coupling, Uniform[0.0, 2.0]   (hard cut y^4 < 1.5 g_D^4)
    log10_w : log10 of vev w/GeV, Uniform[log10(0.05), log10(10.0)]
              (w spans >2 orders of magnitude -> logarithmic prior)

Dependent FOPT quantities (alpha, beta_H, Treh) are computed per point with the
actual backend (semianalytic_pipeline via fopt_model.evaluate_point), and the
GW spectrum is computed with the dbf template (arXiv:2511.15687) via the
deterministic backend Spectrum class. No caching, no interpolation.
"""

import sys
from pathlib import Path
import numpy as np

from ptarcade.models_utils import prior

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parents[1]
sys.path.insert(0, str(_HERE))
sys.path.insert(0, str(_ROOT / "backend"))

from fopt_model import evaluate_point  # noqa: E402
from spectrum import Spectrum  # noqa: E402

name = "np_model"
smbhb = False

_SPECTRUM = Spectrum(template="dbf")

# enlarged priors (user override); w logarithmic
parameters = {
    "g_D": prior("Uniform", 0.1, 2.0),
    "y": prior("Uniform", 0.0, 2.0),
    "log10_w": prior("Uniform", np.log10(0.05), np.log10(10.0)),
}


def _scalar(x):
    a = np.asarray(x)
    return float(a.item() if a.size == 1 else a.flat[0])


def spectrum(f, g_D, y, log10_w):
    f = np.atleast_1d(np.asarray(f, dtype=float))
    zero = np.zeros_like(f)

    g_D = _scalar(g_D)
    y = _scalar(y)
    w = 10.0 ** _scalar(log10_w)

    # hard cut y^4 < 1.5 g_D^4 (beta_lambda > 0, boson-dominated CW breaking)
    if y ** 4 >= 1.5 * g_D ** 4:
        return zero

    r = evaluate_point(g_D, y, w)
    if r["status"] != "viable":
        return zero
    alpha, beta_H, Treh = r["alpha"], r["beta_H"], r["Treh"]
    if not (np.isfinite(alpha) and np.isfinite(beta_H) and np.isfinite(Treh)):
        return zero
    if alpha <= 0 or beta_H <= 0 or Treh <= 0:
        return zero
    try:
        out = _SPECTRUM.get_h2OmegaGW(f, Treh, alpha, beta_H)
    except Exception:
        return zero
    out = np.asarray(out, dtype=float)
    out[~np.isfinite(out)] = 0.0
    return out
