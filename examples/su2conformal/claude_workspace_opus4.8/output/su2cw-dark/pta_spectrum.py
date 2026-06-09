"""Model-specific GW spectrum wrapper for su2cw-dark.

Template choice
---------------
The su2cw-dark FOPT is a classically-conformal, Coleman-Weinberg, strongly
supercooled first-order phase transition. The viable FOPT points have very large
transition strength (alpha ~ 6 to ~930), vacuum-energy domination, and
relativistic / runaway bubble walls (vw -> 1). In this regime the latent heat is
carried by the scalar-field/bulk fluid motion (bulk flow) rather than by
long-lived acoustic sound waves.

- The "higgsless" (sound-wave) template is validated only up to alpha ~ 0.5
  (see SPECTRUM.md and 2209.04369) and is therefore OUT of its validity domain
  for this model.
- The bulk-flow / dissipative-bulk-flow template of 2511.15687 is built and
  validated for strongly supercooled transitions with very large alpha and
  includes cosmic-expansion effects on the spectral shape. This is the
  appropriate choice.

We use the dissipative-bulk-flow ("dbf") template as the default physical
choice (a steeper high-frequency falloff than pure bf, expected once plasma
dissipation acts on the relativistic shells). The "bf" template is kept
available as a cross-check.

Caveat: the templates are evaluated with the default efficiency factor ksw=1
and the redshift convention internal to backend/spectrum.py; alpha for some
points exceeds the largest values explicitly displayed in 2511.15687, so the
amplitude there is an extrapolation of the fitted amplitude relation.
"""

import sys
from pathlib import Path

import numpy as np

_BACKEND_DIR = Path(__file__).resolve().parents[2] / "backend"
if str(_BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(_BACKEND_DIR))

from spectrum import Spectrum  # noqa: E402

TEMPLATE = "dbf"


def make_spectrum(template=TEMPLATE):
    return Spectrum(template=template)


def h2OmegaGW(f, Treh, alpha, beta_H, template=TEMPLATE):
    """h^2 Omega_GW(f) for the su2cw-dark supercooled FOPT (dbf template)."""
    spec = Spectrum(template=template)
    return spec.h2OmegaGW(np.asarray(f, dtype=float), Treh, alpha, beta_H)
