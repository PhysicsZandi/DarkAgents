# Preliminary Literature Search: `conformal_u1_dark_fopt`

Model and branch: classically conformal dark `U(1)_D` Coleman-Weinberg scalar plus dark gauge boson plus anomaly-safe dark fermion pair, on `fopt-pta`.

## Search Summary

The target model is not locally novel as a broad idea: classically conformal or Coleman-Weinberg Abelian dark sectors with MeV-scale first-order phase transitions have been studied as NANOGrav/PTA explanations. The exact proposed charge convention with a complex scalar of charge 2 and an anomaly-cancelling Weyl pair of charges `+1,-1`, with `lambda_HP = epsilon = 0` for backend compatibility, was not found as an exact one-to-one benchmark source in this preliminary scan. The closest benchmark sources are conformal hidden `U(1)'` dark-sector papers and the earlier dark `U(1)_D` NANOGrav 12.5 yr analysis.

## Kept Papers

1. Borah, Dasgupta, Kang, `arXiv:2105.01007`, "Gravitational waves from a dark U(1)_D phase transition in the light of NANOGrav 12.5 yr data", Phys. Rev. D 104, 063501 (2021).
   - Classification: structurally similar model.
   - Relevance: dark `U(1)_D`, complex scalar, vector-like dark fermion variant, conformal invariance, NANOGrav 12.5 yr FOPT target.
   - Benchmark hint: `g_D = 0.32`, `m_ZD = 12.6 MeV`, `T_* = 2.25 MeV`, `alpha_* = 0.68`, `beta/H = 82.4`, `v_w = 0.91`, `T_p = 1.9 MeV`.
   - Convention note: their scalar vev convention is `<Phi> = M/sqrt(2)` and `m_ZD = 2 g_D M`, so in the proposed backend convention `v_D` likely maps to `M`, giving `v_D ~ 19.7 MeV` for the benchmark if the same charge normalization is used. Their Yukawa is neglected, unlike the proposed scan where `y_D` is an explicit parameter.

2. Goncalves, Marfatia, Morais, Pasechnik, `arXiv:2501.11619`, "Supercooled phase transitions in conformal dark sectors explain NANOGrav data", Phys. Lett. B 869, 139829 (2025).
   - Classification: structurally similar model.
   - Relevance: conformal dark `U(1)'`, Coleman-Weinberg breaking, MeV-scale supercooled FOPT, NANOGrav 15 yr/PTArcade fit.
   - Benchmark hint: best-fit including SMBHB contribution has `g_L = 0.59`, `M_h2 = 12.4 MeV`, `M_Z' = 107.3 MeV`, `T_RH = 11.7 MeV`, `alpha = 2.60e5`, `beta/H = 39.5`.
   - Additional range hint: NANOGrav 15 yr favors `Z'` and dark scalar masses in the `10-100 MeV` range; without SMBHBs they report `g_L in [0.57,0.86]` and `lambda_sigma in [-0.062,-0.028]` at 68% CL.
   - Convention note: not the same fermion/Yukawa content; uses a portal/kinetic-mixing setup and RG-evolved parameters at `mu = 0.1 MeV`.

3. Balan, Bringmann, Kahlhoefer, Matuszak, Tasillo, `arXiv:2502.19478`, "Sub-GeV dark matter and nano-Hertz gravitational waves from a classically conformal dark sector", JCAP 08 (2025) 062.
   - Classification: same_model-level structure for conformal hidden `U(1)'` with stable fermionic dark matter, but not identical charge and portal assumptions.
   - Relevance: classically conformal hidden `U(1)'`, dark photon, dark Higgs, stable fermion, kinetic mixing, MeV FOPT, NANOGrav/PTArcade likelihood.
   - Benchmark hints:
     - Point A: `g = 0.677`, `y = 0.224`, `v = 173 MeV`, `m_A' = 117 MeV`, `m_phi = 36.3 MeV`, `m_chi = 27.4 MeV`, `T_p = 2.28 MeV`, `T_reh = 16.8 MeV`, `alpha = 4.7e3`, `beta/H = 33.7`.
     - Point B: `g = 0.601`, `y = 0.234`, `v = 692 MeV`, `m_A' = 416 MeV`, `m_phi = 114 MeV`, `m_chi = 115 MeV`, `T_p = 1.21 MeV`, `T_reh = 55.9 MeV`, `alpha = 9.48e6`, `beta/H = 18.0`.
   - Range hint: PTA-favored region roughly requires `v ~ 60-900 MeV`, gauge couplings high enough for strong slow transitions, `m_A' ~ 50-600 MeV`, and typical `beta/H ~ 15-45`.
   - Convention note: their mass relation uses `m_A' = g v`; the proposed model has `m_X/v_D = 2 g_D`, so the same physical vector mass maps to different `g_D` or `v_D` depending on charge normalization.

4. Fujikura, Girmohanta, Nakai, Suzuki, `arXiv:2306.17086`, "NANOGrav Signal from a Dark Conformal Phase Transition".
   - Classification: same target signal, different model.
   - Relevance: nearly conformal confining dark sector, not Abelian Higgs; useful for PTA/conformal supercooling context only.
   - Benchmark confidence: qualitative. The paper is not a source of `v_D`, `g_D`, or `y_D` points for the Abelian Higgs backend.

5. Hashino, Kanemura, Takahashi, Tanaka, `INSPIRE:1705442`, "Phase transition and vacuum stability in the classically conformal B-L model".
   - Classification: background context only.
   - Relevance: classically conformal gauged Abelian symmetry and gravitational waves, but primarily B-L/EW-scale and not PTA/NANOGrav benchmark focused.

## Benchmark Guidance For Downstream Agents

Priority for `fopt-agent` and `pta-agent` should be the MeV-to-sub-GeV scale. Directly useful starting points are the Balan et al. points, mapped with care to the proposed charge convention:

- Start with `v_D = 100-700 MeV`, `g_D = 0.30-0.70` if keeping `m_X/v_D = 2 g_D`, and `y_D = 0.2-0.4` as an initial Yukawa range.
- Also test the Borah et al. low-mass benchmark after mapping `m_ZD = 2 g_D v_D`: `g_D = 0.32`, `v_D ~ 19.7 MeV`, with `y_D` initially small or scanned upward subject to a positive Coleman-Weinberg beta coefficient.
- Use convention-aware comparisons: sources differ on `m_A'/v`, scalar charge normalization, portal/kinetic mixing, and whether the dark fermion Yukawa contributes to the effective potential.

No FOPT/PTA calculation was performed in this preliminary literature scan.
