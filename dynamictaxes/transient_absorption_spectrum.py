'''

A class for TA spectra

'''

import numpy
import matplotlib.pyplot as plt
import matplotlib
import re
import os
import dynamictaxes as dt

class TransientAbsorptionSpectrum:
    '''
    This class is used as a storage for all data relevant to a TA spectrum as well as relevant methods.

    Attributes
    ----------
    esa_spectra : list
        List of all ESA spectra that make up the TA spectrum.
    cmap_name : str
        Name of the colourmap used for rendering. Loaded from default.config
    wavelength_range : float, float
        Lower and upper end of the wavelength range that is rendered. Loaded from default.config
    wavelength_res : int
        Number of resolved points over the wavelength spectrum.
    timestep : int
        Time between two consecutive ESA spectra. This is generated automatically from the ESA.time values
    time_unit : str
        Unit of timestep. Loaded from default.config
    interpolation : str 
        Style of interpolation used in the TA spectrum. Loaded from default.config
    title : str
        Title of the TA spectrum. Loaded from default.config
    slice_title : str
        Title of a slice spectrum. Loaded from default.config
    avg_slice_title : str   
        Title of an averaged slice spectrum. Loaded from default.config
    peak_breadth : float
        Breadth of a single Gaussian peak. Loaded from default.config
    dpi : int
        DPI at which the TA spectrum should be rendered. Loaded from default.config
    colour : ndarray
        RGBA sytle ndarray that gives the colour of the line in an (averaged) slice spectrum. Loaded from default.config
    linewidth : float
        Linewidth in an (averaged) slice spectrum. Loaded from default.config
    ta_size : float, float
        Width and height of the TA spectrum in inches. Loaded from default.config
    linegraph_size : float, float
        Width and height of (averaged) slice spectra. Loaded from default.config

    '''

    def __init__(self):
        self.esa_spectra = []
        self.cmap_name = dt.get_config("ta_colourmap")
        self.wavelength_range = [dt.get_config("wavelength_range_lower"), dt.get_config("wavelength_range_upper")]
        self.wavelength_res = dt.get_config("wavelength_res")
        self.timestep = 500.0
        self.time_unit = dt.get_config("timestep_unit")
        self.interpolation = dt.get_config("interpolation")
        self.title = dt.get_config("ta_title")
        self.slice_title = dt.get_config("slice_title")
        self.avg_slice_title = dt.get_config("avg_slice_title")
        self.peak_breadth = dt.get_config("peak_breadth")
        self.dpi = dt.get_config("dpi")
        self.colour = dt.get_config("line_colour")
        self.linewidth = dt.get_config("linewidth")
        self.ta_size = (dt.get_config("ta_width"), dt.get_config("ta_height"))
        self.linegraph_size = (dt.get_config("linegraph_width"), dt.get_config("linegraph_height"))

    def __eq__(self, other):
        if len(self.esa_spectra) != len(other.esa_spectra):
            return False
        for i in range(len(self.esa_spectra)):
            if self.esa_spectra[i] != other.esa_spectra[i]:
                return False
        return True

    def sort_esa_spectra(self):
        '''
        This method sorts the list of ESA spectra such that they are ordered in time.
        '''
        def key(e):
            return e.time

        self.esa_spectra.sort(key=key)

    def add_esa_spectrum(self, esa_spectrum):
        '''
        This method adds another ESA spectrum.

        Parameters
        ----------
        esa_spectrum : dynamictaxes.excited_state_absorption_spectrum.ExcitedStateAbsorptionSpectrum
            The ESA spectrum.
        '''
        self.esa_spectra.append(esa_spectrum)

    def prepare_path(self, path, filetype):
        '''
        This method sorts the ESA spectra and prepares the given path to be valid.

        Parameters
        ----------
        path : str
            The path that should be prepared
        filetype : str
            The filetype of the given file.

        Returns
        -------
        path : str  
            The prepared path.
        '''
        self.sort_esa_spectra()
        self.timestep = self.esa_spectra[1].time - self.esa_spectra[0].time

        filepattern = re.compile("[a-zA-Z0-9\-/_\.]*." + filetype)
        if not filepattern.match(path) or filepattern.match(path).string != path:
            filepattern2 = re.compile("[a-zA-Z0-9\-/_\.]*.")
            if not filepattern2.match(path) or filepattern2.match(path).string != path:
                path += "."
            path += filetype
        if "/" in path:
            directory = path[:path[:-1].rfind("/")]
            os.makedirs(directory, exist_ok=True)
        return path

    def render(self, path, filetype='png'):
        '''
        This method renders the collected data to a TA spectrum image.

        Parameters
        ----------
        path : str
            The path to which the TA spectrum should be saved
        filetype : str, optional
            The filetype of the image. Default png
        '''
        path = self.prepare_path(path, filetype)

        density = self.get_spectral_density()
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=self.ta_size)
        ax.imshow(numpy.flip(density.T, axis=0), aspect='auto', interpolation=self.interpolation, extent=(0, self.timestep*len(self.esa_spectra), self.wavelength_range[0], self.wavelength_range[1]))
        ax.set_xlabel("Time [" + self.time_unit + "]")
        ax.set_ylabel("Wavelength [nm]")
        ax.set_title(self.title)

        plt.savefig(path, bbox_inches='tight', dpi=self.dpi)
        plt.close()

    def render_avg_slice(self, centre, span, path, filetype='png', intres=100):
        '''
        This method renders an averaged slice spectrum to the specified path.

        Parameters
        ----------
        centre : float
            The wavelength in nm around which the slice should be centred.
        span : float
            The distance in nm between the edge of the part over which the intensity is averaged and its centre, i.e. the spectrum is averaged over centre-span to centre+span.
        path : str
            The path to which the averaged slice spectrum should be rendered.
        filetype : str, optional
            The filetype of the image. Default png
        intres : int, optional
            The number of points considered in each timestep for averaging. Default 100

        '''
        path = self.prepare_path(path, filetype)

        intensities = numpy.zeros(len(self.esa_spectra))
        intensities_stdev = numpy.zeros(len(self.esa_spectra))
        nm_slice = numpy.linspace(centre-span, centre+span, num=intres)
        timestamps = numpy.array([esa.time for esa in self.esa_spectra])

        for i in range(len(intensities)):
            int_slice = self.esa_spectra[i].evaluate(nm_slice)
            intensities[i] = numpy.average(int_slice)
            intensities_stdev[i] = numpy.std(int_slice)

        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=self.linegraph_size)
        ax.margins(0,0)
        ax.fill_between(timestamps, intensities-intensities_stdev, intensities+intensities_stdev, color=self.colour, alpha=0.2, linewidth=0)
        ax.fill_between(timestamps, intensities-2*intensities_stdev, intensities+2*intensities_stdev, color=self.colour, alpha=0.2, linewidth=0)
        ax.plot(timestamps, intensities, color=self.colour, linewidth=self.linewidth)
        ax.set_xlabel("Time [" + self.time_unit + "]")
        ax.set_ylabel("Transition Moment")
        ax.set_title(self.avg_slice_title.replace("{wavelength}", str(centre)).replace("{span}", str(span)))
        plt.savefig(path, bbox_inches='tight', dpi=self.dpi)
        plt.close()

    def render_mono_slice(self, wavelength, path, filetype='png'):
        '''
        This method renders a (mono) slice spectrum to the specified path.

        Parameters
        ----------
        wavelength : float
            The wavelength in nm at which the slice is to be constructed.
        path : str
            The path to which the spectrum is to be rendered
        filetype : str, optional
            The filetype of the image. Default png

        '''
        path = self.prepare_path(path, filetype)

        intensities = numpy.zeros(len(self.esa_spectra))
        for i in range(len(self.esa_spectra)):
            intensities[i] = self.esa_spectra[i].evaluate(wavelength)

        timestamps = numpy.array([esa.time for esa in self.esa_spectra])

        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=self.linegraph_size)
        ax.margins(0,0)
        ax.plot(timestamps, intensities, color=self.colour, linewidth=self.linewidth)
        ax.set_xlabel("Time [" + self.time_unit + "]")
        ax.set_ylabel("Transition Moment")
        ax.set_title(self.slice_title.replace("{wavelength}", str(wavelength)))

        plt.savefig(path, bbox_inches='tight', dpi=self.dpi)
        plt.close()

    def get_spectral_density(self):
        '''
        This function calculates the spectral density as a 2D array of size (timesteps, wavelength_res)

        Returns
        -------
        density : ndarray
            The spectral density as a 2D ndarray of size (timesteps, wavelength_res)
        '''
        density = numpy.zeros((len(self.esa_spectra), self.wavelength_res))
        for i in range(len(self.esa_spectra)):
            density[i] = self.esa_slice(i)
        
        return density

    def esa_slice(self, index):
        '''
        This function generates a 1D ndarray of the spectral intensity of one ESA spectrum.

        Parameters
        ----------
        index : int
            The index of the ESA spectrum.

        Returns
        -------
        ints : ndarray
            An ndarray of size (wavelength_res,) containing the spectral intensity of the ESA spectrum
        '''
        nm_vals = numpy.linspace(self.wavelength_range[0], self.wavelength_range[1], num=self.wavelength_res)
        excitations = 1239.841 / numpy.array(self.esa_spectra[index].energies)
        transition_moments = numpy.array(self.esa_spectra[index].transition_moments)
        esa = numpy.zeros(nm_vals.shape)
        for e, t in zip(excitations, transition_moments):
            esa += self.gaussian(nm_vals, e, t)
        return esa

    def gaussian(self, xvals, centre, height):
        '''
        This function evaluates a Gaussian with the specified centre and height at the given xvals.

        Parameters
        ----------
        xvals : ndarray
            The wavelengths in nm at which the Gaussian should be evaluated
        centre : float
            The wavelength in nm around which the Gaussian should be centred
        height : float
            The height of the Gaussian at centre.

        Returns
        -------
        ints : ndarray
            The intensities at the given wavelengths.
        '''
        adjusted_xvals = (xvals - centre) / self.peak_breadth
        ep_val = - 2*adjusted_xvals*adjusted_xvals
        return numpy.exp(ep_val) * height


if __name__ == '__main__':
    import dynamictaxes
    dynamictaxes.debug_init_configs()
    ta = TransientAbsorptionSpectrum()
    for i in range(50):
        esa1 = dynamictaxes.ExcitedStateAbsorptionSpectrum()
        esa1.time = i*100
        esa1.energies = numpy.linspace(2.0+i/25, 5.0, num=4)
        esa1.transition_moments = 0.1 * numpy.ones(4)
        ta.add_esa_spectrum(esa1)
    
    ta.render("ta_test.png")
    ta.render_avg_slice(250, 30, "ta_slice.png")

