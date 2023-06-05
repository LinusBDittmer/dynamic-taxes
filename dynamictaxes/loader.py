'''

A class that loads in the relevant information from the given files.

'''

import json
import numpy
import os
import re
import dynamictaxes

class Loader:
    '''
    This class loads data from a directory containing QChem OUT-Files or from a JSON file.

    Attributes
    ----------
    ta_spectrum : dynamictaxes.transient_absorption_spectrum.TransientAbsorptionSpectrum
        TA spectrum in which everything is saved.

    Methods
    -------
    reset()
        Delete all saved data.
    load_from_dir(dirpath, save_json=False, jsonpath='./content.json', compact=False)
        Load data from the directoy specified in dirpath. If save_json is True, it is saved into a JSON file.
    load_from_json(jsonpath)
        Load data from the JSON file specified in jsonpath
    save_to_json(jsonpath, compact=False)
        Write the saved data to the JSON file specified in jsonpath. If compact is True, whitespace and indentation are not included.
    '''

    def __init__(self):
        self.ta_spectrum = dynamictaxes.TransientAbsorptionSpectrum()

    def reset(self):
        '''
        Deletes all data save in ta_spectrum.
        '''
        self.ta_spectrum = dynamictaxes.TransientAbsorptionSpectrum()

    def load_from_dir(self, dirpath, save_json=False, jsonpath='./content.json', compact=False):
        '''
        Loads data from all relevant files in the given dirpath. Only files abiding by a specific name structure are included. Their name has to end in .out, it has to contain an underscore, which can be prefaced by any string, and must be followed by at least one number. The number after the underscore is interpreted as a timestamp.

        Parameters
        ----------
        dirpath : str
            The directory from which the data should be loaded.
        save_json : bool, optional
            Whether the loaded data should be saved to a JSON file. Default False
        jsonpath : str, optional
            If save_json is True, the data is saved to this variable. Default './content.json'
        compact : bool, optional
            If save_json is True, this variable determines whether the JSON file is compact or not.

        '''
        all_content = os.listdir(dirpath)
        regex = re.compile("[a-zA-Z0-9]*[0-9]+\.out")
        out_files = list(filter(regex.match, all_content))

        for outfile_index, outfile in enumerate(out_files):
            with open(outfile) as of:
                esa = dynamictaxes.ExcitedStateAbsorptionSpectrum()
                '''
                The * mAGIC *

                Fields to edit:
                time
                multiplicity
                energies
                transition_moments
                excited_state_labels
                '''
                content = ''.join(of.read())
                
                # Load multiplicity
                multiplicity_start = content.find('\n0 1\n')+3
                multiplicity_content = content[multiplicity_start:multiplicity_start+1]
                esa.multiplicity = int(multiplicity_content)
                
                # Load energies
                ex_start = content.find('Excited state')+2
                ref_energy_pos = content.find('excitation energy (eV) =', ex_start)+28
                ref_energy = float(content[ref_energy_pos:content.find('\n', ref_energy_pos)])
                energy_list = []
                ex_start1 = content.find('Excited state', ex_start)
                while ex_start1 > -1:
                    ex_end = content.find('Total energy for state', ex_start1)-2
                    ex_start2 = content.find('Excited state   ', ex_end)
                    ex_content = content[ex_start1:ex_end]
                    ex_energy = float(ex_content.split("=")[1].strip())-ref_energy
                    energy_list.append(ex_energy)
                    ex_start1 = content.find('Excited state', ex_end)                
                esa.energies = numpy.array(energy_list)

                # Transition moments
                tm_list = []
                tm_start_proxy = content.find('Transition Moments Between Ground')+1
                tm_start = content.find('Transition Moments Between', tm_start_proxy)
                tm_end_proxy = content.find('\n    1   20', tm_start)+3
                tm_end = content.find('\n', tm_end_proxy)
                tm_table = content[tm_start:tm_end].split('\n')[4:]
                
                for entry in tm_table:
                    entry = entry.strip()
                    tm_entry = float(entry.split()[5])
                    tm_list.append(tm_entry)
                
                esa.transition_moments = numpy.array(tm_list)

                # State labels
                labels = ["S" + str(i+2) for i in range(len(tm_list))]
                esa.excited_state_labels = labels

                # Timestamp
                geo_removed = outfile.replace(".out", "")
                num_index = 0
                for i in range(len(geo_removed)):
                    if not geo_removed[len(geo_removed)-1-i].isdigit():
                        num_index = len(geo_removed)-i
                        break
                timestamp = float(geo_removed[num_index:]) * 0.05 # in fs
                esa.time = timestamp
                
                # State number
                esa.state_num = 1

                # Save ESA spectrum
                self.ta_spectrum.add_esa_spectrum(esa)
    

        if save_json:
            self.save_to_json(jsonpath, compact=compact)

    def load_from_json(self, jsonpath):
        '''
        This method loads data from the specified json file.

        Parameters
        ----------
        jsonpath : str
            The path of the JSON file from which the data should be loaded.
        '''
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
        This method saves the data in ta_spectrum into a JSON file specified in jsonpath. The structure of the JSON file is as follows:

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

        Paramters
        ---------
        jsonpath : str
            The path to which the json file should be saved
        compact : bool, optional
            Whether the json enconding should be compact. If not, an indentation level of 4 is used.

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
    import dynamictaxes as dt
    dt.init_configs()
    l = Loader()
    l.load_from_dir(".", save_json=True, compact=False)
