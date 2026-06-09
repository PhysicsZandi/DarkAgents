import numpy as np
import scipy as sci
from pathlib import Path

# constants
GAMMA_EULER = 0.577
A_B = 16 * np.pi**2 * np.exp(3 / 2 - 2 * GAMMA_EULER)
A_F = np.pi**2 * np.exp(3 / 2 - 2 * GAMMA_EULER)
M_PLANCK = 1.22e19 / np.sqrt(8 * np.pi)  # Reduced Planck mass in GeV

# load gstar
_data_candidates = [
    Path(__file__).parent / "T_vs_g_gs_GeV.csv",
    Path(__file__).parent.parent / "T_vs_g_gs_GeV.csv",
]
for _candidate in _data_candidates:
    if _candidate.exists():
        _data_path = _candidate
        break
else:
    raise FileNotFoundError("Could not find T_vs_g_gs_GeV.csv")
data = np.loadtxt(_data_path, delimiter=",", dtype=np.float64)
x_data = data[:, 0]  # T in GeV
y_data = data[:, 1]  # gstar
gstar = sci.interpolate.interp1d(x_data, y_data, fill_value="extrapolate")


# auxiliary functions for numerical derivatives and safe logarithm
def numerical_derivative(f, x):
    h = x * 1e-3
    # return (-f(x + 2 * h) + 8 * f(x + h) - 8 * f(x - h) + f(x - 2 * h)) / (12 * h)
    return (f(x + h) - f(x - h)) / (2 * h)


def numerical_second_derivative(f, x):
    h = x * 1e-3
    # return (
    #    -f(x + 2 * h) + 16 * f(x + h) - 30 * f(x) + 16 * f(x - h) - f(x - 2 * h)
    # ) / (12 * h**2)
    return (f(x + h) - 2 * f(x) + f(x - h)) / (h**2)


def safelog(x):
    x = np.asanyarray(x, dtype=float)
    log_x = np.zeros_like(x, dtype=float)
    mask = x != 0
    log_x[mask] = np.log(x[mask])
    return log_x


