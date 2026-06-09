# Prior Audit Report — su2cw-dark (fopt-pta branch)

**Agent:** prior-agent | **Date:** 2026-06-07 | **Run status:** warning

Model: minimal classically conformal dark SU(2)_D, Coleman-Weinberg radiative breaking, supercooled FOPT targeting NANOGrav 15yr. The user elected to keep the minimal **secluded** model despite the constraint-agent's flagged BBN/Neff portal tension. This audit cross-references all six upstream handoffs (model, critique, librarian, fopt, pta, constraints).

## Upstream pipeline status

| Handoff | Status | Note |
|---|---|---|
| handoff_model.json | ok | finalized model (validated by critic) |
| handoff_critique.json | warning | no red flags; warnings on completion, broad chi0, high-T expansion |
| handoff_librarian_preliminary.json | ok | model not novel (= 2109.11558) |
| handoff_fopt.json | ok | 271/302 viable; deep supercooling, large alpha |
| handoff_pta.json | ok | dbf template, NG15 ceffyl posterior |
| handoff_constraints.json | **warning** | secluded-portal/BBN/Neff unresolved; 0/11 constraints directly testable |

The pipeline does **not** terminate in a clean state: the constraint stage is `warning`, and the binding cosmological constraints (BBN, Neff, relic) are unevaluable without a portal that the minimal model does not provide. The final result should therefore be read as **conditional**, not established.

## Top-ranked findings (by severity)

1. **A01 (sev 9) Missing SM portal.** The model is strictly secluded yet upstream assumes thermal equilibrium (xi=1). Kinetic mixing is forbidden in pure non-abelian SU(2)_D; a Higgs portal breaks the classical conformal invariance the CW mechanism relies on. This single unresolved choice gates BBN reheating, Delta Neff, relic abundance and every coupling-dependent constraint. **Uncontrolled.**

2. **A02 (sev 8) SM-bath reheating not computed.** fopt benchmarks reach Treh ~ 0.5-1.5 MeV (below the ~2-4.7 MeV BBN bound); pta T_star ~ 37-138 MeV would pass *if* that energy reaches the SM bath. The Treh in handoffs is the spectrum combined-bath convention, not the SM photon-neutrino temperature. BBN pass/fail is undetermined.

3. **A07 (sev 8) Delta Neff not computed.** A fully secluded dark-sector FOPT is strongly disfavoured by the dedicated NANOGrav study (2306.09411; Delta Neff > 0.22 excluded at 95% CL). xi at BBN/CMB and Delta Neff are absent everywhere upstream.

4. **A03 (sev 7) Template/prior dependence of the preferred region.** The FOPT-stage band-center benchmarks cluster at chi0 ~ 5 MeV, g ~ 1.3, while the PTArcade NG15 posterior peaks at chi0 ~ 1 GeV, g ~ 0.87. The two stages prefer **different corners** of parameter space; the reported region is driven by the dbf amplitude/peak matching and the adopted (linear g, log chi0) priors, not by a stage-independent fit.

5. **A04 (sev 7) dbf template extrapolated in alpha.** Viable points have alpha ~ 1e5 to >1e15, far beyond the validated/displayed range of 2511.15687. Viability rests on the amplitude-saturation argument (K_sw = alpha/(1+alpha) -> 1), which is plausible but not simulation-validated at these alpha; cosmic-expansion and the super-horizon causality tail noted in 2511.15687 are not propagated.

6. **A06 (sev 7) Secluded thermalization xi=1.** Used upstream as the backend default; internally inconsistent without a portal (A01) and propagates into gstar_eff, alpha, beta_H, Treh and hence the GW spectrum itself.

## Other notable items

- **A08 (6)** chi pseudo-dilaton stability/late decays (m_chi < m_W throughout, chi->WW closed) — stable dark radiation or late SM injection, unresolved.
- **A09 (6)** W_D vector-DM relic abundance and stability not computed.
- **A13 (6)** No Bayesian model comparison vs the astrophysical SMBHB background; evidence is null. A 14/14-bin fit does not establish FOPT preference.
- **A10 (6, controlled)** High-T expansion least accurate exactly in the deep-supercooling regime where the model lives; no daisy resummation.
- **A15 (5)** Beam-dump/SN1987A/direct-detection/Higgs-portal bounds are all conditional on the unspecified portal; adding one tensions the BBN-required coupling against lab limits or breaks conformal invariance.
- **A12 (5, controlled)** ceffyl free-spectrum likelihood inherits NANOGrav power-law/HD assumptions; not a full per-pulsar HD analysis.
- **A11 (5), A05 (5), A16 (4), A14 (4), A17 (3), A18 (3)** — completion approximation, fixed ksw/vw, RG-scale choice, SIDM, perturbativity edge, non-novelty/anchor mismatch.

## Severity/control summary

18 items: 4 uncontrolled at severity >=8 (A01, A02, A07) plus the secluded/template cluster at 7. The dominant message is that the FOPT-to-PTA fit (alpha, beta_H, Treh, GW spectrum) is internally executed and self-consistent, but its **cosmological interpretation is gated by the unspecified portal**, and the **preferred parameter region is template- and prior-dependent**.

## Required follow-ups

- **F1 (high):** Resolve the portal; compute T_SM_reheat (>2-4.7 MeV) and Delta Neff (<0.22), or relabel the result as conditional on a UV completion.
- **F2 (high):** Validate dbf at extreme alpha; quantify residual alpha/ksw/vw dependence and the super-horizon tail.
- **F3 (high):** Test template/prior dependence of the preferred region; reconcile with the 2109.11558 modest-alpha / MeV-vev anchor.
- **F4 (medium):** Compute chi lifetime/abundance, W_D relic/stability, and SIDM sigma/m (inputs available).
- **F5 (medium):** Bayesian model comparison vs SMBHB; note the ceffyl approximation.

## Sources consulted

- [2511.15687 — Impact of cosmic expansion on GW spectra from strongly supercooled FOPTs](https://arxiv.org/abs/2511.15687)
- [2306.16213 — NANOGrav 15yr: Evidence for a GWB](https://arxiv.org/abs/2306.16213)
- [2407.20510 — NANOGrav 15yr: Posterior predictive checks](https://arxiv.org/abs/2407.20510)
- Upstream: handoff_constraints.json (C1 2109.14765/1511.00672; C2 2306.09411; C3/C6/C9 2502.19478), handoff_librarian_preliminary.json (2109.11558).
