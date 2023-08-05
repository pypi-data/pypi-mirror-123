from enum import Enum

import _gaussianfft

from _gaussianfft import *


class VariogramType(Enum):
    GAUSSIAN = 'gaussian'
    EXPONENTIAL = 'exponential'
    GENERAL_EXPONENTIAL = 'general_exponential'
    SPHERICAL = 'spherical'
    MATERN_32 = 'matern32'
    MATERN_52 = 'matern52'
    MATERN_72 = 'matern72'
    CONSTANT = 'constant'


def variogram(type, main_range, perp_range=-1.0, depth_range=-1.0, azimuth=0.0, dip=0.0, power=1.5):
    if isinstance(type, Enum):
        type = type.value
    return _gaussianfft.variogram(type, main_range, perp_range, depth_range, azimuth, dip, power)


def simulate(variogram, nx, dx, ny=1, dy=-1.0, nz=1, dz=-1.0):
    return _gaussianfft.simulate(variogram, nx, dx, ny, dy, nz, dz)


__all__ = [
    'variogram', 'simulate', 'seed', 'advanced', 'simulation_size',
    'quote', 'Variogram', 'VariogramType', 'util', 'SizeTVector', 'DoubleVector',
]
