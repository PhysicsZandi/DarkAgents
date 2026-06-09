# Prior Audit Report: Classically Scale-Invariant Dark U(1)_D (u1conformal)

Agent: prior-agent. Run status: **warning**. Branch: fopt-pta.

Audited handoffs: librarian (ok), critic (warning), fopt (ok), pta (ok), constraints (warning).
Total audit items: **22** (assumptions, priors, approximations, uncertainties, caveats,
limitations, warnings). Full machine-readable details in `handoff_prior_audit.json`;
per-item table in `prior_audit_table.csv`.

## 1. Upstream pipeline status

| Handoff | Status | Note |
|---|---|---|
| librarian_preliminary | ok | Model well-covered (2501.11619, 2502.19478); theory uncertainties flagged. |
| critique | warning | Validated, no red flags, but 5 warnings and 3 unresolved clarification requests. |
| fopt | ok | Backend executed; 148/157 viable, 8 failed (incl. eternal inflation), 1 not_fopt. |
| pta | ok | Benchmark scan + PTArcade NG15 campaign (1e5 samples, dbf template) completed. |
| constraints | warning | Most constraints not yet applicable; 4 missing calcs; no exclusions of 1-sigma region. |

The chain completed end to end, but two stages carry `warning` status and the final
constraint stage cannot exclude or confirm the preferred region because of four missing
calculations. The reported NANOGrav-preferred region is therefore **provisional**.

## 2. Severity / control snapshot

- High-severity uncontrolled items (severity >= 8, controlled=false): **A05, A07, A17, A19, A20**.
- Highest single item: **A19** (four missing constraint calculations, severity 9) which gates
  essentially all cosmological and laboratory bounds (C02-C09).
- Most items in the FOPT/GW/inference categories are *controlled* approximations valid in the
  intended strong-supercooling regime; the dominant *uncontrolled* uncertainties are the
  effective-potential gauge dependence, the xi=1/epsilon tension, the missing dark-sector
  calculations, and the absence of an SMBHB foreground in the fit.

## 3. Main findings

**Model level.** Classical scale invariance and CW radiative breaking (A01) are structurally
sound and validated by the critic, contingent on lambda_HPhi <<1e-10 (A02) and epsilon ~0 (A03)
for the PT/GW dynamics. The minimal DM-free choice (A04) only affects quantitative transfer of
literature benchmarks.

**Central internal tension (A05, severity 8, uncontrolled).** xi = T_dark/T_visible = 1 feeds
g_* and the GW redshift, but a common temperature requires a nonzero portal, while both
lambda_HPhi and epsilon are set to zero. The sectors cannot thermalize with exactly zero portals.
Both the critic and constraint agents flag this; it can only be resolved by computing a minimum
epsilon (or alternative mechanism) and checking it against Delta Neff and laboratory bounds.

**FOPT (A07-A11).** The order-of-magnitude gauge dependence of the CW+thermal effective potential
(A07, severity 8, uncontrolled, 1707.06765) is the dominant theory uncertainty on Omega_GW. The
backend additionally omits RG running and daisy resummation (A08, mu=vev). The high-T expansion
(A09) and Gaussian percolation (A10) are judged valid in the supercooled regime. Very large alpha
(up to ~1e16) and eternal-inflation/percolation failures (A11) bound the viable window by physics.

**PTA / GW (A12-A18).** The dissipative bulk-flow (dbf) template (A12, 2511.15687) is the
physically motivated strong-supercooling choice; ksw=1 (A13) and the dbf amplitude/shape exponents
(A14) are template approximations. PTArcade priors (A15) are wide and the posterior does not touch
the edges. Sampler/ceffyl settings (A16) and inherited NG15 dataset assumptions (A18) are standard.
**A17 (severity 8, uncontrolled)** is a newly surfaced item from the literature check: this campaign
fits a model-only signal with **no SMBHB astrophysical foreground**, whereas the same-model
literature best-fits (2501.11619) add an SMBHB component, and NANOGrav new-physics conclusions
depend strongly on foreground modeling. The preferred region and any implicit model-vs-SMBHB
preference should be treated cautiously until refit with a foreground component.

**Constraints (A19-A22).** Four high-priority missing calculations (A19, severity 9): epsilon_min
for thermalization, dark-photon widths/lifetime/branchings (A'->rho rho vs visible), Delta Neff
(A21), and scalon relic + decay lifetime (A20). These gate constraints C02-C09; none currently
excludes the region, but they could exclude or confirm it. The scalon (lightest dark state,
11-24 MeV) is either stable and overclosing (epsilon=0) or long-lived and risking BBN/CMB injection
(epsilon!=0). Laboratory epsilon bounds (A22) are currently only order-of-magnitude bands.

## 4. Required follow-ups (unresolved, high-impact)

1. **F1 (high):** compute epsilon_min for xi=1 plus dark-photon widths/branchings/lifetime.
2. **F2 (high):** compute Delta Neff and confront Planck (strongest xi=1 test).
3. **F3 (high):** compute scalon relic abundance and lifetime (overclosure / BBN-CMB).
4. **F4 (high):** quantify and propagate the gauge-dependence band on Omega_GW.
5. **F5 (high):** refit PTArcade including an SMBHB foreground and report the Bayes factor.
6. **F6 (medium):** add RG running / daisy resummation; resolve critic thermal-mass clarification.
7. **F7 (medium):** validate PTArcade convergence (multi-chain) and cross-check ceffyl.
8. **F8 (low):** recast laboratory dark-photon bounds with darkcast once epsilon is known.

## Sources

- [NANOGrav 15yr: Search for Signals from New Physics (2306.16219)](https://arxiv.org/pdf/2306.16219)
- [PTArcade (2306.16377)](https://arxiv.org/pdf/2306.16377)
- [Chiang & Senaha, gauge dependence of GW from scale-invariant U(1)' FOPT (1707.06765)](https://arxiv.org/abs/1707.06765)
- [Goncalves et al. (2501.11619)](https://arxiv.org/abs/2501.11619)
- [Balan et al. (2502.19478)](https://arxiv.org/abs/2502.19478)
