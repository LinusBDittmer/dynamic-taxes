'''

Main Package for the dynamic-taxes module

'''

import dynamictaxes.excited_state_absorption_spectrum as esa
import dynamictaxes.transient_absorption_spectrum as tas

def ExcitedStateAbsorptionSpectrum():
    return esa.ExcitedStateAbsorptionSpectrum()

def TransientAbsorptionSpectrum():
    return tas.TransientAbsorptionSpectrum()
