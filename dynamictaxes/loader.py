'''

A class that loads in the relevant information from the given files.

'''

import json
import numpy
import os
import re
import dynamictaxes

class Loader:

    def __init__(self):
        self.ta_spectrum = dynamictaxes.TransientAbsorptionSpectrum()

    def load_from_dir(self, dirpath, save_json=False, jsonpath='./content.json', compact=False):
        all_content = os.listdir(dirpath)
        regex = re.compile("[a-zA-Z0-9]*_[0-9]+\.out")
        out_files = list(filter(regex.match, all_content))

        for outfile_index, outfile in enumerate(out_files):
            with open(outfile) as of:
                esa = dynamictaxes.ExcitedStateAbsorptionSpectrum()
                '''
                The * mAGIC *
                '''
                self.ta_spectrum.add_esa_spectrum(esa)

        if save_json:
            self.save_to_json(jsonpath, compact=compact)

    def load_from_json(self, jsonpath):
        json_dict = {}
        with open(jsonpath, "r") as jsonfile:
            json_dict = json.load(jsonfile)

        for esa_key in json_dict:
            esa = dynamictaxes.ExcitedStateAbsorptionSpectrum()
            esa_dict = json_dict[esa_key] # esa_dict = json_dict['esa0']
            esa.time = esa_dict['time']
            esa.state_num = esa_dict['state_number']
            esa.energies = numpy.array(esa_dict['absorption_energies'])
            esa.transition_moments = numpy.array(esa_dict['transition_moments'])
            self.ta_spectrum.add_esa_spectrum(esa)

    def save_to_json(self, jsonpath, compact=False):
        '''
        JSON structure:

        {
            "esa1":
            {
                "time": 0,                                          // float
                "state_number": 1                                   // integer
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

        for e, esa_spectrum in enumerate(self.ta_spectrum.esa_spectra):
            json_key = "esa" + str(e)
            esa_dict = {"time": esa_spectrum.time}
            esa_dict["absorption_energies"] = tuple(esa_spectrum.energies)
            esa_dict["transition_moments"] = tuple(esa_spectrum.transition_moments)
            esa_dict["state_number"] = esa_spectrum.state_num
            json_dict[json_key] = esa_dict

        json_indent = 4
        if compact:
            json_indent = None
        with open(jsonpath, 'w') as jsonfile:
            json.dump(json_dict, jsonfile, ensure_ascii=True, indent=json_indent)


if __name__ == '__main__':
    l = Loader()
    l.load_from_dir("./", save_json=True)
