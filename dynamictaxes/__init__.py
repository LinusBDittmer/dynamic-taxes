'''

=== THE DYNAMIC-TAXES MODULE ===

The Dynamic-Taxes module is a Python module that allows for the extraction of ESA data from QChem Files, saving these in a lightweight json format and rendering them to image files. For a detailed explanation of installing and using Dynamic-Taxes, pleas visit the GitHub Page https://github.com/LinusBDittmer/dynamic-taxes


Non-Python Files
----------------
default.config:
    This file stores permanent configurations and can be modified.
installer.sh:
    This file is a simple installer that brings Dynamic-Taxes to your system. 


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

def debug_init_configs():
    configs = {}
    configs["testkey"] = "testval"

def init_configs():
    main.load_configs()

def get_config(name):
    global configs
    if not name in configs:
        return None
    return configs[name] 

def set_config(config_dict):
    global configs
    configs = config_dict

def set_config_key(key, val):
    global configs
    configs[key] = val
