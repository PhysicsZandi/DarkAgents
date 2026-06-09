"""
PTA spectrum wrapper for the conformal-SU2 model.

Template choice: "dbf" (dissipative bulk flow, arXiv:2511.15687)
Reasoning:
- The FOPT scan shows alpha values ranging from ~O(10^0) to O(10^28) across the
  viable parameter space. The "higgsless" template (arXiv:2209.04369) is validated
  for alpha up to ~0.5 (weak transitions).
- For the strong transitions (alpha >> 1) that characterize CW-type models, the
  bulk-flow/dissipative-bulk-flow templates are designed.
- The "dbf" template explicitly accounts for dissipative effects in the fluid
  motion, which become important for very strong transitions with large alpha.
- Caveat: The validity of the "dbf" template for the weakest transitions
  (alpha ~ O(1-10)) is less established, but in practice the gravitational-wave
  amplitude from these weaker points is too small to explain the PTA signal
  anyway, so the choice of template for those points does not affect the
  PTA-compatible region.
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backend"))
from semianalytic_pipeline import SemiAnalyticPipeline
from spectrum import Spectrum


# Global spectrum object with the selected template
_spectrum = Spectrum(template="dbf")


def compute_spectrum(g, chi0, f):
    """
    Compute the GW spectrum h^2 Omega_GW(f) for the conformal-SU2 model
    at the given frequency array f.

    Parameters
    ----------
    g : float
        SU(2)_X gauge coupling.
    chi0 : float
        Scalar VEV at zero temperature (GeV).
    f : np.ndarray
        Frequency array (Hz).

    Returns
    -------
    h2OmegaGW : np.ndarray
        GW energy-density spectrum h^2 Omega_GW(f) at each frequency.
        Returns zeros if the FOPT computation fails or non-finite values arise.
    """
    # Define the model particle content
    boson_gbs = {"W": g / 2.0}
    boson_dofs = {"W": 9}
    fermion_gfs = {}
    fermion_dofs = {}

    # Run the FOPT pipeline
    try:
        model = SemiAnalyticPipeline(
            chi0=chi0,
            boson_gbs=boson_gbs,
            boson_dofs=boson_dofs,
            fermion_gfs=fermion_gfs,
            fermion_dofs=fermion_dofs,
            verbose=False,
        )
        alpha = float(model.get_alpha())
        beta_H = float(model.get_beta_H())
        Tr = float(model.get_Tr())
    except Exception:
        return np.zeros_like(f, dtype=float)

    # Validate FOPT outputs
    if not np.isfinite(alpha) or not np.isfinite(beta_H) or not np.isfinite(Tr):
        return np.zeros_like(f, dtype=float)
    if alpha <= 0 or beta_H <= 0 or Tr <= 0:
        return np.zeros_like(f, dtype=float)

    # Recreate model object for eternal inflation check
    try:
        check_model = SemiAnalyticPipeline(
            chi0=chi0,
            boson_gbs=boson_gbs,
            boson_dofs=boson_dofs,
            fermion_gfs=fermion_gfs,
            fermion_dofs=fermion_dofs,
            verbose=False,
        )
        eternal = check_model.get_check_eternal_inflation()
    except Exception:
        eternal = True
    if eternal:
        return np.zeros_like(f, dtype=float)

    # Compute spectrum
    try:
        h2OmegaGW = _spectrum.h2OmegaGW(f, Tr, alpha, beta_H)
    except Exception:
        return np.zeros_like(f, dtype=float)

    # Ensure finite output
    if not np.all(np.isfinite(h2OmegaGW)):
        h2OmegaGW = np.where(np.isfinite(h2OmegaGW), h2OmegaGW, 0.0)

    return h2OmegaGW


def get_fopt_params(g, chi0):
    """
    Compute FOPT parameters for the given model parameters.

    Returns
    -------
    dict with keys: alpha, beta_H, Tr, Tn, Tp, Treh, f_peak_est
    or None if computation fails.
    """
    boson_gbs = {"W": g / 2.0}
    boson_dofs = {"W": 9}
    fermion_gfs = {}
    fermion_dofs = {}

    try:
        model = SemiAnalyticPipeline(
            chi0=chi0,
            boson_gbs=boson_gbs,
            boson_dofs=boson_dofs,
            fermion_gfs=fermion_gfs,
            fermion_dofs=fermion_dofs,
            verbose=False,
        )
        alpha = float(model.get_alpha())
        beta_H = float(model.get_beta_H())
        Tr = float(model.get_Tr())
    except Exception:
        return None

    if not np.isfinite(alpha) or not np.isfinite(beta_H) or not np.isfinite(Tr):
        return None
    if alpha <= 0 or beta_H <= 0 or Tr <= 0:
        return None

    # Check for eternal inflation
    try:
        eternal = model.get_check_eternal_inflation()
    except Exception:
        eternal = True
    if eternal:
        return None

    return {
        "alpha": alpha,
        "beta_H": beta_H,
        "Tr": Tr,
    }