'''

A class for TA spectra

'''

import numpy
import matplotlib

class TransientAbsorptionSpectrum:

    def __init__(self):
        self.esa_spectra = []

    def add_esa_spectrum(self, esa_spectrum):
        self.esa_spectra.extend(esa_sepctrum)

    def render_to_file(self, path, filetype='png'):
        pass
