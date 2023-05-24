'''

Class for the Excited State Absorption Spectrum

'''

import numpy
import matplotlib
import json

class ExcitedStateAbsorptionSpectrum:

    def __init__(self):
        self.state_num = -1
        self.time = -1
        self.energies = None
        self.energy_unit = 'ev'
        self.transition_moments = None
        self.peak_breadth = 50.0

    def render(self, path, filetype='png'):
        pass


