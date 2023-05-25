'''

Class for the Excited State Absorption Spectrum

'''

import numpy
import matplotlib
import json

class ExcitedStateAbsorptionSpectrum:

    def __init__(self):
        self.state_num = 0
        self.time = 0
        self.energies = numpy.zeros(1)
        self.energy_unit = 'ev'
        self.transition_moments = numpy.zeros(1)
        self.peak_breadth = 50.0

    def render(self, path, filetype='png'):
        pass


