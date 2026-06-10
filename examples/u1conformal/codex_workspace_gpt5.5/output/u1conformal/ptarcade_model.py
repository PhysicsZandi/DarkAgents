"""PTArcade model for the u1conformal FOPT spectrum."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from ptarcade.models_utils import prior


HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parents[1]
BACKEND_DIR = PROJECT_ROOT / "backend"
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from pta_spectrum import SELECTED_TEMPLATE, evaluate_fopt, h2omega_from_fopt  # noqa: E402


parameters = {
    "log10_v": prior("Uniform", np.log10(0.003), np.log10(5.0)),
    "g_D": prior("Uniform", 0.42, 1.05),
}


def _scalar(value):
    arr = np.asarray(value)
    return float(arr.item() if arr.size == 1 else arr.flat[0])


def spectrum(f, log10_v, g_D):
    """Return h^2 Omega_GW for PTArcade frequencies."""
    f_arr = np.asarray(f, dtype=float)
    try:
        log10_v = _scalar(log10_v)
        g_D = _scalar(g_D)
        v = 10.0**log10_v
    except Exception:
        return np.zeros_like(f_arr, dtype=float)
    if (
        not np.isfinite(v)
        or not np.isfinite(g_D)
        or v <= 0.0
        or g_D <= 0.0
        or np.any(~np.isfinite(f_arr))
        or np.any(f_arr <= 0.0)
    ):
        return np.zeros_like(f_arr, dtype=float)
    point = evaluate_fopt(v, g_D)
    omega = h2omega_from_fopt(f_arr, point, template=SELECTED_TEMPLATE)
    omega = np.asarray(omega, dtype=float)
    omega[~np.isfinite(omega)] = 0.0
    omega[omega < 0.0] = 0.0
    return omega

