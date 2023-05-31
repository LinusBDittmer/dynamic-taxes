'''

Main Package for the dynamic-taxes module

'''

try:
    import dynamictaxes.excited_state_absorption_spectrum as esa
    import dynamictaxes.transient_absorption_spectrum as tas
    import dynamictaxes.loader as loader
    import dynamictaxes.main as main
except:
    import dynamic-taxes.excited_state_absorption_spectrum as esa
    import dynamic-taxes.transient_absorption_spectrum as tas
    import dynamic-taxes.loader as loader
    import dynamic-taxes.main as main


configs = None


def ExcitedStateAbsorptionSpectrum():
    return esa.ExcitedStateAbsorptionSpectrum()

def TransientAbsorptionSpectrum():
    return tas.TransientAbsorptionSpectrum()

def Loader():
    return loader.Loader()

def debug_init_configs():
    main.load_configs()
def init_configs():
    main.load_configs()

def get_config(name):
    global configs
    return configs[name] 

def set_config(config_dict):
    global configs
    configs = config_dict

def set_config_key(key, val):
    global configs
    configs[key] = val
