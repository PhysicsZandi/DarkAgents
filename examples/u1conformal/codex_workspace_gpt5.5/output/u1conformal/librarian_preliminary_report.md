# Preliminary literature report: u1conformal

Date: 2026-06-10
Agent: preliminary-librarian-agent
Branch: fopt-pta

## Target model read

The supplied model is a classically scale-invariant dark Abelian Higgs sector with a complex scalar Phi and a dark gauge boson A'. The prompt uses

- Phi = (chi + rho + i G)/sqrt(2)
- V_tree(chi) = lambda_Phi chi^4 / 4
- free parameters v and g_D
- m_A'^2(chi) = g_D^2 chi^2
- m_rho^2 = beta_lambda v^2 with beta_lambda = 3 g_D^4/(8 pi^2)
- small Higgs portal and kinetic mixing for phenomenology, assumed negligible for the phase transition
- common dark/visible temperature xi = 1

## Search summary

I searched arXiv, INSPIRE-HEP metadata/API, and web search results for dark U(1), classically conformal, Coleman-Weinberg, first-order phase transition, NANOGrav/PTA, and nano-Hz gravitational wave combinations. Kept papers were checked against arXiv metadata, and several were cross-checked against INSPIRE-HEP metadata.

## Main findings

The model is not novel as a broad structure. Dark Abelian Higgs sectors with Coleman-Weinberg/classical conformal symmetry breaking and gravitational waves from a first-order dark phase transition have been studied. The most direct earlier study for the same minimal dark U(1)_D PTA target is Borah, Dasgupta and Kang, arXiv:2105.01007. A later and even more target-aligned study is Balan et al., arXiv:2502.19478, which studies a classically conformal hidden U(1)' with a dark Higgs, dark photon, and anomaly-cancelling fermions, and fits nano-Hz PTA data with PTArcade.

For the supplied no-fermion minimal version, benchmark points must be translated with care:

- Borah et al. use hPhi = M/sqrt(2), U(1)_D charge 2 n1 for Phi, and m_ZD = 2 g_D M. The supplied prompt uses m_A' = g_D v with charge-one Phi convention. If M corresponds to the prompt v, their benchmark m_ZD = 12.6 MeV at g_D = 0.32 maps to a different effective charge normalization than the prompt.
- Balan et al. use Q_Phi = 1 and m_A' = g v, which matches the prompt gauge-boson mass convention, but their model includes two fermions for anomaly cancellation and dark matter. For small Yukawa y, the GW potential is close to gauge dominated, but the thermal masses include fermion contributions.
- Several studies use Landau-gauge one-loop finite-temperature effective potentials with Arnold-Espinosa daisy resummation. The 2026 Feng-Zhang paper emphasizes that gauge dependence can materially alter GW predictions and provides gauge-independent high- and low-temperature treatments for a minimal dark U(1) sector.

## Kept papers

### 1. Borah, Dasgupta, Kang, arXiv:2105.01007

Title: "Gravitational waves from a dark U(1)_D phase transition in the light of NANOGrav 12.5 yr data"  
Journal: Phys. Rev. D 104, 063501 (2021)  
Classification: same_model

This is the closest match to the supplied model. It studies a classically conformal dark U(1)_D with a complex scalar singlet and gauge boson, neglecting the portal and Yukawa couplings for the FOPT/GW calculation. It uses Landau gauge and Arnold-Espinosa daisy resummation. Its headline PTA-scale benchmark is:

- g_D = 0.32
- m_ZD = 12.6 MeV
- T_* = 2.25 MeV
- T_c = 4.18 MeV
- T_p = 1.9 MeV
- alpha_* = 0.68
- beta/H_* = 82.4
- v_w = 0.91

The paper scans alpha_D in 0.002-0.01 and compares alpha_* and T_* with NANOGrav 12.5-year preferred regions. It notes BBN/CMB pressure on light dark photons and says m_ZD of order 10 MeV is needed for the benchmark phenomenology.

Convention notes: Their scalar charge and mass convention gives m_ZD = 2 g_D M, while the target prompt uses m_A' = g_D v. This is the largest benchmark translation issue.

### 2. Balan, Bringmann, Kahlhoefer, Matuszak, Tasillo, arXiv:2502.19478

Title: "Sub-GeV dark matter and nano-Hertz gravitational waves from a classically conformal dark sector"  
Journal: JCAP 08, 062 (2025)  
Classification: structurally_similar_model

