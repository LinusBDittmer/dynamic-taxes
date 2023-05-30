'''

A class for TA spectra

'''

import numpy
import matplotlib.pyplot as plt
import matplotlib

class TransientAbsorptionSpectrum:

    def __init__(self):
        self.esa_spectra = []
        self.cmap_name = 'viridis'
        self.wavelength_bounds = [200, 1000]
        self.wavelength_res = 500
        self.timestep = 500.0
        self.time_unit = "ps"
        self.interpolation = 'bilinear'
        self.title = "Transient Absorption"
        self.peak_breadth = 50.0
        self.dpi = 200

    def sort_esa_spectra(self):
        def key(e):
            return e.time

        self.esa_spectra.sort(key=key)

    def add_esa_spectrum(self, esa_spectrum):
        self.esa_spectra.append(esa_spectrum)

    def render(self, path, filetype='png'):
        self.sort_esa_spectra()
        filepattern = re.compile("[a-zA-Z0-9\-]*." + filetype)
        if filepattern.match(path).string != path:
            filepattern2 = re.compile("[a-zA-Z0-9\-]*.")
            if filepattern2.match(path).string != path:
                path += "."
            path += filetype
        directory = path[:path.rfind("/")]
        os.makedirs(directory, exist_ok=True)
        
        self.timestep = self.esa_spectra[1].time - self.esa_spectra[0].time
        density = self.get_spectral_density()
        ax, fig = plt.subplots(nrows=1, ncols=1, figsize=(12, 8))
        ax.imshow(density, aspect='auto', interpolation=self.interpolation, extent=(0, self.timestep*len(self.esa_spectra), self.wavelength_bounds[0], self.wavelength_bounds[1]))
        ax.set_xlabel("Time [" + self.time_unit + "]")
        ax.set_ylabel("Wavelength [nm]")
        ax.set_title(self.title)

        plt.savefig(path+filetype, bbox_inches='tight', dpi=self.dpi)

    def get_spectral_density(self):
        density = numpy.zeros((len(self.esa_spectra), self.wavelength_res))
        for i in range(len(self.esa_spectra)):
            density[i] = self.esa_slice(i)
        
        return desity

    def esa_slice(self, index):
        nm_vals = numpy.linspace(self.wavelength_bounds[0], self.wavelength_bounds[1], num=self.wavelength_res)
        excitations = 1239.841 / numpy.array(self.esa_spectra[index].energies)
        transition_moments = numpy.array(self.esa_spectra[index].transition_moments)
        esa = numpy.zeros(nm_vals.shape)
        for e, t in zip(excitations, transition_moments):
            esa += self.gaussian(nm_vals, e, t)
        return esa

    def gaussian(self, xvals, centre, height):
        adjusted_xvals = (xvals - centre) / self.peak_breadth
        ep_val = - 2*adjusted_xvals*adjusted_xvals
        return numpy.exp(ep_val) * height


if __name__ == '__main__':
    import dynamictaxes
    esa1 = dynamictaxes.ExcitedStateAbsorptionSpectrum()
    esa1.energies = numpy.linspace(1.0, 5.0, num=4)
    esa1.transition_moments = 0.1 * numpy.ones(4)
    ta = TransientAbsorptionSpectrum()
    ta.esa_spectra = [esa1] * 5
    ta.get_spectral_density()


