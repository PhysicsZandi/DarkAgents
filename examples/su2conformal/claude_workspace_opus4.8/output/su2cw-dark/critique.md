# Critique: su2cw-dark

**Branch:** fopt-pta | **Origin:** proposer-agent (minimal fixes permitted) | **Status:** warning (no red flags)

## Summary

The model is a minimal classically conformal dark SU(2)_D gauge theory with one
complex scalar doublet, no fermions, scale invariance broken radiatively via
Coleman-Weinberg, producing a supercooled first-order phase transition targeting
NANOGrav. It is physically consistent at the level of field content, symmetries,
Lagrangian, CW dimensional transmutation, and FOPT backend mapping. **No red flags;
no fixes required.** Three non-blocking warnings are recorded for downstream agents.

## Checklist results

- **Gauge anomalies:** None possible. The model contains no fermions, so gauge and
  mixed gauge-gravitational anomalies cannot arise. OK.
- **Scale invariance:** Lagrangian has no dimensionful parameter; potential is pure
  quartic `lambda(Phi^dag Phi)^2`, no `mu^2` term. Conformal symmetry intact at
  tree level, broken by CW. OK.
- **SSB pattern / vev:** A single fundamental vev breaks SU(2)_D completely. dof
  balance verified: 10 before (4 scalar + 3x2 massless vectors) = 10 after
  (1 radial scalar + 3x3 massive vectors), 3 Goldstones eaten. vev convention
  `Phi=(1/sqrt2)(0,chi)^T` correctly identifies the broken vacuum. OK.
- **Field-dependent masses:** From the doublet kinetic term all three gauge bosons
  are degenerate, `m_W^2 = g^2 chi^2/4` (gb=g/2, dof=9). The 1/2 in m_W=g*chi/2 and
  the absence of spurious sqrt(2) factors were checked against the doublet
  convention. Radial scalar `m^2=beta_lambda*chi^2`. Both are SymPy-compatible
  strings. OK.
- **CW / dimensional transmutation:** `beta_lambda = (1/8pi^2)(sum_B dof*gb^4 -
  sum_F dof*gf^4) = (9*(g/2)^4 + gb_scalar^4)/(8pi^2)`. Matches the required
  model-independent form. With no fermions, `beta_lambda > 0` identically, ensuring
  radiative SSB and positive `m_chi^2 = beta_lambda*chi0^2`. Self-consistency
  checked numerically at g=1.37: scalar back-reaction shifts beta_lambda by
  <0.04% (0.025097 -> 0.025105). OK.
- **Parameter classification:** Independent {g, chi0}; dependent {lambda,
  beta_lambda, gb_scalar, m_chi}. The CW-fixed quartic lambda is correctly
  dependent and never scanned, as required for CW models. No dependent quantity is
  scanned as independent. OK.
- **Backend mapping:** `boson_gbs={'Wprime': g/2}`, `boson_dofs={'Wprime': 9}`, no
  fermions. The scalar (dof=1, gb=m_chi/chi0) is injected automatically by the
  backend `get_scalar_mass()` and must not be double-counted. Matches
  `backend/semianalytic_pipeline.py` `get_beta_lambda`/`get_coeffs`. OK.

## Warnings (non-blocking)

1. **Transition completion (FOPT viability).** Supercooled conformal FOPTs can fail
   to percolate/complete (false-vacuum domination), flagged by the librarian
   (2501.11619, 2502.19478). This is a viability check for the fopt-agent, not a
   Lagrangian inconsistency. The fopt-agent must verify completion, not merely
   nucleation.
2. **chi0 range.** Scan range [1e-4, 1e2] GeV is broad; PTA-band literature anchors
   (2109.11558) sit near MeV (chi0 ~ 1e-3 to 1 GeV). Permissive, not wrong.
3. **High-T expansion.** Backend uses the high-temperature thermal-potential
   expansion, whose accuracy degrades in deep supercooling. Inherited approximation.

## Fixes applied

None. The proposer model is internally consistent and backend-ready.

## Downstream clearance

**Cleared for fopt-agent and pta-agent.** No red flags remain. Authoritative model:
`output/su2cw-dark/model.md` / `output/su2cw-dark/handoff_model.json`.
