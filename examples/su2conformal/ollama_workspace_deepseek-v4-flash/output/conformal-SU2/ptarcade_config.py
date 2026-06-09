"""
PTArcade configuration for the conformal-SU2 model.
"""
from pathlib import Path

pta_data = "NG15"
mode = "ceffyl"
mod_sel = False
out_dir = str(Path(__file__).resolve().parent / "chains")
resume = False
N_samples = 100000  # production run
red_components = 14
corr = False
gwb_components = 14
bhb_th_prior = True