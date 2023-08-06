# from math import atan2, cos, sin, sqrt
from numpy import vectorize
from numpy import arctan2, cos, sin, sqrt
from types import SimpleNamespace

# Default parameters if no input parameters
default_parameters = {
    'l': 4,  # Fracture length, m
    'p': 2,  # net pressure, MPa
    'E': 20e3,  # Young's modulus, Mpa
    'nu': 0.2,  # Poission's ratio
}


class Sneddon():
    name = "Sneddon"

    def __init__(self, in_params=None) -> None:
        params = default_parameters.copy()
        if in_params:
            params.update(in_params)

        self.params = SimpleNamespace(**params)

        self.stress = vectorize(self._stress)

    def _stress(self, x, y):
        # def stress(x, y, in_params=None):
        """ Stress at a single point (x, y).
        """
        l = self.params.l
        p = self.params.p
        c = l / 2  # half length

        # Compute radius
        r = sqrt(x**2 + y**2)
        r_1 = sqrt((x + c)**2 + y**2)
        r_2 = sqrt((x - c)**2 + y**2)

        if (x == 0 and y == 0):  # the origin
            f_1 = -1
            f_2 = 0
        else:
            theta = arctan2(y, x)
            theta_1 = arctan2(y, x + c)
            theta_2 = arctan2(y, x - c)

            f_1 = r / sqrt(r_1 * r_2) \
                *cos(theta - 0.5 * theta_1 - 0.5 * theta_2) - 1
            f_2 = r / c * (c**2 / r_1 / r_2)**1.5 * sin(theta) \
                * sin( 1.5 * (theta_1 + theta_2))

        sigma_x = p * (f_1 - f_2)
        sigma_y = p * (f_1 + f_2)

        return sigma_x, sigma_y

    def width(self, x):
        """ Fracture width along the fracture surface (x axis).
        """
        l = self.params.l
        p = self.params.p
        E = self.params.E
        nu = self.params.nu
        # half crack length
        c = 0.5 * l
        # plane strain
        E_ = E / (1 - nu**2)

        return 4 * p * c / E_ * sqrt(1 - (x / c)**2)
