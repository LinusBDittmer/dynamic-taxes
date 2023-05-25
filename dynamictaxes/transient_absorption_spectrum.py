'''

A class for TA spectra

'''

import numpy
import matplotlib

class TransientAbsorptionSpectrum:

    def __init__(self):
        self.esa_spectra = []

    def add_esa_spectrum(self, esa_spectrum):
        self.esa_spectra.append(esa_spectrum)

    def render_to_file(self, path, filetype='png'):
        pass
