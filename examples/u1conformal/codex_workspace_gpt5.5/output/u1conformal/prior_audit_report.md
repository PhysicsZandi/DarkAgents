# Prior Audit Report: u1conformal

Branch: `fopt-pta`

Run status: `warning`

This audit inspected the available structured handoffs for the completed `u1conformal` pipeline and did not perform new physics calculations, scans, or constraint recasts. No new web fetch was needed because the librarian and constraint handoffs already include the relevant literature checks and missing-observable inventory.

## Upstream Statuses

| Stage | Handoff | Status | Audit summary |
| --- | --- | --- | --- |
| Preliminary literature | `handoff_librarian_preliminary.json` | `warning` | No exact no-fermion, charge-one, PTArcade-ready match; closest papers require convention and model-content translation. |
| Critic/model | `handoff_critique.json` | `warning` | Model is internally consistent for the selected backend, but portal values, thermalization, gauge dependence, and full thermal masses remain open. |
| Authoritative model | `handoff_model.json` | `warning` | Uses independent `v` and `g_D`, dependent `lambda_Phi`, fixed `q_Phi = 1`, fixed `xi = 1`, and negligible portal effects for FOPT. |
| FOPT | `handoff_fopt.json` | `ok` | Semi-analytic scan executed, with 79 viable points out of 120, but relies on high-temperature and percolation approximations. |
| PTA/PTArcade | `handoff_pta.json` | `warning` | PTA fit completed, but template choice, wall dynamics, convergence, and prior sensitivity remain limited. |
| Constraints | `handoff_constraints.json` | `warning` | Only direct theory checks were applied; most laboratory and cosmology constraints require missing observables or new recasts. |

## Top Risks

1. `PA04`, `PA18`-`PA21`: constraints are largely unapplied because `epsilon`, `lambda_HP`, lifetimes, widths, branching ratios, abundances, and thermal history are missing. This is the largest phenomenological limitation.
2. `PA05`: the pipeline assumes `xi = 1` while also treating portal and kinetic-mixing effects as small or unspecified. A thermal-contact calculation is needed before interpreting the result as cosmologically viable.
3. `PA09`-`PA12`: the PTA-preferred region is strongly supercooled and uses the closest available `bf` template without wall-friction, runaway, or source-partition calculations. The fit is not a first-principles validation of the GW source.
4. `PA06`-`PA08`, `PA11`: the FOPT backend is semi-analytic and omits full Daisy/RG/gauge-prescription variations. Percolation checks exist, but only within the backend approximation.
5. `PA14`-`PA16`, `PA26`: the PTArcade result comes from one campaign with no multi-chain convergence or evidence estimate, and the posterior depends on informative `log10_v` and linear `g_D` priors.

## Severity Summary

Total audit items: 26

| Severity | Count | Controlled count |
| --- | ---: | ---: |
| 3 | 2 | 2 |
| 4 | 2 | 1 |
| 5 | 5 | 0 |
| 6 | 3 | 1 |
| 7 | 2 | 0 |
| 8 | 4 | 0 |
| 9 | 8 | 0 |

No item was ranked severity 10 because no handoff is failed or blocked, and the model is internally usable for the stated approximate pipeline. The high-severity issues are uncontrolled interpretation risks, not evidence that the pipeline artifacts are invalid.

## Controlled Items

The controlled items are `PA03`, `PA13`, `PA17`, and `PA23`. These cover dependent `lambda_Phi` handling, the decision not to use the sound-wave template as primary, the limited role of `f_peak_est`, and the non-applicability of direct detection for the current no-DM model.

## Required Followups

High-priority followups are:

- `FUP01`: specify `epsilon` and `lambda_HP`, then implement dark photon and dark Higgs decay/portal calculations.
- `FUP02`: compute thermalization and `xi(T)` to test the `xi = 1` assumption.
- `FUP03`: apply BBN, CMB, Delta N_eff, freeze-in, and late-decay constraints after decay tables and yields exist.
- `FUP04`: compare the semi-analytic FOPT backend against fuller finite-temperature calculations and posterior-level percolation checks.
- `FUP05`: compute or bracket wall dynamics before treating the `bf` template posterior as physically robust.

See `prior_audit_table.csv` and `handoff_prior_audit.json` for the full item list and ID-linked followups.
