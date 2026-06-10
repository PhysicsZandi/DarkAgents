# Constraint report: u1conformal

## Input region

Analysis mode: `ptarcade_1sigma`, using `output/u1conformal/ptarcade_bayes.json`.

The 68% PTArcade posterior region is:

| parameter | low | high |
| --- | ---: | ---: |
| `v` [GeV] | 0.5364446220 | 1.4744990631 |
| `g_D` | 0.5230639417 | 0.5739085244 |

Using the validated conventions `m_Aprime = g_D * v`, `beta_lambda = 3*g_D**4/(8*pi**2)`, and `m_rho = sqrt(beta_lambda) * v`, the rectangular 1 sigma mass ranges are:

| derived quantity | low | high |
| --- | ---: | ---: |
| `m_Aprime` [GeV] | 0.2805948385 | 0.8462275816 |
| `beta_lambda` | 0.0028441379 | 0.0041219453 |
| `m_rho` [GeV] | 0.0286088382 | 0.0946663458 |

At the MAP point, `v = 1.3387506947 GeV` and `g_D = 0.5357342712`, giving `m_Aprime = 0.7172146277 GeV`, `beta_lambda = 0.0031298912`, and `m_rho = 0.0748969839 GeV`.

## Main classification

No laboratory, supernova, BBN, CMB, or direct-detection exclusion is applied to the PTArcade-preferred region. The reason is not lack of mass overlap. It is that the required observables are not in the upstream handoffs: `epsilon`, `lambda_HP`, scalar-Higgs mixing, lifetimes, visible and invisible branching fractions, production rates, relic/freeze-in abundances, temperature-ratio evolution, and detector acceptances.

Summary:

| class | count |
| --- | ---: |
| direct | 2 |
| approximate | 2 |
| recast_needed | 1 |
| requires_new_backend | 11 |
| not_applicable | 2 |

The directly checked items are theory-validity checks: perturbativity and anomaly/degree-of-freedom consistency. Both pass in the 1 sigma region. They are not experimental exclusions.

## Constraint map

Dark photon accelerator searches overlap the derived `m_Aprime` range. BaBar visible searches cover a broad 0.02-10.2 GeV mass range and set limits on the kinetic mixing for `A_prime -> e+e-, mu+mu-`, while LHCb covers prompt dimuon dark photons from threshold to high masses and a displaced low-mass window. These are not applicable from mass alone. They require `epsilon`, the total width, visible branching ratios, and the prompt/displaced lifetime regime.

Fixed-target and beam-dump searches are also relevant to `m_Aprime = 0.28-0.85 GeV`, but need experiment-specific production and decay probabilities. A DarkCast-style recast is the right backend once the kinetic-mixing and decay table are defined.

Invisible dark photon searches are only a conditional recast target. The minimal validated model has no specified light dark matter state. An invisible search would require an actual invisible final state or a long-lived dark-sector particle, plus `BR(A_prime -> invisible)`.

The light scalar `rho` lies at `29-95 MeV`. This overlaps light Higgs-portal scalar cosmology, rare-meson, and beam-dump regimes. The missing quantities are the Higgs-portal coupling `lambda_HP`, scalar-Higgs mixing angle, scalar decay widths, scalar branching fractions, and production rates. Since `m_rho < 2*m_Aprime` throughout the preferred region, decays to two on-shell dark photons are closed; visible decays are portal controlled.

BBN, CMB, and `Delta N_eff` are high-priority. The FOPT/PTA calculation assumes `xi = T_dark/T_visible = 1`, while the visible-sector portals are assumed negligible for FOPT. A quantitative cosmological test needs the thermalization rate versus Hubble, decoupling temperature, dark/visible temperature evolution, mediator lifetimes, branching fractions, and freeze-in or residual abundances. None of these are available upstream.

Ordinary stellar-cooling bounds are classified as not applicable because both new particles are far heavier than keV stellar core temperatures. SN1987A is treated separately as approximate: the `m_Aprime` range is above the strongest low-mass supernova region, but the lower edge could merit a dedicated in-medium production/trapping check if `epsilon` is specified.

Direct detection is not applicable to the minimal no-fermion model as a dark-matter model. If `rho` is later promoted to metastable dark matter, direct and indirect detection must be reopened with a relic abundance, local density fraction, lifetime, and scattering rates.

## Missing backend modules

The highest-priority additions are:

1. Dark photon decay and production module: computes `Gamma(A_prime -> e+e-, mu+mu-, hadrons)`, total width, decay length, and production rates as functions of `epsilon`.
2. Dark Higgs portal module: maps `lambda_HP` to scalar-Higgs mixing, `rho` widths, branching ratios, Higgs exotic decays, and meson-production rates.
3. Thermal-history module: computes thermalization, decoupling, `xi(T)`, freeze-in/residual yields, lifetimes, BBN/CMB energy injection, and `Delta N_eff`.
4. Recast module for accelerator searches: BaBar, LHCb, NA64, visible beam dumps, fixed-target searches, and rare meson decays.
5. FOPT validity module: posterior-level percolation/reheating checks, gauge-dependence variations, wall-friction/runaway classification, and spectrum-template validity flags.

## Literature used

- BaBar Collaboration, "Search for a dark photon in e+e- collisions at BABAR", arXiv:1406.2980.
- J. P. Lees on behalf of BaBar, "Search for Invisible Decays of a Dark Photon Produced in e+e- Collisions at BaBar", arXiv:1702.03327.
- LHCb Collaboration, "Search for dark photons produced in 13 TeV pp collisions", arXiv:1710.02867.
- Philip Ilten, Yotam Soreq, Mike Williams, Wei Xue, "Serendipity in dark photon searches", arXiv:1801.04847.
- Marco Battaglieri et al., "US Cosmic Visions: New Ideas in Dark Matter 2017: Community Report", arXiv:1707.04591.
- C. Antel et al., "Feebly Interacting Particles: FIPs 2022 workshop report", arXiv:2305.01715.
- Joshua Berger, Karsten Jedamzik, Devin G. E. Walker, "Cosmological Constraints on Decoupled Dark Photons and Dark Higgs", arXiv:1605.07195.
- Anthony Fradette, Maxim Pospelov, Josef Pradler, Adam Ritz, "Cosmological beam dump: constraints on dark scalars mixed with the Higgs boson", arXiv:1812.07585.
- Cameron Mahoney, Adam K. Leibovich, Andrew R. Zentner, "Updated Constraints on Self-Interacting Dark Matter from Supernova 1987A", arXiv:1706.08871.
- Sowmiya Balan, Torsten Bringmann, Felix Kahlhoefer, Jonas Matuszak, Carlo Tasillo, "Sub-GeV dark matter and nano-Hertz gravitational waves from a classically conformal dark sector", arXiv:2502.19478.
- Kohei Fujikura, Sudhakantha Girmohanta, Yuichiro Nakai, Motoo Suzuki, "NANOGrav Signal from a Dark Conformal Phase Transition", arXiv:2306.17086.
- Wan-Zhe Feng, Zi-Hui Zhang, "Gauge-independent gravitational waves from a minimal dark U(1) sector with viable dark matter candidates", arXiv:2602.14866.
