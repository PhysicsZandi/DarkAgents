"""
GW spectrum template selection for u1conformal (classically scale-invariant
dark U(1)_D, strongly supercooled FOPT).

TEMPLATE CHOICE: dissipative bulk flow ("dbf") from Lewicki et al. 2511.15687.

Reasoning
---------
The FOPT here is in the *strong supercooling* regime: from the FOPT handoff the
transition strength alpha spans alpha ~ 2 (at g_D ~ 0.9) up to alpha ~ 1e16
(at low g_D), with beta/H ~ 12-160. In this regime:

  * The energy budget is vacuum-dominated (alpha >> 1). The plasma trace anomaly
    is tiny compared to the released latent heat, so the long-lived *sound wave*
    picture underlying the "higgsless" template (2209.04369), which is calibrated
    on hydrodynamic simulations for moderate alpha <~ O(1) where the bulk of the
    energy is carried by the fluid, is NOT valid. Using "higgsless" here would
    extrapolate that template far outside its calibrated domain.

  * For strongly supercooled transitions the bubble walls accelerate to large
    Lorentz factors and the released energy is concentrated in thin shells around
    the bubbles. After collision these shells free-stream ("bulk flow"). The
    paper 2511.15687 is explicitly titled/aimed at "GW spectra from strongly
    supercooled first-order phase transitions" and provides the bulk-flow (bf)
    and dissipative-bulk-flow (dbf) templates for exactly this regime.

  * Between bf and dbf: the pure bulk-flow (bf) limit assumes free runaway walls
    with negligible interaction of the shells with the surrounding plasma. The
    dissipative bulk flow (dbf) includes dissipation/friction of the shells in
    the (dark) plasma. The model has a thermal dark plasma (A', scalar) so the
    shells are not fully collisionless; dbf is the more physically representative
    choice. bf is retained as a comparison/caveat (it gives a slightly different
    high-frequency slope and overall normalisation).

CAVEATS
-------
  * Order-of-magnitude theory uncertainty from gauge dependence of the CW+thermal
    potential (1707.06765) propagates into alpha, beta_H, Treh and hence the GW
    amplitude/peak.
  * Both bf and dbf use ksw (efficiency) = 1 here; in the runaway/vacuum-dominated
    limit essentially all energy goes into the scalar/shell motion, so K ~ alpha/
    (1+alpha) ~ 1, consistent with ksw=1.
  * The "dbf" amplitude scales as 1/beta_H^2 (thin-wall thin-shell counting in
    2511.15687); this is built into the backend Spectrum class.
"""

import os
import sys
import numpy as np

_HERE = os.path.dirname(__file__)
_BACKEND_DIR = os.path.abspath(os.path.join(_HERE, "..", "..", "backend"))
if _BACKEND_DIR not in sys.path:
    sys.path.insert(0, _BACKEND_DIR)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from spectrum import Spectrum  # noqa: E402
from fopt_model import evaluate_point  # noqa: E402

# Primary template for this strongly supercooled FOPT.
TEMPLATE = "dbf"


def spectrum_from_fopt(f, Treh, alpha, beta_H, template=TEMPLATE):
    """h^2 Omega_GW(f) from already-computed FOPT quantities."""
    spec = Spectrum(template=template)
    return spec.get_h2OmegaGW(np.asarray(f, dtype=float), Treh, alpha, beta_H)


def spectrum_from_params(f, v, g_D, template=TEMPLATE):
    """
    Full chain: (v, g_D) -> FOPT (actual backend) -> GW spectrum.
    Returns (h2OmegaGW array, fopt_result_dict). If the point is not a viable
    FOPT, returns a finite zero array and the result dict.
    """
    f = np.asarray(f, dtype=float)
    res = evaluate_point(v, g_D, verbose=False)
    if res["status"] != "viable":
        return np.zeros_like(f), res
    alpha = res["alpha"]
    beta_H = res["beta_H"]
    Treh = res["Treh"]
    if not (np.isfinite(alpha) and np.isfinite(beta_H) and np.isfinite(Treh)
            and alpha > 0 and beta_H > 0 and Treh > 0):
        return np.zeros_like(f), res
    h2 = spectrum_from_fopt(f, Treh, alpha, beta_H, template=template)
    h2 = np.where(np.isfinite(h2), h2, 0.0)
    return h2, res


if __name__ == "__main__":
    f = np.logspace(-9, -7, 50)
    for (v, g_D) in [(0.018, 0.55), (0.05, 0.65), (0.173, 0.65), (0.3, 0.7)]:
        h2, res = spectrum_from_params(f, v, g_D)
        print(f"v={v} g_D={g_D} status={res['status']} "
              f"alpha={res['alpha']:.3e} beta_H={res['beta_H']:.2f} "
              f"Treh={res['Treh']:.3e} peak_h2={np.max(h2):.3e} "
              f"f_at_peak={f[np.argmax(h2)]:.3e}")
