# Validated Model: Classically Scale-Invariant Dark U(1)_D (u1conformal)

Status: VALIDATED with warnings (no red flags). Source: user-supplied, self-contained.
Branch: fopt-pta. Backend: `backend/semianalytic_pipeline.py`.

## 1. Field content and gauge group

| Field | Spin | Gauge rep | U(1)_D charge | dof |
|-------|------|-----------|---------------|-----|
| Phi (complex scalar, scalon) | 0 | SM singlet | +1 | 2 (rho + G) |
| A' (dark gauge boson) | 1 | — | gauge field | 2 -> 3 |

Gauge group: SM x U(1)_D. No new chiral fermions => no gauge/mixed anomalies.

## 2. Lagrangian

L_D = |D_mu Phi|^2 - lambda_Phi |Phi|^4 - (1/4) F'_munu F'^munu,  D_mu = d_mu - i g_D A'_mu.

Optional, assumed negligible for PT/GW: lambda_HPhi |H|^2|Phi|^2 and (epsilon/2) F'_munu F^munu.

## 3. Background/vev convention and SSB

Phi = (chi + rho + i G)/sqrt2. SSB: U(1)_D -> nothing. dof: 4 before = 4 after
(rho:1, massive A':3); Goldstone G eaten by A'.

## 4. Tree potential and CW dimensional transmutation

V_tree(chi) = lambda_Phi chi^4/4, with lambda_Phi a DEPENDENT parameter (renormalized
coupling at mu=v) fixed by V_eff'(v)=0. No tree-level mass term => classical scale invariance.

## 5. Spectrum (field-dependent masses)

- m_A'^2(chi) = g_D**2 * chi**2  (n_A' = 3)
- m_rho^2 = beta_lambda * v**2,  beta_lambda = (1/(8*pi**2))*(sum_b n_b g_b^4 - sum_f n_f g_f^4) = 3*g_D**4/(8*pi**2)
- m_G^2: unphysical (eaten), gauge-dependent, subdominant.

beta_lambda > 0 (boson-dominated) => radiative symmetry breaking realized.

## 6. Parameter basis

- Independent (scanned): v [GeV], g_D.
- Dependent: lambda_Phi (CW-fixed, computed by backend), m_A' = g_D v, m_rho = sqrt(beta_lambda) v.
- Fixed assumptions: xi = 1; lambda_HPhi, epsilon ~ 0 for PT/GW.

## 7. Backend mapping (semianalytic_pipeline.py)

Single-field scale-invariant, masses prop. to one vev, no tree mass term => compatible.
Input: chi0 = v (GeV); boson_gbs = {"Aprime": g_D}; boson_dofs = {"Aprime": 3};
empty fermion dicts. Do NOT pass lambda_Phi or scalar/Goldstone (computed internally).

## 8. Open clarifications (warnings)

1. Confirm lambda_Phi = renormalized quartic at mu=v fixed by V_eff'(v)=0, no implicit tree mass term.
2. Thermal/Debye masses handled by backend high-T expansion (Pi_A' ~ (g_D^2/3) T^2); no daisy/RG running (mu = vev).
3. xi=1 vs negligible portal/kinetic mixing tension; specify thermalization and dark dof added to g_*.
4. Theory uncertainty: gauge dependence of CW+thermal V_eff (~order of magnitude on Omega_GW).
5. Higgs portal must stay << 1e-10 to preserve conformality.
