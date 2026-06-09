# Preliminary Literature Report: minimal_conformal_su2_doublet

Date: 2026-06-07

Agent: preliminary-librarian-agent

Branch: fopt-pta

User prompt: "what is the minimal conformal non-abelian model that can explain the NANOGrav signal?"

## Target Model

The proposed model is a dark `SU(2)_D` gauge theory with one complex scalar doublet `Phi`, classically scale invariant at tree level, negligible Higgs portal, and symmetry breaking `SU(2)_D -> nothing`. The independent proposal-stage parameters are `gD` and `vD`, with the proposer convention

`Phi = (0, chi / sqrt(2))^T`, `m_WD(chi) = gD chi / 2`, `m_WD = gD vD / 2`.

## Search Strategy

Sources searched or fetched:

- arXiv search/fetch for conformal `SU(2)` dark sectors, non-Abelian dark FOPT, NANOGrav/PTA, and vector dark matter.
- INSPIRE-HEP metadata pages where available; INSPIRE's web app was JavaScript-only in this environment for the exact-model record, so arXiv metadata and PDF text were used as the authoritative verified source.
- arXiv PDF/HTML for benchmark and convention extraction where accessible.

## Kept Papers

### 1. Borah, Dasgupta, Kang, arXiv:2109.11558

Title: "A first order dark SU(2)_D phase transition with vector dark matter in the light of NANOGrav 12.5 yr data"

Classification: `same_model`

This is the closest and most important result. The paper studies a dark `SU(2)_D` extension with a single complex scalar doublet, all SM fields neutral under `SU(2)_D`, a classically conformal scalar potential, negligible Higgs portal coupling, and massive vector dark matter from the dark phase transition. It explicitly targets the NANOGrav 12.5-year interpretation of a first-order phase transition below the electroweak scale.

Relevant extracted details:

- Tree potential: `lambda1 (H^\dagger H)^2 + lambda2 (Phi^\dagger Phi)(H^\dagger H) + lambda3 (Phi^\dagger Phi)^2`; `lambda2` is neglected for the FOPT analysis.
- Dark scalar parameterization: `Phi = 1/sqrt(2) (G2+iG3, M + phi + iG1)^T`.
- SSB pattern: the dark scalar doublet breaks `SU(2)_D`, producing massive dark vector bosons.
- Effective potential: tree plus Coleman-Weinberg plus finite-temperature part, in Landau gauge.
- Daisy treatment: daisy diagrams included; the text discusses Parwani and Arnold-Espinosa prescriptions and then writes a daisy-improved potential.
- Field-dependent masses reported by the paper: `m_D^2(phi) = g_D^2 phi^2 / 2`, `m_phi^2 = 3 lambda3 phi^2`, `m_G^2 = lambda3 phi^2`.
- Thermal masses reported: `Pi_ZD = (5/6) g_D^2 T^2`, `Pi_phi,G = (lambda3/2 + 3 g_D^2/16) T^2`.
- RGE constants for `SU(2)_D`: `b = -43/3`, `a1 = 24`, `a2 = 9/2`, `a3 = 9/16`.
- FOPT definitions include critical temperature, nucleation temperature from `Gamma(T*) = H^4(T*)`, bounce action `S3`, strength `alpha*`, and inverse duration `beta/H*`.
- PTA/NANOGrav comparison: `gD` scanned in the range corresponding to `alphaD in [0.01, 0.2]`; the paper overlays 68/90/95 percent NANOGrav-preferred regions depending on the approximation.

Direct benchmark hint from the paper:

- Figure 1 benchmark: `alpha* = 0.45`, `T* = 1.8 MeV`, `gD = 1.37`, `M_ZD = 8.23 MeV`, with `phi_c / T_c = 3.56`.

Important convention warning:

- The paper's displayed field-dependent vector mass `m_D^2(phi) = g_D^2 phi^2 / 2` conflicts with the usual fundamental-doublet convention and the proposer/backend convention `m_WD^2(chi) = gD^2 chi^2 / 4`. The same paper also states the physical mass as `M_ZD = gD M / 2`. Downstream agents must not copy the displayed `g_D^2 phi^2 / 2` blindly without checking whether it is a normalization/typographical convention issue.

### 2. Balan, Bringmann, Kahlhoefer, Matuszak, Tasillo, arXiv:2502.19478

Title: "Sub-GeV dark matter and nano-Hertz gravitational waves from a classically conformal dark sector"

Classification: `structurally_similar_model`

