can you study the model in input/u1conformal/prompt.md?

The input/u1conformal/prompt.md file contains the following text:
# Dark U(1) conformal model

## Model description

Consider a classically scale-invariant/conformal dark $U(1)_D$ extension of the Standard Model. The dark sector contains a complex scalar $\Phi$ of $U(1)_D$ and a dark gauge boson $A'$.

The dark-sector Lagrangian is
$$
L_D = |D_\mu \Phi|^2 - \lambda_\Phi |\Phi|^4 - \frac{1}{4} F'_{\mu \nu} F'^{\mu \nu} ~,
$$
where
$$
D_\mu = \partial_\mu - i g_D A'_\mu ~.
$$

The background-field/vev convention is 
$$
\Phi(x) = \frac{\chi + \rho(x) + i G(x)}{\sqrt{2}} ~,
$$
where $\chi$ is the classical background field (associated to the vev), $\rho$ is the radial fluctuation, and $G$ is the Goldstone mode. 

The tree-level potential is
$$
V_{\text{tree}}(\chi) = \lambda_\Phi \frac{\chi^4}{4}  ~,
$$
where the quartic $\lambda_\Phi$ is a dependent parameter fixed by the Coleman-Weinberg minimization condition $V_{\text{eff}}'(v) = 0$.

The free parameters of the model are the vev $v$ and the gauge coupling $g_D$. The field-dependent mass of the gauge boson is
$$
m_A'^2(\chi) = g_D^2 \chi^2 ~.
$$

The radial mode then acquires a radiatively generated mass set by the one-loop $\beta$-function of the quartic,
$$
m_\rho^2 = \beta_\lambda v^2 ~, \qquad
\beta_\lambda = \frac{1}{8 \pi^2} \left( \sum_b n_b g_b^4 - \sum_f n_f g_f^4 \right) = \frac{3 g_D^4}{8 \pi^2} ~,
$$
where $g_b = m_b/v$ and $g_f = m_f/v$ are the mass-over-vev ratios and the only contribution here is the dark gauge boson ($g_b = g_D$, $n_b = 3$).

For phenomenological purposes, the model may also include the Standard Model portal interactions
$$
\lambda_{H\Phi} |H|^2 |\Phi|^2
$$
and gauge kinetic mixing
$$
\frac{\epsilon}{2} F'_{\mu \nu} F^{\mu \nu} ~.
$$
For the analysis of the phase transition dynamics and the gravitational wave signal, this couplings are assumed to be small enough to not affect the results. However, they can be important for the phenomenology of the model and for the constraints on the parameter space. Finally, suppose that the dark sector and the visible sector are thermalised at the same temperature, i.e. $\xi \equiv T_{\rm dark}/T_{\rm visible} = 1$, with the dark relativistic degrees of freedom added to $g_*$ separately from the visible ones.

## Target signal 

I would like to analyze the gravitational wave spectrum from a first-order phase transition in this model and compare it to PTA data. I would also like to prepare for a possible PTArcade inference campaign and extract the parameter space regions that can be probed by PTArcade. Finally, I want to check for all contraints on the model parameter space from collider, astrophysical and cosmological data, and determine whether there are some assumptions, uncertainties or caveats that I should keep in mind when interpreting the results.