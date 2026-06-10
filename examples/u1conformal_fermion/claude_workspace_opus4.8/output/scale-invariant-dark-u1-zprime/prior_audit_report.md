# Prior Audit Report: scale-invariant-dark-u1-zprime

**Branch:** fopt-pta | **Agent:** prior-agent | **Run status:** warning | **Date:** 2026-06-10

Model: classically scale-invariant gauged dark U(1)_D (Coleman-Weinberg), proposed to explain the NANOGrav 15yr signal via a strongly supercooled first-order phase transition (FOPT).

## Scope and upstream status

| Handoff | Status |
|---|---|
| handoff_model.json | ok |
| handoff_critique.json | ok |
| handoff_librarian_preliminary.json | ok |
| handoff_fopt.json | warning (beta/H convention, extreme alpha) |
| handoff_pta.json | warning (K_sw saturation, no Bayes factor) |
| handoff_constraints.json | warning (epsilon=0 vs reheating, 5 missing calculations) |

22 audit items were extracted, classified and ranked. Severity distribution (1-10): one item at 10, one at 9, three at 8, three at 7, three at 6, four at 5, three at 4, two at 3, one at 2-equivalent. Roughly half are uncontrolled.

## The two science questions and the verdict

1. **Does the model explain NANOGrav?** Partially established but soft. PTArcade returns peaked, interior posteriors (g_D~0.59, y~0.38, log10_w~0.0) and best-fit points scoring 14/14 in-band bins. BUT (i) no Bayes factor / evidence was computed (A04), so this is a goodness-of-region statement, not a model comparison against SMBHB; (ii) the amplitude is saturated (K_sw->1) at extreme alpha (A03), so the fit constrains essentially beta/H and Treh, not alpha; (iii) a beta/H convention mismatch of ~7x (A02) may systematically bias the very quantity the fit depends on.

2. **Is the model cosmologically viable?** UNRESOLVED. The entire FOPT/PTA chain fixed epsilon=0 (kinetic mixing), making the dark sector secluded. SM reheating and BBN require epsilon~1e-6..1e-3 (A01). Five decisive constraints (portal reheating, Z' decays, Delta N_eff, chi relic, scalon decay) are uncomputed; no PTA-preferred point can yet be declared cosmologically allowed.

## Top decision-driving assumptions (ranked)

1. **A01 (sev 10, uncontrolled) - epsilon=0 vs required reheating.** Dominant. With strictly secluded dark sector the latent heat never reaches the SM bath; the scenario fails BBN/N_eff as pure dark radiation. The reference model arXiv:2502.19478 requires kappa~2e-6..3e-4 to reheat the SM to 16.8-55.9 MeV. The cosmological-viability half of the analysis cannot be closed without a portal reheating module.

2. **A02 (sev 9, uncontrolled) - beta/H convention mismatch.** Backend gives beta_H~152.7 at literature Point A vs 21.1 published (factor ~7). The GW peak amplitude ~ (beta/H)^-2 and peak frequency ~ beta/H, so this directly biases the spectrum and the PTA posterior. Tp/Treh/alpha agree to ~15%, isolating the discrepancy to the beta/H definition.

3. **A03 (sev 8, uncontrolled) - dbf template at extreme alpha / K_sw saturation.** alpha up to ~1e15-1e16 with the efficiency saturated; the predicted amplitude is pinned at its ceiling and is insensitive to the true (extreme) alpha. Extrapolating the template into ultra-supercooling (cosmic-expansion corrections, arXiv:2511.15687) is an uncontrolled systematic.

4. **A04 (sev 8, uncontrolled) - no Bayes factor.** The "explains NANOGrav" claim lacks an evidence/model-comparison number.

5. **A22 (sev 7) + A05 (sev 7) + A10 (sev 7).** Reheating-viable epsilon~1e-6..1e-4 overlaps the dark-photon lab/SN1987A probed window and may itself be excluded (A22); Delta N_eff is uncomputed and most dangerous at the y=0 best-fit point with a massless chi (A05); the effective potential carries an uncontrolled mu-scale / no-Daisy systematic on Tp/alpha/beta (A10).

## Testable now vs needs new calculation

- **Controlled / testable now:** perturbativity and beta_lambda>0 (C10, satisfied; A15), percolation/eternal-inflation (C11, checked upstream; A12), prior-window and convention bookkeeping (A06, A07, A16, A19, A20, A21).
- **Needs new calculations (cross-referencing constraint-agent missing_calculations):** A01/A22 (portal_reheating.py, darkphoton_decays.py), A05 (deltaNeff.py), A08 (relic_chi.py), A09 (scalon_decay.py). A02, A03, A10, A11, A13, A18 require backend/template reconciliation rather than entirely new modules.

## Recommendation

Treat the NANOGrav fit as conditional and preliminary. Before any headline claim: (F1) compute SM reheating with epsilon restored; (F2) resolve the beta/H convention and re-fit; (F3) quantify template systematics at extreme alpha; (F4) compute Delta N_eff for the y=0 region; (F5) compute a Bayes factor. Items F1-F5 are high priority; F6-F9 medium/low.

## Artifacts

- /Users/mattezandi/Desktop/code/run_folder/claude_workspace/output/scale-invariant-dark-u1-zprime/handoff_prior_audit.json
- /Users/mattezandi/Desktop/code/run_folder/claude_workspace/output/scale-invariant-dark-u1-zprime/prior_audit_table.csv
- /Users/mattezandi/Desktop/code/run_folder/claude_workspace/output/scale-invariant-dark-u1-zprime/prior_audit_report.md

Sources consulted for template validity: [arXiv:2511.15687](https://arxiv.org/abs/2511.15687).
