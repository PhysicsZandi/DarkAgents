# Constraint Analysis - su2cw-dark (fopt-pta)

## PTA-preferred region (PTArcade 1-sigma, NG15)

| Quantity | Low | MAP | High |
|---|---|---|---|
| g | 0.852 | 0.866 | 0.916 |
| chi0 (GeV) | 0.605 | 1.122 | 1.281 |
| m_W = g*chi0/2 (GeV) | 0.258 | 0.486 | 0.586 |
| m_chi = sqrt(beta_lambda)*chi0 (GeV) | 0.037 | 0.071 | 0.091 |
| beta_lambda | 0.0038 | 0.0040 | 0.0050 |
| Treh / T_star (spectrum conv., GeV) | ~0.04 | ~0.1 | ~0.14 |

Particles in scope: three degenerate dark gauge bosons W_D (m ~ 0.26-0.59 GeV, vector DM candidate) and the CW pseudo-dilaton chi (m ~ 37-91 MeV). Note **m_chi < m_W throughout**, so chi -> W_D W_D is kinematically closed across the entire preferred region.

## Central structural issue: the missing portal

`handoff_model.json` assumes the dark sector is in thermal equilibrium with the SM (xi = 1) but specifies **no portal**. Equilibrium and, crucially, draining the supercooled latent heat into the SM both require a portal. In pure non-abelian SU(2)_D:
- kinetic mixing is forbidden at renormalizable level (no abelian factor to mix with);
- a Higgs portal |Phi|^2|H|^2 breaks the classical conformal invariance that the entire Coleman-Weinberg mechanism relies on.

This unresolved choice controls almost every cosmological and astrophysical bound below. The closest sister model (2502.19478, conformal U(1)' with a dark photon) needs kinetic mixing kappa ~ 1e-6..1e-4 precisely to keep thermal contact and decay the dark sector to e+e- before BBN. That mechanism is unavailable to a pure SU(2)_D model without adding fields.

## Binding constraints

1. **BBN reheating (C1, approximate).** The SM photon-neutrino bath must reheat above ~2-4.7 MeV after the transition. The PTA-preferred points have T_star ~ 40-140 MeV (above the bound) **but only if that energy reaches the SM bath**. In the strictly secluded model the SM bath is not reheated at all, effectively violating the bound. Requires computing the SM-only reheating temperature including dark->SM energy transfer (not in any handoff).

2. **Dark radiation / Neff (C2, requires_new_backend).** A completely secluded dark-sector FOPT is "strongly disfavoured" (2306.09411), with Delta Neff > 0.22 excluded at 95% CL. The required xi(T) and Delta Neff are not computed upstream.

3. **Portal / thermalization (C3, requires_new_backend).** Foundational; determines whether C1, C2, C5-C9, C11 are evaluated in the equilibrium or secluded regime. The model is under-specified here and should be referred back to proposer/critic.

## Conditional constraints (apply only once a portal is specified)

- **Beam dump (C7, recast):** for a kinetic-mixing portal, m_W ~ 0.26-0.59 GeV overlaps E137/CHARM/nu-cal coverage; the epsilon ~ 1e-6..1e-4 window needed for thermal contact overlaps the excluded band - a genuine tension.
- **SN1987A (C8, recast):** relevant mainly for m_chi ~ 37-91 MeV and epsilon ~ 1e-9..1e-6 if these states couple to the SM.
- **Direct detection (C9, not_applicable):** no DM-SM coupling in the secluded model; sub-GeV DM evades current heavy-WIMP limits even with a small portal.
- **Higgs-portal collider (C11, recast):** would induce h->invisible but breaks conformal invariance - records the portal trade-off.

## Constraints evaluable with existing inputs

- **Transition completion (C4, applied/passed):** fopt-agent verified Tp finite and eternal_inflation = False for all viable points; pta-agent confirmed viability across the 1-sigma window.
- **Vector-DM relic (C5, requires_new_backend):** if W_D is the DM, abundance must satisfy Omega h^2 <= 0.12; in 2109.11558 (same model) this is set non-thermally via scalar-portal mixing - again needs the portal.
- **DM self-interaction (C10, requires_new_backend):** g, m_W and the lighter mediator m_chi are all available; sub-GeV vector DM with O(1) coupling and a ~10x lighter mediator can be strongly self-interacting (sigma/m <~ 1 cm^2/g). Only the cross-section computation is missing.

## Missing calculations (priority)

- HIGH: SM-bath reheating temperature with dark->SM energy transfer (C1, C2).
- HIGH: dark-to-SM temperature ratio xi and Delta Neff at BBN/CMB (C2, C6).
- HIGH: portal operator/coupling and thermalization rate vs Hubble, with conformal-breaking check (C1, C2, C3, C5-C9, C11).
- HIGH: W_D vector-DM relic abundance and W_D stability/lifetime (C5).
- MEDIUM: chi decay width, lifetime and abundance for BBN/CMB injection (C6).
- MEDIUM: W_D self-interaction cross section per mass (C10).

## Does the PTA-preferred region survive?

**Not decided - conditional.** No point can yet be declared excluded because the binding observables (SM reheating temperature, Delta Neff, relic abundance) have not been computed. The decisive question is the **portal**:
- As written (strictly secluded), the region is **strongly disfavored** by dark-radiation/Neff and BBN reheating arguments (C1, C2, C3) - but this requires the xi/Neff and SM-reheating calculations to be made quantitative before a hard exclusion.
- With a minimal kinetic-mixing portal (requires adding a U(1)), the region can in principle survive BBN/Neff, but then **beam-dump (C7) and supernova (C8) bounds bite the same coupling window**, and the relic abundance (C5) must be checked.

Recommendation: refer the portal question to the proposer/critic and run the HIGH-priority calculations (SM reheating, Delta Neff, relic) before any exclusion claim.

## Sources

- Bai, Korwar, Cosmological constraints on first-order phase transitions, arXiv:2109.14765 (PRD 105, 095015).
- de Salas et al., Bounds on very low reheating scenarios after Planck, arXiv:1511.00672.
- Bringmann et al., Does NANOGrav observe a dark sector phase transition?, arXiv:2306.09411.
- Balan, Bringmann, Kahlhoefer, Matuszak, Tasillo, Sub-GeV DM and nano-Hz GW from a classically conformal dark sector, arXiv:2502.19478 (JCAP 08 (2025) 062).
- Goncalves, Marfatia, Morais, Pasechnik, Supercooled phase transitions in conformal dark sectors, arXiv:2501.11619.
- Borah, Dasgupta, Kang, First-order dark SU(2)_D PT with vector DM (NANOGrav 12.5yr), arXiv:2109.11558.
- Kazanas et al., Supernova bounds on the dark photon, arXiv:1410.0221.
- Dark-photon kinetic-mixing compilation, arXiv:2507.11163.
- Tulin, Yu, Dark matter self-interactions, arXiv:1705.02358.
