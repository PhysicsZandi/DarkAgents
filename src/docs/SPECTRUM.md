# Spectrum

This class only works for gravitational-wave spectrum from first-order phase transitions.

## Model skeleton

To define a spectrum, the spectrum class must implement the following methods:
```python
from spectrum import Spectrum

# alpha, beta_H and Treh must be computed by other methods
alpha = METHODS_TO_COMPUTE_ALPHA
beta_H = METHODS_TO_COMPUTE_BETA_H
Treh = METHODS_TO_COMPUTE_TREH

spectrum = Spectrum(template="higgsless" or "dbf" or "bf")

f = FREQUENCY_VALUES

# If values are compatible with the chosen template
h2OmegaGW = spectrum.get_h2OmegaGW(f, Treh, alpha, beta_H)
```

References for the implemented templates are:
- Bulk flow/dissipative bulk flow: 2511.15687;
- Higgsless: 2209.04369.

## Template selection and validation

Choose the template using the FOPT regime and the assumptions documented in the cited papers. If more than one template is plausible, record the reason for the selected template in `output/<model-name>/handoff_pta.json`. If no template is strictly valid, use the closest implemented template only with an explicit caveat in the report and handoff.

