"""PTArcade stochastic-background model for conformal_u1_dark_fopt."""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
from ptarcade.models_utils import prior

OUTDIR = Path(__file__).resolve().parent
REPO_ROOT = Path(__file__).resolve().parents[2]
if str(OUTDIR) not in sys.path:
    sys.path.insert(0, str(OUTDIR))
if str(REPO_ROOT / "backend") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "backend"))

from pta_spectrum import evaluate_spectrum  # noqa: E402

name = "conformal_u1_dark_fopt"

parameters = {
    "log10_v_D": prior("Uniform", -3.5, 1.0),
    "g_D": prior("Uniform", 0.15, 1.0),
    "y_D": prior("Uniform", 0.0, 0.95),
}


def _scalar(value):
    array = np.asarray(value)
    return float(array.item() if array.size == 1 else array.flat[0])


def spectrum(f, log10_v_D, g_D, y_D):
    f = np.asarray(f, dtype=float)
    zeros = np.zeros_like(f, dtype=float)
    if not np.all(np.isfinite(f)) or np.any(f <= 0.0):
        return zeros

    log10_v_D = _scalar(log10_v_D)
    g_D = _scalar(g_D)
    y_D = _scalar(y_D)
    if not all(np.isfinite([log10_v_D, g_D, y_D])):
        return zeros
    v_D = 10.0 ** log10_v_D
    if v_D <= 0.0 or g_D <= 0.0 or y_D < 0.0:
        return zeros

    _, values = evaluate_spectrum(f, v_D, g_D, y_D)
    values = np.asarray(values, dtype=float)
    values[~np.isfinite(values)] = 0.0
    values[values < 0.0] = 0.0
    return values
