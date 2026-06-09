can you study the model in input/u1conformal/prompt.md?

The input/u1conformal/prompt.md file contains the following text:
# Dark U(1) conformal model

## Model description

Consider a classically scale-invariant dark U(1)_D extension of the Standard Model. The dark sector contains one complex scalar Phi of U(1)_D charge +1 and a dark gauge boson A'_mu.

The dark-sector Lagrangian is
L_D = |D_mu Phi|^2 - lambda_Phi |Phi|^4 - 1/4 F'_{mu nu} F'^{mu nu},
with
D_mu = partial_mu - i g_D A'_mu.

We use the background-field convention
Phi(x) = [phi + rho(x) + i G(x)] / sqrt(2),
where phi is the classical background field, rho is the radial fluctuation, and G is the Goldstone mode. The radiatively generated vacuum expectation value is v, and the MS-bar renormalization scale is chosen as mu = m_A'(v) = g_D v.

The tree-level background potential is
V_tree(phi) = lambda_Phi phi^4 / 4.

The field-dependent tree-level masses are
m_rho^2(phi) = 3 lambda_Phi phi^2,
m_G^2(phi) = lambda_Phi phi^2,
m_A'^2(phi) = g_D^2 phi^2.

The free parameters of the model are the vev v and the gauge coupling g_D. The quartic coupling lambda_Phi is fixed by the CW condition to be 
lambda_Phi = g_D^4 / (16 pi^2) 

In fact, the effective potential is 
V_eff(phi) = lambda_Phi phi^4 / 4 + (3 m_A'^4(phi) / (64 pi^2)) [log(m_A'^2(phi)/mu^2) - 5/6],
where the gauge boson contribution dominates over the scalar contributions. The CW condition is derived by minimizing the effective potential 
dV_eff/dphi = 0 at phi = v, which gives the relation between lambda_Phi and g_D
lambda_Phi = 3 g_D^4 / (16 pi^2) [1/3 - log(g_D^2 v^2 / mu^2)],
where c is a numerical constant that depends on the renormalization scheme. Choosing mu = g_D v gives the simplified relation
lambda_Phi = g_D^4 / (16 pi^2).

At finite temperature, the daisy-resummed scalar masses are
M_rho^2(phi,T) = 3 lambda_Phi phi^2 + Pi_Phi(T),
M_G^2(phi,T) = lambda_Phi phi^2 + Pi_Phi(T),
where 
Pi_Phi(T) = [lambda_Phi/3 + g_D^2/4] T^2 ~.

The dark gauge boson thermal masses are separated into transverse and longitudinal modes:
M_A'_T^2(phi,T) = g_D^2 phi^2,
M_A'_L^2(phi,T) = g_D^2 phi^2 + Pi_A'(T),
where 
Pi_A'(T) = g_D^2 T^2 / 3 ~.
Only the longitudinal gauge mode receives the perturbative Debye thermal mass. The transverse gauge modes do not receive a perturbative O(g_D^2 T^2) thermal mass.

For phenomenological purposes, the model may also include the Standard Model portal interactions
lambda_HPhi |H|^2 |Phi|^2
and gauge kinetic mixing
epsilon/2 F'_{mu nu} F^{mu nu}.

Suppose that the temperature of the dark sector is the same as the visible sector, and that the portal coupling lambda_HPhi and the kinetic mixing epsilon are small enough to not affect the phase transition dynamics.

## Target signal 

I would like to analyze the gravitational wave spectrum from a first-order phase transition in this model and compare it to PTA data. I would also like to prepare for a possible PTArcade inference campaign and extract the parameter space regions that can be probed by PTArcade. Finally, I want to check for all contraints on the model parameter space from collider, astrophysical and cosmological data, and determine whether there are some assumptions, uncertainties or caveats that I should keep in mind when interpreting the results.