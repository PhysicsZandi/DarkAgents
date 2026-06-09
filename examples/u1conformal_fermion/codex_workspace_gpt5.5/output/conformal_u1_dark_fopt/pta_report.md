# PTA Report: conformal_u1_dark_fopt

Branch: `fopt-pta`. Analysis mode: `benchmark_plus_ptarcade`.

## Spectrum template

Selected template: `dbf` from `backend/spectrum.py`. This is the closest supported implemented template for the strong/supercooled FOPT regime, but the result has a validity caveat: several 14/14 benchmark points have extremely large `alpha`, outside strict template assumptions. Do not read this as a precision calculation for those points.

## Benchmark scan

Input points: 791 rows from the FOPT-agent benchmark CSV, evaluated with the selected template and scored against the 14 tabulated PTA violin windows. Number of 14/14 in-window rows: 19.

Best ranked point:

- name: `extended_broad_v0.7653_g0.35_y0.9`
- parameters: `v_D=0.765286 GeV`, `g_D=0.35`, `y_D=0.9`
- FOPT diagnostics: `alpha=4.21827e+11`, `beta_H=17.5212`, `Treh=0.0469063 GeV`
- score: `14/14`

Benchmark files: `pta_benchmark_scan.csv`, `pta_benchmark_spectrum.pdf`.

## PTArcade campaign

Smoke test passed with `N_samples=100`. Final campaign completed with `N_samples=100000` using priors on independent model parameters only: `log10_v_D in [-3.5, 1.0]`, `g_D in [0.15, 1.0]`, `y_D in [0.0, 0.95]`.

Bayes estimates from final chains:

- `v_D`: mean approximately `0.959784 GeV` with reported log10 std `0.181788`
- `g_D`: `0.285578 +/- 0.0261305`
- `y_D`: `0.405356 +/- 0.254536`

MAP estimate: `v_D=1.1755 GeV`, `g_D=0.262002`, `y_D=0`. The MAP sits at the physical lower boundary `y_D=0`, so the Yukawa posterior should be treated with boundary caution.

PTArcade files: `ptarcade_bayes.json`, `pta_posteriors.pdf`, `pta_ptarcade_spectrum.pdf`.

## Conclusion

Within the implemented DBF template and its stated validity caveat, the model can match all 14 tabulated PTA violin bins for multiple direct FOPT benchmark points. The Bayesian campaign also finds support near `v_D ~ GeV`, `g_D ~ 0.29`, with broad/boundary-sensitive `y_D`. Because the strongest benchmark points are outside strict template validity, this is a positive benchmark-level match, not a precision validation of the supercooled spectrum.
