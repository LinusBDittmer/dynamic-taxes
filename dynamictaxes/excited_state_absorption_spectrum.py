'''

Class for the Excited State Absorption Spectrum

'''

import numpy
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.colors as colours
import json
import re

class ExcitedStateAbsorptionSpectrum:

    def __init__(self):
        self.state_num = 0
        self.multiplicity = 1
        self.time = 0
        self.energies = numpy.zeros(1)
        self.energy_unit = 'ev'
        self.transition_moments = numpy.zeros(1)
        self.excited_state_multiplicities = numpy.ones(1, dtype=numpy.int32)
        self.peak_breadth = 100.0
        self.resolution = 500
        self.dpi = 200
        self.wavelength_range = (200.0, 1000.0)
        self.normalise_peakheight = True
        self.peak_style = 'bar'

    def render(self, path, filetype='png', ax=None):
        filepattern = re.compile("[a-zA-Z0-9\-]*.png")
        if filepattern.match(path).string != path:
            filepattern2 = re.compile("[a-zA-Z0-9\-]*.")
            if filepattern2.match(path).string != path:
                path += "."
            path += filetype


        wavelength_space = numpy.linspace(self.wavelength_range[0], self.wavelength_range[1], num=self.resolution)
        norm_tm = numpy.copy(self.transition_moments)
        if self.normalise_peakheight:
            norm_tm /= numpy.amax(norm_tm)
        
        self_plot = False
        if ax is None:
            self_plot = True
            plt.figure()
            fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8,6))
       
        ax.margins(x=0, y=0)
        ax.set_xlim(self.wavelength_range[0], self.wavelength_range[1])
        ax.set_ylim(0.0, 1.25)
        ax.set_xlabel("Wavelength [nm]")
        ax.set_ylabel("Rel. Transition Moment")
        gaussians = numpy.zeros((len(self.energies), self.resolution))
        for i in range(len(gaussians)):
            nm = 1239.841 / self.energies[i]
            gaussians[i] = self.gaussian(wavelength_space, nm, norm_tm[i])

        absorption = numpy.sum(gaussians, axis=0)
        absorption /= numpy.amax(absorption)
        cmap = matplotlib.colormaps['Spectral']
        norm = colours.Normalize(vmin=350, vmax=820, clip=True)

        peak_styles = [s.strip() for s in self.peak_style.split(",")]
        for i, g in enumerate(gaussians):
            gc = cmap(norm(1239.841 / self.energies[i]))
            label = self.get_multiplicity_label(self.multiplicity) + "$_" + str(self.state_num) + " \\rightarrow$ " + self.get_multiplicity_label(self.excited_state_multiplicities[i]) + "$_" + str(i+self.state_num+1) + "$" 
            if 'gauss' in peak_styles or 'band' in peak_styles:
                gc = list(gc)
                gc[3] = 0.5
                gc = tuple(gc)
                ax.plot(wavelength_space, g, c=gc, label=label)
            if 'bar' in peak_styles:
                ax.vlines(1239.841 / self.energies[i], 0, norm_tm[i], colors=[gc], label=label)

        for i in range(self.resolution-1):
            xs = wavelength_space[i:i+2]
            ys = absorption[i:i+2]
            ci = i * (self.wavelength_range[1] - self.wavelength_range[0]) / self.resolution + self.wavelength_range[0]
            ax.plot(xs, ys, c=cmap(norm(ci)))

        plt.legend()

        plt.savefig("test.png", dpi=self.dpi, bbox_inches='tight')
        

    def gaussian(self, xvals, centre, height):
        adjusted_xvals = (xvals - centre) / self.peak_breadth
        ep_val = - 2*adjusted_xvals*adjusted_xvals
        return numpy.exp(ep_val) * height

    def get_multiplicity_label(self, m):
        return ["", "S", "D", "T", "Q"][int(m)]


if __name__ == '__main__':
    esa = ExcitedStateAbsorptionSpectrum()
    esa.energies = numpy.linspace(2.0, 4.0, 4)
    esa.transition_moments = numpy.linspace(0.1, 0.5, 4)
    esa.excited_state_multiplicities = numpy.ones(4, dtype=numpy.int32)
    esa.excited_state_multiplicities[2] = 2
    esa.render('test.png')
