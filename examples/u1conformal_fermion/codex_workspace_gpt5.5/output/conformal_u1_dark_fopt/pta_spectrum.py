"""PTA spectrum utilities for conformal_u1_dark_fopt.

The only scan axes are the independent model parameters v_D [GeV], g_D, y_D.
All FOPT quantities are computed by the upstream FOPT model at each point.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import Any

import numpy as np

OUTDIR = Path(__file__).resolve().parent
REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_DIR = REPO_ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
if str(OUTDIR) not in sys.path:
    sys.path.insert(0, str(OUTDIR))

from spectrum import Spectrum  # noqa: E402
from fopt_model import evaluate_point  # noqa: E402

SELECTED_TEMPLATE = "dbf"
TEMPLATE_VALIDITY_STATUS = "warning"
TEMPLATE_VALIDITY_REASON = (
    "The conformal U(1)_D scan contains very strong or supercooled points "
    "(alpha up to extremely large values), outside the strict validity domain "
    "of the implemented templates. The dissipative-bulk-flow template is used "
    "as the closest supported template for strong transitions, with this caveat."
)


def finite_scalar(value: Any) -> float:
    array = np.asarray(value)
    if array.size == 0:
        return math.nan
    try:
        return float(array.item() if array.size == 1 else array.flat[0])
    except Exception:
        return math.nan


def safe_fopt(v_D: float, g_D: float, y_D: float) -> dict[str, Any]:
    try:
        row = evaluate_point(float(v_D), float(g_D), float(y_D))
    except Exception as exc:
        return {
            "v_D": float(v_D),
            "g_D": float(g_D),
            "y_D": float(y_D),
            "status": "numerical_failure",
            "failure_reason": type(exc).__name__,
        }
    return row


def spectrum_from_fopt(
    frequencies_hz: np.ndarray,
    fopt: dict[str, Any],
    template: str = SELECTED_TEMPLATE,
) -> np.ndarray:
    f = np.asarray(frequencies_hz, dtype=float)
    zeros = np.zeros_like(f, dtype=float)
    if fopt.get("status") != "viable":
        return zeros
    alpha = finite_scalar(fopt.get("alpha"))
    beta_H = finite_scalar(fopt.get("beta_H"))
    Treh = finite_scalar(fopt.get("Treh"))
    if not all(np.isfinite([alpha, beta_H, Treh])) or alpha <= 0.0 or beta_H <= 0.0 or Treh <= 0.0:
        return zeros
    if not np.all(np.isfinite(f)) or np.any(f <= 0.0):
        return zeros
    try:
        values = Spectrum(template=template).get_h2OmegaGW(f, Treh, alpha, beta_H)
    except Exception:
        return zeros
    values = np.asarray(values, dtype=float)
    values[~np.isfinite(values)] = 0.0
    values[values < 0.0] = 0.0
    return values


def evaluate_spectrum(
    frequencies_hz: np.ndarray,
    v_D: float,
    g_D: float,
    y_D: float,
    template: str = SELECTED_TEMPLATE,
) -> tuple[dict[str, Any], np.ndarray]:
    fopt = safe_fopt(v_D, g_D, y_D)
    return fopt, spectrum_from_fopt(frequencies_hz, fopt, template=template)


def peak_diagnostics(fopt: dict[str, Any], template: str = SELECTED_TEMPLATE) -> dict[str, float]:
    grid = np.logspace(-10, -6, 600)
    values = spectrum_from_fopt(grid, fopt, template=template)
    if values.size == 0 or not np.any(values > 0.0):
        return {"peak_frequency_Hz": math.nan, "peak_h2OmegaGW": math.nan}
    idx = int(np.nanargmax(values))
    return {"peak_frequency_Hz": float(grid[idx]), "peak_h2OmegaGW": float(values[idx])}
