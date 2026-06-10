# Critique: scale-invariant-dark-u1-zprime

Branch: fopt-pta. Source: proposer-agent (deterministic fixes permitted).
Result: **run_status = ok** (no unresolved red flags). Two minimal deterministic fixes applied.

## 1. Gauge anomalies (dark fermion sector)

Weyl charges (as written): psi_L (+1/2), psi_R (-1/2), eta_L (-1/2), eta_R (+1/2).
Recast as left-handed Weyl fermions (conjugating the right-handed ones):
psi_L (+1/2), (psi_R)^c (+1/2), eta_L (-1/2), (eta_R)^c (-1/2).

- U(1)_D^3: sum q^3 = 1/8 + 1/8 - 1/8 - 1/8 = 0. Cancels.
- Mixed gauge-gravitational (sum q): 1/2 + 1/2 - 1/2 - 1/2 = 0. Cancels.

The spectrum is vector-like (psi = Dirac with q=+1/2, eta = Dirac with q=-1/2), so all
U(1)_D anomalies vanish exactly. The mirror partner eta does its job. **OK.**

## 2. Classically scale-invariant / Coleman-Weinberg construction

- No tree-level mass scale: potential is purely `-lambda (Phi*Phi)^2`, i.e. `(lambda/4) chi^4`
  along the radial direction. No mu^2 term. **OK.**
- CW quartic is correctly classified as a **dependent** parameter (fixed by CW minimization).
- beta_lambda = (1/(8 pi^2))(3 g_D^4 - 8 (y/sqrt2)^4) matches the model-independent form
  `sum_B n_B gb^4 - sum_F n_F gf^4` with n_B = 3 (Zp), n_F = 8 (two Dirac fermions, 4 dof each),
  gb = g_D, gf = y/sqrt(2). **OK.**
- Radiative SB requires beta_lambda > 0, i.e. `3 g_D^4 > 8 (y/sqrt2)^4`, i.e. `y^4 < 1.5 g_D^4`.
  The proposed independent ranges (g_D in [0.1,1.5], y in [0,1]) allow violations.
  **FIX applied:** added the hard constraint `y^4 < 1.5 g_D^4` to the independent y parameter.
- Radial (scalon) mass `m_chi_radial = sqrt(beta_lambda) * w` is the standard CW result. **OK.**

## 3. Lagrangian gauge invariance and spectrum

- Yukawa charge balance: q(Phi)+q(psi_R)-q(psi_L) = 1 - 1/2 - 1/2 = 0 (and same for eta).
  Gauge invariant. **OK.**
- Field-dependent masses, with Phi = chi/sqrt(2):
  - Zp: m_Zp^2 = g_D^2 chi^2 (real vector, 1/2 factor handled). Matches m_Zp = g_D w. **OK.**
  - Dirac fermions: m = y chi/sqrt(2), m^2 = (y^2/2) chi^2, dof = 8. Matches m_chi = y w/sqrt(2). **OK.**
- DOF bookkeeping across SSB: complex Phi (2) -> 1 radial scalar + 1 Goldstone eaten;
  massless Zp (2) -> massive Zp (3); total bosonic dof 4 -> 4. **OK.**

## 4. Backend (fopt-pta) compatibility

Single classically scale-invariant scalar, all masses proportional to w, no tree mass term,
CW-fixed quartic dependent. Mapping chi0=w, boson gb=g_D (dof 3), fermion gf=y/sqrt(2) (dof 8)
is correct for `semianalytic_pipeline`. Thermal Debye mass supplied as SymPy-parseable string
(informational; backend rebuilds the barrier internally). **OK.**

## 5. VEV / scale range vs the nanohertz PTA band (key consistency flag)

The proposed independent range `w in [100, 1e6] GeV` is 1-4 orders of magnitude **above** the
literature window that produces a nHz signal:
- arXiv:2502.19478: v = 92.9 MeV (Point A), 343 MeV (Point B).
- arXiv:2501.15649: v = 0.5-10 GeV.
- arXiv:2501.11619: m_Zp = 107 MeV at g_D = 0.59.

At w >~ TeV the GW peak frequency lands well above the PTA band, so the proposed range cannot
realistically yield a NANOGrav-band signal. **FIX applied:** restricted `w` to `[0.05, 10] GeV`,
which brackets all literature benchmarks with margin. This is a minimal one-parameter range change;
gauge group, field content, and Lagrangian are untouched.

## Fixes (deterministic, minimal)

1. `w`: [100, 1e6] GeV -> [0.05, 10] GeV (nHz-band viability).
2. `y`: added constraint `y^4 < 1.5 g_D^4` (ensures beta_lambda > 0, radiative SB).

## Warnings (non-blocking)

- Apply `y^4 < 1.5 g_D^4` as a hard cut in the downstream scan; discard violating points.
- Only strongly supercooled points within [0.05,10] GeV reach the nHz band; verify Tp/alpha/beta_H
  per point and exclude eternal-inflation regions.
- Structurally non-novel (closest: arXiv:2502.19478); distinctive features are the mirror fermion
  eta and the neglect of kinetic mixing.

## Red flags

None. Authoritative post-critic model: `output/scale-invariant-dark-u1-zprime/handoff_model.json`.
