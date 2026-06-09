# FOPT Report: conformal_u1_dark_fopt

Backend: `semianalytic_pipeline`.

Total scan points: 791.
Viable FOPT points: 416.
Viable points with `f_peak_est` in 1e-9--1e-7 Hz: 187.
Status counts: {'viable': 416, 'numerical_failure': 307, 'not_fopt': 32, 'physical_failure': 36}.

Independent scan axes are `v_D` [GeV], `g_D`, and `y_D`. Dependent quantities use `gb_X=2*g_D`, `gf_psi=y_D/sqrt(2)`, and `beta_lambda=(3*gb_X**4 - 4*gf_psi**4)/(8*pi**2)`. `lambda_D` was not scanned.

## Best Points

| name | v_D [GeV] | g_D | y_D | Treh [GeV] | alpha | beta/H | f_peak_est [Hz] | status |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| extended_low_v0.002_g0.5_y0.5 | 0.002 | 0.5 | 0.5 | 0.000352564 | 0.803898 | 253.706 | 9.65061e-09 | viable |
| extended_broad_v0.08367_g0.25_y0.25 | 0.083666 | 0.25 | 0.25 | 0.00668165 | 2.03511e+16 | 12.9662 | 9.56109e-09 | viable |
| extended_low_v0.002_g0.5_y0.35 | 0.002 | 0.5 | 0.35 | 0.000366305 | 0.622683 | 264.807 | 1.04812e-08 | viable |
| extended_low_v0.01108_g0.38_y0.5 | 0.0110784 | 0.38 | 0.5 | 0.00119084 | 83.7431 | 79.995 | 1.04895e-08 | viable |
| extended_broad_v0.003024_g0.5_y0.9 | 0.00302439 | 0.5 | 0.9 | 0.000446596 | 2.47309 | 196.144 | 9.52592e-09 | viable |
| extended_broad_v0.08367_g0.25_y0.1 | 0.083666 | 0.25 | 0.1 | 0.00671598 | 5.9616e+14 | 14.2646 | 1.05726e-08 | viable |
| extended_low_v0.02607_g0.3_y0 | 0.0260735 | 0.3 | 0 | 0.00247502 | 529232 | 34.62 | 9.45386e-09 | viable |
| extended_low_v0.02607_g0.3_y0.05 | 0.0260735 | 0.3 | 0.05 | 0.00247642 | 557855 | 34.543 | 9.43819e-09 | viable |

## Diagnostics

The scan used seeded literature-mapped points, a MeV/sub-GeV coarse grid, and one-order extended low/broad ranges. Points with nonpositive beta_lambda, nonpositive temperatures/alpha/beta_H, nonfinite backend outputs, timeouts, or eternal inflation were not marked viable.
