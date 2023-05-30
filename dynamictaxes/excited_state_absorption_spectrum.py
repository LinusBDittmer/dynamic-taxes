'''

Class for the Excited State Absorption Spectrum

'''

import numpy
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.colors as colours
import json
import re
import os
import dynamictaxes as dt


class ExcitedStateAbsorptionSpectrum:

    def __init__(self):
        self.state_num = 0
        self.multiplicity = 1
        self.time = 0
        self.energies = numpy.zeros(1)
        self.energy_unit = dt.get_config("energy_unit")
        self.transition_moments = numpy.zeros(1)
        self.excited_state_labels = ["S1"]
        self.peak_breadth = dt.get_config("peak_breadth")
        self.resolution = dt.get_config("wavelength_res")
        self.dpi = dt.get_config("dpi")
        self.wavelength_range = [dt.get_config("wavelength_range_lower"), dt.get_config("wavelength_range_upper")]
        self.normalise_peakheight = dt.get_config("normalise_peak_height")
        self.peak_style = dt.get_config("peak_style")
        self.cmap = matplotlib.colormaps['Spectral']
        self.norm = colours.Normalize(vmin=350, vmax=820, clip=False)

    def __eq__(self, other):
        if len(self.energies) != len(other.energies):
            return False
        for i in range(len(self.energies)):
            if abs(self.energies[i] - other.energies[i]) > 10**-7:
                return False
            if abs(self.transition_moments[i] - other.transition_moments[i]) > 10**-7:
                return False
        return True

    def render(self, path, filetype='png', ax=None):
        filepattern = re.compile("[a-zA-Z0-9\-]*." + filetype)
        if filepattern.match(path).string != path:
            filepattern2 = re.compile("[a-zA-Z0-9\-]*.")
            if filepattern2.match(path).string != path:
                path += "."
            path += filetype
        directory = path[:path.rfind("/")]
        os.makedirs(directory, exist_ok=True)

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
        ax.set_xlabel("Wavelength [nm]")
        ax.set_ylabel("Rel. Transition Moment")
        gaussians = numpy.zeros((len(self.energies), self.resolution))
        for i in range(len(gaussians)):
            nm = 1239.841 / self.energies[i]
            gaussians[i] = self.gaussian(wavelength_space, nm, norm_tm[i])

        absorption = numpy.sum(gaussians, axis=0)
        #absorption /= numpy.amax(absorption)
        ax.set_ylim(0.0, numpy.amax(absorption)*1.1)

        peak_styles = [s.strip() for s in self.peak_style.split(",")]
        for i, g in enumerate(gaussians):
            gc = self.col(1239.841 / self.energies[i])
            label = self.get_multiplicity_label(self.multiplicity) + "$_" + str(self.state_num) + " \\rightarrow$ " + self.reformat_state_label(self.excited_state_labels[i]) 
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
            ax.plot(xs, ys, c=self.col(ci))

        plt.legend()

        plt.savefig("test.png", dpi=self.dpi, bbox_inches='tight')
        
    def _eval_scalar(self, nm):
        val = 0.0
        for i in range(len(self.energies)):
            val += self.gaussian(nm, 1239.841 / self.energies[i], self.transition_moments[i])
        return val

    def evaluate(self, nm):
        if type(nm) is not numpy.ndarray:
            return self._eval_scalar(nm)
        val = numpy.zeros(len(nm))
        for i in range(len(self.energies)):
            val += self.gaussian(nm, 1239.841 / self.energies[i], self.transition_moments[i])
        return val

    def col(self, nm):
        n = self.norm(nm)
        black = numpy.array([0.0, 0.0, 0.0, 1.0])
        if n < 0 or n > 1:
            return black
        else:
            return self.cmap(n)

    def gaussian(self, xvals, centre, height):
        adjusted_xvals = (xvals - centre) / self.peak_breadth
        ep_val = - 2*adjusted_xvals*adjusted_xvals
        return numpy.exp(ep_val) * height

    def get_multiplicity_label(self, m):
        return ["", "S", "D", "T", "Q"][int(m)]

    def reformat_state_label(self, l):
        return l[0] + "$_" + l[1] + "$"


if __name__ == '__main__':
    esa = ExcitedStateAbsorptionSpectrum()
    esa.energies = numpy.linspace(2.0, 4.0, 4)
    esa.transition_moments = numpy.linspace(0.1, 0.5, 4)
    esa.excited_state_labels = ["S2", "S3", "T1", "S4"]
    esa.render('test.png')
