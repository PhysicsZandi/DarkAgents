# Constraints Report for u1conformal_fermion

## Model Summary

The u1conformal_fermion model is a classically scale-invariant U(1)_D dark sector with:
- Complex scalar Phi (dark Higgs, charge +1)
- Dark gauge boson A'_mu
- Two Dirac fermions psi_1 (charge +1/2), psi_2 (charge -1/2) with Yukawa y_psi Phi psi1_bar psi2
- Zero Higgs portal (lambda_HPhi = 0)
- Zero gauge kinetic mixing (epsilon = 0)

## Key Finding: The Secluded Dark Sector

The defining feature of this model for constraint purposes is that **all portal couplings to the Standard Model are set to zero**. This means:

1. **No SM coupling for the dark photon**: Without kinetic mixing, A' cannot be produced in colliders, beam dumps, stars, or supernovae. It does not decay to SM particles (e+e-, mu+ mu-, etc.).

2. **No SM coupling for the dark Higgs**: Without the Higgs portal, chi does not mix with the SM Higgs. No production via Higgsstrahlung or Higgs decays.

3. **No SM coupling for the dark fermions**: psi_1 and psi_2 interact only via U(1)_D gauge and Yukawa interactions.

**Consequence**: All standard dark photon constraints (beam dumps, colliders, stellar cooling, SN1987A, direct detection) are **not applicable** to this model because they all require a non-zero kinetic mixing epsilon.

## PTArcade 1-Sigma Region

From the Bayesian analysis (PTArcade with NANOGrav 15-year data):

| Parameter | 68% Credible Interval | MAP |
|-----------|----------------------|-----|
| g_D | [0.526, 0.648] | 0.532 |
| y_psi | [0.110, 0.605] | 0.109 |
| v | [0.650, 1.448] GeV | 1.187 GeV |

Derived masses at MAP: m_A' = 631 MeV, m_psi = 91 MeV, m_chi = 65 MeV

**Mass hierarchy at MAP**: m_chi < m_psi < m_A', so chi (CW pseudo-dilaton) is the lightest dark sector particle and is stable (dark matter candidate).

## Summary of Constraints

### Directly Testable / Already Enforced

| Constraint | Status |
|-----------|--------|
| Vacuum stability (beta_lambda > 0) | Enforced by upstream agent |
| Supercooling condition (g_D > y_psi/sqrt(2)) | Enforced by upstream agent |
| Standard perturbativity (g_D < 4*pi, y_psi < sqrt(4*pi)) | Satisfied by entire 1-sigma region |

### Directly Applicable (Satisfied)

| Constraint | Status |
|-----------|--------|
| Delta N_eff from dark radiation | **Satisfied** - All DS particles have m > 20 MeV, non-relativistic at BBN/CMB |

### Not Applicable (Zero Portal Couplings)

| Constraint | Reason for Non-Applicability |
|-----------|------------------------------|
| Dark photon beam dump searches | Require epsilon != 0 for production |
| Dark photon collider searches (BaBar, LHCb) | Require epsilon != 0 |
| Stellar cooling bounds | Require epsilon != 0 for plasmon decay |
| SN1987A cooling | Require epsilon != 0 |
| Higgs invisible decays | Require lambda_HPhi != 0 |
| DM direct detection | Require epsilon or lambda_HPhi != 0 |
| DM indirect detection | DM annihilates only to dark sector |

### Requires New Backend Calculations

| Calculation | Priority | Reason |
|------------|----------|--------|
| DS thermal history / xi(T) | **High** | xi=1 assumption inconsistent with zero portal couplings |
| DM relic abundance | **High** | chi is stable DM candidate; may overclose universe |
| BBN constraint on PT energy injection | **Medium** | FOPT latent heat may affect BBN if it couples to SM |
| DM self-interaction cross-section | **Low** | If chi is DM, self-scattering via A' exchange |
| Perturbative unitarity (specific) | **Low** | General bounds satisfied; specific coupled-channel check needed |

## Critical Missing Calculations

### 1. Dark Sector Thermal History (xi evolution)

The assumption xi = T_dark/T_SM = 1 is inconsistent with zero portal couplings (epsilon = 0, lambda_HPhi = 0). Without any portal, the gravitational interaction rate Gamma_grav ~ T^8/M_Pl^4 is many orders of magnitude smaller than the Hubble rate H ~ T^2/M_Pl at all temperatures below the Planck scale (ratio Gamma_grav/H ~ T^6/M_Pl^3 ~ 10^{-51} at T = 1 GeV). Therefore the dark sector cannot maintain thermal equilibrium with the SM.

The correct treatment requires:
- Determining initial T_dark/T_SM after inflation (depends on inflaton-dark sector coupling)
- Tracking independent entropy conservation in both sectors
- Computing the FOPT reheating effect (which reheats only the dark sector)
- Computing xi(T) at BBN and CMB epochs

### 2. Dark Matter Relic Abundance

In the 1-sigma PTArcade region, the lightest dark sector particle is almost always **chi** (the CW pseudo-dilaton scalar). With m_chi = 20-120 MeV and no decay channels to SM particles or lighter DS particles, chi is stable and constitutes a dark matter candidate.

The relic abundance of chi depends on:
- chi internal thermalisation and freeze-out within the dark sector
- chi chi -> A A annihilation cross-section (gauge coupling g_D)
- Dilution from the first-order phase transition entropy production
- The dark sector temperature at freeze-out

If Omega_chi h^2 > 0.12, this parameter region would be ruled out by DM overproduction. If Omega_chi h^2 < 0.12, chi could be a subdominant DM component or require an additional production mechanism.

### 3. FOPT BBN Constraints

The first-order phase transition releases latent heat that reheats the dark sector to T_reh ~ 1-200 MeV. For the FOPT benchmark points with v ~ 10-20 MeV, T_reh ranges from 0.45 to 2.0 MeV. The Bai-Korwar bound (T_* > ~2 MeV for strong PTs) applies when the latent heat reheats SM photons. In this secluded model, the latent heat reheats only the dark sector, so the constraint on SM BBN is much weaker - but a proper calculation is needed.

## Model Assumption Flags

1. **xi = 1 requires a portal**: The assumption that the dark sector is in thermal equilibrium with the SM (xi = 1) contradicts the assumption of zero portal couplings. This is a significant inconsistency that should be addressed.

2. **Zero portal couplings are tree-level statements**: Even if epsilon = 0 and lambda_HPhi = 0 at tree level, they can be generated at loop level by heavy mediator fermions or by SM particles. The typical size of loop-induced epsilon could be ~ 10^{-4}-10^{-6} (from 2-loop W-boson/Higgs exchange). This would re-open many of the excluded constraints, though likely at a level below current sensitivity.

3. **DM relic abundance is uncomputed**: The model has a stable DM candidate (chi in most of the preferred region), but its relic abundance has not been calculated. This is a critical missing piece for assessing the viability of the preferred parameter space.