This paper studies a classically conformal hidden `U(1)'` model, not the non-Abelian `SU(2)_D` target. It is useful for PTA-scale benchmark logic and constraints because it treats a MeV-scale conformal FOPT, sub-GeV dark-sector masses, PTA data, dark-matter abundance, and laboratory/cosmological constraints.

Relevant differences:

- Gauge group is Abelian `U(1)'`, not `SU(2)_D`.
- The portal is kinetic mixing, while the target proposal takes negligible visible-sector portal at proposal stage.
- Benchmark information is adaptable only at the scale/target-signal level, not as a direct `gD, vD` benchmark.

Useful qualitative benchmark guidance:

- The abstract states that PTA explanation requires a phase transition in the MeV temperature range.
- The model finds viable regions only after combining the PTA signal with dark matter and laboratory/cosmology constraints.

### 3. Fujikura, Girmohanta, Nakai, Suzuki, arXiv:2306.17086

Title: "NANOGrav Signal from a Dark Conformal Phase Transition"

Classification: `same_target_signal_different_model`

This is a dark conformal phase-transition explanation of NANOGrav, but the theory is a nearly conformal confining/dilaton sector rather than the perturbative Higgsed `SU(2)_D` scalar-doublet model. It is relevant for target-signal context, temperature-sector assumptions, and dark-radiation/Delta N_eff issues, but it does not provide direct parameters for the target model.

### 4. Goncalves, Marfatia, Morais, Pasechnik, arXiv:2501.11619

Title: "Supercooled phase transitions in conformal dark sectors explain NANOGrav data"

Classification: `same_target_signal_different_model`

This paper studies conformal dark `U(1)'` models, not the target non-Abelian model. It is useful for supercooled FOPT PTA benchmarks. A best-fit table gives, for its `U(1)'` model, `g_L = 0.59`, `M_h2 = 12.4 MeV`, `M_Z' = 107.3 MeV`, `T_RH = 11.7 MeV`, `alpha/10^5 = 2.60`, and `beta/H = 39.5`. These values are not directly portable to the target `SU(2)_D` model.

### 5. Bringmann, Depta, Konstandin, Schmidt-Hoberg, Tasillo, arXiv:2306.09411

Title: "Does NANOGrav observe a dark sector phase transition?"

Classification: `same_target_signal_different_model`

This paper is not a model match, but it is important context for PTA interpretation and cosmological consistency. It emphasizes MeV-scale dark-sector phase transitions, BBN/CMB energy-release constraints, and the distinction between secluded dark sectors and sectors that decay before neutrino decoupling.

## Novelty Verdict

Not novel as an exact model class for the stated NANOGrav 12.5-year FOPT target. The exact core model, a classically conformal dark `SU(2)_D` gauge theory with one complex scalar doublet and negligible Higgs portal, was already studied in arXiv:2109.11558.

The current proposal may still differ in downstream implementation details, especially if it uses the semianalytic backend convention `m_WD = gD vD / 2`, a different treatment of thermal masses/daisy resummation, NANOGrav 15-year/PTArcade likelihoods, or omits dark-matter relic requirements. Those differences should be treated as implementation or analysis novelty, not model novelty.

## Benchmark Hint Confidence

- Direct: arXiv:2109.11558 provides the same-model benchmark `gD = 1.37`, `M_ZD = 8.23 MeV`, `T* = 1.8 MeV`, `alpha* = 0.45`, `phi_c/T_c = 3.56`.
- Adaptable: arXiv:2502.19478 and arXiv:2501.11619 support the general PTA-scale expectation of MeV-scale conformal FOPTs, but not direct `SU(2)_D` parameters.
- Qualitative/context: arXiv:2306.17086 and arXiv:2306.09411 motivate target-signal and cosmological-consistency checks.

## Warnings and Blockers

- INSPIRE pages were not fully readable because the web app requires JavaScript. arXiv metadata and PDFs were used to verify kept citations.
- The exact-model paper contains a vector mass convention tension: physical mass text says `M_ZD = gD M / 2`, while one displayed field-dependent mass line says `m_D^2(phi) = g_D^2 phi^2 / 2`. Downstream convention reconciliation is required.
- Benchmarks from Abelian conformal papers must not be copied as `SU(2)_D` benchmarks.
- No new numerical FOPT or PTA fit was performed by this preliminary literature search.

## Files Written

- `output/minimal_conformal_su2_doublet/librarian_preliminary_report.md`
- `output/minimal_conformal_su2_doublet/handoff_librarian_preliminary.json`
