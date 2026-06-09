# Constraint Map: minimal_conformal_su2_doublet

## Input Region

Primary region: PTArcade 1-sigma posterior from `ptarcade_bayes.json` / `handoff_pta.json`.

- `gD = 0.8528 - 0.9159`
- `log10_vD = -0.2217 - 0.1005`, so `vD = 0.600 - 1.260 GeV`
- Derived vector mass, using `m_WD = gD * vD / 2`: `m_WD = 0.256 - 0.577 GeV`
- Derived CW radial scalar mass estimate from the model handoff, `m_chi = sqrt(beta_lambda) vD`: `m_chi = 0.0368 - 0.0892 GeV`

Benchmark context only: the PTArcade MAP has `gD = 0.8632`, `log10_vD = 0.04455`, `vD = 1.108 GeV`, `m_WD = 0.478 GeV`, `Treh = 0.0978 GeV`, `alpha = 2.14e14`, and `beta/H = 13.98`. The MAP is not used as the primary constraint region.

## Model Features Relevant To Constraints

The new particles are three massive dark `SU(2)_D` vectors and one Coleman-Weinberg radial scalar. They are Standard Model singlets. The minimal model has Higgs portal coupling fixed to zero, no Abelian kinetic mixing before breaking, and no dark fermions. Therefore collider, fixed-target, beam-dump, and direct-detection constraints do not apply from mass alone.

The important unresolved cosmological question is whether the secluded sector was populated, what its temperature was relative to the Standard Model bath, and where the supercooled FOPT energy went. The PTA MAP is in a very strongly supercooled regime, so FOPT-template and cosmological-history caveats are leading limitations.

## Constraint Classification

Total constraints considered: 12.

- Direct consistency checks: 1
- Approximately testable: 0
- Recast needed: 0
- Requires new backend calculations: 7
- Not applicable in the minimal zero-portal model: 4

No parameter-space exclusion is claimed. The available handoffs provide masses, `gD`, FOPT quantities, and PTArcade fit information, but not the abundance, dark-sector temperature ratio, portal production rate, decay branching fractions, or self-interaction observables required for most constraints.

## Main Constraints

BBN/CMB thermal dark-sector bounds overlap the MeV-GeV scale but cannot be applied directly. Refined MeV-scale thermal relic analyses constrain light BSM states that are thermally coupled to the SM plasma; this model is secluded unless an additional portal or initial-condition assumption is added. Required calculations are `T_dark/T_SM`, abundance/energy density, entropy transfer, and branching fractions.

Dark radiation / `Delta N_eff` is relevant if the dark sector was populated or left relativistic relics. Planck gives tight constraints on `N_eff`, but the model handoffs do not provide a decoupling temperature or dark-sector temperature ratio.

Self-interacting dark matter constraints are relevant only if the dark vectors are stable and make up a non-negligible DM fraction. The preferred `m_WD` range is sub-GeV and `gD` is moderate, but the required observable is `sigma_T/m(v)` plus the relic fraction, not mass alone.

Higgs portal, direct detection, collider, and beam-dump searches are not applicable to the minimal model because the Higgs portal is fixed to zero and there is no non-Abelian kinetic mixing portal. These become relevant only for non-minimal extensions with explicit portal couplings and decay/production rates.

Basic perturbativity is directly checkable: `gD` in the 1-sigma region and at the MAP is below `sqrt(4*pi)`. This is a consistency check, not an experimental exclusion.

## Key Missing Calculations

- Dark-sector temperature ratio and decoupling history.
- BBN/CMB energy-density and entropy-injection likelihood inputs.
- Decay widths and branching fractions if any portal is added.
- Vector self-interaction transfer cross section `sigma_T/m(v)` at dwarf, galaxy, and cluster velocities.
- Relic abundance or fractional DM abundance of `W_D`.
- Reheating partition between visible radiation, dark radiation, and nonrelativistic dark states.
- Higher-order/RG validity checks for the strongly supercooled Coleman-Weinberg regime.

## Verified Sources

- Sabti, Alvey, Escudero, Fairbairn, Blas, "Refined Bounds on MeV-scale Thermal Dark Sectors from BBN and the CMB", arXiv:1910.01649.
- Sabti, Alvey, Escudero, Fairbairn, Blas, "Addendum: Refined bounds on MeV-scale thermal dark sectors from BBN and the CMB", arXiv:2107.11232.
- Planck Collaboration, "Planck 2018 results. VI. Cosmological parameters".
- Tulin and Yu, "Dark matter self-interactions and small scale structure", Physics Reports 730.
- "Dark Sectors 2016 Workshop: Community Report", arXiv:1608.08632.
- "US Cosmic Visions: New Ideas in Dark Matter 2017: Community Report", arXiv:1707.04591.
- Arcadi et al., "The Higgs-portal for dark matter: effective field theories versus concrete realizations".

## Warnings

- Strong supercooling at the PTA MAP makes gravitational-wave template validity and thermal-history assumptions central.
- The CSV/JSON table deliberately marks portal searches as not applicable for the minimal model, even though the mass range overlaps many light-dark-sector searches.
- One decoupled-hidden-sector source was used from metadata/search context only and is marked citation-unverified in the JSON/CSV.
