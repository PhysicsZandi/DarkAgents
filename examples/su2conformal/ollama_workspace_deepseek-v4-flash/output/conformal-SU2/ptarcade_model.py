"""
PTArcade model for the conformal-SU2 model.

Classically scale-invariant SU(2) gauge theory with one complex scalar doublet.
GW spectrum from first-order phase transition using the bulk-flow template.
"""
from ptarcade.models_utils import prior
from pathlib import Path
import sys
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backend"))
from semianalytic_pipeline import SemiAnalyticPipeline
from spectrum import Spectrum

# ---------- free parameters ----------
# g: SU(2) gauge coupling, linear prior in [0.5, 3.0]
# chi0: VEV in GeV, log prior in [1e-5, 5.0] GeV
parameters = {
    "g": prior("Uniform", 0.5, 3.0),
    "log10_chi0": prior("Uniform", -5.0, np.log10(5.0)),
}

_spectrum = Spectrum(template="dbf")


def spectrum(f, g, log10_chi0):
    """
    Compute h^2 Omega_GW(f) for the conformal-SU2 model.

    Parameters
    ----------
    f : np.ndarray
        Frequency array (Hz).
    g : float or list[float]
        SU(2) gauge coupling.
    log10_chi0 : float or list[float]
        Base-10 logarithm of the VEV (GeV).

    Returns
    -------
    h2OmegaGW : np.ndarray
        GW energy-density spectrum at each frequency.
    """
    # PTArcade passes lists; extract scalar
    g = float(np.asarray(g).flat[0])
    log10_chi0 = float(np.asarray(log10_chi0).flat[0])
    chi0 = 10.0**log10_chi0

    # Compute FOPT parameters
    boson_gbs = {"W": g / 2.0}
    boson_dofs = {"W": 9}
    fermion_gfs = {}
    fermion_dofs = {}

    try:
        model_obj = SemiAnalyticPipeline(
            chi0=chi0,
            boson_gbs=boson_gbs,
            boson_dofs=boson_dofs,
            fermion_gfs=fermion_gfs,
            fermion_dofs=fermion_dofs,
            verbose=False,
        )
        alpha = float(model_obj.get_alpha())
        beta_H = float(model_obj.get_beta_H())
        Tr = float(model_obj.get_Tr())
    except Exception:
        return np.zeros_like(f, dtype=float)

    if not np.isfinite(alpha) or not np.isfinite(beta_H) or not np.isfinite(Tr):
        return np.zeros_like(f, dtype=float)
    if alpha <= 0 or beta_H <= 0 or Tr <= 0:
        return np.zeros_like(f, dtype=float)

    # Check for eternal inflation
    try:
        eternal = model_obj.get_check_eternal_inflation()
    except Exception:
        eternal = True
    if eternal:
        return np.zeros_like(f, dtype=float)

    # Compute spectrum
    try:
        h2OmegaGW = _spectrum.h2OmegaGW(f, Tr, alpha, beta_H)
    except Exception:
        return np.zeros_like(f, dtype=float)

    if not np.all(np.isfinite(h2OmegaGW)):
        h2OmegaGW = np.where(np.isfinite(h2OmegaGW), h2OmegaGW, 0.0)

    return h2OmegaGW