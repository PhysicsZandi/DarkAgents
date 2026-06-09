# Prior Audit Report: minimal_conformal_su2_doublet

## Scope
Audit-only pass over completed handoff JSONs for the `fopt-pta` pipeline. No new physics calculations, FOPT scans, PTA scans, or PTArcade runs were performed.

## Upstream Statuses

| Handoff | Status | Summary |
| --- | --- | --- |
| `handoff_model.json` | warning | Authoritative model usable with literature, portal, and backend caveats. |
| `handoff_librarian_preliminary.json` | warning | Exact model already studied; benchmark conventions require care. |
| `handoff_critique.json` | warning | No red flags, but same-model precedent and convention/backend caveats. |
| `handoff_fopt.json` | ok | Usable scan with semianalytic and percolation approximations. |
| `handoff_pta.json` | warning | DBF/template/large-alpha and prior-boundary caveats; no 14/14 benchmark. |
| `handoff_constraints.json` | warning | No exclusions claimed because most required observables are missing. |

## Audit Summary

Total audit items: 18. High-severity items (severity >= 8): 11. Controlled items: 4. Run status is `warning` because all required inputs were usable, but interpretation is dominated by unresolved assumptions.

Severity distribution: {'1': 0, '2': 0, '3': 0, '4': 0, '5': 1, '6': 4, '7': 2, '8': 5, '9': 4, '10': 2}.
Controlled distribution: {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 4, '7': 0, '8': 0, '9': 0, '10': 0}.

## Top Severity Items

- **PA03 (10/10, limitation, thermal_history)**: No thermal history, dark-sector temperature ratio, decoupling history, reheating partition, relic abundance, or entropy transfer observable was computed. Required followup: Implement thermal_history.py/cosmo_constraints.py with T_dark/T_SM, entropy evolution, FOPT energy partition, and BBN/CMB likelihood mapping.
- **PA13 (10/10, warning, cosmology)**: Sub-GeV strongly supercooled FOPT can affect BBN/CMB through energy release or dark radiation, but visible/dark reheating and Delta N_eff are not mapped. Required followup: Compute dark radiation, entropy injection, and BBN/CMB likelihood for the fitted posterior region.
- **PA02 (9/10, assumption, model_building)**: Minimal model fixes Higgs portal coupling to zero and treats the dark sector as secluded. Required followup: Specify a thermal origin or nonzero portal extension, or state that portal searches and thermal-SM constraints are not directly testable.
- **PA04 (9/10, limitation, dark_matter)**: No relic abundance or fractional dark-vector DM abundance was computed, so vector-DM claims and self-interaction bounds cannot be applied. Required followup: Compute Omega_WD/Omega_DM for the assumed thermal/nonthermal history and document whether W_D is stable and cosmologically relevant.
- **PA08 (9/10, warning, spectrum_template)**: PTA analysis uses DBF template for very large-alpha points; wall velocity and microscopic efficiency are not independently computed. Required followup: Compute or marginalize wall velocity and efficiency, compare DBF/BF/Higgsless templates only within documented validity domains.
- **PA12 (9/10, limitation, constraints)**: Constraint stage claims no exclusions mainly because required cosmological, portal, abundance, and self-interaction observables are missing. Required followup: Phrase constraint result as unconstrained/not testable with current observables, not as physically allowed.
- **PA05 (8/10, limitation, self_interactions)**: No non-Abelian vector self-interaction transfer or viscosity cross section sigma/m(v) was computed. Required followup: Implement self_interactions.py for dwarf, Milky Way, and cluster velocities with unit conversion and transfer/viscosity convention.
- **PA06 (8/10, approximation, fopt_backend)**: FOPT calculation uses a semianalytic conformal high-temperature/polynomial backend with Gaussian percolation approximation. Required followup: Cross-check selected benchmarks with a full finite-temperature effective-potential/bounce calculation and alternate percolation criteria.
- **PA10 (8/10, prior, ptarcade_priors)**: Initial PTArcade final run hit the upper log10_vD prior boundary and was rerun with a wider prior; posterior boundary sensitivity remains a required caveat. Required followup: Inspect final chains for boundary contact, rerun with still-wider/alternative priors if posterior support approaches limits.
- **PA11 (8/10, warning, ptarcade_map)**: Final PTArcade MAP has extremely large alpha and f_peak_est above nominal PTA steering band; f_peak_est is approximate while DBF spectrum is fitted. Required followup: Assess MAP validity using full spectrum, template domain, and prior-boundary diagnostics rather than f_peak_est alone.
- **PA15 (8/10, uncertainty, gauge_dependence)**: Perturbative finite-temperature effective potential in conformal models has gauge/daisy/RG prescription dependence not quantified by the scan. Required followup: Run gauge/prescription/RG-scale variations or use gauge-invariant diagnostics where possible.

## Interpretation Warnings

The strongest caveat is not a failed numerical run; it is missing physical context. The model can fit a PTA-shaped DBF spectrum in the produced handoffs, but the pipeline has not computed the thermal history, dark-sector temperature ratio, visible/dark reheating partition, relic abundance, or self-interaction observables needed to convert that fit into a cosmologically viable model statement.

The constraint-agent result should therefore be read as `not excluded with missing observables`, not as an affirmative exclusion test. The zero-portal assumption makes laboratory portal searches inapplicable to the minimal model, but that same assumption makes the cosmological initial condition and reheating history central.

The PTA result also carries template and prior caveats: DBF is used for very large alpha, wall velocity and efficiency are not independently computed, no 14/14 violin benchmark was found, and an initial PTArcade run hit the log10_vD prior boundary before the accepted widened-prior rerun.

## Required Followups

- **FU01 (high)**: Build thermal-history and BBN/CMB observable backend for T_dark/T_SM, entropy transfer, reheating partition, Delta N_eff, and energy injection. Suggested action: Implement thermal_history.py and cosmo_constraints.py, then rerun constraint-agent.
- **FU02 (high)**: Compute relic abundance or dark-vector fractional abundance and non-Abelian self-interaction cross sections. Suggested action: Implement relic_density.py and self_interactions.py before making dark-matter viability claims.
- **FU03 (high)**: Assess GW template validity for extremely large alpha and independently determine or marginalize wall velocity and efficiency. Suggested action: Compare DBF/BF/Higgsless where valid and add wall-dynamics nuisance parameters or calculations.
- **FU04 (medium)**: Audit final PTArcade posterior boundary behavior and prior sensitivity after the widened-prior rerun. Suggested action: Inspect chain extrema and repeat with alternate priors if support remains close to boundaries.
- **FU05 (medium)**: Quantify effective-potential gauge, daisy, and RG prescription uncertainty for representative posterior and benchmark points. Suggested action: Run controlled theory-validity variations or full bounce cross-checks.

## Files Written

- `output/minimal_conformal_su2_doublet/prior_audit_report.md`
- `output/minimal_conformal_su2_doublet/prior_audit_table.csv`
- `output/minimal_conformal_su2_doublet/handoff_prior_audit.json`

## Validation

CSV and JSON are consistent: each CSV row corresponds to one `assumptions` entry in `handoff_prior_audit.json` with matching id, kind, category, severity, controlled flag, description, source file, and required solution.
