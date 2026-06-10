"""PTA-band GW spectrum wrapper for the u1conformal FOPT model.

This file intentionally keeps all FOPT quantities derived.  Public entry points
accept only the independent model parameters v [GeV] and g_D.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import Any

import numpy as np


MODEL = "u1conformal"
BRANCH = "fopt-pta"
SELECTED_TEMPLATE = "bf"
TEMPLATE_CAVEAT = (
    "The model points are strongly supercooled with alpha often much larger "
    "than unity. The bulk-flow template from arXiv:2511.15687 is the closest "
    "implemented template, but wall dynamics, efficiency, and the precise "
    "bulk-flow/dissipative-bulk-flow partition are not solved in this PTA "
    "wrapper."
)

HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parents[1]
BACKEND_DIR = PROJECT_ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from fopt_model import evaluate_point, point_to_dict  # noqa: E402
from spectrum import Spectrum  # noqa: E402


def scalar(value: Any) -> float:
    arr = np.asarray(value)
    if arr.size == 0:
        return float("nan")
    return float(arr.item() if arr.size == 1 else arr.flat[0])


def finite_positive(value: Any) -> bool:
    try:
        x = float(value)
    except Exception:
        return False
    return math.isfinite(x) and x > 0.0


def evaluate_fopt(v: float, g_D: float) -> dict[str, Any]:
    """Evaluate the upstream FOPT model for independent parameters only."""
    point = evaluate_point(float(v), float(g_D), verbose=False)
    return point_to_dict(point)


def valid_fopt(point: dict[str, Any]) -> bool:
    return (
        point.get("status") == "viable"
        and finite_positive(point.get("alpha"))
        and finite_positive(point.get("beta_H"))
        and finite_positive(point.get("Treh"))
    )


def h2omega_from_fopt(
    f: np.ndarray | float,
    point: dict[str, Any],
    template: str = SELECTED_TEMPLATE,
    ksw: float = 1.0,
) -> np.ndarray:
    """Compute h^2 Omega_GW(f) from a previously evaluated viable FOPT point."""
    f_arr = np.asarray(f, dtype=float)
    if not valid_fopt(point) or np.any(~np.isfinite(f_arr)) or np.any(f_arr <= 0.0):
        return np.zeros_like(f_arr, dtype=float)
    spec = Spectrum(template=template)
    try:
        omega = spec.get_h2OmegaGW(
            f_arr,
            float(point["Treh"]),
            float(point["alpha"]),
            float(point["beta_H"]),
            ksw=ksw,
        )
    except Exception:
        return np.zeros_like(f_arr, dtype=float)
    omega = np.asarray(omega, dtype=float)
    omega[~np.isfinite(omega)] = 0.0
    omega[omega < 0.0] = 0.0
    return omega


def spectrum(
    f: np.ndarray | float,
    v: float,
    g_D: float,
    template: str = SELECTED_TEMPLATE,
) -> np.ndarray:
    """Evaluate FOPT and spectrum for independent model parameters v and g_D."""
    point = evaluate_fopt(float(v), float(g_D))
    return h2omega_from_fopt(f, point, template=template)
