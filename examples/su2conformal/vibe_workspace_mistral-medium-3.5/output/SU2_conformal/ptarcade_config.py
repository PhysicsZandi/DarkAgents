"""
PTArcade configuration for SU2_conformal model.
"""
# PTA data set
pta_data = "NG15"

# Mode for inference
mode = "ceffyl"

# Output directory for chains
out_dir = "./output/SU2_conformal/chains"

# Model and config files
mod_sel = False
resume = False

# Number of samples for MCMC
N_samples = int(1e5)

# Number of frequency components
red_components = 14
gwb_components = 14

# Correlations
corr = False

# BHB threshold prior
bhb_th_prior = True
