import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from decimal import Decimal

TS_INITIAL_GUESS = 5


class StiffenedPlateService():

    def calc_stiffener_dimensions(self, a, b, t_0, phi, Nls, Nts, k):
        if k != 0.000:    
            volumetric_fraction_equation = lambda t_s: a*b*t_0*phi - (Nls*(a*k*Decimal(t_s.item())*Decimal(t_s.item())) + Nts*((b - Nls*Decimal(t_s.item()))*k*Decimal(t_s.item())*Decimal(t_s.item())))

            ts_initial_guess = TS_INITIAL_GUESS

            ts_calculated = (fsolve(func=volumetric_fraction_equation, x0=ts_initial_guess))
            hs_calculated = k*Decimal(ts_calculated.item())

            ts_rounded = np.round(float(ts_calculated), 1)
            hs_rounded = np.round(float(hs_calculated), 1)

            return hs_rounded, ts_rounded
        else:
            ts_zero = 0.00
            hs_zero = 0.00
            return hs_zero, ts_zero
            

    def calc_corrected_plate_thickness(self, phi, t_0, k):
        if k != 0.000:
            t_1_calculated = (1 - phi)*t_0
            t_1_rounded = np.round(float(t_1_calculated), 1)

            return t_1_rounded
        else:
            return t_0
        
    def calc_section_length_in_both_directions(self, a, b, k, N_ls, N_ts, h_s):
        if k != 0.000:
            length_ts = round(float(b) + float(N_ls*h_s), 2)
            length_ls = round(float(a) + float(N_ts*h_s), 2)
        else:
            length_ts = b
            length_ls = a
        return length_ts, length_ls
    
    def calc_section_area_in_both_directions(self, a, b, k, t_1, N_ls, N_ts, h_s, t_s):
        if k != 0.000:
            area_ts = round(float(b)*t_1 + float(N_ls*h_s*t_s), 2)
            area_ls = round(float(a)*t_1 + float(N_ts*h_s*t_s), 2)
        else:
            area_ts = round(float(b)*t_1, 2)
            area_ls = round(float(a)*t_1, 2)
        return area_ts, area_ls
    
    def calc_section_equivalent_thickness_in_both_directions(self, length_ts, length_ls, area_ts, area_ls):
        t_eq_ts = area_ts/length_ts
        t_eq_ls = area_ls/length_ls
        return t_eq_ts, t_eq_ls




