"""
Title: 
Author: Julio Rodriguez
Organization: SENER
"""

# BLK: Imports

# Standard Libraries
import cProfile
import pstats


# 3rd Party
# import pandas as pd
import numpy as np


# Local Libraries


# Global variables
class Cstruct:
    pass


# Code

# Clases

# Funciones
def describe(dataframe):
    """
    Soluciona el problema con PyCharm al utilizar la función describe() que pone % en los índices
    :param dataframe: Pandas DataFrame a aplicar la función describe
    :return: Función describe aplicada sin % en los índices
    """
    df_describe = dataframe.describe().rename(index={'25%': '25', '50%': '50', '75%': 75})
    return df_describe


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]


def rms_calculate(array):
    return np.sqrt(np.mean(array ** 2))


def time_string_to_seconds(string):
    ftr = [3600, 60, 1]
    return int(sum([a * b for a, b in zip(ftr, map(int, string.split(':')))]))