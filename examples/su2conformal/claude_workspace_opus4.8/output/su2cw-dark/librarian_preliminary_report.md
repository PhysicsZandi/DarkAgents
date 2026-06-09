# Preliminary Literature Search — su2cw-dark

**Model:** Classically conformal (scale-invariant) dark SU(2)_D with one complex scalar doublet, no fermions, Coleman-Weinberg dimensional transmutation, supercooled sub-GeV FOPT, vector dark matter; target signal = NANOGrav 15yr nano-Hz GW background.

**Sources searched:** arXiv, INSPIRE-HEP (via web), publisher pages (JCAP/PRD/PLB/EPJC), NASA ADS.

## Novelty verdict: NOT NOVEL

The su2cw-dark model is essentially the model of **Borah, Dasgupta & Kang (arXiv:2109.11558)**, which already realized a classically conformal dark SU(2)_D with a single complex doublet, CW radiative breaking, and a supercooled sub-GeV FOPT fitting the NANOGrav 12.5yr signal. The conformal/supercooled-FOPT-for-NANOGrav approach has since been pushed to the 15yr dataset in closely related conformal U(1)' models. The genuinely new task element is fitting the SU(2)_D (non-Abelian) realization specifically to NANOGrav 15yr.

## Key references and benchmark points

### 1. arXiv:2109.11558 — same model (relevance 10, verified)
Borah, Dasgupta, Kang, *A first order dark SU(2)_D phase transition with vector dark matter in the light of NANOGrav 12.5 yr data*, Phys. Rev. D 104, 063501 (2021).
- Conventions match the proposer: `<Phi> = M/sqrt(2)`, `M_ZD = g_D M/2` == `m_W = g*chi/2`; `g_D` == `g`, `M` == `chi0`.
- Benchmarks (NANOGrav 12.5yr, 95% CL):
  - Scenario 1: g_D = 1.37, M_ZD = 8.23 MeV (=> chi0 ~ 12 MeV), T* = 1.8 MeV, alpha = 0.45, beta/H = 143.
  - Scenario 2: g_D = 1.37, M_ZD = 817 keV (=> chi0 ~ 1.2 MeV), T* = 190 keV, alpha = 0.36, beta/H = 151.
- **Direct** benchmark anchor; needs re-fit to the 15yr posterior. Note: modest alpha ~ O(0.4), strong coupling g_D near the proposer upper edge (g <= 1.5).

### 2. arXiv:2502.19478 — structurally similar (relevance 8, verified)
Balan, Bringmann, Kahlhoefer, Matuszak, Tasillo, *Sub-GeV dark matter and nano-Hertz gravitational waves from a classically conformal dark sector*, JCAP 08 (2025) 062.
- Conformal dark **U(1)'** (not SU(2)) + dark Higgs + fermionic DM; `m_A' = g v` (Abelian convention differs).
- Targets NANOGrav **15yr** directly. Benchmarks:
  - Point A (coupled): g=0.677, v=173 MeV, Tp=2.28 MeV, alpha=4.7e3, beta/H=33.7.
  - Point B (secluded): g=0.601, v=692 MeV, Tp=1.21 MeV, alpha=9.48e6, beta/H=18.0.
- **Adaptable** only: gauge group/dof differ, so alpha/beta not one-to-one, but they bracket the deep-supercooling FOPT magnitudes for the PTA band.

### 3. arXiv:2501.11619 — same target, different model (relevance 6, metadata-only)
Goncalves, Marfatia, Morais, Pasechnik, *Supercooled phase transitions in conformal dark sectors explain NANOGrav data*, Phys. Lett. B 869 (2025) 139829.
- Conformal dark U(1)' supercooled FOPTs for the NANOGrav signal. Confirms the landscape and flags transition-completion subtleties. No numerical benchmarks extracted.

### 4. arXiv:1907.08899 — structurally similar, wrong scale (relevance 5, metadata-only)
Mohamadnejad, *Gravitational waves from scale-invariant vector dark matter model: probing below the neutrino-floor*, Eur. Phys. J. C 80, 197 (2020).
- Same SU(2)+doublet+CW structure (vector triplet DM), but at the **electroweak scale** => mHz LISA band, NOT PTA. Useful for effective-potential/FOPT methodology (tree + CW + thermal + daisy) only; **benchmarks not usable** for the PTA target.

## Convention notes / caveats
- SU(2) gauge boson mass `m_W = g*chi/2` (proposer, 2109.11558) vs Abelian `m_A' = g v` (2502.19478) — mind the factor when importing benchmarks.
- PTA-band requirement => MeV-scale vev: literature points sit at chi0 ~ 1e-3 to 1e0 GeV, i.e. the lower-middle of the proposer chi0 range [1e-4, 1e2] GeV.
- Two FOPT regimes appear: modest-alpha O(0.4) (SU(2)_D, 12.5yr) vs extreme supercooling alpha >> 1 (U(1)', 15yr). Worth checking which better matches the 15yr posterior.
- Supercooled conformal FOPTs raise transition-completion / percolation concerns (flagged in 2501.11619, 2502.19478).

## Recommended next steps
- Anchor FOPT validation on arXiv:2109.11558 (same SU(2)_D model): g_D=1.37, chi0 ~ 1-12 MeV, alpha ~ 0.4, beta/H ~ 140-150, Tn ~ 0.2-2 MeV.
- Use arXiv:2502.19478 to gauge the 15yr-targeted deep-supercooling regime and compare modest- vs extreme-alpha fits.
