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

            ts_rounded = np.round(float(ts_calculated), 0)
            hs_rounded = np.round(float(hs_calculated), 0)

            return hs_rounded, ts_rounded
        else:
            ts_zero = 0.00
            hs_zero = 0.00
            return hs_zero, ts_zero
            

    def calc_corrected_plate_thickness(self, phi, t_0, k):
        if k != 0.000:
            t_1_calculated = (1 - phi)*t_0
            t_1_rounded = np.round(float(t_1_calculated), 0)

            return t_1_rounded
        else:
            return t_0
