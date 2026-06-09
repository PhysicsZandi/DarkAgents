# FOPT report: minimal_conformal_su2_doublet

Backend: `backend/semianalytic_pipeline.py`.
Independent scan axes: `gD`, `vD` only.
Mapping: `chi0 = vD`, `boson_gbs = {'W_D': gD / 2}`, `boson_dofs = {'W_D': 9}`.

Total evaluated points: 934.
Viable points: 662.
Numerical failures: 268.
Physical/non-FOPT exclusions: 4.

Best viable points by closeness to the PTA steering estimate:
- point_0594: gD=0.9, vD=0.04201 GeV, Treh=0.00386749 GeV, alpha=2.10105e+10, beta/H=21.2085, f_peak_est=1.00152e-08 Hz, in_PTA_band=True
- point_0769: gD=1.4, vD=0.00410893 GeV, Treh=0.000549149 GeV, alpha=10.4378, beta/H=148.631, f_peak_est=9.91903e-09 Hz, in_PTA_band=True
- point_0681: gD=1.15, vD=0.0120146 GeV, Treh=0.00130544 GeV, alpha=930.021, beta/H=62.1849, f_peak_est=9.90426e-09 Hz, in_PTA_band=True
- point_0441: gD=1.82333, vD=0.00104453 GeV, Treh=0.00022144 GeV, alpha=0.864807, beta/H=381.206, f_peak_est=1.00261e-08 Hz, in_PTA_band=True
- point_0715: gD=1.25, vD=0.00702618 GeV, Treh=0.000824339 GeV, alpha=72.5193, beta/H=97.7048, f_peak_est=9.81458e-09 Hz, in_PTA_band=True

Warnings:
- f_peak_est is a template-independent order-of-magnitude estimate for PTA-band steering only.
- The semianalytic backend uses its high-temperature polynomial approximation and Gaussian percolation approximation.
- The exact core model has same-model literature precedent; this scan recomputes observables locally with the critic-authoritative vector mass convention.
