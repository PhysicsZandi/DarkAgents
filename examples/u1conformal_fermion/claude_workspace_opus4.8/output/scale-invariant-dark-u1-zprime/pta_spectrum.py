"""Spectrum-template selection and helper for the scale-invariant dark U(1)_D
(Coleman-Weinberg) model.

TEMPLATE CHOICE: dissipative bulk flow ("dbf"), from arXiv:2511.15687
(Lewicki et al., "Gravitational waves from strongly supercooled first-order
phase transitions").

REASONING
---------
The FOPT in this classically scale-invariant CW model is *strongly supercooled
and vacuum-dominated*. From the FOPT handoff the viable in-band points have:
  - alpha ~ 1e12 - 1e16  (energy budget completely dominated by the latent/
    vacuum energy; alpha >> 1),
  - beta_H ~ 12 - 17      (slow transition, large mean bubble radius),
  - runaway bubble walls   (vw -> 1; no terminal velocity in vacuum domination).

In this regime the standard sound-wave (fluid) picture used by the "higgsless"
template (arXiv:2209.04369) is NOT valid: that template is derived for
fluid-driven deflagrations/detonations with non-runaway walls and a sound-wave
source, where only a fraction kappa_sw of a *moderate* alpha is converted to
bulk fluid motion. For alpha >> 1 with runaway walls the GW source is the bulk
flow of the scalar field / dark-sector fluid, not long-lived sound waves.

arXiv:2511.15687 is explicitly designed for *strongly supercooled* transitions
and provides two templates:
  - "bf"  : pure (non-dissipative) bulk flow,
  - "dbf" : dissipative bulk flow.
Because the dark sector here contains a thermalised dark gauge boson (Z') that
couples to and is pushed by the wall, energy injected into the bulk flow is
partly dissipated into the dark plasma. The dissipative bulk-flow ("dbf")
template is therefore the most physically appropriate choice; the pure "bf"
template is retained as a cross-check (it gives a nearly identical peak with a
slightly different low-frequency slope).

CAVEATS
-------
- Wall velocity is taken as vw -> 1 (runaway), consistent with vacuum
  domination; the dbf/bf amplitude and peak frequency in spectrum.py depend on
  T (=Treh), alpha and beta_H only (vw enters via the runaway assumption built
  into the template), so no explicit vw is passed.
- The dbf amplitude saturates for alpha >> 1 (it enters through
  K_sw = ksw*alpha/(1+alpha) -> 1), so the extreme alpha values are handled
  gracefully and do not blow up.
- T = Treh (reheating temperature) is used as the redshift temperature, matching
  the FOPT backend convention (temperature_key = "Treh").
"""

import sys
from pathlib import Path
import numpy as np

_BACKEND = Path("/Users/mattezandi/Desktop/code/run_folder/claude_workspace/backend")
if str(_BACKEND) not in sys.path:
    sys.path.insert(0, str(_BACKEND))

from spectrum import Spectrum  # noqa: E402

TEMPLATE = "dbf"  # dissipative bulk flow (arXiv:2511.15687)
_SPECTRUM = Spectrum(template=TEMPLATE)


def omega_gw(f, Treh, alpha, beta_H):
    """h^2 Omega_GW(f) using the dbf template. Returns finite zeros on bad input."""
    f = np.atleast_1d(np.asarray(f, dtype=float))
    if not (np.isfinite(Treh) and np.isfinite(alpha) and np.isfinite(beta_H)):
        return np.zeros_like(f)
    if Treh <= 0 or alpha <= 0 or beta_H <= 0:
        return np.zeros_like(f)
    try:
        out = _SPECTRUM.get_h2OmegaGW(f, Treh, alpha, beta_H)
    except Exception:
        return np.zeros_like(f)
    out = np.asarray(out, dtype=float)
    out[~np.isfinite(out)] = 0.0
    return out
