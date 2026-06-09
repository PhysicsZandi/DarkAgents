# Prior Audit Report: conformal_u1_dark_fopt

## Status

Run status: warning. The upstream workflow is usable, but multiple interpretation-critical assumptions remain uncontrolled. No new physics calculations or scans were performed in this audit.

## Highest-Severity Uncontrolled Issues

1. Exact-zero portals: epsilon=0 and lambda_HP=0 remove visible production, visible decays, and SM thermal contact. These are symmetry-allowed operators, so the current workflow needs either a protective model argument or a nonzero-portal scan and constraint recast.
2. Physical posterior mask: the rectangular PTArcade 1-sigma region contains beta_lambda<0 corners. Physical credible regions and derived masses should be recomputed from posterior samples with beta_lambda>0 imposed.
3. Thermal history: BBN, CMB, Delta N_eff, decoupling, dark-sector temperature ratio, species abundances, and lifetimes are not computed. This is a major limitation for a MeV-GeV hidden sector.
4. Supercooling and template validity: strongly supercooled points rely on an approximate percolation/completion treatment and the DBF GW template, whose validity is not strict for the strongest transitions.

## Other Material Caveats

- PTArcade MAP is at y_D=0, the physical lower boundary. The y_D posterior should be treated as boundary-sensitive rather than an interior preference.
- The FOPT backend is semianalytic, conformal, single-field, and high-temperature/small-field polynomial. Key points need full finite-temperature potential and bounce/percolation cross-checks for robust claims.
- The dark fermion is not yet established as stable dark matter, and no relic-density or CMB energy-injection calculation exists.
- No RG running, Landau-pole, or Coleman-Weinberg scale-variation analysis was performed.
- Literature benchmark mapping is useful for scan seeding but remains convention-dependent.

## Required Followups

The authoritative followup list is in `handoff_prior_audit.json`. It is restricted to items that materially affect interpretation: beta_lambda masking, thermal-history/BBN/CMB calculations, supercooling completion checks, portal justification or recast, relic abundance, RG validity, and self-interaction recasts if the fermion is dark matter.

## Files Written

- `output/conformal_u1_dark_fopt/handoff_prior_audit.json`
- `output/conformal_u1_dark_fopt/prior_audit_table.csv`
- `output/conformal_u1_dark_fopt/prior_audit_report.md`
