"""PTA spectrum wrapper for minimal_conformal_su2_doublet."""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np


MODEL_DIR = Path(__file__).resolve().parent
PROJECT_DIR = MODEL_DIR.parents[1]
BACKEND_DIR = PROJECT_DIR / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from spectrum import Spectrum  # noqa: E402
from fopt_model import evaluate_point  # noqa: E402


TEMPLATE = "dbf"
TEMPLATE_REASON = (
    "Selected dissipative bulk-flow template for strongly supercooled points. "
    "The best PTA-steering FOPT points often have alpha >> 0.5, outside the "
    "local Higgsless-template validation hint, while the DBF/BF template is "
    "documented locally as appropriate for very large alpha."
)
TEMPLATE_CAVEAT = (
    "Wall velocity and microscopic efficiency are not computed by the FOPT "
    "backend; backend/spectrum.py uses the default ksw=1. Treat amplitudes as "
    "template-level estimates, especially for moderate-alpha points where "
    "higgsless and bulk-flow assumptions overlap only partially."
)


def _zero_like(f):
    return np.zeros_like(np.asarray(f, dtype=float), dtype=float)


def fopt_from_model_parameters(gD: float, vD: float) -> dict:
    result = evaluate_point(float(gD), float(vD))
    if result.get("status") != "viable":
        raise ValueError(f"non-viable FOPT point: {result.get('failure_reason', result.get('status'))}")
    for key in ("Treh", "alpha", "beta_H"):
        value = float(result[key])
        if not math.isfinite(value) or value <= 0.0:
            raise ValueError(f"invalid {key}={value}")
    return result


def h2omega_from_fopt(f, Treh: float, alpha: float, beta_H: float, template: str = TEMPLATE):
    f = np.asarray(f, dtype=float)
    if (
        np.any(~np.isfinite(f))
        or np.any(f <= 0.0)
        or not math.isfinite(float(Treh))
        or not math.isfinite(float(alpha))
        or not math.isfinite(float(beta_H))
        or float(Treh) <= 0.0
        or float(alpha) <= 0.0
        or float(beta_H) <= 0.0
    ):
        return _zero_like(f)
    values = Spectrum(template=template).h2OmegaGW(f, float(Treh), float(alpha), float(beta_H))
    values = np.asarray(values, dtype=float)
    return np.where(np.isfinite(values) & (values > 0.0), values, 0.0)


def h2omega_from_model(f, gD: float, vD: float, template: str = TEMPLATE):
    result = fopt_from_model_parameters(gD, vD)
    return h2omega_from_fopt(f, result["Treh"], result["alpha"], result["beta_H"], template=template)

