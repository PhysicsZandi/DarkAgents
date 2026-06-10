# Preliminary Literature Search Report

**Model:** scale-invariant-dark-u1-zprime
**Branch:** fopt-pta
**Target signal:** Stochastic GW background from a strongly supercooled first-order phase transition in the nanohertz (PTA / NANOGrav) band.

## Model recap

Classically scale-invariant (Coleman-Weinberg) gauged dark `U(1)_D`: complex dark scalar `Phi` (radial = pseudo-dilaton, angular eaten by `Z'`), dark gauge boson `Z'` with `m_Z' = g_D * w`, and a Dirac dark fermion `chi` with `m_chi = y*w/sqrt(2)` (plus a mirror fermion `eta` purely for anomaly cancellation). Radiative SSB along the flat direction drives a supercooled FOPT. Free parameters: `g_D in [0.1,1.5]`, `y in [0,1]`, `w in [100, 1e6]` GeV.

## Novelty verdict

**Not novel — a very close precedent exists.** The structure is essentially reproduced by Balan et al. (arXiv:2502.19478), which is a classically conformal dark `U(1)'` with a complex dark scalar, a dark photon, and a Yukawa-mass Dirac dark fermion as sub-GeV dark matter, all tuned to a supercooled MeV-scale FOPT for NANOGrav. The only distinctive ingredient of the target is the explicit mirror fermion `eta` for `U(1)_D` anomaly cancellation, and the deliberate neglect of kinetic mixing in the FOPT analysis. The FOPT phenomenology itself is well-established.

## Papers (verified)

| arXiv | Authors | Journal/Year | Class | Score |
|---|---|---|---|---|
| 2502.19478 | Balan, Bringmann, Kahlhoefer, Matuszak, Tasillo | JCAP 08(2025)062 | same_model | 10 |
| 2501.11619 | Goncalves, Marfatia, Morais, Pasechnik | PLB 869 (2025) 139829 | structurally_similar | 9 |
| 2501.15649 | Costa, Hoefken Zink, Lucente, Pascoli, Rosauro-Alcaraz | PLB 868 (2025) 139634 | structurally_similar | 9 |
| 2105.01007 | Borah, Dasgupta, Kang | PRD 104 (2021) 063501 | same_target_diff_model | 7 |
| 2306.17086 | Fujikura, Girmohanta, Nakai, Suzuki | PLB (2023) | background_context | 5 |

Note: 2105.01007 and 2306.17086 are treated as metadata-only (PDF text not machine-extractable / different mechanism); used for context, not for benchmark numbers.

## Benchmark points (direct anchors)

**Balan et al. 2502.19478 — Table 1 (same field content & conventions: m_Z'=g_D v, m_chi=y v/sqrt2):**
- Point A (coupled): g_D=0.877, y=0.363, v=92.9 MeV, m_Z'=81.4 MeV, m_chi=23.8 MeV, T_p=8.36 MeV, T_reh=12.9 MeV, **alpha=4.99, beta/H=21.1**.
- Point B (secluded): g_D=0.790, y=0.401, v=343 MeV, T_p=15.2 MeV, T_reh=39.3 MeV, **alpha=62.6, beta/H=13.3**.

**Costa et al. 2501.15649 — Table 1 (GeV-scale vev window, near-conformal, uses H*R*):**
- BP1: v=0.5 GeV, g_D=0.75, lambda=0.006, T_p=12.5 MeV, alpha=342, H*R*=0.48.
- BP2: v=1.0 GeV, g_D=0.75, T_p=22.5 MeV, alpha=523.
- BP3: v=10 GeV, g_D=0.75, T_p=194 MeV, alpha=463.
- BP4: v=1.0 GeV, g_D=0.86, lambda=0.010, T_p=38 MeV, alpha=102.

**Goncalves et al. 2501.11619 — Table 1 (fully CW/conformal, extreme supercooling):**
- g_D=0.59, m_Z'=107.3 MeV, scalon=12.4 MeV, T_reh=11.7 MeV, **alpha=2.6e5, beta/H=39.5**, kinetic mixing=2e-10.

## Convention / theory notes (fopt-pta)

- **vev convention** matches across CW papers and the target: `m_Z' = g_D w`, `m_chi = y w/sqrt(2)`; Point A of 2502.19478 maps one-to-one onto the target's `(g_D, y, w)`.
- **Quartic:** strictly CW-fixed in the target / 2502.19478 / 2501.11619, but a small free input in 2501.15649 — shifts the g_D-lambda correlation and supercooling depth.
- **GW measures differ:** alpha+beta/H (2502.19478, 2501.11619) vs alpha+H*R* (2501.15649) — convert consistently for the spectrum template.
- **Temperatures:** T_p (34% true vacuum), T_*, and reheating after vacuum domination are distinct; align with the backend definitions.
- **Renormalization:** target fixes mu=w, no RG running, no Daisy. The supercooled-CW literature (e.g. 2511.02910, seen in searches) cautions about Daisy vs 3D-EFT treatment — a theory uncertainty to flag downstream.

## Recommended next steps

1. Use 2502.19478 Point A as the primary anchor (identical field content/conventions).
2. Use 2501.15649 BP1-BP4 to populate the GeV-scale vev window of the target.
3. Use 2501.11619 to bracket the deep-supercooling (large alpha) g_D-only limit.
4. Reconcile T_*/T_p/T_reh and alpha/beta/H/H*R* definitions before transferring numbers.
5. Inform the critic-agent that the model is structurally non-novel; the mirror fermion `eta` and neglected kinetic mixing are the only distinctive features.

## Sources

- https://arxiv.org/abs/2502.19478 (JCAP 08(2025)062)
- https://arxiv.org/abs/2501.11619 (PLB 869 (2025) 139829)
- https://arxiv.org/abs/2501.15649 (PLB 868 (2025) 139634)
- https://arxiv.org/abs/2105.01007 (PRD 104 (2021) 063501)
- https://arxiv.org/abs/2306.17086 (PLB 2023)