This is highly relevant to PTA-scale conformal U(1) physics. The model is a classically conformal U(1)' with dark Higgs Phi, dark photon A', and two left-handed fermions with opposite charges. The paper uses Q_Phi = 1 and m_A'^2(phi_b) = g^2 phi_b^2, matching the prompt's mass convention. It uses MS-bar Coleman-Weinberg, Landau gauge, and Arnold-Espinosa daisy resummation.

Key benchmark points from Table 1:

- Point A, coupled dark sector: g = 0.677, y = 0.224, kappa = 2.29e-6, v = 173 MeV, m_A' = 117 MeV, m_phi = 36.3 MeV, m_chi = 27.4 MeV, T_p = 2.28 MeV, T_reh = 16.8 MeV, alpha = 4.7e3, beta/H = 33.7.
- Point B, secluded dark sector: g = 0.601, y = 0.234, kappa = 2.7e-4, v = 692 MeV, m_A' = 416 MeV, m_phi = 114 MeV, m_chi = 115 MeV, T_p = 1.21 MeV, T_reh = 55.9 MeV, alpha = 9.48e6, beta/H = 18.0.

Global scan hints:

- PTA-preferred coupled scenario: g roughly 0.57-0.75, v roughly 60-900 MeV, beta/H roughly 15-45, m_A' roughly 50-600 MeV, m_phi roughly 20-170 MeV.
- The paper explicitly uses PTArcade with the ceffyl backend and NANOGrav 15-year data.

Applicability: direct for PTA/FOPT scale and mass convention; adaptable rather than exact because the target model omits the anomaly-cancelling fermions and dark-matter sector.

### 3. Khoze and Milne, arXiv:2212.04784

Title: "Gravitational waves and dark matter from classical scale invariance"  
Journal: Phys. Rev. D 107, 095012 (2023)  
Classification: structurally_similar_model

This paper studies a minimal classically conformal U(1) model of fermionic dark matter with Gildener-Weinberg symmetry breaking. It is not PTA-scale; benchmark transition temperatures are tens to hundreds of GeV and spectra are aimed at LISA/DECIGO/BBO-like detectors.

Useful FOPT benchmarks:

- BP1: T_N = 84.2 GeV, alpha = 0.547, beta/H = 129
- BP2: T_N = 115.2 GeV, alpha = 5.70, beta/H = 63.5
- BP3: T_N = 30.8 GeV, alpha = 10.1, beta/H = 85.4
- BP4: T_N = 273.9 GeV, alpha = 0.0698, beta/H = 290

Useful conventions: unitary gauge for field parametrization, finite-temperature potential with thermal functions, daisy resummation, and thermal masses. Its benchmark masses are not useful for PTA priors because the frequency scale is too high.

### 4. Feng and Zhang, arXiv:2602.14866

Title: "Gauge-independent gravitational waves from a minimal dark U(1) sector with viable dark matter candidates"  
Journal: preprint as of 2026-06-10  
Classification: structurally_similar_model

This paper is not classically conformal in the same strict target-model sense, but it is important for the FOPT-PTA branch because it treats a minimal gauged dark U(1) with dark Higgs and dark photon and constructs gauge-independent effective actions using the Nielsen identity. It states that v_x in the 10-100 MeV range can yield peak frequencies approaching the nHz/PTA band, while v_x in the 1-100 GeV range tends toward mHz space-interferometer frequencies.

Useful benchmark table for its dark-fermion case:

- model d: v_x = 1 GeV, g_x = 0.0208, lambda_x = 1.93e-7, m_A' = 0.0208 GeV, T_p = 0.0423 GeV
- model e: v_x = 10 GeV, g_x = 0.505, lambda_x = 1.17e-4, m_A' = 5.05 GeV, T_p = 0.54 GeV
- model f: v_x = 100 GeV, g_x = 0.391, lambda_x = 3.13e-5, m_A' = 39.10 GeV, T_p = 3.34 GeV

The paper's most important use for the target analysis is methodological: gauge dependence of Landau-gauge effective potentials should be treated as a theory uncertainty.

### 5. Fujikura, Girmohanta, Nakai, Suzuki, arXiv:2306.17086

Title: "NANOGrav Signal from a Dark Conformal Phase Transition"  
Journal: Phys. Lett. B 846, 138203 (2023)  
Classification: same_target_signal_different_model

