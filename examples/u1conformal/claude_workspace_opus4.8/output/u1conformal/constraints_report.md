# Constraint Report: Classically Scale-Invariant Dark U(1)_D (u1conformal)

Analysis mode: `ptarcade_1sigma`. Run status: **warning** (most cosmological/laboratory
constraints cannot yet be applied to a point because the required observables — `epsilon`,
dark photon/scalon decay widths and lifetimes, `Delta Neff`, relic yields — are absent from
all upstream handoffs).

## 1. Preferred region (PTArcade NANOGrav-15yr, 68% credible)

| Quantity | Range (1-sigma) | MAP |
|---|---|---|
| g_D | 0.508 - 0.546 | 0.528 |
| v | 0.61 - 1.23 GeV | 1.09 GeV |
| m_A' = g_D v (dark photon) | 0.31 - 0.67 GeV | 0.58 GeV |
| m_rho = sqrt(3 g_D^4/8pi^2) v (scalon) | 11 - 24 MeV | 21 MeV |
| Treh | 60 - 100 MeV | ~85 MeV |

Fixed assumptions (upstream): xi = 1, epsilon ~ 0, lambda_HPhi ~ 0 for the GW dynamics;
dark relativistic dof A' (3) + scalon (1) added to g_*.

## 2. Key physics findings

- **The dark photon is GeV-scale (0.3-0.7 GeV), not the usual ~MeV dark photon.** This places
  it ABOVE the SN1987A energy-loss reach (m_A' < ~0.1 GeV, 1611.03864), so SN1987A is **not
  applicable** (C07).
- **The dark decay channel A' -> rho rho is kinematically OPEN** because 2 m_rho ~ 21-49 MeV
  is far below m_A' ~ 0.31-0.67 GeV. The dark photon is therefore likely *dominantly invisible*,
  which (i) weakens visible-decay collider (C04) and beam-dump (C05) bounds and (ii) makes
  missing-energy searches (NA64-invisible, BaBar mono-photon, C06) the physically relevant
  laboratory category — pending the predicted branching split.
- **Central tension: xi=1 vs epsilon~0.** The GW computation fixes epsilon=0, but the
  xi=1 thermal-equilibrium assumption that feeds g_* and the GW redshift *requires* a nonzero
  portal. With lambda_HPhi forced << 1e-10 by conformality (C10), the only bridge is kinetic
  mixing epsilon. The same-model literature (2502.19478) uses epsilon in [1e-7, 1e-3] to both
  thermalize the sectors and let A' -> e+e- decay before BBN. A minimum epsilon for
  thermalization must be computed (C03) and intersected with C04-C06.
- **The lightest dark state is the scalon rho (~11-24 MeV).** With epsilon=0 it is stable and
  could overclose the Universe (C09); with epsilon nonzero it decays to e+e- via an
  epsilon^4-suppressed loop, with a potentially long lifetime (~10^3 s for nearby parameters),
  risking BBN/CMB energy-injection bounds (C08). Its abundance and lifetime must be computed.

## 3. Constraints that CAN be applied now

- **C01 BBN reheating floor (direct, ALLOWED):** Treh ~ 60-100 MeV >> ~3 MeV floor.
- **C10 Higgs portal / Higgs invisible width (approximate, ALLOWED):** lambda_HPhi << 1e-10 is
  far below any collider reach; trivially satisfied (it is a theory requirement, not a bound).
- **C11 Perturbativity (direct, ALLOWED):** alpha_D = g_D^2/4pi ~ 0.02 << 1 across the region.

No constraint currently EXCLUDES any part of the 1-sigma region.

## 4. Constraints requiring new calculations (cannot exclude yet)

| ID | Constraint | Class | What is missing |
|---|---|---|---|
| C02 | Delta Neff (CMB+BBN) | requires_new_backend | Delta Neff, dark decoupling T, entropy ratio |
| C03 | xi=1 thermalization | requires_new_backend | epsilon_min, Gamma/H |
| C04 | Visible collider (BaBar/LHCb...) | recast_needed | epsilon, A' visible BR, lifetime |
| C05 | Electron beam dump (E137/E141) | recast_needed | epsilon, A' lifetime, visible BR |
| C06 | Invisible/missing-energy (NA64) | recast_needed | epsilon, A' invisible BR |
| C08 | Scalon late decay (BBN/CMB) | requires_new_backend | Gamma_rho, tau_rho, Y_rho, epsilon |
| C09 | Scalon relic overabundance | requires_new_backend | <sigma v>, Omega_rho h^2 |

## 5. Not applicable

- **C07 SN1987A:** dark photon mass 0.3-0.7 GeV is above the SN production/reach window.
- **C12 dark photon direct detection:** A' is an unstable FOPT mediator, not relic dark matter.

## 6. Missing calculations (priority HIGH)

1. **Kinetic mixing epsilon** — predicted/minimum value for xi=1 thermalization (suggested
   module `dark_portal_thermalization.py`). Gates C03/C04/C05/C06/C08.
2. **Dark photon decay** — widths, lifetime, visible vs invisible (A'->rho rho) branching
   (`dark_photon_decay.py`). Gates C04/C05/C06/C08.
3. **Delta Neff** — thermalized dark-sector contribution at BBN/CMB vs Planck Neff=2.99+/-0.17
   (`dark_Neff.py`). Gates C02 — likely the strongest test of the xi=1 assumption.
4. **Scalon relic + decay** — freeze-out yield, epsilon-loop lifetime, injection epoch
   (`scalon_relic_decay.py`). Gates C08/C09.

## 7. Theory caveat (not an exclusion)

Order-of-magnitude gauge dependence of the CW+thermal effective potential (1707.06765)
propagates into alpha, beta/H, Treh and the GW amplitude; already flagged upstream. It widens
the effective preferred region rather than excluding it.

## Sources

- [The Dark Photon: a 2026 Perspective (2603.08430)](https://arxiv.org/abs/2603.08430)
- [Balan et al., Sub-GeV DM and nHz GW from a conformal dark sector (2502.19478)](https://arxiv.org/abs/2502.19478)
- [Goncalves et al., Supercooled PT in conformal dark sectors explain NANOGrav (2501.11619)](https://arxiv.org/abs/2501.11619)
- [Chang, Essig, McDermott, Revisiting SN1987A Constraints on Dark Photons (1611.03864)](https://arxiv.org/abs/1611.03864)
- [Batell, Essig, Surujon, Constraints from SLAC Beam Dump E137 (1406.2698)](https://arxiv.org/abs/1406.2698)
- [Chiang, Senaha, Gauge dependence of GW from scale-invariant U(1)' FOPT (1707.06765)](https://arxiv.org/abs/1707.06765)
