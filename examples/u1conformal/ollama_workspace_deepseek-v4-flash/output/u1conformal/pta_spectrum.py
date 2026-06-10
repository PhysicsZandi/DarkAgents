"""
PTA spectrum template for the Dark U(1)_D conformal model.

Template selection rationale:
- The FOPT parameters show very strong supercooling: alpha ranges from ~200 to 10^15,
  with beta/H ~ 20-500 and T_reh ~ 0.001-10 GeV (MeV-GeV scale).
- The "higgsless" (sound wave, LISA 2024 / 2209.04369) template is designed for weaker
  phase transitions where sound waves are the dominant GW source and alpha ~ O(1).
- For strong supercooling (alpha >> 1), the bubble dynamics are qualitatively different:
  the bubbles run away (vw -> 1) and the dominant GW source is bulk flow, not sound waves.
  The "dissipative bulk flow" (dbf) template from Lewicki et al. 2025 (arXiv:2511.15687)
  is designed for this regime and accounts for dissipation during bubble expansion.

Selected template: "dbf" (dissipative bulk flow, Lewicki 2025).

Caveats:
- The dbf template assumes runaway walls (vw -> 1), which is appropriate for very strong
  supercooling where the vacuum energy dominates and there is no significant friction.
- The template includes a spectral shape with low-frequency slope of f^2 (causality) and
  high-frequency falloff, which matches the expected physical behavior.
- For the extreme alpha values (10^5-10^15), the K_sw = alpha/(1+alpha) ~ 1, so the
  amplitude scaling saturates.

Usage:
    from pta_spectrum import get_spectrum
    h2Omega = get_spectrum(f, Treh, alpha, beta_H)
"""
import sys
import os
import numpy as np

# Add backend directory to path
_backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "backend")
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

from spectrum import Spectrum

# Selected template
TEMPLATE = "dbf"


def get_spectrum(f, Treh, alpha, beta_H):
    """
    Compute GW spectrum using the selected template.

    Parameters
    ----------
    f : array-like
        Frequency array in Hz.
    Treh : float
        Reheating temperature in GeV.
    alpha : float
        Phase transition strength.
    beta_H : float
        Characteristic timescale (inverse duration).

    Returns
    -------
    h2OmegaGW : ndarray
        h^2 * Omega_GW(f) values.
    """
    spectrum = Spectrum(template=TEMPLATE)
    return spectrum.get_h2OmegaGW(np.asarray(f, dtype=float), float(Treh), float(alpha), float(beta_H))