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

# Local Libraries


# Global variables
class Cstruct:
    pass

# Code

# Clases


class SlowFunction:
    def __init__(self):
        self.profile = cProfile.Profile()

    def start(self):
        self.profile.enable()

    def stop(self):
        self.profile.disable()
        ps = pstats.Stats(self.profile)
        ps.sort_stats('calls', 'cumtime')
        ps.print_stats(20)


# Funciones

