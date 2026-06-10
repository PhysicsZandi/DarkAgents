# Constraint Report: scale-invariant-dark-u1-zprime (fopt-pta)

## Audited region (PTA-preferred)

PTArcade 1sigma posterior (NG15): g_D in [0.529, 0.653], y in [0.119, 0.638], w in [0.67, 1.46] GeV.
MAP point: g_D = 0.535, y = 0.294, w = 1.25 GeV.
Conservative mass span over the 3sigma posterior + four best benchmarks:

| Quantity | Range | MAP |
|---|---|---|
| m_Zp = g_D w | 0.30 - 2.17 GeV | 0.669 GeV |
| m_chi = y w / sqrt2 | 0.0 - 1.70 GeV | 0.260 GeV |
| m_scalon = sqrt(beta_lambda) w | 0.02 - 0.11 GeV | 0.068 GeV |
| T_reh (dark-sector) | 3.7 - 100 MeV | 99 MeV |

This is a GeV-scale dark sector with strong supercooling (alpha ~ 1e8-1e16, beta/H ~ 12-24).

## Central issue: epsilon = 0 is unphysical for cosmology

The FOPT and PTA analyses fixed kinetic mixing epsilon = 0 and Higgs portal lambda_portal = 0. With epsilon strictly 0 the dark sector is fully secluded and **cannot reheat the SM plasma**: the quoted T_reh is a dark-sector temperature only, and the model would fail BBN as pure dark radiation. A nonzero kinetic mixing **epsilon ~ 1e-6 to 1e-3 is physically required** to thermalize the dark sector with the SM and to dump the latent heat into the SM bath before BBN. This single hidden parameter activates essentially all of the experimental dark-photon constraints. The closest reference model (Balan et al., arXiv:2502.19478) treats exactly this and finds viable points with kappa ~ 2e-6 (coupled) to 3e-4 (secluded), yielding SM T_reh = 16.8-55.9 MeV.

## Most dangerous constraints

1. **BBN reheating (C1) + portal thermalization (C2)** - the make-or-break condition. Requires a portal energy-transfer calculation not present upstream. MAP dark T_reh ~ 99 MeV is comfortably above the ~3-4 MeV BBN floor *if* the portal thermalizes; the lowest benchmarks (dark T_reh ~ 3.7 MeV) are marginal.
2. **Delta N_eff (C3)** - dark radiation from the residual dark sector. Most dangerous in the y -> 0 subregion (e.g. rank1 benchmark with y = 0 exactly), where chi is massless and acts as permanent free-streaming dark radiation. Needs the dark/SM temperature ratio and species lifetimes.
3. **Dark photon visible-decay + beam-dump + SN1987A (C4-C6)** - once epsilon is fixed, the high-epsilon part (3e-4 to 2e-2) is excluded by BaBar/KLOE/LHCb, the low-epsilon visible tail (1e-8 to 1e-5) by E137/CHARM/NA64, and the light end (m_Zp 0.3-0.5 GeV, epsilon 1e-10 to 1e-6) by SN1987A. An intermediate window (epsilon ~ 1e-6 to 1e-4) survives for m_Zp ~ 0.3-0.7 GeV per the 2026 dark-photon review (arXiv:2603.08430) and coincides with the reheating-required range, so consistency must be checked jointly per point.
4. **chi relic abundance (C7)** - must not overclose; viable via secluded/forbidden annihilation in the reference model.

## Satisfied / not applicable

- **Perturbativity & vacuum stability (C10)**: directly satisfied throughout (g_D, y are O(1), well below 4pi; y^4 < 1.5 g_D^4 enforced per point). Constraint applied = true.
- **Percolation / no eternal inflation (C11)**: already verified by the FOPT backend (percolation_checked, eternal_inflation_checked = true). Applied = true.
- **Higgs invisible/exotic decay (C12)**: not applicable because lambda_portal = 0; would re-activate only if a Higgs portal is added.

## Does the MAP point survive?

Cannot be declared excluded, and cannot be declared safe, with current outputs. The MAP point (m_Zp = 0.67 GeV, m_chi = 0.26 GeV, m_scalon = 68 MeV, dark T_reh = 99 MeV) sits in the region that the reference model arXiv:2502.19478 finds cosmologically viable for kappa ~ few x 1e-6, with m_Zp in the open dark-photon window. The decisive observables (SM reheating temperature, Z' branching ratios/lifetime, Delta N_eff, chi relic abundance, scalon lifetime) are all functions of the unset epsilon and have not been computed in any upstream handoff. Per the no-false-exclusion rule, the MAP point is provisionally allowed but UNVERIFIED pending the five missing calculations below.

## Missing calculations (priority)

- **high**: portal reheating / SM T_reh (C1,C2); Z' decay widths/BR/lifetime (C4,C5,C6,C2,C3); Delta N_eff (C3).
- **medium**: chi relic abundance (C7,C8); scalon decay width/lifetime (C9,C3).

## Files

- /Users/mattezandi/Desktop/code/run_folder/claude_workspace/output/scale-invariant-dark-u1-zprime/handoff_constraints.json
- /Users/mattezandi/Desktop/code/run_folder/claude_workspace/output/scale-invariant-dark-u1-zprime/constraints_table.csv
- /Users/mattezandi/Desktop/code/run_folder/claude_workspace/output/scale-invariant-dark-u1-zprime/constraints_report.md

## Sources

- Balan et al., Sub-GeV dark matter and nano-Hertz GW from a classically conformal dark sector, arXiv:2502.19478
- Caputo & Essig, The Dark Photon: a 2026 Perspective, arXiv:2603.08430
- Chang, Essig, McDermott, Revisiting Supernova 1987A Constraints on Dark Photons, arXiv:1611.03864
- Costa et al., arXiv:2501.15649 (supercooled dark scalar PT / NANOGrav)