This is a conformal dark-sector NANOGrav paper, but the model is a nearly conformal confining sector described by a dilaton/radion potential generated by dark Yang-Mills dynamics, not a perturbative Abelian Coleman-Weinberg U(1). It is useful for target-scale intuition:

- secluded scenario examples use T_* = 120 MeV or 10 MeV, alpha' = 0.1, beta/H_* = 4 or 8
- decaying dark sector examples use T_* = 120 MeV or 10 MeV, alpha' = 10, beta/H_* = 5 or 21

It also emphasizes Delta N_eff and dark-radiation constraints when the dark sector is secluded.

### 6. Hashino, Kakizaki, Kanemura, Ko, Matsui, arXiv:1802.02947

Title: "Gravitational waves from first order electroweak phase transition in models with the U(1)_X gauge symmetry"  
Journal: JHEP 06, 088 (2018)  
Classification: background_context_only

This is a dark U(1)_X Abelian Higgs model with portal mixing and kinetic mixing, but it is an electroweak-scale/multi-field analysis. It is useful for general dark-Higgs and dark-photon conventions and for constraints, not for PTA benchmark priors. It uses Landau gauge and notes gauge-dependence issues. Its detectable GW regions require m_X roughly above 25 GeV and g_X roughly above 0.5, so the benchmarks are not PTA-scale.

## Benchmark guidance for downstream FOPT/PTA

Recommended starting priors should not be centered on electroweak-scale studies. The strongest target-relevant hints are:

- Minimal U(1)_D PTA-scale direct benchmark from arXiv:2105.01007: g_D around 0.32 and MeV-scale transition temperature, but translate m_ZD = 2 g_D M to the prompt convention before use.
- Conformal U(1)' PTA-scale scan from arXiv:2502.19478: use v from roughly 60 MeV to 900 MeV and g roughly 0.57 to 0.75 as a high-confidence PTA-scale region when fermion effects are present or negligible; the prompt's no-fermion version may shift the viable range.
- Gauge-independent dark U(1) scan from arXiv:2602.14866: v_x around 10-100 MeV tends toward the nHz band, but exact amplitudes and nucleation depend on the selected gauge-independent regime.

## Theory and convention caveats

- Gauge dependence: several older papers use Landau gauge for the finite-temperature effective potential. The 2026 gauge-independent study indicates this can materially change predicted spectra.
- Daisy prescription: closest PTA studies generally use Arnold-Espinosa resummation, not Parwani.
- VEV and charge normalization: do not mix m_ZD = 2 g_D M benchmarks with prompt m_A' = g_D v without an explicit charge/vev translation.
- Thermal history: the target prompt assumes xi = 1. Some conformal dark-sector NANOGrav papers assume dark/visible temperature decoupling or late decay.
- Completion/percolation: in supercooled conformal models, nucleation and percolation can fail or require careful treatment; beta/H from d(S3/T)/dT may be unreliable for strong supercooling.
- Cosmology: MeV-scale reheating/transition temperatures require BBN, CMB, Delta N_eff, and late-decay checks.

## Recommended next steps

1. Critic/fopt agents should first normalize the target convention: charge of Phi, definition of v, and whether m_A' = g_D v is fixed.
2. Use arXiv:2105.01007 as the closest minimal U(1)_D PTA benchmark after translating conventions.
3. Use arXiv:2502.19478 as the best PTArcade/PTA prior guide, but mark fermion/thermal-mass effects as a model difference.
4. Treat gauge-dependence and thermal-resummation scheme as explicit theory uncertainties in any FOPT scan.
5. For PTArcade priors, start broad around MeV transition temperatures and v in the 10 MeV-1 GeV decade, rather than TeV/electroweak benchmarks.

## Verified source URLs

- https://arxiv.org/abs/2105.01007
- https://arxiv.org/abs/2502.19478
- https://arxiv.org/abs/2212.04784
- https://arxiv.org/abs/2602.14866
- https://arxiv.org/abs/2306.17086
- https://arxiv.org/abs/1802.02947
- https://inspirehep.net/api/literature?q=arxiv:2105.01007
- https://inspirehep.net/api/literature?q=arxiv:2502.19478
- https://inspirehep.net/api/literature?q=arxiv:2602.14866
- https://inspirehep.net/api/literature?q=arxiv:2212.04784
- https://inspirehep.net/api/literature?q=arxiv:2306.17086
- https://inspirehep.net/api/literature?q=arxiv:1802.02947
