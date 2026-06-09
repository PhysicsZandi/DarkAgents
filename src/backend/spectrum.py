import numpy as np
import scipy as sci
from pathlib import Path

data = np.loadtxt(
    Path(__file__).parent / "T_vs_g_gs_GeV.csv", delimiter=",", dtype=np.float32
)
x_data = data[:, 0]  # T in GeV
y_data = data[:, 1]  # g_star
gstar = sci.interpolate.interp1d(x_data, y_data, fill_value="extrapolate")
z_data = data[:, 2]  # g_star_s
g_star_s = sci.interpolate.interp1d(x_data, z_data, fill_value="extrapolate")


def redshift_f(T):
    gstarT = gstar(T)
    return 1.65e-5 * (gstarT / 100) ** (1 / 6) * T / 100


def redshift_omegaGW(T):
    gstarT = gstar(T)
    return 1.64e-5 * (gstarT / 100) ** (-1 / 3)


class Spectrum:
    def __init__(self, template=None):
        self.template = template

    # useful quantities

    def delta_w(self, vw, cs):
        v_shell = np.abs(vw - cs)

        return v_shell / np.maximum(vw, cs)

    def K_col(self, alpha, kcoll):
        return kcoll * alpha / (1 + alpha)

    def K_sw(self, alpha, ksw):
        return ksw * alpha / (1 + alpha)

    def H_tausw(self, H_R, alpha, ksw):
        K_sw = self.K_sw(alpha, ksw)
        Gamma = 4 / 3
        vf_sq = K_sw / Gamma
        H_taush = H_R / np.sqrt(vf_sq)

        return np.minimum(1, H_taush)

    # spectrum sound waves LISA 2024 (2403.03723 from 2209.04369 "higgsless")

    def S_sw_LISA2024(self, f, f1, f2):
        n1 = 3
        n2 = 1
        n3 = -3
        a1 = 2
        a2 = 4

        f_f1 = f / f1
        f_f2 = f / f2

        S = (
            f_f1**n1
            * (1 + f_f1**a1) ** ((-n1 + n2) / a1)
            * (1 + f_f2**a2) ** ((-n2 + n3) / a2)
        )

        return S

    def S2_sw_LISA2024(self, f, f1, f2):
        return self.S_sw_LISA2024(f, f1, f2) / self.S_sw_LISA2024(f2, f1, f2)

    def f1_sw_LISA2024(self, T, H_R):
        return redshift_f(T) * 0.2 / H_R

    def f2_sw_LISA2024(self, T, H_R, vw, cs):
        delta_w = self.delta_w(vw, cs)

        return redshift_f(T) * 0.5 / H_R / delta_w

    def h2Omega2_sw_LISA2024(self, T, alpha, H_R, ksw, vw, cs):
        A_sw = 0.11
        f1 = self.f1_sw_LISA2024(T, H_R)
        f2 = self.f2_sw_LISA2024(T, H_R, vw, cs)
        K_sw = self.K_sw(alpha, ksw) * 0.6
        H_tausw = self.H_tausw(H_R, alpha, ksw)
        h2Omegaint = redshift_omegaGW(T) * A_sw * K_sw**2 * H_R * H_tausw
        prefactor = 1 / np.pi * (np.sqrt(2) + 2 * f2 / f1 / (1 + (f2 / f1) ** 2))
        h2Omega2 = prefactor * h2Omegaint

        return h2Omega2

    def h2OmegaGW_sw_LISA2024(self, f, T, alpha, H_R, ksw=1, vw=1, cs=1 / np.sqrt(3)):
        h2Omega2 = self.h2Omega2_sw_LISA2024(T, alpha, H_R, ksw, vw, cs)
        f1 = self.f1_sw_LISA2024(T, H_R)
        f2 = self.f2_sw_LISA2024(T, H_R, vw, cs)
        S2 = self.S2_sw_LISA2024(f, f1, f2)

        return h2Omega2 * S2

    # spectrum LEWICKI2025 (2511.15687 "bulk flow / dissipative bulk flow with expansion")

    def S_dbf_LEWICKI2025(self, f, fp):
        a = 2
        b = 2
        c = 2

        f_fp = f / fp
        S_dbf = (a + b) ** c / (b * f_fp ** (-a / c) + a * f_fp ** (b / c)) ** c

        return S_dbf

    def S_bf_LEWICKI2025(self, f, fp):
        a = 1
        b = 2
        c = 1

        f_fp = f / fp
        S_bf = (a + b) ** c / (b * f_fp ** (-a / c) + a * f_fp ** (b / c)) ** c

        return S_bf

    def A_LEWICKI2025(self, T, alpha, beta_H, ksw):
        A = 0.06 * (1 + 0.8 * (1 - np.exp(1 / np.sqrt(beta_H))))
        K_sw = self.K_sw(alpha, ksw)
        return A * redshift_omegaGW(T) * K_sw**2

    def fp2pi_aH_LEWICKI2025(self, T, beta_H):
        return 0.7 * beta_H * (1 + 1.8 * beta_H ** (-1.2))

    def fp_LEWICKI2025(self, T, beta_H):
        fp2pi_aH = self.fp2pi_aH_LEWICKI2025(T, beta_H)
        redshift_f = 2.6e-8 * T * (gstar(T) / 100) ** (1 / 6)
        return fp2pi_aH * redshift_f

    def h2OmegaGW_dbf_2025(self, f, T, alpha, beta_H, ksw=1):
        A = self.A_LEWICKI2025(T, alpha, beta_H, ksw)
        fp = self.fp_LEWICKI2025(T, beta_H)
        S_dbf = self.S_dbf_LEWICKI2025(f, fp)

        return A * S_dbf / beta_H**2

    def h2OmegaGW_bf_2025(self, f, T, alpha, beta_H, ksw=1):
        A = self.A_LEWICKI2025(T, alpha, beta_H, ksw)
        fp = self.fp_LEWICKI2025(T, beta_H)
        S_bf = self.S_bf_LEWICKI2025(f, fp)

        return A * S_bf / beta_H**2

    def get_h2OmegaGW(self, f, T, alpha, beta_H, ksw=1, vw=1, cs=1 / np.sqrt(3)):
        if self.template == "higgsless":
            H_R = (8 * np.pi) ** (1 / 3) * vw / beta_H
            h2Omega_sw = self.h2OmegaGW_sw_LISA2024(f, T, alpha, H_R, ksw, vw, cs)
        elif self.template == "dbf":
            h2Omega_sw = self.h2OmegaGW_dbf_2025(f, T, alpha, beta_H, ksw)
        elif self.template == "bf":
            h2Omega_sw = self.h2OmegaGW_bf_2025(f, T, alpha, beta_H, ksw)
        else:
            raise ValueError(f"Unknown spectrum template: {self.template}")
        return h2Omega_sw


"""
Example usage of the Spectrum with a simple model.

chi0 = 1
gprime = 0.6

boson_gbs = {"Aprime": gprime}
boson_dofs = {"Aprime": 3}
fermion_gfs = {}
fermion_dofs = {}

model = SemiAnalyticPipeline(
    chi0=chi0,
    boson_gbs=boson_gbs,
    boson_dofs=boson_dofs,
    fermion_gfs=fermion_gfs,
    fermion_dofs=fermion_dofs,
    verbose=False,
)
alpha = model.get_alpha()
beta_H = model.get_beta_H()
Tr = model.get_Tr()

spectrum = Spectrum(template="higgsless")
f = np.logspace(-9, -7, 100)
h2OmegaGW = spectrum.get_h2OmegaGW(f, Tr, alpha, beta_H)
"""
