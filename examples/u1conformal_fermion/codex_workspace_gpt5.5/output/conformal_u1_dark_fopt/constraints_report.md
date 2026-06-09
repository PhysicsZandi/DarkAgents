# Constraint Report: conformal_u1_dark_fopt

## Input Region

Analysis mode: `ptarcade_1sigma`, with the 14/14 PTA benchmark points used only as supporting checks.

PTArcade 1-sigma posterior:

- `v_D = 0.6524223090101575 - 1.3946423272935458 GeV`
- `g_D = 0.2604596540094731 - 0.31488766085794484`
- `y_D = 0.11853518564406271 - 0.7049053385665409`

Derived ranges using the validated backend conventions:

- `m_X = 2 g_D v_D = 0.340 - 0.878 GeV`
- `m_psi = y_D v_D / sqrt(2) = 0.055 - 0.695 GeV`
- `beta_lambda = (3 (2 g_D)^4 - 4 (y_D/sqrt(2))^4)/(8 pi^2)`. The rectangular 1-sigma region includes a negative-beta corner, with corner range `-3.29e-4` to `5.97e-3`.
- Where `beta_lambda > 0`, a corner estimate gives `m_chi = sqrt(beta_lambda) v_D ~ 0.034 - 0.108 GeV`.

The backend fixes `lambda_HP = 0` and `epsilon = 0`. Therefore bounds requiring Higgs portal mixing, kinetic mixing, SM production, or visible decays are not direct exclusions of this backend model.

## Strongest Constraint Classes

The strongest directly relevant constraints are cosmological and theoretical, not laboratory limits:

- BBN and CMB `Delta N_eff` constraints are potentially important because the preferred FOPT region is sub-GeV and the transition occurs around tens of MeV in the benchmarks. They are not directly testable yet because the upstream handoffs do not provide the dark-sector temperature ratio, decoupling history, species abundances, or lifetimes.
- Percolation/completion and template validity are a high-priority theory check. The PTA best benchmark points include very large `alpha`, and the PTA handoff already warns that the DBF template is not strictly valid for the strongest/supercooled points.
- `beta_lambda > 0` is an immediate physical-region requirement. The independent rectangular PTArcade 1-sigma box includes beta-negative corners, so downstream interpretation should mask those points rather than treating the whole box as physical.

## Directly Testable Now

No published non-PTA constraint was applied as an exclusion with the current observables. The only approximately testable constraints are theory-side consistency checks using already available parameters:

- perturbativity of `g_D` and `y_D`;
- beta-lambda positivity;
- approximate percolation/completion warnings from the FOPT backend outputs.

## Not Applicable Under Exact-Zero Portals

Dark photon visible and invisible searches in the MeV-GeV range overlap the `m_X` range, but they assume nonzero kinetic mixing or another SM production channel. With exact `epsilon = 0`, they are not applicable as published.

Dark scalar beam-dump, Higgs-exotic, visible-decay and direct-detection constraints require a Higgs portal or scalar mixing. With exact `lambda_HP = 0`, they are not applicable as published.

## Missing Calculations

The required backend additions are:

- hidden-sector temperature history and `Delta N_eff` at BBN/recombination;
- decay widths and branching ratios for `X_mu`, `chi`, and `psi` if nonzero portals are ever enabled;
- relic abundance and stability analysis for the degenerate Majorana pair;
- velocity-dependent self-interaction cross sections and relic fraction;
- CMB/BBN energy-injection observables;
- RG running, Landau-pole scale, and Coleman-Weinberg validity diagnostics;
- stronger percolation/completion and wall-velocity validity checks for supercooled points.

## Sources Verified

- Marco Hufnagel, Kai Schmidt-Hoberg, Sebastian Wild, "BBN constraints on MeV-scale dark sectors. Part I. Sterile decays", arXiv:1712.03972.
- Marco Hufnagel, Kai Schmidt-Hoberg, Sebastian Wild, "BBN constraints on MeV-scale dark sectors. Part II. Electromagnetic decays", arXiv:1808.09324.
- Eleonora Di Valentino, Alessandro Melchiorri, Joseph Silk, "Cosmological constraints in extended parameter space from the Planck 2018 Legacy release", arXiv:1908.01391.
- Marco Fabbrichesi, Emidio Gabrielli, Gaia Lanfranchi, "The Dark Photon", arXiv:2005.01515.
- Thomas Hambye, Laurent Vanderheyden, "Minimal self-interacting dark matter models with light mediator", arXiv:1912.11708.
- Torsten Bringmann, Felix Kahlhoefer, Kai Schmidt-Hoberg, Parampreet Walia, "Strong constraints on self-interacting dark matter with light mediators", arXiv:1612.00845.
- R. Jinno, T. Konstandin, H. Rubira, J. van de Vis, "Supercool subtleties of cosmological phase transitions", arXiv:2212.07559.
