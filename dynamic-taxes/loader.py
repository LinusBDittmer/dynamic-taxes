'''

A class that loads in the relevant information from the given files.

'''

import json
import numpy
import os
import re

class Loader:

    def __init__(self):
        self.ta_spectrum = None

    def load_from_dir(self, dirpath, save_json=False, jsonpath='./content.json'):
        all_content = os.listdir(dirpath)
        regex = re.compile("[a-zA-Z0-9]*_[0-9]*\.out")
        out_files = list(filter(regex.match, all_content))
        
        for outfile_index, outfile in enumerate(out_files):
            self.esa_spectra = []
            with open(outfile) as of:
                esa = dynamictaxes.ExcitedStateAbsorptionSpectrum()
                '''
                The * MAGIC *
                '''
                self.esa_spectra.extend(



    def save_to_json(self, jsonpath, compact=True):
        '''
        JSON structure:

        {
            "esa1":
            {
                "time": 0,                                          // integer
                "absorption_energies": [0.1, 0.4],                  // float array
                "transition_moments": [0.001, 0.54]                 // float array
            },
            "esa2":
            {
                ...
            },
            ...
        }

        '''
        json_dict = {}

        for e, esa_spectrum in enumerate(self.esa_spectra):
            json_key = "esa" + str(e)
            esa_dict = {"time": esa_spectrum.time}
            esa_dict["absorption_energies"] = tuple(esa_spectrum.energies)
            esa_dict["transition_moments"] = tuple(esa_spectrum.transition_moments)
            json_dict[json_key] = esa_dict

        json_indent = 4
        if compact:
            json_indent = None
        with open(jsonpath, 'w') as jsonfile:
            json.dump(json_dict, jsonfile, ensure_ascii=True, indent=json_indent)


if __name__ == '__main__':
    l = Loader()
    l.load_from_dir("./")
