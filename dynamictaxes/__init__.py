'''

Main Package for the dynamic-taxes module

'''

import dynamictaxes.excited_state_absorption_spectrum as esa
import dynamictaxes.transient_absorption_spectrum as tas
import dynamictaxes.loader as loader
import dynamictaxes.main as main

configs = None


def ExcitedStateAbsorptionSpectrum():
    return esa.ExcitedStateAbsorptionSpectrum()

def TransientAbsorptionSpectrum():
    return tas.TransientAbsorptionSpectrum()

def Loader():
    return loader.Loader()

def get_config(name):
    global configs
    return configs[name] 

def set_config(config_dict):
    global configs
    configs = config_dict

