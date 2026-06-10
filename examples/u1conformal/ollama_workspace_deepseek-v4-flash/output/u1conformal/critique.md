# Critique Report: Dark U(1) Conformal Model (u1conformal)

## Model Summary

The model is a classically scale-invariant (conformal) dark U(1)_D extension of the Standard Model, containing:
- A complex scalar Phi charged under U(1)_D
- A dark gauge boson A' (dark photon)
- Optional small portal interactions (Higgs portal lambda_{HPhi}, kinetic mixing epsilon)

Symmetry breaking occurs via the Coleman-Weinberg mechanism, where the U(1)_D gauge interaction radiatively generates a potential minimum. The dark sector is assumed to be thermalised with the visible sector (xi = T_dark/T_visible = 1).

## Validation Results

### 1. Gauge Groups -- PASS

The U(1)_D gauge group is anomaly-free since no chiral fermions are charged under it. The complex scalar Phi carries charge +1.

### 2. Global Symmetries -- PASS

Classical scale invariance is realized by the absence of dimensionful parameters in the tree-level Lagrangian. The CW mechanism breaks scale invariance radiatively (dimensional transmutation).

### 3. Particle Content -- PASS with warnings

**Particle count (dofs) before SSB**: Complex scalar Phi (2) + massless A' (2) = 4 dofs.
**Particle count after SSB**: Radial mode rho (1) + massive A' (3) = 4 dofs. The Goldstone G is eaten by A' (longitudinal polarization).

**Warning**: SM particle content is not listed explicitly. The backend handles SM contributions via an interpolated g_star(T) table, so this is acceptable for the FOPT analysis.

### 4. Lagrangian Consistency -- PASS

Each term in `L_D = |D_mu Phi|^2 - lambda_Phi |Phi|^4 - 1/4 F'_mu_nu F'^mu_nu` is gauge-invariant under U(1)_D. No mass terms appear, consistent with classical scale invariance. The sign of the quartic term is correct: L = kinetic - potential, so V = lambda_Phi |Phi|^4 (lambda_Phi > 0 for stability).

### 5. SSB Pattern -- PASS

U(1)_D is completely broken: U(1)_D -> nothing. One Goldstone mode is eaten, leaving no unbroken gauge symmetry in the dark sector.

### 6. VEV Convention -- PASS

`Phi = (chi + rho + i G) / sqrt(2)` is the standard convention. The factor of sqrt(2) correctly normalises the kinetic terms. The background field chi is the RG-improved invariant (RGI) direction.

### 7. Tree-Level Potential -- PASS

`V_tree(chi) = lambda_Phi * chi^4 / 4` is correctly derived from `V = lambda_Phi |Phi|^4` with the background convention.

### 8. Field-Dependent Masses -- PASS

**A' mass**: `m_A'^2(chi) = g_D^2 * chi^2`

Derivation: `|D_mu <Phi>|^2 = (1/2) g_D^2 chi^2 A'_mu A'^mu`. For a real vector field, the canonical mass term is `(1/2) m^2 A'_mu A'^mu`, giving `m_A'^2 = g_D^2 chi^2`. No factors of 2 or sqrt(2) errors.

**Radial mode mass**: `m_rho^2(chi) = 3 * g_D^4 * chi^2 / (8 * pi^2)`

Derivation: d^2V_eff/dchi^2 at minimum gives `m_rho^2 = beta_lambda * v^2` with `beta_lambda = (1/(8 pi^2)) (sum_B n_B g_B^4 - sum_F n_F g_F^4) = 3 g_D^4 / (8 pi^2)`. This matches the classic Coleman-Weinberg result for scalar QED (PRD 7, 1888, 1973). The condition beta_lambda > 0 is satisfied (boson-dominated CW).

**Goldstone mode**: Zero mass in Landau gauge, eaten by A' in unitary gauge.

### 9. Thermal Masses -- PASS (handled internally by backend)

The backend `semianalytic_pipeline.py` computes thermal masses internally via:
- `msq = T^2 * g2sq / 12`, where `g2sq = sum(n_b * g_b^2 + n_f * g_f^2 / 2)`
- For the current model: `g2sq = 3 * g_D^2` (gauge boson) + 0 (scalar, since g_b=0) = `3 * g_D^2`
- Debye mass squared: `g_D^2 * T^2 / 4`
- Scalar thermal mass: the backend sets `boson_gbs["scalar"] = 0`, `boson_dofs["scalar"] = 1`

### 10. Parameter Basis -- PASS

- **Independent**: v (vev, MeV-GeV scale), g_D (gauge coupling, 0.1-4*pi)
- **Dependent**: lambda_Phi (CW-fixed), m_rho (CW-fixed), m_A' (tree-level), beta_lambda
- **Fixed**: xi = 1, epsilon (unspecified), lambda_HPhi (unspecified)

This classification is consistent with the CW mechanism. The quartic lambda_Phi is correctly classified as dependent; it must not be scanned independently.

### 11. Backend Compatibility -- PASS

The backend `semianalytic_pipeline.py` is designed exactly for this type of model (single-field CSI Abelian Higgs). The example usage in the code matches:
```python
boson_gbs = {"Aprime": g_D}
boson_dofs = {"Aprime": 3}
fermion_gfs = {}
fermion_dofs = {}
```

## Warnings (non-blocking, should be addressed downstream)

1. **Portal coupling values not quantified**: The kinetic mixing epsilon and Higgs portal lambda_{HPhi} are described as "small" but no numerical values or bounds are given. These are needed for:
   - Verifying the xi=1 thermalization assumption
   - BBN constraints (dark Higgs decay lifetime)
   - Dark radiation (Delta N_eff) constraints
   - Collider constraints on dark photons
   Recommendation: specify benchmark values or upper bounds.

2. **xi=1 assumption vs small portals**: The model simultaneously assumes (a) the dark and visible sectors are at the same temperature (xi=1) and (b) portal couplings are small. These are compatible only if portals are large enough for thermalization (typically epsilon >= 10^{-10} for MeV-scale temperatures) but small enough to not affect FOPT dynamics. This tension should be addressed explicitly.

3. **RG scheme dependence**: The backend uses a simplified fixed-scale approximation for CW log terms. Full RG-improvement (as in arXiv:2501.11619, 2511.02910) could give quantitatively different FOPT parameters. This is a known systematic uncertainty in the field.

4. **No dark matter candidate**: The minimal model has no fermionic DM candidate. This is not a bug but a feature of the model; it simplifies the analysis but means fewer experimental handles.

5. **Potential completion issues for supercooled FOPTs**: The Athron et al. (2024) challenge about false vacuum trapping may need to be addressed. The conformal nature (S_E -> 0 as T -> 0) is expected to circumvent this, but a percolation check is still needed. The backend includes a percolation check (get_Tp via I(T) condition).

## Red Flags

**None**. The model is physically consistent at the Lagrangian level. All checks pass.

## Recommended User Clarifications

Since this model is user-supplied, please confirm:

1. Are there any intended numerical values or upper bounds for the portal couplings (epsilon, lambda_HPhi)? This is needed for the constraint analysis and for verifying the xi=1 assumption.

2. Is the xi = T_dark/T_visible = 1 assumption a firm choice, or should it be treated as a parameter to scan? The backend currently hardcodes xi=1.

3. Is the absence of fermionic dark matter intentional, or should a dark fermion be added?

## Conclusion

The model passes all validation checks. No blocking red flags are present. The model is ready for downstream FOPT-PTA analysis using the `semianalytic_pipeline` backend. The warnings above should be addressed in the constraint analysis stage.