# main class for the semi-analytic pipeline
class SemiAnalyticPipeline:
    def __init__(
        self, chi0, boson_gbs, boson_dofs, fermion_gfs, fermion_dofs, verbose=False
    ):
        self.verbose = verbose

        self.xi = 1  # = Tdark / TSM for coupled dark sector
        self.chi0 = chi0
        self.boson_gbs = boson_gbs
        self.boson_dofs = boson_dofs
        self.fermion_gfs = fermion_gfs
        self.fermion_dofs = fermion_dofs
        self.boson_gbs["scalar"] = 0  # subleading order
        self.boson_dofs["scalar"] = 1
        self.new_dof = sum(self.boson_dofs.values()) + 7 / 8 * sum(
            self.fermion_dofs.values()
        )

        # Convert any single-value arrays to scalars
        try:
            if np.asarray(self.chi0).size == 1:
                self.chi0 = float(np.asarray(self.chi0).item())
        except Exception:
            pass

        for d in ("boson_gbs", "boson_dofs", "fermion_gfs", "fermion_dofs"):
            mapping = getattr(self, d)
            if isinstance(mapping, dict):
                for k, v in list(mapping.items()):
                    try:
                        arr = np.asarray(v)
                        if arr.size == 1:
                            mapping[k] = float(arr.item())
                    except Exception:
                        pass

        self.Tn = None
        self.Tp = None
        self.Tr = None

        self.alpha = None
        self.beta_H = None

    # POTENTIAL
    def get_coeffs(self, T):
        g2sq = 0
        g3 = 0
        g4 = 0

        for boson, gb in self.boson_gbs.items():
            dof = self.boson_dofs.get(boson, 0)
            g2sq += dof * gb**2
            g3 += dof * gb**3
            g4 += dof * gb**4 * safelog(gb**4 * self.chi0**4 * np.e / (A_B**2 * T**4))

        for fermion, gf in self.fermion_gfs.items():
            dof = self.fermion_dofs.get(fermion, 0)
            g2sq += dof * gf**2 / 2
            g4 -= (
                dof * gf**4 / 2 * safelog(gf**4 * self.chi0**4 * np.e / (A_F**2 * T**4))
            )

        msq = T**2 * g2sq / 12
        k = T * g3 / (4 * np.pi)
        l = g4 / (32 * np.pi**2)

        return msq, k, l

    def get_potential(self, chi, T):
        msq, k, l = self.get_coeffs(T)
        return msq * chi**2 / 2 - k * chi**3 / 3 - l * chi**4 / 4

    # BOUNCE ACTION
    def get_lambdatilde(self, T):
        msq, k, l = self.get_coeffs(T)
        lambdatilde = l * msq / k**2
        return lambdatilde

    def compute_S3_minus(self, T):
        msq, k, l = self.get_coeffs(T)
        m = np.sqrt(msq)
        prefactor = 27 * np.pi * m**3
        numerator = 1 + np.exp(-k / (m * np.sqrt(l)))
        denominator = 2 * k**2 + 9 * l * m**2
        action = prefactor * numerator / denominator
        return action

    def compute_S3_plus(self, T):
        msq, k, l = self.get_coeffs(T)
        m = np.sqrt(msq)
        kappa = -self.get_lambdatilde(T)
        numerator = 2 * np.pi * m**3
        denominator = 3 * k**2 * (kappa - 2 / 9) ** 2
        polynomial = (
            1
            - 38.23 * (kappa - 2 / 9)
            + 115.26 * (kappa - 2 / 9) ** 2
            + 58.07 * kappa ** (1 / 2) * (kappa - 2 / 9) ** 2
            + 229.07 * kappa * (kappa - 2 / 9) ** 2
        )
        action = 16 / 243 * numerator / denominator * polynomial
        return action

    def get_S3(self, T):
        lambdatilde = self.get_lambdatilde(T)
        if lambdatilde > 0:
            S3 = self.compute_S3_minus(T)
        else:
            S3 = self.compute_S3_plus(T)
        if lambdatilde > -2 / 9 and S3 > 0:
            return S3
        return np.nan

    def get_S3_prime(self, T):
        return numerical_derivative(self.get_S3, T)

    def get_S3_T(self, T):
        return self.get_S3(T) / T

    def get_S3_T_prime(self, T):
        return numerical_derivative(self.get_S3_T, T)

    def get_gamma(self, T):
        S3_T = self.get_S3_T(T)
        gamma = T**4 * np.exp(-S3_T) * (S3_T / (2 * np.pi)) ** (3 / 2)
        return gamma

    # COLEMAN-WEINBERG
    def get_beta_lambda(self):
        boson = 0
        for name, gb in self.boson_gbs.items():
            boson += self.boson_dofs.get(name, 0) * gb**4
        fermion = 0
        for name, gf in self.fermion_gfs.items():
            fermion += self.fermion_dofs.get(name, 0) * gf**4
        return (boson - fermion) / (8 * np.pi**2)

    def get_delta_V(self):
        beta_lambda = self.get_beta_lambda()
        if beta_lambda <= 0:
            return np.nan
        return beta_lambda * self.chi0**4 / 16

    # HUBBLE
    def get_H_vacuum(self, T):
        deltaV = np.abs(self.get_delta_V())
        return np.sqrt(deltaV / (3 * M_PLANCK**2))

    def get_gstar_eff(self, T):
        return self.new_dof + gstar(T / self.xi) / self.xi**4

    def get_H_rad(self, T):
        return np.sqrt(np.pi**2 / 90 * self.get_gstar_eff(T) * T**4 / M_PLANCK**2)

    def get_H(self, T):
        H_vacuum_sq = self.get_H_vacuum(T) ** 2
        H_rad_sq = self.get_H_rad(T) ** 2
        return np.sqrt(H_vacuum_sq + H_rad_sq)

    # TEMPERATURES
    def get_Tn(self):
        if self.Tn is not None:
            return self.Tn
        if self.verbose:
            print("computing Tn")

        def condition_nucleation(T):
            gamma = self.get_gamma(T)
            H = self.get_H(T)
            condition = np.log(gamma) - 4.0 * np.log(H)
            if self.verbose:
                print(T, condition)
            return condition

        def scan_for_bracket(n_points):
            Tvals = np.geomspace(
                self.chi0 * 1e-10, self.chi0, n_points
            )  # at chi0*10^-10, eternal inflation is very likely
            Fvals = np.array([condition_nucleation(T) for T in Tvals])
            valid = np.isfinite(Fvals)
            Tvals, Fvals = Tvals[valid], Fvals[valid]
            for i in range(len(Tvals) - 1):
                f1, f2 = Fvals[i], Fvals[i + 1]
                if f1 == 0:
                    return Tvals[i], Tvals[i]
                if np.sign(f1) != np.sign(f2):
                    return Tvals[i], Tvals[i + 1]
            return None, None

        n_points_list = [10, 40, 100]
        for n_points in n_points_list:
            T1, T2 = scan_for_bracket(n_points)
            if T1 is not None and T2 is not None:
                break

        if T1 is None or T2 is None:
            self.Tn = np.nan
            return self.Tn

        self.Tn = sci.optimize.brentq(condition_nucleation, T1, T2)
        return self.Tn

    def get_G(self, T, Tprime):
        S3_T = self.get_S3_T(Tprime)
        return S3_T - 3 / 2 * np.log(S3_T / (2 * np.pi)) - np.log(self.get_f(T, Tprime))

    def get_Tstar(self, T):
        result = sci.optimize.minimize_scalar(
            lambda Tprime: self.get_G(T, Tprime),
            bounds=(T, 2 * T),  # Tstar must be near T
            method="bounded",
        )
        return result.x

    def get_f(self, T, Tprime):
        return 4 * np.pi / (3 * self.get_H(Tprime) ** 4) * (Tprime - T) ** 3

    def get_Gsecond(self, T, Tprime):
        return numerical_second_derivative(lambda Tprime: self.get_G(T, Tprime), Tprime)

    def get_I(self, T):
        Tstar = self.get_Tstar(T)
        Gstar = self.get_G(T, Tstar)
        Gsecondstar = self.get_Gsecond(T, Tstar)
        if (
            (not np.isfinite(Gstar))
            or (not np.isfinite(Gsecondstar))
            or (Gsecondstar <= 0)
        ):
            return np.inf
        I = np.exp(-Gstar) * np.sqrt(2 * np.pi / (Gsecondstar))
        return I

    def get_Tp(self):
        if self.Tn is None:
            self.Tn = self.get_Tn()

        if self.Tp is not None:
            return self.Tp

        if self.verbose:
            print("computing Tp")

        def condition_percolation(T):
            try:
                I = self.get_I(T)
                condition = np.log(I) - np.log(0.34)
                if self.verbose:
                    print(T, condition)
                return condition
            except Exception as e:
                return np.nan

        def scan_for_bracket(n_points):
            Tvals = np.geomspace(
                self.chi0 * 1e-10, self.Tn, n_points
            )  # at chi0*10^-10, eternal inflation is very likely
            Fvals = np.array([condition_percolation(T) for T in Tvals])
            valid = np.isfinite(Fvals)
            Tvals, Fvals = Tvals[valid], Fvals[valid]
            for i in range(len(Tvals) - 1):
                f1, f2 = Fvals[i], Fvals[i + 1]
                if f1 == 0:
                    return Tvals[i], Tvals[i]
                if np.sign(f1) != np.sign(f2):
                    return Tvals[i], Tvals[i + 1]
            return None, None

        n_points_list = [10, 40, 100]
        for n_points in n_points_list:
            T1, T2 = scan_for_bracket(n_points)
            if T1 is not None and T2 is not None:
                break

        if T1 is None or T2 is None:
            self.Tp = np.nan
            return self.Tp

        self.Tp = sci.optimize.brentq(condition_percolation, T1, T2)
        return self.Tp

    def get_alpha(self):
        if self.alpha is not None:
            return self.alpha

        if self.Tp is None:
            self.Tp = self.get_Tp()

        deltaV = self.get_delta_V()
        rho_rad = np.pi**2 / 30.0 * self.get_gstar_eff(self.Tp) * self.Tp**4
        self.alpha = deltaV / rho_rad

        return self.alpha

    def get_beta_H(self):
        if self.beta_H is not None:
            return self.beta_H

        if self.Tp is None:
            self.Tp = self.get_Tp()

        try:
            S3_T_prime = self.get_S3_T_prime(self.Tp)
            self.beta_H = self.Tp * S3_T_prime
            if self.beta_H < 0:
                self.beta_H = np.nan
                return np.nan
            return self.Tp * S3_T_prime
        except:
            return np.nan

    def get_Tr(self):
        if self.Tr is not None:
            return self.Tr

        if self.Tp is None:
            self.Tp = self.get_Tp()
        if self.alpha is None:
            self.alpha = self.get_alpha()

        try:
            self.Tr = self.Tp * (1 + self.alpha) ** (1 / 4)
            return self.Tr
        except:
            self.Tr = np.nan
            return self.Tr

    def get_check_eternal_inflation(self):
        if self.Tp is np.nan:
            return np.nan

        if self.Tp is None:
            self.Tp = self.get_Tp()

        try:
            I_prime = numerical_derivative(self.get_I, self.Tp)
        except Exception as e:
            return np.nan

        if 3 + self.Tp * I_prime < 0:
            return False
        else:
            return True


""" Example usage

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
print("Tn:                  ", f"{model.get_Tn():.3g}", "GeV")
print("Tp:                  ", f"{model.get_Tp():.3g}", "GeV")
print("Tr:                  ", f"{model.get_Tr():.3g}", "GeV")
print("alpha:               ", f"{model.get_alpha():.3g}")
print("beta_H:              ", f"{model.get_beta_H():.4g}")
print("eternal inflation:   ", model.get_check_eternal_inflation())
"""
