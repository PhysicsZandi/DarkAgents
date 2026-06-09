"""PTArcade stochastic GW model for minimal_conformal_su2_doublet."""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
from ptarcade.models_utils import prior


MODEL_DIR = Path(__file__).resolve().parent
PROJECT_DIR = MODEL_DIR.parents[1]
BACKEND_DIR = PROJECT_DIR / "backend"
if str(MODEL_DIR) not in sys.path:
    sys.path.insert(0, str(MODEL_DIR))
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from pta_spectrum import TEMPLATE, h2omega_from_fopt, fopt_from_model_parameters  # noqa: E402


name = "minimal_conformal_su2_doublet"

parameters = {
    "gD": prior("Uniform", 0.45, 1.55),
    "log10_vD": prior("Uniform", -3.2, 0.7),
}


def _scalar(value):
    arr = np.asarray(value)
    return float(arr.item() if arr.size == 1 else arr.flat[0])


def spectrum(f, gD, log10_vD):
    f = np.asarray(f, dtype=float)
    zero = np.zeros_like(f, dtype=float)
    try:
        gD = _scalar(gD)
        log10_vD = _scalar(log10_vD)
        vD = 10.0**log10_vD
        if np.any(~np.isfinite(f)) or np.any(f <= 0.0):
            return zero
        if not (np.isfinite(gD) and np.isfinite(vD) and gD > 0.0 and vD > 0.0):
            return zero
        fopt = fopt_from_model_parameters(gD, vD)
        values = h2omega_from_fopt(f, fopt["Treh"], fopt["alpha"], fopt["beta_H"], template=TEMPLATE)
        return np.where(np.isfinite(values) & (values > 0.0), values, 0.0)
    except Exception:
        return zero
